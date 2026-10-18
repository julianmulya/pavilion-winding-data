# -*- coding: utf-8 -*-
# One native Karamba Analyze invocation for five frozen load cases. No custom FE solver.
import os,json,time,math,hashlib,traceback,sys,gc,System,Rhino,Grasshopper as gh,clr
clr.AddReference('KarambaCommon');import feb
from System.Collections.Generic import List
W=r'C:\Users\Acer\Documents\Codex\2026-10-04\be\work\sleeve_sequence';sys.path.insert(0,W)
import export_ng09_compiled_native as ex
GAP=1.;MODE=VARIANT;O=RUN_ROOT+'/'+MODE;TAG='NG10_'+MODE+'_NATIVE_NINE_V2';started=os.path.join(O,TAG+'_STARTED.json');r={'run_group':TAG,'native_analyze_started':False,'native_analyze_completed':False,'case_results':[]}

def memory():
 p=System.Diagnostics.Process.GetCurrentProcess();p.Refresh();clr.AddReference('Microsoft.VisualBasic');from Microsoft.VisualBasic.Devices import ComputerInfo
 return {'private_bytes':int(p.PrivateMemorySize64),'available_physical_bytes':int(ComputerInfo().AvailablePhysicalMemory)}
def result_component(guid,goo,case):
 c=gh.Instances.ComponentServer.EmitObjectProxy(System.Guid(guid)).CreateInstance()
 for p in c.Params.Input:p.PersistentData.Clear()
 c.Params.Input[0].PersistentData.Append(goo)
 i=2 if guid=='6d2f9c9a-c9d2-4a5e-bb24-73bba5763ac0' else 2
 c.Params.Input[i].PersistentData.Append(gh.Kernel.Types.GH_String(case));c.CollectData();c.ComputeData()
 assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 return c
try:
 assert not os.path.exists(started),'Already started; no automatic replay'
 F=os.path.join(O,'INPUT_COMPLETE.json');freeze=json.load(open(F));d=gh.Instances.ActiveCanvas.Document
 assert d.FilePath==freeze['gh'] and hashlib.sha256(open(d.FilePath,'rb').read()).hexdigest()==freeze['sha256']
 ids=freeze['component_ids'];byid={str(o.InstanceGuid):o for o in d.Objects};analyze=byid[ids['analyze']];owned=byid[ids['owned']];assert analyze.Locked
 model=ex.data(owned.Params.Output[0])[0];assert not model.forcesReady();r['license']=str(feb.LicenseValidation.instance().license_info().license_type());assert r['license']!='lic_trial'
 r['memory_before']=memory();assert r['memory_before']['private_bytes']<6000000000 and r['memory_before']['available_physical_bytes']>2500000000,'Native solve resource guard HOLD before Analyze'
 r['resource_policy']={'max_private_before_bytes':6000000000,'min_available_before_bytes':2500000000,'basis':'NG03/NG04 observed solve and export footprint; runtime result caches released; export components not retained'};r['input_freeze']=F;r['input_sha256']=hashlib.sha256(open(F,'rb').read()).hexdigest();r['case_names']=freeze['cases'];r['initial_strain']=False
 ex.write_new(started,dict(r,pid=os.getpid(),time_unix=time.time()))
 analyze.Locked=False;analyze.ExpireSolution(False);r['native_analyze_started']=True;t=time.time();d.NewSolution(False);r['solve_seconds']=time.time()-t
 r['analyze_component']=ex.direct(analyze);assert not r['analyze_component']['errors'],'Native Analyze error'
 model=ex.data(analyze.Params.Output[0])[0];assert model.forcesReady();r['native_analyze_completed']=True
 goo=list(analyze.Params.Output[0].VolatileData.AllData(True))[0]
 # No further document solution is requested while native results are exported.
 mesh=freeze['model'];ctx={'model':{'triangles':mesh['triangles'],'boundary_beams':mesh['frame_segments'],'equivalent_sleeve_links':mesh['equivalent_sleeve_links']},'input_freeze':F}
 # Record completion before any export. Recovery of exports never re-runs Analyze.
 ex.write_new(os.path.join(O,TAG+'_ANALYZE_COMPLETE.json'),r)
 cases=[('G',[0,0,0]),('G_X_POS',[1,0,0]),('G_X_NEG',[-1,0,0]),('G_Y_POS',[0,1,0]),('G_Y_NEG',[0,-1,0]),('L_X_POS',[1,0,0]),('L_X_NEG',[-1,0,0]),('L_Y_POS',[0,1,0]),('L_Y_NEG',[0,-1,0])]
 correction=2*math.pi*.0065*.02*.000981747704*15.886773+math.pi/4*(.012**2-.0066**2)*(.018-.0065)*26.477955
 for case,force in cases:
  tag=TAG+'_'+case;dr=result_component('6d2f9c9a-c9d2-4a5e-bb24-73bba5763ac0',goo,case);rr=result_component('4786a421-313c-4673-b8b0-20b59742a7f2',goo,case)
  displacement=ex.data(dr.Params.Output[1]);assert len(displacement)==len(model.nodes),'Native displacement case sample count differs'
  umetrics=ex.displacement_metrics(d,model,displacement,ctx);peak=int(umetrics[1]);maximum={'value_mm':float(umetrics[0]),'node_index':peak,'coordinate_m':ex.xyz(model.nodes[peak].pos),'translation_mm':[x*1000 for x in ex.xyz(displacement[peak])]}
  reaction=ex.xyz(ex.data(rr.Params.Output[4])[0]);expected=[float(x) for x in force];expected[2]-=(float(model.mass())*10+mesh['wrap_count']*correction+mesh['added_turn_weight_kN']) if not case.startswith('L_') else 0;residual=[reaction[i]+expected[i] for i in range(3)]
  eq={'native_reaction_sum_kN':reaction,'applied_force_kN_from_native_element_weight_and_native_point_loads':expected,'residual_vector_kN':residual,'residual_kN':ex.norm(residual)}
  ex.write_new(os.path.join(O,tag+'_DIRECT_NATIVE_COMPACT.json'),{'run_id':tag,'case':case,'analyze':r['analyze_component'],'node_displacement_component':ex.component_status(dr),'reaction_component':ex.component_status(rr),'sample_count':len(displacement),'all_translations_finite':True,'maximum_displacement':maximum,'equilibrium':eq})
  assert eq['residual_kN']<=1e-7,'Native force balance HOLD'
  stress=ex.export(d,tag,case,O,ctx)
  count=ctx['_cache']['panels']
  for panelIndex in range(count):
   panel=stress['panels']['P'+str(panelIndex+1).zfill(3)];panel['shell_node_u_mm']=float(umetrics[2+panelIndex]);panel['node_u_mm']=float(umetrics[2+count+panelIndex])
  record={'run_id':tag,'case':case,'maximum_displacement':maximum,'equilibrium':eq,'stress':stress,'status':'NATIVE_CONCEPTUAL_RESULTS_RECORDED'};r['case_results'].append(record);ex.write_new(os.path.join(O,tag+'_SUMMARY.json'),record)
  Rhino.RhinoApp.WriteLine('NG09 '+MODE+' '+case+': native shell max '+str(stress['shell_max_abs_principal_stress']['value_MPa'])+' MPa; '+str(maximum['value_mm'])+' mm; force residual '+str(eq['residual_kN'])+' kN.')
  dr.ClearData();rr.ClearData()
 r['compact_export_seconds']=time.time()-t-r['solve_seconds']
 if not globals().get('BENCHMARK_ONLY',False) or globals().get('FORCE_DETAIL',False):
  bestfile=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs/NG09_FULL_BATCH_H100_20261018/BEST_NATIVE_ENVELOPES.json'
  best=json.load(open(bestfile)) if os.path.exists(bestfile) else {'shell_MPa':float('inf'),'u_mm':float('inf')}
  shellmax=max(x['stress']['shell_max_abs_principal_stress']['value_MPa'] for x in r['case_results']);umax=max(x['maximum_displacement']['value_mm'] for x in r['case_results'])
  retain=globals().get('FORCE_DETAIL',False) or shellmax<best['shell_MPa'] or umax<best['u_mm'];r['full_contours_retained']=retain
  if retain:
   import export_ng09_compressed_native as detail
   for row in r['case_results']:
    case=row['case'];detailtag=TAG+'_'+case+'_DETAIL';native=detail.export(d,detailtag,case,O,{'model':ctx['model'],'input_freeze':ctx['input_freeze']})
    assert abs(native['shell_max_abs_principal_stress']['value_MPa']-row['stress']['shell_max_abs_principal_stress']['value_MPa'])<1e-10
    for category in ['cfrp_boundary','equivalent_aluminium_link']:assert abs(native['beam_max_abs_normal_stress_by_category'][category]['value_MPa']-row['stress']['beam_max_abs_normal_stress_by_category'][category]['value_MPa'])<1e-10
    dr=result_component('6d2f9c9a-c9d2-4a5e-bb24-73bba5763ac0',goo,case)
    detail.write_new(os.path.join(O,detailtag+'_DIRECT_NATIVE_RAW.json'),{'case':case,'node_displacement_component':detail.direct(dr),'maximum_displacement':row['maximum_displacement'],'equilibrium':row['equilibrium']});dr.ClearData()
 r['total_solve_and_export_seconds']=time.time()-t
 for o in d.Objects:
  if str(o.ComponentGuid)=='7cc6e19a-7a2e-4b47-8dce-a906b2b11c7a':o.Locked=True
 analyze.Locked=True
 target=os.path.join(O,TAG+'_ANALYZE_LOCKED.gh');d.FilePath=target;saver=gh.Kernel.GH_DocumentIO();saver.Document=d;assert saver.SaveQuiet(target);r['gh']=target;r['gh_sha256']=hashlib.sha256(open(target,'rb').read()).hexdigest();r['export_mode']='NATIVE_COMPACT_V2';r['status']='NINE_NATIVE_CONCEPTUAL_CASES_RECORDED';r['memory_after']=memory();ex.write_new(os.path.join(O,TAG+'_COMPLETE.json'),r)
except:
 r['error']=traceback.format_exc();r['status']='HOLD_OR_PARTIAL_NO_AUTOMATIC_REPLAY'
 if 'analyze' in globals():analyze.Locked=True
 ex.write_new(os.path.join(O,TAG+'_HOLD_'+str(int(time.time()))+'.json'),r);Rhino.RhinoApp.WriteLine(traceback.format_exc())
