import json,math,hashlib,re
from pathlib import Path
B=Path(r'C:/Users/Acer/Documents/Codex/2026-10-04/be');O=B/'outputs/NG05_REINFORCEMENT_PAIR_20261018'
sources={'BASELINE':B/'outputs/NG04_G_L_GL_20261018/web','REPEAT':O/'REPEAT/web','NEW_ANCHOR':O/'NEW_ANCHOR/web'}
panel=lambda s:re.search(r'_P(\d{3})_',s).group(1)
models={};evidence=[];baseline_nodes={}
keys=['shell','original_shell','additional_shell','boundary','link','displacement','original_displacement']
for mode,folder in sources.items():
 g=json.loads((folder/'geometry.json').read_text());summary=json.loads((folder/'summary.json').read_text());cases={}
 ownership={f'{i:03d}':{'shells':[],'beams':[],'nodes':set()} for i in range(1,37)}
 for i,sh in enumerate(g['shells']):
  p=ownership[panel(sh['id'])];p['shells'].append(i);p['nodes'].update(sh['node_indices'])
 for i,beam in enumerate(g['beams']):
  p=ownership[panel(beam['id'])];p['beams'].append(i);p['nodes'].update(beam['nodes'])
 if mode=='BASELINE':baseline_nodes={p:set(row['nodes']) for p,row in ownership.items()}
 for row in summary['cases']:
  f=folder/row['file'];data=json.loads(f.read_text());evidence.append({'model':mode,'case':row['case'],'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()});rows=[]
  for p,owned in ownership.items():
   values={k:{'value':0,'case':row['case'],'id':None} for k in keys}
   def record(k,value,identifier):
    if value>values[k]['value']:values[k]={'value':value,'case':row['case'],'id':identifier}
   for i in owned['shells']:
    sh=g['shells'][i];v=max(data['shell_abs_principal_MPa'][i]);record('shell',v,sh['id']);record('additional_shell' if sh['id'].endswith('_F1') else 'original_shell',v,sh['id'])
   for i in owned['beams']:
    beam=g['beams'][i];record('boundary' if beam['category']=='cfrp_boundary' else 'link',data['beam_abs_normal_MPa'][i],beam['id'])
   for node in owned['nodes']:record('displacement',math.hypot(*data['node_translation_m'][node])*1000,node)
   for node in baseline_nodes[p]:record('original_displacement',math.hypot(*data['node_translation_m'][node])*1000,node)
   rows.append({'panel':'P'+p,'reinforced':p in ['024','033','034'],'metrics':values})
  cases[row['case']]=rows
 envelope=[]
 for i in range(36):envelope.append({'panel':cases['G'][i]['panel'],'reinforced':cases['G'][i]['reinforced'],'metrics':{k:max((rows[i]['metrics'][k] for rows in cases.values()),key=lambda r:r['value']) for k in keys}})
 cases['ENVELOPE']=envelope;models[mode]=cases
assert len(evidence)==27
# Per-panel envelopes recover the recorded global native extrema.
for mode,folder in sources.items():
 s=json.loads((folder/'summary.json').read_text())
 for metric,global_key in [('shell','shell_MPa'),('boundary','boundary_MPa'),('link','aluminium_link_MPa'),('displacement','displacement_mm')]:assert abs(max(r['metrics'][metric]['value'] for r in models[mode]['ENVELOPE'])-s['scales'][global_key])<1e-10
stats={}
for mode in ['REPEAT','NEW_ANCHOR']:
 stats[mode]={}
 for metric in keys:
  if metric=='additional_shell':continue
  rows=[]
  for old,new in zip(models['BASELINE']['ENVELOPE'],models[mode]['ENVELOPE']):
   a=old['metrics'][metric]['value'];b=new['metrics'][metric]['value'];delta=100*(1-b/a) if a else None
   rows.append({'panel':old['panel'],'baseline':a,'candidate':b,'reduction_pct':delta})
  stats[mode][metric]={'improved':sum(r['reduction_pct'] is not None and r['reduction_pct']>.1 for r in rows),'increased':sum(r['reduction_pct'] is not None and r['reduction_pct']<-.1 for r in rows),'near_equal':sum(r['reduction_pct'] is not None and abs(r['reduction_pct'])<=.1 for r in rows),'rows':rows}
result={'schema':'NG05_PANEL_COMPARISON/1','models':models,'statistics':stats,'classification_band_pct':.1,'notes':['Maximum per panel, not average. Envelope selects maximum over all nine cases separately for each metric; the governing case may differ between cells.','Shell includes original and additional winding. Original and additional maxima remain available separately.','Displacement includes nodes owned by the panel, including new ribbon nodes. Original displacement compares the same baseline panel nodes.','Each owner boundary beam is assigned to its panel; shared interface ownership is retained.','0.1% is a display description band, not an acceptance tolerance or safety criterion.','No new FE solve. All values selected from saved native Karamba fields.'],'evidence':evidence}
(O/'panel-comparison.json').write_text(json.dumps(result,separators=(',',':')),encoding='utf-8')
lines=['# Perbandingan per panel NG05','','Maksimum tiap panel dari sembilan kasus native Karamba. Kolom dapat dikendalikan kasus yang berbeda; bukan penjumlahan maksimum. Shell mencakup winding asli dan tambahan. Tidak ada solve baru.','', '| Panel | Baseline MPa | Ulang MPa | Turun % | Anchor MPa | Turun % |','|---|---:|---:|---:|---:|---:|']
for i in range(36):
 old=models['BASELINE']['ENVELOPE'][i];a=old['metrics']['shell']['value'];r=models['REPEAT']['ENVELOPE'][i]['metrics']['shell']['value'];n=models['NEW_ANCHOR']['ENVELOPE'][i]['metrics']['shell']['value'];lines.append(f"| {old['panel']} | {a:.4f} | {r:.4f} | {100*(1-r/a):.3f} | {n:.4f} | {100*(1-n/a):.3f} |")
lines+=['','## Sebaran perubahan','','Batas deskriptif hampir sama: +/-0,1%. Ini bukan toleransi penerimaan hasil atau penilaian keamanan.']
for mode,metrics in stats.items():
 for metric,s in metrics.items():lines.append(f"- {mode} {metric}: {s['improved']} turun; {s['increased']} naik; {s['near_equal']} hampir sama.")
lines+=['','Nilai negatif berarti kenaikan. Panel yang menerima reinforcement langsung: P024, P033, P034. Perubahan panel lain menunjukkan redistribusi respons dalam model, bukan bukti arah transfer gaya tanpa pemeriksaan gaya elemen.','', 'Detail nilai dan kasus pengendali per panel tersedia di panel-comparison.json. Tambahan massa kedua kandidat berbeda.']
(O/'PERBANDINGAN_PANEL.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({mode:{k:{x:s[x] for x in ['improved','increased','near_equal']} for k,s in metrics.items()} for mode,metrics in stats.items()}))
print('\n'.join(lines[5:]))
