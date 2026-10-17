import os,json,hashlib,traceback,sys,time,io,gc,System,Rhino,Grasshopper as gh,clr
clr.AddReference('KarambaCommon');import feb
from System import Decimal
from System.Globalization import CultureInfo
from Grasshopper.Kernel.Data import GH_Path
W=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/work/sleeve_sequence';sys.path.insert(0,W)
import export_ground_native as ex
B=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs';ROOT=B+'/NG07_BOUNDARY_GAP_N29_S14_P55_20261018/V2'
GAP=float(globals().get('GAP_VALUE',.4));MODE='H'+str(int(round(GAP*100))).zfill(3);O=ROOT+'/'+MODE
if not os.path.isdir(O):os.makedirs(O)
try:
 assert not os.path.exists(O+'/INPUT_COMPLETE.json'),'Frozen input exists; no automatic replay'
 f=json.load(open(B+'/NG04_G_L_GL_20261018/NG04_INPUT_COMPLETE.json'))
 assert hashlib.sha256(open(f['gh'],'rb').read()).hexdigest()==f['sha256']
 old=gh.Instances.ActiveCanvas.Document
 if old:old.Enabled=False
 loader=gh.Kernel.GH_DocumentIO();assert loader.Open(f['gh']);d=loader.Document;d.Enabled=False
 byid={str(x.InstanceGuid):x for x in d.Objects};ids=f['component_ids'];geom=byid[ids['geometry']];owned=byid[ids['owned']];assemble=byid[ids['assemble']];analyze=byid[ids['analyze']];clip=byid[ids['local_support']];assert analyze.Locked
 assemble.Locked=True;owned.Locked=True
 if MODE!='H040':
  reference=json.load(open(ROOT+'/H040/INPUT_COMPLETE.json'));threshold=reference['model']['zmin_m']+.25*(reference['model']['zmax_m']-reference['model']['zmin_m'])
  src=geom.ScriptSource;code=src.AdditionalCode
  assert 'if(q.Z>zmin+.25*(zmax-zmin))' in code,'Frozen load-selection rule not found'
  src.AdditionalCode=code.replace('if(q.Z>zmin+.25*(zmax-zmin))','if(q.Z>'+repr(threshold)+')');geom.ScriptSource=src
 sliders={key:byid[guid] for key,guid in [('panels','05430e99-d225-467d-81ac-0cf8c64eaf9f'),('gap','87f56f05-9476-4c70-bfb7-fc361aea424b'),('anchors','e665e218-74e1-4316-9204-607352327306'),('shift','8a39333d-d789-4c25-9565-e4f046c10e3b')]}
 for key,x in [('panels',55),('gap',GAP),('anchors',29),('shift',14)]:sliders[key].SetSliderValue(Decimal.Parse(str(x),CultureInfo.InvariantCulture));sliders[key].ExpireSolution(False)
 owned.Code=io.open(W+'/owned_reinforcement.txt',encoding='utf-8').read()
 gh.Instances.DocumentServer.AddDocument(d);gh.Instances.ActiveCanvas.Document=d;d.Enabled=True;d.NewSolution(True)
 for c in [clip,geom]:assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 meta=json.loads(str(ex.data(geom.Params.Output[14])[0]));ground=json.loads(str(ex.data(clip.Params.Output[5])[0]))
 assert meta['panels']==55 and meta['strands']==3190 and meta['wrap_count']==3190 and meta['triangles']==25520
 assert ground['max_abs_ground_Z_m']==0 and ground['max_XY_change_m']==0 and ground['open_ground_panels']>=1 and ground['open_elevated_edges']>=2
 seed=assemble.Params.Input[7].Sources[0];seed.PersistentData.Clear()
 for goo in geom.Params.Output[6].VolatileData.get_Branch(GH_Path(0,0)):seed.PersistentData.Append(gh.Kernel.Types.GH_Point(ex.val(goo)),GH_Path(0))
 seed.ExpireSolution(False)
 normalized=[]
 active_ports=set(str(port.InstanceGuid) for port in assemble.Params.Input[2].Sources)
 for c in d.Objects:
  if not hasattr(c,'Params') or c.Params.Input.Count<5:continue
  if not any(str(port.InstanceGuid) in active_ports for port in c.Params.Output):continue
  try:case=str(ex.data(c.Params.Input[4])[0])
  except:continue
  if case not in ['G_X_POS','G_X_NEG','G_Y_POS','G_Y_NEG','L_X_POS','L_X_NEG','L_Y_POS','L_Y_NEG']:continue
  # Only point-load components with the force vector at input zero.
  try:vector=ex.data(c.Params.Input[0])[0];assert hasattr(vector,'X') and hasattr(vector,'Y') and hasattr(vector,'Z')
  except:continue
  if abs(float(vector.Z))>1e-12 or abs(float(vector.X))+abs(float(vector.Y))<1e-12:continue
  axis=[1 if '_X_' in case else 0,1 if '_Y_' in case else 0,0];sgn=-1 if case.endswith('NEG') else 1
  p=c.Params.Input[0];p.RemoveAllSources();p.PersistentData.Clear();p.PersistentData.Append(gh.Kernel.Types.GH_Vector(Rhino.Geometry.Vector3d(*[sgn*x/float(meta['load_nodes']) for x in axis])));p.ExpireSolution(False);c.ExpireSolution(False);normalized.append(case)
 assert sorted(normalized)==sorted(['G_X_POS','G_X_NEG','G_Y_POS','G_Y_NEG','L_X_POS','L_X_NEG','L_Y_POS','L_Y_NEG']),normalized
 assemble.Locked=False;owned.Locked=False;assemble.ExpireSolution(False);owned.ExpireSolution(False);d.NewSolution(True)
 for c in [geom,assemble,owned]:assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 model=ex.data(owned.Params.Output[0])[0];assert not model.forcesReady() and analyze.Locked
 totals={case:[0.,0.,0.] for case in f['cases']}
 for load in model.ploads:
  v=ex.xyz(load.force);case=str(load.LcName)
  for k in range(3):totals[case][k]+=v[k]
 ex.write_new(O+'/PRE_ANALYZE_LOAD_AUDIT_'+str(int(time.time()))+'.json',{'totals':totals,'normalized_cases':normalized})
 for case in f['cases']:
  expectedX=(1. if case.endswith('POS') else -1.) if '_X_' in case else 0.
  expectedY=(1. if case.endswith('POS') else -1.) if '_Y_' in case else 0.
  assert abs(totals[case][0]-expectedX)<1e-9 and abs(totals[case][1]-expectedY)<1e-9,repr(totals)
 f['native_point_load_totals_before_analyze']=totals
 assert len(model.nodes)==meta['explicit_master_nodes'] and len(model.supports)==meta['support_count']
 assert len(model.ploads)==5*3190+8*meta['load_nodes'] and len(model.gravities)==5
 assert len([e for e in model.elems if e.GetType().Name=='ModelShell'])==55
 assert all([bool(x) for x in s.Condition]==[True,True,True,False,False,False] and abs(model.nodes[s.node_ind].pos.Z)<1e-10 for s in model.supports)
 crc=[int(x.DataCRC(0)) for x in ex.data(byid['bc8a0310-6789-436c-a822-f3e48b9d5885'].Params.Output[0])];assert crc==[2859397175]
 boundaries={}
 for layer,index in [('A',1),('B',2)]:
  boundaries[layer]=[]
  for curve in ex.data(clip.Params.Output[index]):
   ok,pl=curve.TryGetPolyline();assert ok;boundaries[layer].append([ex.xyz(p) for p in pl])
 load_points=[ex.xyz(p) for p in ex.data(geom.Params.Output[12])]
 if MODE!='H040':
  reference=json.load(open(ROOT+'/H040/INPUT_COMPLETE.json'))
  assert load_points==reference['load_points_m'],'Lateral station coordinates changed; comparison held before Analyze'
  originalA=json.load(open(ROOT+'/H040/BOUNDARIES.json'))['A']
  assert boundaries['A']==originalA,'Original A panel geometry changed beyond the gap variable'
  assert ground['selected_open_panel']==reference['ground']['selected_open_panel'],'Ground foot panel changed'
 f.update(tag='NG07_'+MODE,configuration={'anchors':29,'shift':14,'panels':55,'gap_m':GAP},slider_readback={k:float(v.CurrentValue) for k,v in sliders.items()},ground=ground,main_loft_crc=crc,support_coordinates_m=[ex.xyz(model.nodes[s.node_ind].pos) for s in model.supports],load_points_m=load_points,parent_freeze=B+'/NG04_G_L_GL_20261018/NG04_INPUT_COMPLETE.json',initial_strain=False)
 f['model']={k:v for k,v in meta.items() if k!='records'};f['model']['native_mass_equivalent_kg']=float(model.mass())*1000;f['model']['added_turn_weight_kN']=0
 for prefix in ['NG_EDGE','NG_LINK']:f['beam_sections'][prefix]['count']=len([e for e in model.elems if str(e.id).startswith(prefix)])
 f['normalized_lateral_cases']=normalized;f['license']=str(feb.LicenseValidation.instance().license_info().license_type());f['assumptions']['study']='Boundary A/B offset only; N29 S14 P55 fixed. Main loft and A polygon same; B offset, winding lengths/mass and ground support coordinates follow original native Z0 rule. Total lateral 1kN per direction, original A upper vertices. No reinforcement.'
 ex.write_new(O+'/BOUNDARIES.json',boundaries);ex.write_new(O+'/MESH_META.json',meta)
 target=O+'/INPUT.gh';d.FilePath=target;saver=gh.Kernel.GH_DocumentIO();saver.Document=d;assert saver.SaveQuiet(target);f.update(gh=target,sha256=hashlib.sha256(open(target,'rb').read()).hexdigest())
 ex.write_new(O+'/INPUT_COMPLETE.json',f);Rhino.RhinoApp.WriteLine('NG07 '+MODE+' input frozen: '+str(len(model.nodes))+' nodes; '+str(meta['load_nodes'])+' lateral stations; Analyze locked; '+f['license'])
except:
 ex.write_new(O+'/PREPARE_HOLD_'+str(int(time.time()))+'.json',{'error':traceback.format_exc()});Rhino.RhinoApp.WriteLine(traceback.format_exc())
