# -*- coding: utf-8 -*-
import os,json,hashlib,traceback,sys,time,io,math,System,Rhino,Grasshopper as gh,clr
clr.AddReference('KarambaCommon');import feb
W=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/work/sleeve_sequence';sys.path.insert(0,W)
import export_ground_native as ex
O=RUN_ROOT+'/'+VARIANT
if not os.path.isdir(O):os.makedirs(O)
try:
 assert not os.path.exists(O+'/INPUT_COMPLETE.json'),'Frozen input exists; no replay'
 contract=json.load(open(RUN_ROOT+'/CONTRACT.json'));f=json.load(open(contract['baseline_input']));base=os.path.dirname(contract['baseline_input']);assert hashlib.sha256(open(f['gh'],'rb').read()).hexdigest()==f['sha256']
 old=gh.Instances.ActiveCanvas.Document
 if old:old.Enabled=False
 loader=gh.Kernel.GH_DocumentIO();assert loader.Open(f['gh']);d=loader.Document;d.Enabled=False
 byid={str(x.InstanceGuid):x for x in d.Objects};ids=f['component_ids'];geom=byid[ids['geometry']];owned=byid[ids['owned']];assemble=byid[ids['assemble']];analyze=byid[ids['analyze']];assert analyze.Locked
 assemble.Locked=True;owned.Locked=True;src=geom.ScriptSource;src.AdditionalCode=io.open(W+'/ng10/NativeFE_'+VARIANT+'.cs',encoding='utf-8').read();geom.ScriptSource=src;owned.Code=io.open(W+'/owned_reinforcement.txt',encoding='utf-8').read()
 gh.Instances.DocumentServer.AddDocument(d);gh.Instances.ActiveCanvas.Document=d;d.Enabled=True;geom.ExpireSolution(False);d.NewSolution(False)
 assert not list(geom.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(geom)
 meta=json.loads(str(ex.data(geom.Params.Output[14])[0]));original=json.load(open(base+'/MESH_META.json'))
 for key in ['panels','frame_seed_nodes','frame_segments','equivalent_sleeve_links','load_nodes','support_count','wrap_count','boundary_length_m','width_m','thickness_m']:assert meta[key]==original[key],key
 added={'REPEAT':6,'NEW_ANCHOR':9,'AB_SHIFT6':78}[VARIANT];assert meta['triangles']==original['triangles']+8*added and meta['strands']==original['strands']+added
 assemble.Locked=False;owned.Locked=False;assemble.ExpireSolution(False);owned.ExpireSolution(False);d.NewSolution(False)
 for c in [geom,assemble,owned]:assert not list(c.RuntimeMessages(gh.Kernel.GH_RuntimeMessageLevel.Error)),ex.direct(c)
 model=ex.data(owned.Params.Output[0])[0];assert not model.forcesReady() and analyze.Locked
 assert len(model.nodes)==meta['explicit_master_nodes'] and len(model.supports)==original['support_count'] and len(model.gravities)==5
 assert len(model.ploads)==5*original['wrap_count']+8*original['load_nodes']+5*meta['additional_turn_count']
 assert [ex.xyz(model.nodes[s.node_ind].pos) for s in model.supports]==f['support_coordinates_m']
 assert all([bool(x) for x in s.Condition]==[True,True,True,False,False,False] for s in model.supports)
 baseline=json.load(open(r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs/NG09_PUBLIC_500_20261018/web/contours/N13_S06_H100_P087/geometry.json'));elements={str(e.id):e for e in model.elems};coordinate_error=0.
 for sh in baseline['shells']:
  e=elements[sh['id']];assert list(e.node_inds)==sh['node_indices']
  for index,p in zip(e.node_inds,sh['vertices']):coordinate_error=max(coordinate_error,ex.norm([a-b for a,b in zip(ex.xyz(model.nodes[index].pos),p)]))
  assert [[int(face.A),int(face.B),int(face.C)] for face in e.mesh.Faces]==sh['faces']
 for beam in baseline['beams']:
  e=elements[beam['id']];assert list(e.node_inds)==beam['nodes'];assert ex.norm([a-b for a,b in zip(ex.xyz(model.nodes[e.node_inds[0]].pos),beam['a'])])<1e-10 and ex.norm([a-b for a,b in zip(ex.xyz(model.nodes[e.node_inds[1]].pos),beam['b'])])<1e-10
 assert coordinate_error<1e-10
 for prefix in ['NG_EDGE','NG_LINK']:
  group=[e for e in model.elems if str(e.id).startswith(prefix)];actual={'count':len(group),'area_m2':float(group[0].crosec.A),'E1_kN_m2':float(group[0].crosec.material.E(0))};assert actual==f['beam_sections'][prefix],actual
 for name,expected in f['native_materials'].items():
  mat=(next(e for e in model.elems if e.GetType().Name=='ModelShell').crosec.material if 'CFRP' in name else next(e for e in model.elems if str(e.id).startswith('NG_LINK')).crosec.material);actual={'E1_kN_m2':float(mat.E(0)),'E2_kN_m2':float(mat.E(1)),'G12_kN_m2':float(mat.G12()),'gamma_kN_m3':float(mat.gamma())};assert actual==expected
 assert [ex.xyz(p) for p in ex.data(geom.Params.Output[12])]==f['load_points_m']
 totals={case:[0.,0.,0.] for case in f['cases']}
 for load in model.ploads:
  for k,v in enumerate(ex.xyz(load.force)):totals[str(load.LcName)][k]+=v
 force=meta['additional_turn_count']*2*math.pi*.0065*.02*.000981747704*15.886773
 for case in f['cases']:
  expected=list(f['native_point_load_totals_before_analyze'][case]);expected[2]-=0 if case.startswith('L_') else force;assert ex.norm([totals[case][k]-expected[k] for k in range(3)])<1e-9,case
 baseline=None;f['parent_freeze']=contract['baseline_input'];f['reinforcement']=VARIANT;f['model']={k:v for k,v in meta.items() if k!='records'};f['model']['native_mass_equivalent_kg']=float(model.mass())*1000;f['model']['added_turn_weight_kN']=force;f['native_point_load_totals_before_analyze']=totals
 f['input_comparison']={'original_F0_nodes_faces_identical':True,'coordinate_error_m':coordinate_error,'beam_geometry_connectivity_material_section_identical':True,'materials_identical':True,'support_conditions_and_coordinates_identical':True,'lateral_load_points_and_forces_identical':True,'initial_strain_OFF':True,'changes_only_additional_F1_shells_and_dead_weight':True};f['assumptions']['reinforcement']=contract['new_anchor_assumption'] if VARIANT=='NEW_ANCHOR' else contract['ab_assumption'] if VARIANT=='AB_SHIFT6' else 'Repeat two highest-stress original spans in each of three fixed target panels; perfectly bonded original nodes.'
 ex.write_new(O+'/MESH_META.json',meta);ex.write_new(O+'/BOUNDARIES.json',json.load(open(base+'/BOUNDARIES.json')))
 target=O+'/INPUT.gh';d.FilePath=target;saver=gh.Kernel.GH_DocumentIO();saver.Document=d;assert saver.SaveQuiet(target);f.update(gh=target,sha256=hashlib.sha256(open(target,'rb').read()).hexdigest());ex.write_new(O+'/INPUT_COMPLETE.json',f)
except:
 ex.write_new(O+'/PREPARE_HOLD_'+str(int(time.time()))+'.json',{'error':traceback.format_exc()});Rhino.RhinoApp.WriteLine(traceback.format_exc())
