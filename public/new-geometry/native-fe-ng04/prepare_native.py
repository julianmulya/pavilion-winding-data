import os,json,hashlib,traceback,sys,time,System,Rhino,Grasshopper as gh,clr
clr.AddReference('GH_IO');import GH_IO
W=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/work/sleeve_sequence';sys.path.insert(0,W)
import export_ground_native as ex
B=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs'
O=B+'/NG04_G_L_GL_20261018'
if not os.path.isdir(O):os.makedirs(O)
try:
 assert not os.path.exists(O+'/NG04_INPUT_COMPLETE.json'),'Input exists; do not replay'
 f=json.load(open(B+'/NG03_N25_S6_H04_P36_20261018/NG03_INPUT_1792258618_COMPLETE.json'))
 assert hashlib.sha256(open(f['gh'],'rb').read()).hexdigest()==f['sha256']
 old=gh.Instances.ActiveCanvas.Document
 if old:old.Enabled=False
 loader=gh.Kernel.GH_DocumentIO();assert loader.Open(f['gh']);d=loader.Document;d.Enabled=False
 ids=f['component_ids'];byid={str(o.InstanceGuid):o for o in d.Objects}
 analyze=byid[ids['analyze']];assemble=byid[ids['assemble']];owned=byid[ids['owned']];assert analyze.Locked
 nick_ids={row['nick']:row['id'] for row in json.load(open(B+'/NEW_GEOMETRY_NATIVE_KARAMBA_20261017/NG02_INPUT_FREEZE_1792253064_COMPLETE.json'))['components']}
 added=[]
 for j,case in enumerate(['G_X_POS','G_X_NEG','G_Y_POS','G_Y_NEG']):
  original=byid[nick_ids['NG01 '+case+' | total lateral 1 kN']]
  archive=GH_IO.Serialization.GH_Archive();assert archive.AppendObject(original,'Copy')
  c=gh.Instances.ComponentServer.EmitObjectProxy(original.ComponentGuid).CreateInstance();assert archive.ExtractObject(c,'Copy');c.NewInstanceGuid();c.CreateAttributes()
  for port in list(c.Params.Input)+list(c.Params.Output):port.NewInstanceGuid()
  for p,q in zip(c.Params.Input,original.Params.Input):
   p.RemoveAllSources()
   for source in q.Sources:p.AddSource(source)
  name=case.replace('G_','L_');c.NickName='NG04 '+name+' | lateral only 1 kN';c.Attributes.Pivot=System.Drawing.PointF(13000,3100+j*300)
  p=c.Params.Input[4];p.RemoveAllSources();p.PersistentData.Clear();p.PersistentData.Append(gh.Kernel.Types.GH_String(name))
  d.AddObject(c,False);assemble.Params.Input[2].AddSource(c.Params.Output[0]);added.append(c)
 gh.Instances.DocumentServer.AddDocument(d);gh.Instances.ActiveCanvas.Document=d;d.Enabled=True
 for c in added+[assemble,owned]:c.ExpireSolution(False)
 d.NewSolution(False)
 m=ex.data(owned.Params.Output[0])[0];assert not m.forcesReady()
 cases=[str(x) for x in ex.data(assemble.Params.Output[4])]
 assert len(cases)==9 and len(m.gravities)==5 and len(m.ploads)==5*1800+8*62
 assert len(m.nodes)==16276 and len(m.elems)==5417 and len(m.supports)==101
 assert abs(float(m.mass())*1000-f['model']['native_mass_equivalent_kg'])<1e-8
 for c in added+[assemble,owned]:assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 target=O+'/NG04_INPUT.gh';d.FilePath=target;io=gh.Kernel.GH_DocumentIO();io.Document=d;assert io.SaveQuiet(target)
 f.update(gh=target,sha256=hashlib.sha256(open(target,'rb').read()).hexdigest(),cases=cases,tag='NG04_INPUT',parent_freeze=B+'/NG03_N25_S6_H04_P36_20261018/NG03_INPUT_1792258618_COMPLETE.json')
 f['assumptions']['loads']='G, lateral only +/-X +/-Y 1kN, and G plus each lateral direction. Identical lateral application and structure to NG03.'
 ex.write_new(O+'/NG04_INPUT_COMPLETE.json',f)
 Rhino.RhinoApp.WriteLine('NG04 ready: nine native cases, same model, Analyze locked.')
 execfile(W+'/run_ng04_once.py')
except:
 ex.write_new(O+'/PREPARE_HOLD_'+str(int(time.time()))+'.json',{'error':traceback.format_exc()});Rhino.RhinoApp.WriteLine(traceback.format_exc())
