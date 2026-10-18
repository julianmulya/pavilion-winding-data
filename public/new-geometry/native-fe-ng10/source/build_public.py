from pathlib import Path
import json,zipfile,hashlib,math,csv
B=Path('.').resolve();O=B/'outputs/NG10_REINFORCEMENT_FROM_BATCH500_20261018';W=O/'web';W.mkdir(exist_ok=True);contract=json.loads((O/'CONTRACT.json').read_text());base=B/'outputs/NG09_FULL_BATCH_H100_20261018/runs'/contract['baseline'];rows=[];reviews={};summaryAll={}
for mode in ['BASELINE']+contract['variants']:
 folder=base if mode=='BASELINE' else O/mode;review=json.loads((folder/'REVIEW_COMPLETE.json').read_text());freeze=json.loads((folder/'INPUT_COMPLETE.json').read_text());assert len(review['cases'])==9 and not review['analyze']['errors'] and not review['initial_strain'];reviews[mode]=review
 if mode!='BASELINE':assert all(v for k,v in freeze['input_comparison'].items() if k!='coordinate_error_m') and freeze['input_comparison']['coordinate_error_m']<1e-10
 def vals(c):return [c['stress']['shell_max_abs_principal_stress']['value_MPa'],c['stress']['beam_max_abs_normal_stress_by_category']['cfrp_boundary']['value_MPa'],c['stress']['beam_max_abs_normal_stress_by_category']['equivalent_aluminium_link']['value_MPa'],c['maximum_displacement']['value_mm']]
 values=[max(vals(c)[i] for c in review['cases']) for i in range(4)];governing=[max(review['cases'],key=lambda c:vals(c)[i])['case'] for i in range(4)];m=review['model'];added=(m.get('additional_transfer_length_m',0)+m.get('additional_turn_count',0)*2*math.pi*.0065)*m['width_m']*m['thickness_m']*1620
 rows.append({'id':mode,'values':values,'governing':governing,'added_CFRP_kg':added,'added_length_m':m.get('additional_transfer_length_m',0),'added_turn_count':m.get('additional_turn_count',0),'max_force_residual_kN':max(c['equilibrium']['residual_kN'] for c in review['cases']),'shell_hotspot':max(review['cases'],key=lambda c:vals(c)[0])['stress']['shell_max_abs_principal_stress'],'input_checks':freeze.get('input_comparison',{}),'input_gh_sha256':freeze['sha256'],'review_sha256':hashlib.sha256((folder/'REVIEW_COMPLETE.json').read_bytes()).hexdigest(),'shell_category_envelopes':({'original_winding':values[0],'additional_winding':None} if mode=='BASELINE' else {category:max(c['stress']['shell_maxima_by_category'][category]['value_MPa'] for c in review['cases']) for category in ['original_winding','additional_winding']})})
 if mode=='BASELINE':continue
 dest=W/mode;dest.mkdir(exist_ok=True);summary={'configuration':freeze['configuration'],'model':m,'cases':[],'scales':dict(zip(['shell_MPa','boundary_MPa','aluminium_link_MPa','displacement_mm'],values)),'ground':{'selected_open_panel':freeze['ground']['selected_open_panel']},'analyze':review['analyze'],'source_gh':{'name':'NG10_'+mode+'_ANALYZE_LOCKED.gh'},'max_force_residual_kN':rows[-1]['max_force_residual_kN']};geometry=None
 with zipfile.ZipFile(folder/'NATIVE_RAW.zip') as z:
  assert len(z.namelist())==27
  for c in review['cases']:
   prefix='NG10_'+mode+'_NATIVE_NINE_V2_'+c['case']+'_DETAIL';shell=json.loads(z.read(prefix+'_SHELL_STRESS_RAW.json'));beam=json.loads(z.read(prefix+'_BEAM_STRESS_RAW.json'));direct=json.loads(z.read(prefix+'_DIRECT_NATIVE_RAW.json'));assert shell['shell_face_mapping_error_m']<1e-8
   if geometry is None:geometry={'schema':'NG10_NATIVE_FE_GEOMETRY/1','shells':[{k:s[k] for k in ['id','vertices','faces','node_indices']} for s in shell['shells']],'beams':[{k:b[k] for k in ['id','category','a','b','nodes']} for b in beam['beams']],'supports':freeze['support_coordinates_m'],'load_points_m':freeze['load_points_m']}
   field={'schema':'NG10_NATIVE_FE_CASE/1','case':c['case'],'shell_abs_principal_MPa':[[max(abs(surf[key][i]) for surf in s['surfaces'].values() for key in ['sigma1_MPa','sigma2_MPa']) for i in range(len(s['faces']))] for s in shell['shells']],'node_translation_m':[v for br in direct['node_displacement_component']['outputs'][1]['branches'] for v in br['values']],'beam_abs_normal_MPa':[max(abs(v) for key in ['minimum_MPa','maximum_MPa'] for v in b[key]) for b in beam['beams']]}
   assert max(v for sh in field['shell_abs_principal_MPa'] for v in sh)==c['stress']['shell_max_abs_principal_stress']['value_MPa'];assert abs(max(math.hypot(*v) for v in field['node_translation_m'])*1000-c['maximum_displacement']['value_mm'])<1e-8
   for category in ['cfrp_boundary','equivalent_aluminium_link']:
    assert abs(max(v for v,b in zip(field['beam_abs_normal_MPa'],geometry['beams']) if b['category']==category)-c['stress']['beam_max_abs_normal_stress_by_category'][category]['value_MPa'])<1e-8
   for pid,pnl in c['panels'].items():
    indices=[i for i,sh in enumerate(geometry['shells']) if '_'+pid+'_' in sh['id']];assert abs(max(v for i in indices for v in field['shell_abs_principal_MPa'][i])-pnl['shell_MPa'])<1e-8
   assert sum(len(s['faces']) for s in shell['shells'])==m['triangles'];(dest/(c['case']+'.json')).write_text(json.dumps(field,separators=(',',':')));summary['cases'].append({**{k:c[k] for k in ['case','stress','maximum_displacement','equilibrium']},'file':c['case']+'.json'})
 (dest/'geometry.json').write_text(json.dumps(geometry,separators=(',',':')));(dest/'summary.json').write_text(json.dumps(summary,separators=(',',':')))
superposition={}
for mode in ['BASELINE']+contract['variants']:
 folder=(B/'outputs/NG09_PUBLIC_500_20261018/web/contours'/contract['baseline']) if mode=='BASELINE' else W/mode
 fields={c:json.loads((folder/(c+'.json')).read_text())['node_translation_m'] for c in contract['cases']};maximum=0.
 for axis in ['X_POS','X_NEG','Y_POS','Y_NEG']:
  maximum=max(maximum,max(abs(combo[k]-g[k]-lat[k]) for combo,g,lat in zip(fields['G_'+axis],fields['G'],fields['L_'+axis]) for k in range(3)))
 assert maximum<1e-8,(mode,maximum);superposition[mode]=maximum
for row in rows:
 row['reduction_pct']=[(a-b)/a*100 for a,b in zip(rows[0]['values'],row['values'])];row['shell_claim']='BASELINE' if row['id']=='BASELINE' else 'SHELL_ENVELOPE_REDUCED' if row['values'][0]<rows[0]['values'][0] else 'SHELL_ENVELOPE_NOT_REDUCED';row['capacity_assessed']=False
panels=[]
for pid in sorted(reviews['BASELINE']['cases'][0]['panels']):
 panels.append({'id':pid,'variants':{mode:{'envelope':[max(c['panels'][pid][k] for c in d['cases']) for k in ['shell_MPa','cfrp_boundary_MPa','equivalent_aluminium_link_MPa','shell_node_u_mm']],'cases':{c['case']:[c['panels'][pid][k] for k in ['shell_MPa','cfrp_boundary_MPa','equivalent_aluminium_link_MPa','shell_node_u_mm']] for c in d['cases']}} for mode,d in reviews.items()}})
comparison={'status':'THREE_NATIVE_REINFORCEMENTS_REVIEWED','configuration':contract['configuration'],'baseline':contract['baseline'],'targets':[t['panel'] for t in contract['targets']],'rows':rows,'panels':panels,'cases':contract['cases'],'scales':dict(zip(['shell_MPa','boundary_MPa','aluminium_link_MPa','displacement_mm'],[max(r['values'][i] for r in rows) for i in range(4)])),'capacity_assessed':False,'native_displacement_superposition_error_m':superposition,'notes':[contract['new_anchor_assumption'],contract['ab_assumption'],contract['mass_comparison'],'Maximum shell includes original and additional winding; beam normal stress remains separate. All9cases native Karamba; InitialStrain OFF. Baseline500 batch remains paused.']}
conclusions=[]
for row in rows[1:]:
 conclusions.append('%s: maksimum shell %s %.2f%% terhadap baseline; tambahan winding %.3f kg.'%(row['id'],'turun' if row['reduction_pct'][0]>0 else 'naik',abs(row['reduction_pct'][0]),row['added_CFRP_kg']))
 for k,title in [(1,'boundary CFRP'),(2,'link aluminium'),(3,'perpindahan global')]:
  if row['reduction_pct'][k]<0:conclusions.append('%s: %s naik %.2f%%; penurunan shell tidak berarti semua hasil membaik.'%(row['id'],title,abs(row['reduction_pct'][k])))
best=min(rows[1:],key=lambda r:r['values'][0]);conclusions.append('Maksimum shell terendah di antara tiga kandidat adalah %s. Kesimpulan terbatas pada baseline dan kandidat ini, bukan optimum global atau bukti kapasitas aman.'%best['id']);comparison['conclusions']=conclusions
(W/'comparison.json').write_text(json.dumps(comparison,separators=(',',':')))
with (W/'panel-comparison.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.writer(f);writer.writerow(['panel','variant','shell_MPa','boundary_MPa','link_MPa','shell_node_u_mm'])
 for p in panels:
  for mode,v in p['variants'].items():writer.writerow([p['id'],mode,*v['envelope']])
print(json.dumps({'rows':rows,'bytes':sum(p.stat().st_size for p in W.rglob('*') if p.is_file())}))
