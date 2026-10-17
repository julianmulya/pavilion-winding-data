# -*- coding: utf-8 -*-
# Export already computed native component/API values; no solver or custom stress recovery.
import os,json,time,math
import System,Grasshopper as gh
from Grasshopper.Kernel.Data import GH_Path
from Karamba.Results import BeamStresses
from System.Collections.Generic import List
def val(x):
 for _ in range(5):
  if hasattr(x,'Value'):x=x.Value
  else:break
 return x
def data(p):return [val(x) for x in p.VolatileData.AllData(True)]
def xyz(p):return [float(p.X),float(p.Y),float(p.Z)]
def norm(v):return math.sqrt(sum(x*x for x in v))
def serial(v):
 v=val(v)
 if v is None or isinstance(v,(bool,int,long,float,basestring)):return v
 if hasattr(v,'X') and hasattr(v,'Y') and hasattr(v,'Z'):return xyz(v)
 try:return [serial(x) for x in v]
 except:return unicode(v)
def direct(c):
 return {'name':unicode(c.Name),'errors':[unicode(x) for x in c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)],'warnings':[unicode(x) for x in c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Warning)],
  'outputs':[{'name':unicode(p.Name),'branches':[{'path':str(path),'values':[serial(x) for x in p.VolatileData.get_Branch(path)]} for path in p.VolatileData.Paths]} for p in c.Params.Output]}
def clean(value):
 # IronPython/.NET label strings bypass json's encoding argument. Canonical units are explicit above.
 # Encode non-ASCII label characters as visible U+ markers; never modify native numeric values.
 if isinstance(value,(basestring,System.String)):return u''.join(unichr(ord(c)) if ord(c)<128 else u'[U+%04X]'%ord(c) for c in value)
 if isinstance(value,dict):return {clean(k):clean(v) for k,v in value.items()}
 if isinstance(value,(list,tuple)):return [clean(v) for v in value]
 return value
def write_new(path,value):
 assert not os.path.exists(path),'Refuse raw evidence overwrite: '+path
 with open(path,'w') as f:json.dump(clean(value),f,separators=(',',':'))
def ensure_catalogue(model):
 # Actual public native registry methods; no change to FE matrices or solution states.
 catalogue=model.ElemGuid2Ind;before=len(catalogue);added_id=0;added_guid=0;count=len(model.elems);ready=model.forcesReady()
 for e in model.elems:
  if e.GetType().Name!='ModelBeam' or not str(e.id).startswith(('NG_EDGE','NG_LINK')):continue
  selected=list(model.elemId2elemInd.Select(str(e.id)))
  if not selected:model.elemId2elemInd.Enlist(str(e.id),System.Int32(e.ind));added_id+=1
  else:assert selected==[int(e.ind)],'Native ID catalogue points to a different element'
  if not catalogue.ContainsKey(e.guid):catalogue.Add(e.guid,List[System.Int32]([int(e.ind)]));added_guid+=1
  else:assert list(catalogue[e.guid])==[int(e.ind)],'Native GUID catalogue points to a different element'
 assert len(model.elems)==count and model.forcesReady()==ready
 return {'guid_entries_before':before,'guid_entries_after':len(catalogue),'ids_registered':added_id,'guids_registered':added_guid,'physical_element_count_unchanged':count,'forces_ready_unchanged':ready}
def export(doc,tag,case,out,context):
 o={};o[142]=next(c for c in doc.Objects if str(c.InstanceGuid)=='868f3a65-9c94-45b4-aa55-5c9d3c1dcc8f');o[130]=next(c for c in doc.Objects if str(c.InstanceGuid)=='2abb3baf-043d-48bf-b513-826cc4dee3f3');model=data(o[142].Params.Output[0])[0];assert model.forcesReady()
 registration=ensure_catalogue(model)
 r={'schema':'NG02_NATIVE_STRESS_FIELDS/1','run_id':tag,'load_case':case,'initial_strain':False,'native_solve_called_by_export':False,'custom_recovery':False,'native_catalogue_registration':registration,
  'units':{'coordinates':'m','shell_stress':'MPa = native kN/cm2 x10','beam_normal_stress':'MPa = native kN/m2 /1000'},'model_context':context,'shells':[],'beams':[]}
 goo=list(o[142].Params.Output[0].VolatileData.AllData(True))[0];surfaces={};components=[]
 for side in [-1,1]:
  c=gh.Instances.ComponentServer.EmitObjectProxy(System.Guid('7cc6e19a-7a2e-4b47-8dce-a906b2b11c7a')).CreateInstance();c.SwitchUnit('PrincStress',True,False)
  for p in c.Params.Input:p.PersistentData.Clear()
  c.Params.Input[0].PersistentData.Append(goo);c.Params.Input[1].PersistentData.Append(gh.Kernel.Types.GH_String(case));c.Params.Input[2].PersistentData.Append(gh.Kernel.Types.GH_Number(side))
  t=time.time();c.CollectData();c.ComputeData();errors=[unicode(x) for x in c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)];assert not errors,repr(errors)
  v=[data(p) for p in c.Params.Output];assert len(v)==6
  surfaces[side]={'origins':[xyz(x) for x in v[1]],'s1':[float(x)*10 for x in v[4]],'s2':[float(x)*10 for x in v[5]],'v1':[xyz(x) for x in v[2]],'v2':[xyz(x) for x in v[3]]}
  r.setdefault('native_stress_components',[]).append({'guid':str(c.ComponentGuid),'side':side,'load_case':case,'unit_setting':'PrincStress','errors':errors,'output_names':[unicode(p.Name) for p in c.Params.Output],'seconds':time.time()-t,'samples':len(v[4])})
  components.append(c)
 offset=0;shellorder=0;mapping_error=0.;maximum={'value_MPa':-1}
 for e in model.elems:
  if e.GetType().Name!='ModelShell':continue
  owner=int(str(e.id).split('_P')[1].split('_')[0])-1;family=int(str(e.id).rsplit('_F',1)[1]);mesh=val(o[130].Params.Output[1].VolatileData.get_Branch(GH_Path(owner,family))[0]);shellorder+=1
  vertices=[xyz(mesh.Vertices.Point3dAt(i)) for i in range(mesh.Vertices.Count)];faces=[[int(f.A),int(f.B),int(f.C)] for f in mesh.Faces]
  assert len(vertices)==len(e.node_inds)
  assert max(norm([vertices[i][k]-xyz(model.nodes[idx].pos)[k] for k in range(3)]) for i,idx in enumerate(e.node_inds))<1e-8
  sh={'id':str(e.id),'element_index':int(e.ind),'vertices':vertices,'faces':faces,'node_indices':[int(x) for x in e.node_inds],'surfaces':{}}
  for side in [-1,1]:
   s=surfaces[side];part={key:values[offset:offset+len(faces)] for key,values in s.items()};assert len(part['s1'])==len(faces)
   for j,face in enumerate(faces):
    centre=[sum(vertices[v][k] for v in face)/3. for k in range(3)];mapping_error=max(mapping_error,norm([part['origins'][j][k]-centre[k] for k in range(3)]))
    for name in ['s1','s2']:
     value=part[name][j]
     if abs(value)>maximum['value_MPa']:maximum={'value_MPa':abs(value),'signed_value_MPa':value,'component':name,'shell_id':str(e.id),'element_index':int(e.ind),'face_index':j,'surface':side,'coordinate_m':centre}
   sh['surfaces'][str(side)]={'sigma1_MPa':part['s1'],'sigma2_MPa':part['s2'],'centres_xyz_m':part['origins'],'principal_vector1_native':part['v1'],'principal_vector2_native':part['v2']}
  r['shells'].append(sh);offset+=len(faces)
 assert offset==len(surfaces[1]['s1'])==context['model']['triangles'] and mapping_error<1e-8
 r['shell_face_mapping_error_m']=mapping_error;r['shell_max_abs_principal_stress']=maximum
 categories={}
 for sh in r['shells']:
  category='additional_winding' if sh['id'].endswith('_F1') else 'original_winding'
  for side,surface in sh['surfaces'].items():
   for field in ['sigma1_MPa','sigma2_MPa']:
    for fi,value in enumerate(surface[field]):
     if abs(value)>categories.get(category,{'value_MPa':-1})['value_MPa']:categories[category]={'value_MPa':abs(value),'signed_value_MPa':value,'shell_id':sh['id'],'face_index':fi,'surface':int(side),'coordinate_m':surface['centres_xyz_m'][fi]}
 r['shell_maxima_by_category']=categories
 write_new(os.path.join(out,tag+'_SHELL_STRESS_RAW.json'),r)
 beams=[e for e in model.elems if e.GetType().Name=='ModelBeam'];guids=[e.guid for e in beams];assert len(guids)==len(set(str(g) for g in guids))==context['model']['boundary_beams']+context['model']['equivalent_sleeve_links']
 stations=[i/16. for i in range(17)];t=time.time();res,governing=BeamStresses.solve(model,List[System.String](),List[System.Guid](guids),case,List[System.Double](stations))
 assert len(res)==len(beams),'Native beam stress selection mismatch: %d != %d'%(len(res),len(beams))
 maxima={};beamraw={'schema':'NG02_NATIVE_BEAM_NORMAL_STRESS/1','run_id':tag,'load_case':case,'units':'MPa','stations':stations,'native_recovery_seconds':time.time()-t,'beams':[]}
 for e,values in zip(beams,res):
  assert len(values)==17 and all(len(p)==2 for p in values)
  a=xyz(model.nodes[e.node_inds[0]].pos);b=xyz(model.nodes[e.node_inds[1]].pos)
  category='cfrp_boundary' if str(e.id).startswith('NG_EDGE') else 'equivalent_aluminium_link'
  original_id=str(e.id)
  record={'id':str(e.id),'guid':str(e.guid),'original_id':original_id,'element_index':int(e.ind),'category':category,'nodes':[int(x) for x in e.node_inds],'a':a,'b':b,'minimum_MPa':[float(p[0])/1000 for p in values],'maximum_MPa':[float(p[1])/1000 for p in values]}
  for j,pair in enumerate(values):
   for side,v in enumerate(pair):
    v=float(v)/1000
    if abs(v)>maxima.get(category,{'value_MPa':-1})['value_MPa']:maxima[category]={'value_MPa':abs(v),'signed_value_MPa':v,'beam_id':str(e.id),'original_id':original_id,'element_index':int(e.ind),'station':stations[j],'normal_stress_extreme_index':side,'coordinate_m':[a[k]+(b[k]-a[k])*stations[j] for k in range(3)]}
  beamraw['beams'].append(record)
 # Check native subset selection against the first bulk record of each material group.
 probes=[]
 for category in ['cfrp_boundary','equivalent_aluminium_link']:
  index=next(i for i,x in enumerate(beamraw['beams']) if x['category']==category);e=beams[index]
  single,sg=BeamStresses.solve(model,List[System.String](),List[System.Guid]([e.guid]),case,List[System.Double](stations));assert len(single)==1
  delta=max(abs(float(single[0][j][k])-float(res[index][j][k])) for j in range(17) for k in range(2));assert delta<1e-8
  probes.append({'category':category,'beam_id':str(e.id),'bulk_vs_native_single_max_difference_kN_m2':delta})
 beamraw['mapping_checks']=probes;beamraw['maxima']=maxima;write_new(os.path.join(out,tag+'_BEAM_STRESS_RAW.json'),beamraw)
 for j,c in enumerate(components):
  c.Params.Input[0].PersistentData.Clear();c.Params.Input[0].AddSource(o[142].Params.Output[0]);c.CreateAttributes();c.Attributes.Pivot=System.Drawing.PointF(2400,700+j*200);doc.AddObject(c,False)
 return {'shell_max_abs_principal_stress':maximum,'shell_maxima_by_category':categories,'beam_max_abs_normal_stress_by_category':maxima,'shell_faces':offset,'beam_records':len(beams),'beam_stations':17,'mapping_checks':probes}
