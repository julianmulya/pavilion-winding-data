from pathlib import Path
import json,math,sys,hashlib
p=Path(sys.argv[1]);tag='NG10_'+p.name+'_NATIVE_NINE_V2';c=json.loads((p/(tag+'_COMPLETE.json')).read_text());f=json.loads((p/'INPUT_COMPLETE.json').read_text());assert c['native_analyze_completed'] and len(c['case_results'])==9 and not c['analyze_component']['errors'];assert c['export_mode']=='NATIVE_COMPACT_V2' and f['initial_strain']==False;cases=[]
assert set(x['case'] for x in c['case_results'])==set(['G','G_X_POS','G_X_NEG','G_Y_POS','G_Y_NEG','L_X_POS','L_X_NEG','L_Y_POS','L_Y_NEG'])
for row in c['case_results']:
 prefix=tag+'_'+row['case'];stress=json.loads((p/(prefix+'_STRESS_NATIVE_COMPACT.json')).read_text());direct=json.loads((p/(prefix+'_DIRECT_NATIVE_COMPACT.json')).read_text());assert stress['shell_face_mapping_error_m']<1e-8 and row['equilibrium']['residual_kN']<1e-7
 assert stress['shell_faces']==f['model']['triangles'] and stress['beam_records']==f['model']['frame_segments']+f['model']['equivalent_sleeve_links'];assert len(stress['panels'])==f['configuration']['panels'];assert all(x['bulk_vs_native_single_max_difference_kN_m2']<1e-8 for x in stress['mapping_checks']);assert all(not x['errors'] for x in stress['native_stress_components'])
 assert direct['sample_count']==f['model']['explicit_master_nodes'] and direct['all_translations_finite'];assert not direct['node_displacement_component']['errors'] and not direct['reaction_component']['errors']
 panels=row['stress']['panels'];assert all(all(math.isfinite(v) for k,v in panel.items() if isinstance(v,(int,float))) for panel in panels.values())
 assert abs(max(x['shell_MPa'] for x in panels.values())-row['stress']['shell_max_abs_principal_stress']['value_MPa'])<1e-8
 for category in ['cfrp_boundary','equivalent_aluminium_link']:assert abs(max(x[category+'_MPa'] for x in panels.values())-row['stress']['beam_max_abs_normal_stress_by_category'][category]['value_MPa'])<1e-8
 assert abs(max(x['node_u_mm'] for x in panels.values())-row['maximum_displacement']['value_mm'])<1e-8
 cases.append(dict(case=row['case'],stress={k:v for k,v in row['stress'].items() if k!='panels'},maximum_displacement=row['maximum_displacement'],equilibrium=row['equilibrium'],panels=panels))
review={'status':'NINE_NATIVE_CASES_REVIEWED','configuration':f['configuration'],'configuration_id':p.name,'export_mode':'NATIVE_COMPACT_V2','cases':cases,'model':f['model'],'license':c['license'],'analyze':c['analyze_component'],'initial_strain':False,'input_gh_sha256':f['sha256'],'capacity_assessed':False,'full_contours_retained':c.get('full_contours_retained',False),'native_compact_evidence_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in p.glob('*_NATIVE_COMPACT.json')},'timing':{'solve_seconds':c['solve_seconds'],'compact_export_seconds':c['compact_export_seconds'],'total_solve_and_export_seconds':c['total_solve_and_export_seconds']}}

if c.get('full_contours_retained'):
 import zipfile
 with zipfile.ZipFile(p/'NATIVE_RAW.zip') as archive:
  assert len(archive.namelist())==27
  for row in c['case_results']:
   detailed=json.loads(archive.read(tag+'_'+row['case']+'_DETAIL_SHELL_STRESS_RAW.json'))
   assert abs(detailed['shell_max_abs_principal_stress']['value_MPa']-row['stress']['shell_max_abs_principal_stress']['value_MPa'])<1e-10
 review['raw_zip_sha256']=hashlib.sha256((p/'NATIVE_RAW.zip').read_bytes()).hexdigest()
(p/'REVIEW_COMPLETE.json').write_text(json.dumps(review,separators=(',',':')),encoding='utf-8');print(json.dumps({'id':p.name,'cases':9,'shell_MPa':max(r['stress']['shell_max_abs_principal_stress']['value_MPa'] for r in cases),'u_mm':max(r['maximum_displacement']['value_mm'] for r in cases),'bytes':sum(x.stat().st_size for x in p.iterdir() if x.is_file()),'mode':'NATIVE_COMPACT_V2'}))
