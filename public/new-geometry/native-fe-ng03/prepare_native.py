# -*- coding: utf-8 -*-
# GH wiring, parameter inputs, native readback and saving only. Geometry remains C#.
import os,json,time,hashlib,traceback,math,io,clr,System,Rhino,Grasshopper as gh
clr.AddReference('GH_IO');import GH_IO
clr.AddReference('KarambaCommon');import feb
from System import Decimal
from System.Globalization import CultureInfo
from Grasshopper.Kernel.Data import GH_Path
B=r'C:\Users\Acer\Documents\Codex\2026-10-04\be'
O=os.path.join(B,'outputs','NG03_N25_S6_H04_P36_20261018')
if not os.path.isdir(O):os.makedirs(O)
tag='NG03_INPUT_'+str(int(time.time()));r={'tag':tag,'native_FE_runs':0,'configuration':{'anchors':25,'shift':6,'gap_m':.4,'panels':36},'geometry_contract':'GH_LOCAL_SUPPORT_BASE_Z0_V1'}
def sha(p):return hashlib.sha256(open(p,'rb').read()).hexdigest()
def val(x):
 for _ in range(6):
  if hasattr(x,'Value'):x=x.Value
  else:break
 return x
def data(p):return [val(x) for x in p.VolatileData.AllData(True)]
def xyz(p):return [float(p.X),float(p.Y),float(p.Z)]
def clean(x):
 if isinstance(x,(basestring,System.String)):return u''.join(unichr(ord(c)) if ord(c)<128 else u'[U+%04X]'%ord(c) for c in x)
 if isinstance(x,dict):return {clean(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def write(p,x):
 assert not os.path.exists(p),p
 with open(p,'w') as f:json.dump(clean(x),f,indent=2,default=lambda a:unicode(a))
def errors(o):return [unicode(v) for v in o.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)]
try:
 source=os.path.join(B,'outputs','NEW_GEOMETRY_LOCAL_SUPPORT_Z0_20261017','LOCAL_SUPPORT_Z0_1792255508.gh')
 assert sha(source)=='3cd66fbbd48c1d0aecb4673b4232c80443ce244f14903c1e7020c65d566b256d'
 template=os.path.join(B,'outputs','NEW_GEOMETRY_NATIVE_KARAMBA_20261017','NG02_INPUT_FREEZE_1792253064.gh')
 r.update(geometry_source=source,geometry_source_sha256=sha(source),native_template=template,native_template_sha256=sha(template))
 a=gh.Kernel.GH_DocumentIO();assert a.Open(source);correct=a.Document;correct.Enabled=False
 local=next(o for o in correct.Objects if str(o.InstanceGuid)=='185edc65-de87-40de-be82-c03ee4078dc0')
 archive=GH_IO.Serialization.GH_Archive();assert archive.AppendObject(local,'Copy')
 loader=gh.Kernel.GH_DocumentIO();assert loader.Open(template);d=loader.Document;d.Enabled=False
 old=gh.Instances.ActiveCanvas.Document
 if old:old.Enabled=False;old.PreviewMode=gh.Kernel.GH_PreviewMode.Disabled
 gh.Instances.DocumentServer.AddDocument(d);gh.Instances.ActiveCanvas.Document=d
 objects=list(d.Objects);byid={str(o.InstanceGuid):o for o in objects}
 nick_ids={row['nick']:row['id'] for row in json.load(open(os.path.join(B,'outputs','NEW_GEOMETRY_NATIVE_KARAMBA_20261017','NG02_INPUT_FREEZE_1792253064_COMPLETE.json')))['components']}
 def find(n):
  if n in nick_ids:return byid[nick_ids[n]]
  return next(o for o in d.Objects if unicode(o.NickName)==n)
 geom=find('NG01 | GEOMETRI FE NATIVE C#');assemble=find('NG01 native Assemble | no InitialStrain');owned=find('NG01 native owned shell connectivity adapter');analyze=find('NG01 NATIVE ANALYZE | LOCKED UNTIL INPUT FREEZE')
 for o in objects:
  if hasattr(o,'Locked') and ('analy' in unicode(o.Name).lower()):o.Locked=True
 assemble.Locked=True;owned.Locked=True
 clip=gh.Instances.ComponentServer.EmitObjectProxy(local.ComponentGuid).CreateInstance();assert archive.ExtractObject(clip,'Copy');clip.CreateAttributes();clip.Hidden=True;clip.NickName='NG03 | LOCAL SUPPORT / slopes retained';clip.Attributes.Pivot=System.Drawing.PointF(9800,1700)
 for p in clip.Params.Input:p.RemoveAllSources()
 for p,guid,index in zip(clip.Params.Input,['328389a0-0aac-426a-88ca-c252e45ee818','c8a6bc86-a628-4218-bf97-38c3d091e794','007674be-77ab-4ee2-aade-4e582302698b'],[0,0,1]):p.AddSource(byid[guid].Params.Output[index])
 d.AddObject(clip,False)
 originals=[byid['328389a0-0aac-426a-88ca-c252e45ee818'],byid['c8a6bc86-a628-4218-bf97-38c3d091e794']]
 previous=byid['bdde4c48-d240-4231-a6b7-2a2b3bc04ebd']
 # Do not touch source geometry ancestors. Only consumers of the previous ground adapter are rerouted.
 oldports={str(previous.Params.Output[1].InstanceGuid):1,str(previous.Params.Output[2].InstanceGuid):2}
 for o in objects:
  if o is previous or not hasattr(o,'Params'):continue
  for p in o.Params.Input:
   sources=list(p.Sources)
   if any(str(s.InstanceGuid) in oldports for s in sources):
    p.RemoveAllSources()
    for s in sources:p.AddSource(clip.Params.Output[oldports[str(s.InstanceGuid)]] if str(s.InstanceGuid) in oldports else s)
    o.ExpireSolution(False)
 previous.Locked=True;previous.Hidden=True
 # Explicit exact native A/B inputs; anchor inputs retain the source's corrected downstream components.
 for i in [0,1]:geom.Params.Input[i].RemoveAllSources();geom.Params.Input[i].AddSource(clip.Params.Output[i+1])
 sliders={key:byid[guid] for key,guid in [('panels','05430e99-d225-467d-81ac-0cf8c64eaf9f'),('gap','87f56f05-9476-4c70-bfb7-fc361aea424b'),('anchors','e665e218-74e1-4316-9204-607352327306'),('shift','8a39333d-d789-4c25-9565-e4f046c10e3b')]}
 for key,x in [('panels',36),('gap',.4),('anchors',25),('shift',6)]:sliders[key].SetSliderValue(Decimal.Parse(str(x),CultureInfo.InvariantCulture));sliders[key].ExpireSolution(False)
 d.Enabled=True;gh.Kernel.GH_Document.EnableSolutions=True;d.NewSolution(True)
 r['slider_readback']={k:float(s.CurrentValue) for k,s in sliders.items()};assert r['slider_readback']=={'panels':36.,'gap':.4,'anchors':25.,'shift':6.}
 assert not errors(clip),repr(errors(clip));ground=json.loads(str(data(clip.Params.Output[5])[0]));r['ground']=ground
 assert ground['panels']==36 and ground['max_abs_ground_Z_m']==0 and ground['max_XY_change_m']==0 and ground['open_ground_panels']>=1 and ground['open_elevated_edges']>=2
 meta=json.loads(str(data(geom.Params.Output[14])[0]));assert meta['panels']==36 and meta['strands']==1800 and meta['wrap_count']==1800 and meta['zmin_m']>=-1e-8
 seed=find('NG01 FROZEN native C# frame points');seed.PersistentData.Clear()
 for g in geom.Params.Output[6].VolatileData.get_Branch(GH_Path(0,0)):seed.PersistentData.Append(gh.Kernel.Types.GH_Point(val(g)),GH_Path(0))
 seed.ExpireSolution(False);assemble.Params.Input[7].RemoveAllSources();assemble.Params.Input[7].PersistentData.Clear();assemble.Params.Input[7].AddSource(seed)
 for case,axis in [('G_X_POS',[1,0,0]),('G_X_NEG',[-1,0,0]),('G_Y_POS',[0,1,0]),('G_Y_NEG',[0,-1,0])]:
  component=find('NG01 '+case+' | total lateral 1 kN');p=component.Params.Input[0];p.RemoveAllSources();p.PersistentData.Clear();p.PersistentData.Append(gh.Kernel.Types.GH_Vector(Rhino.Geometry.Vector3d(*[x/float(meta['load_nodes']) for x in axis])));component.ExpireSolution(False)
 assemble.Locked=False;owned.Locked=False;assemble.ExpireSolution(False);owned.ExpireSolution(False);d.NewSolution(True)
 r['components']=[{'id':str(o.InstanceGuid),'nick':unicode(o.NickName),'errors':errors(o),'warnings':[unicode(v) for v in o.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Warning)]} for o in d.Objects if hasattr(o,'Params') and (unicode(o.NickName).startswith('NG01') or o is clip)]
 assert not any(row['errors'] for row in r['components']),'Native input build error'
 model=data(owned.Params.Output[0])[0];assert not model.forcesReady() and analyze.Locked
 beams=[e for e in model.elems if e.GetType().Name=='ModelBeam'];shells=[e for e in model.elems if e.GetType().Name=='ModelShell']
 assert len(model.nodes)==meta['explicit_master_nodes'] and len(shells)==36 and len(beams)==meta['frame_segments']+meta['equivalent_sleeve_links']
 assert len(model.supports)==meta['support_count'] and all([bool(x) for x in s.Condition]==[True,True,True,False,False,False] and abs(model.nodes[s.node_ind].pos.Z)<1e-10 for s in model.supports)
 assert set(i for e in model.elems for i in e.node_inds)==set(range(len(model.nodes)))
 assert len(set(str(e.guid) for e in beams))==len(beams)
 assert len(model.gravities)==5 and len(model.ploads)==5*1800+4*meta['load_nodes']
 r['cases']=[str(x) for x in data(assemble.Params.Output[4])];assert len(r['cases'])==5
 r['license']=str(feb.LicenseValidation.instance().license_info().license_type())
 r['model']={k:v for k,v in meta.items() if k!='records'};r['model']['native_mass_equivalent_kg']=float(model.mass())*1000
 r['support_coordinates_m']=[xyz(model.nodes[s.node_ind].pos) for s in model.supports]
 r['native_materials']={}
 for name in ['NG01 CFRP | Ding2022 inherited','NG01 aluminium | local equivalent sleeve']:
  material=data(find(name).Params.Output[0])[0];r['native_materials'][name]={'E1_kN_m2':float(material.E(0)),'E2_kN_m2':float(material.E(1)),'G12_kN_m2':float(material.G12()),'gamma_kN_m3':float(material.gamma())}
 r['beam_sections']={}
 for prefix in ['NG_EDGE','NG_LINK']:
  group=[e for e in beams if str(e.id).startswith(prefix)];r['beam_sections'][prefix]={'count':len(group),'area_m2':float(group[0].crosec.A),'E1_kN_m2':float(group[0].crosec.material.E(0))}
 r['initial_strain']=False;r['local_contact_analyzed']=False;r['main_loft_crc']=[int(x.DataCRC(0)) for x in data(byid['bc8a0310-6789-436c-a822-f3e48b9d5885'].Params.Output[0])];assert r['main_loft_crc']==[2859397175]
 r['assumptions']={'boundary':'Inherited equivalent CFRP reinforced D10 edge, local aluminium sleeve links OD12/ID6.6mm; no continuous aluminium frame added','joints':'Perfect bonded shared DOFs of co-located owner edges; no bolt contact or slip','loads':'G plus conceptual total 1kN lateral at upper original-A polygon vertices for G+X, G-X, G+Y, G-Y','supports':'All XYZ translations fixed at native nodes along complete Z=0 boundary edges; rotations free','mesh':'Inherited 2 by 2 ribbon grid, 8 shell triangles per transfer','tolerance_m':1e-8,'initial_strain':False}
 boundaries={}
 for layer,index in [('A',1),('B',2)]:
  boundaries[layer]=[]
  for curve in data(clip.Params.Output[index]):
   ok,pl=curve.TryGetPolyline();assert ok;boundaries[layer].append([xyz(p) for p in pl])
 write(os.path.join(O,tag+'_BOUNDARIES.json'),boundaries);write(os.path.join(O,tag+'_MESH_META.json'),meta)
 r['component_ids']={k:str(v.InstanceGuid) for k,v in [('geometry',geom),('assemble',assemble),('owned',owned),('analyze',analyze),('local_support',clip)]}
 r['status']='NATIVE_INPUTS_FROZEN_READY_FOR_ANALYZE' if r['license']!='lic_trial' else 'INPUT_READY_LICENSE_HOLD'
 target=os.path.join(O,tag+'.gh');d.FilePath=target;saver=gh.Kernel.GH_DocumentIO();saver.Document=d;assert saver.SaveQuiet(target);r['gh']=target;r['sha256']=sha(target)
 write(os.path.join(O,tag+'_COMPLETE.json'),r)
 with open(os.path.join(O,'CURRENT_INPUT.json'),'w') as f:json.dump({'freeze':os.path.join(O,tag+'_COMPLETE.json')},f)
 Rhino.RhinoApp.WriteLine('NG03 READY: N25 S6 gap0.4 P36; '+str(meta['triangles'])+' triangles; '+str(meta['support_count'])+' ground nodes; '+r['license']+'; Analyze locked.')
except:
 r['status']='INPUT_HOLD_NO_ANALYZE';r['error']=traceback.format_exc()
 if 'd' in globals():r['observed_objects']=[{'id':str(o.InstanceGuid),'nick':unicode(o.NickName),'type':str(o.GetType())} for o in d.Objects]
 write(os.path.join(O,tag+'_HOLD.json'),r);Rhino.RhinoApp.WriteLine(traceback.format_exc())
