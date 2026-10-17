import os,json,hashlib,traceback,sys,time,io,gc,System,Rhino,Grasshopper as gh,clr
clr.AddReference('KarambaCommon');import feb
W=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/work/sleeve_sequence';sys.path.insert(0,W)
import export_ground_native as ex
B=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs';ROOT=B+'/NG05_REINFORCEMENT_PAIR_20261018'
MODE=os.environ.get('PAVILION_REINFORCEMENT_MODE','REPEAT');assert MODE in ['REPEAT','NEW_ANCHOR']
O=ROOT+'/'+MODE
if not os.path.isdir(O):os.makedirs(O)
try:
 assert not os.path.exists(O+'/INPUT_COMPLETE.json'),'Frozen input exists; no automatic replay'
 f=json.load(open(B+'/NG04_G_L_GL_20261018/NG04_INPUT_COMPLETE.json'))
 assert hashlib.sha256(open(f['gh'],'rb').read()).hexdigest()==f['sha256']
 old=gh.Instances.ActiveCanvas.Document
 if old:old.Enabled=False
 loader=gh.Kernel.GH_DocumentIO();assert loader.Open(f['gh']);d=loader.Document;d.Enabled=False
 byid={str(x.InstanceGuid):x for x in d.Objects};ids=f['component_ids'];geom=byid[ids['geometry']];owned=byid[ids['owned']];assemble=byid[ids['assemble']];analyze=byid[ids['analyze']];assert analyze.Locked
 assemble.Locked=True;owned.Locked=True
 src=geom.ScriptSource;src.AdditionalCode=io.open(W+'/NativeFE_'+MODE+'.cs',encoding='utf-8').read();geom.ScriptSource=src;owned.Code=io.open(W+'/owned_reinforcement.txt',encoding='utf-8').read()
 gh.Instances.DocumentServer.AddDocument(d);gh.Instances.ActiveCanvas.Document=d;d.Enabled=True;geom.ExpireSolution(False);d.NewSolution(False)
 assert not list(geom.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(geom)
 meta=json.loads(str(ex.data(geom.Params.Output[14])[0]));assert meta['panels']==36 and meta['frame_seed_nodes']==3676 and meta['frame_segments']==3581 and meta['equivalent_sleeve_links']==1800 and meta['load_nodes']==62 and meta['support_count']==101
 assert meta['triangles']==14400+(48 if MODE=='REPEAT' else 72)
 assemble.Locked=False;owned.Locked=False;assemble.ExpireSolution(False);owned.ExpireSolution(False);d.NewSolution(False)
 for c in [geom,assemble,owned]:assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 model=ex.data(owned.Params.Output[0])[0];assert not model.forcesReady() and analyze.Locked
 assert len(model.elems)==5420 and len(model.nodes)==meta['explicit_master_nodes'] and len(model.supports)==101
 assert len(model.ploads)==9496+5*meta['additional_turn_count'] and len(model.gravities)==5
 assert [ex.xyz(model.nodes[s.node_ind].pos) for s in model.supports]==f['support_coordinates_m']
 baseline=json.load(open(B+'/NG04_G_L_GL_20261018/web/geometry.json'))
 for sh in baseline['shells']:
  e=next(e for e in model.elems if str(e.id)==sh['id']);assert list(e.node_inds)==sh['node_indices']
  for index,p in zip(e.node_inds,sh['vertices']):assert ex.norm([a-b for a,b in zip(ex.xyz(model.nodes[index].pos),p)])<1e-10
  assert [[int(face.A),int(face.B),int(face.C)] for face in e.mesh.Faces]==sh['faces']
 baseline=None
 f['parent_freeze']=B+'/NG04_G_L_GL_20261018/NG04_INPUT_COMPLETE.json';f['reinforcement']=MODE;f['model']={k:v for k,v in meta.items() if k!='records'};f['model']['native_mass_equivalent_kg']=float(model.mass())*1000
 f['model']['added_turn_weight_kN']=meta['additional_turn_count']*2*3.141592653589793*.0065*.02*.000981747704*15.886773
 f['assumptions']['reinforcement']='Additional native F1 shells. REPEAT shares existing ribbon nodes; NEW_ANCHOR closes triangle through an existing native midpoint near hotspot with perfect bond and no new support. Full local CFRP turn dead weights included; new metal hardware/contact capacity not modeled.'
 f['input_comparison']={'all_original_shell_nodes_and_faces_identical':True,'supports_identical':True,'boundary_links_identical_count':True,'original_load_cases_retained':True,'initial_strain':False}
 ex.write_new(O+'/MESH_META.json',meta)
 target=O+'/INPUT.gh';d.FilePath=target;saver=gh.Kernel.GH_DocumentIO();saver.Document=d;assert saver.SaveQuiet(target);f.update(gh=target,sha256=hashlib.sha256(open(target,'rb').read()).hexdigest())
 ex.write_new(O+'/INPUT_COMPLETE.json',f);Rhino.RhinoApp.WriteLine('NG05 '+MODE+' input frozen. Analyze locked; original shell geometry and supports verified.')
except:
 ex.write_new(O+'/PREPARE_HOLD_'+str(int(time.time()))+'.json',{'error':traceback.format_exc()});Rhino.RhinoApp.WriteLine(traceback.format_exc())
