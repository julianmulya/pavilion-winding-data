import {lazy,Suspense,useEffect,useRef,useState} from 'react';

import {Home,Search,Database,Info,Grid2X2,Layers3,Activity,Mouse,Focus,RotateCcw,Expand,Play,Pause,Download,ChevronLeft,ChevronRight} from 'lucide-react';

import {Button} from './ui/button';

import WindingPanelMetrics from './WindingPanelMetrics';

import NewGeometryOpenness from './NewGeometryOpenness';

import NewGeometryTargets from './NewGeometryTargets';
import ModuleConnections from './ModuleConnections';
import {SLEEVED_WINDING_CONTRACT} from '../lib/sleeved-winding';

import {NEW_ITERATIONS_KEY,iterationRecord,readIterationRecords,type OpennessIteration,type NewGeometryStudyModel} from '../lib/new-geometry-openness';

import GeometrySourceSwitch from './GeometrySourceSwitch';

import {loadNewGeometrySource,newMaxShift,NEW_MIN_SHIFT,FULL_BASE_Z0_CONTRACT,isNewDesignParameters,type NewGeometrySource,type NewGeometryParameters} from '../lib/new-geometry';

import {NEW_GEOMETRY_SOURCE_URL} from '../lib/new-geometry-pin';

import './new-geometry.css';

const Viewer=lazy(()=>import('./viewer/NewGeometryViewer'));

const fmt=(v:number,d=2)=>new Intl.NumberFormat('id-ID',{maximumFractionDigits:d}).format(v);

const key=(p:NewGeometryParameters)=>`${p.anchors}/${p.shift}/${p.gap}/${p.panels}`;

function save(name:string,value:unknown){const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}

function Metric({label,value,detail,icon:Icon}:{label:string;value:string;detail:string;icon:typeof Grid2X2}){return <div className="lab-metric"><div className="lab-metric-icon"><Icon size={22}/></div><div><span>{label}</span><strong>{value}</strong><small>{detail}</small></div></div>;}

export default function NewGeometryLab(){

 const [source,setSource]=useState<NewGeometrySource>(),[parameters,setParameters]=useState<NewGeometryParameters>(),[model,setModel]=useState<NewGeometryStudyModel>(),[error,setError]=useState(''),[retry,setRetry]=useState(0);

 const [anchorDetail,setAnchorDetail]=useState(false);
 const [panel,setPanel]=useState('ALL'),[progress,setProgress]=useState<number|null>(null),[playing,setPlaying]=useState(false),[speed,setSpeed]=useState(6),[view,setView]=useState<'perspective'|'top'|'front'|'right'>('perspective'),[reset,setReset]=useState(0),[showAnchors,setShowAnchors]=useState(true),[showBoundary,setShowBoundary]=useState(true),[showWinding,setShowWinding]=useState(true);

 const joint=null,showSleeves=false,showBolts=false; // Saved hardware is deferred from the exploration UI.

 const [designMode,setDesignMode]=useState<'parameters'|'target'>(()=>new URLSearchParams(window.location.search).get('mode')==='target'?'target':'parameters');

 const [iterations,setIterations]=useState<OpennessIteration[]>(()=>{try{return readIterationRecords(localStorage.getItem(NEW_ITERATIONS_KEY));}catch{return [];}});

 const visibleIterations=iterations.filter(r=>r.source_sha256===source?.source_snapshot_sha256&&r.geometry_contract_id===FULL_BASE_Z0_CONTRACT&&r.quantity_contract_id===SLEEVED_WINDING_CONTRACT.id&&isNewDesignParameters(r.parameters));

 const worker=useRef<Worker|null>(null),request=useRef(0),viewer=useRef<HTMLElement>(null),controls=useRef<HTMLElement>(null),method=useRef<HTMLElement>(null);

 useEffect(()=>{const abort=new AbortController();loadNewGeometrySource(abort.signal).then(s=>{if(!abort.signal.aborted){setSource(s);setParameters(s.web_defaults);setError('');}}).catch(e=>{if(!abort.signal.aborted)setError(e.message)});return()=>abort.abort();},[retry]);

 useEffect(()=>{if(!source)return;const w=new Worker(new URL('../lib/new-geometry.worker.ts',import.meta.url),{type:'module'});worker.current=w;w.onmessage=e=>{if(e.data.request!==request.current)return;if(e.data.error){setModel(undefined);setError(e.data.error);}else{setModel(e.data.model);setError('');}};w.onerror=()=>{setModel(undefined);setError('Generator berhenti. Tidak ada hasil lama yang dipakai sebagai pengganti.');};return()=>{worker.current=null;w.terminate();};},[source,retry]);

 useEffect(()=>{if(!source||!parameters)return;const id=++request.current,timer=setTimeout(()=>worker.current?.postMessage({request:id,source,parameters}),80);return()=>clearTimeout(timer);},[source,parameters,retry]);

 const current=parameters&&model&&key(parameters)===key(model.parameters)?model:undefined,selected=current?.panels.find(p=>p.id===panel),first=selected??current?.panels[0],maxSteps=anchorDetail?1:first?.sleeved_winding.steps.length??0;

 useEffect(()=>{if(!current)return;const row=iterationRecord(current);setIterations(old=>[...old.filter(r=>r.id!==row.id),row].slice(-100));},[current]);

 useEffect(()=>{try{localStorage.setItem(NEW_ITERATIONS_KEY,JSON.stringify(iterations));}catch{/* Export still works if storage is unavailable. */}},[iterations]);

 useEffect(()=>{if(!playing||!current||!maxSteps)return;const timer=setInterval(()=>setProgress(p=>Math.min(maxSteps,(p??0)+speed*.05)),50);return()=>clearInterval(timer);},[playing,current,maxSteps,speed]);

 useEffect(()=>{if(progress!==null&&maxSteps&&progress>=maxSteps)setPlaying(false);},[progress,maxSteps]);

 function change(name:keyof NewGeometryParameters,value:number){setAnchorDetail(false);setPlaying(false);setProgress(null);setParameters(old=>{if(!old)return old;const p={...old,[name]:value};p.shift=Math.max(NEW_MIN_SHIFT,Math.min(p.shift,newMaxShift(p.anchors)));return p;});if(name==='panels')setPanel('ALL');}

 function pick(id:string){setAnchorDetail(false);setPanel(id);setProgress(null);setPlaying(false);}

 function movePanel(delta:number){if(!current)return;const i=current.panels.findIndex(p=>p.id===panel),next=(Math.max(0,i)+delta+current.panels.length)%current.panels.length;pick(current.panels[next].id);}

 function exportCurrent(){if(current&&source)save('geometri-baru-'+current.parameters.panels+'-panel.json',{schema:'pavilion.new-geometry-configuration/2',displayed_quantity_contract:SLEEVED_WINDING_CONTRACT.id,source_file:source.source_filename,source_snapshot_sha256:source.source_snapshot_sha256,coordinate_units:source.coordinate_units,unit_note:source.unit_note,material_basis:source.material_basis,model:current,scope:'GEOMETRY_ONLY_NO_KARAMBA_RESULTS',historical_FE_attached:false});}

 return <div className="lab-shell new-geometry-lab">

  <nav className="lab-rail" aria-label="Main navigation">{[[Home,'Overview',()=>viewer.current?.scrollIntoView({behavior:'smooth'})],[Search,'Explore',()=>controls.current?.scrollIntoView({behavior:'smooth'})],[Database,'Dataset',()=>method.current?.scrollIntoView({behavior:'smooth'})],[Info,'Info',()=>method.current?.scrollIntoView({behavior:'smooth'})]].map(([Icon,label,fn])=>{const I=Icon as typeof Home;return <button key={String(label)} onClick={fn as ()=>void} aria-label={String(label)} className={label==='Overview'?'active':''}><I size={23}/><span>{String(label)}</span></button>;})}<span className="lab-rail-footer">CFRP<br/>RESEARCH</span></nav>

  <div className="lab-page"><header className="lab-header"><div><div className="lab-brand-line"><h1>Pavilion Winding Lab</h1><span className="lab-version">Geometri baru</span></div><p>Spatial Winding Research / Interactive Explorer</p></div><div className="lab-header-actions"><Button variant="outline" onClick={()=>method.current?.scrollIntoView({behavior:'smooth'})}>Method</Button><Button disabled={!current} onClick={exportCurrent}><Download size={17}/>Export</Button></div></header>

   <GeometrySourceSwitch active="new"/>

   {error&&<div className="lab-error" role="alert">{error}<Button variant="outline" onClick={()=>setRetry(v=>v+1)}>Retry</Button></div>}

   <div className="lab-layout">

    <section className="lab-summary" aria-label="Ringkasan geometri baru"><Metric icon={Grid2X2} label="Jumlah panel" value={current?String(current.panels.length):'…'} detail="Loft utama tetap"/><Metric icon={Layers3} label="Visual openness" value={current?fmt(current.openness.percent,2)+'%':'…'} detail="Pavilion · proyeksi berbobot luas"/><Metric icon={Activity} label={selected?`Panjang winding · ${selected.id}`:'Panjang winding total'} value={selected?fmt(selected.sleeved_winding.total_length_m,2)+' m':current?fmt(current.sleeved_winding.total_length_m,1)+' m':'—'} detail={selected?'Termasuk putaran sleeve':'Bentang + putaran sleeve'}/><Metric icon={Layers3} label={selected?`Berat winding · ${selected.id}`:'Berat winding total'} value={(selected?.sleeved_winding.material_metrics??current?.sleeved_winding.material_metrics)?fmt((selected?.sleeved_winding.material_metrics??current?.sleeved_winding.material_metrics)!.mass_kg,3)+' kg':'—'} detail="CFRP + lilitan · belum FE"/></section>

    <section className="lab-viewer-card" ref={viewer} aria-label="Viewer geometri baru"><div className="lab-viewer-top"><div className="lab-camera-tabs" role="group" aria-label="Camera view">{(['perspective','top','front','right'] as const).map(v=><button key={v} aria-pressed={view===v} onClick={()=>{setView(v);setReset(x=>x+1)}}>{v[0].toUpperCase()+v.slice(1)}</button>)}</div><div className="lab-mode-tabs"><button aria-pressed="true">Geometry</button><button disabled title="Belum ada hasil native Karamba untuk geometri ini">Structural analysis</button></div></div>

     {current?<Suspense fallback={<div className="lab-viewport lab-loading">Memuat viewer…</div>}><Viewer model={current} panel={panel} joint={joint} anchorDetail={anchorDetail} progress={progress} view={view} reset={reset} showAnchors={showAnchors} showSleeves={showSleeves} showBolts={showBolts} showBoundary={showBoundary} showWinding={showWinding} onSelect={pick}/></Suspense>:<div className="lab-viewport lab-loading" role="status">{error?'Geometri ditahan sampai sumber valid.':'Menghitung geometri dari parameter…'}</div>}

     <div className="lab-viewer-tools"><button aria-label="Fit geometry" onClick={()=>setReset(x=>x+1)}><Focus size={20}/></button><button aria-label="Reset geometry view" onClick={()=>{setView('perspective');setReset(x=>x+1)}}><RotateCcw size={20}/></button><button aria-label="Fullscreen geometry" onClick={()=>{if(document.fullscreenElement)void document.exitFullscreen();else void viewer.current?.requestFullscreen();}}><Expand size={20}/></button></div>

     <div className="new-geometry-view-label"><b>{panel==='ALL'?'Seluruh pavilion':`Panel ${panel}`}</b><span>{anchorDetail?'Detail sleeve · satu putaran':progress===null?'Pola lengkap':`Sequence ${fmt(progress,1)} / ${maxSteps}`}</span></div>



     <div className="lab-viewer-footer"><Mouse size={17}/><span>Drag untuk rotasi · scroll untuk zoom · klik boundary untuk memilih panel</span><small>Geometri GH · tanpa kontur FE</small></div>

    </section>

    <aside className="lab-controls" ref={controls} aria-label="Kontrol geometri baru"><div className="lab-section-title"><h2>Active configuration</h2><span className="lab-dot"/></div><p className="new-geometry-source-name">yang baru sesuai geometri.gh</p>

     <div className="new-design-mode" role="group" aria-label="Mode pencarian desain"><button aria-pressed={designMode==='parameters'} onClick={()=>setDesignMode('parameters')}>Design parameters</button><button aria-pressed={designMode==='target'} onClick={()=>setDesignMode('target')}>Target performance</button></div>

     {designMode==='target'&&source&&parameters&&<NewGeometryTargets source={source} parameters={parameters} history={visibleIterations} onApply={p=>{setAnchorDetail(false);setPlaying(false);setProgress(null);setPanel('ALL');setParameters(p);viewer.current?.scrollIntoView({behavior:'smooth',block:'start'});}}/>}

     {designMode==='target'&&parameters&&<p className="target-active-parameters">Input aktif: N{parameters.anchors} · shift {parameters.shift} · jarak {parameters.gap.toFixed(1)} m · {parameters.panels} panel</p>}

     {designMode==='parameters'&&parameters&&<>

      <div className="lab-slider-control"><label htmlFor="ng-anchors">Jumlah anchor per boundary (N)<output>{parameters.anchors}</output></label><input id="ng-anchors" aria-label="Jumlah anchor per boundary" type="range" min="10" max="50" step="1" value={parameters.anchors} onChange={e=>change('anchors',+e.target.value)}/><div><span>10</span><span>50</span></div></div>

      <div className="lab-slider-control"><label htmlFor="ng-shift">Winding shift (IDX)<output>{parameters.shift}</output></label><input id="ng-shift" aria-label="Winding shift geometri baru" type="range" min={NEW_MIN_SHIFT} max={newMaxShift(parameters.anchors)} step="1" value={parameters.shift} onChange={e=>change('shift',+e.target.value)}/><div><span>{NEW_MIN_SHIFT}</span><span>{newMaxShift(parameters.anchors)} · maksimum ⌊N/2⌋</span></div></div>

      <div className="lab-slider-control"><label htmlFor="ng-gap">Jarak boundary · m<output>{parameters.gap.toFixed(1)}</output></label><input id="ng-gap" aria-label="Jarak boundary geometri baru" type="range" min="0.1" max="1" step="0.1" value={parameters.gap} onChange={e=>change('gap',+e.target.value)}/><div><span>0.1</span><span>1.0 · native GH offset</span></div></div>

      <div className="lab-slider-control"><label htmlFor="ng-panels">Jumlah panel<output>{parameters.panels}</output></label><input id="ng-panels" aria-label="Jumlah panel geometri baru" type="range" min="36" max="100" step="1" value={parameters.panels} onChange={e=>change('panels',+e.target.value)}/><div><span>36</span><span>100 · bentuk utama tetap</span></div></div>

     </>}

     <section className="new-geometry-sequence" aria-label="Animasi winding setiap panel"><h3>Winding sequence</h3><label htmlFor="ng-panel">Pilih panel</label><div className="new-geometry-panel-row"><Button variant="outline" size="icon" disabled={!current} aria-label="Panel sebelumnya" onClick={()=>movePanel(-1)}><ChevronLeft size={16}/></Button><select id="ng-panel" aria-label="Pilih panel geometri baru" value={panel} onChange={e=>pick(e.target.value)}><option value="ALL">Seluruh pavilion</option>{current?.panels.map(p=><option key={p.id}>{p.id}</option>)}</select><Button variant="outline" size="icon" disabled={!current} aria-label="Panel selanjutnya" onClick={()=>movePanel(1)}><ChevronRight size={16}/></Button></div>

      <p>{anchorDetail?'Detail anchor pertama: satu putaran mengelilingi sleeve Ø12 mm. Tekan Play untuk melihat geraknya.':panel==='ALL'?'Semua panel dianimasikan serentak: satu putaran sleeve, lalu bentang lurus ke anchor berikutnya.':`Animasi ${panel}: satu putaran di setiap sleeve, kemudian bentang lurus bergantian B → A.`}</p><Button variant="outline" size="sm" disabled={!current} aria-pressed={anchorDetail} onClick={()=>{setAnchorDetail(v=>!v);if(!anchorDetail)setSpeed(1);if(panel==='ALL'&&current)setPanel(current.panels[0].id);setPlaying(false);setProgress(0);setReset(v=>v+1);}}>{anchorDetail?'Kembali ke panel':'Detail lilitan sleeve'}</Button>

      <label htmlFor="ng-sequence">Langkah winding <output>{progress===null?maxSteps:fmt(progress,1)} / {maxSteps}</output></label><input id="ng-sequence" aria-label="Winding sequence geometri baru" type="range" min="0" max={maxSteps||1} step="0.05" value={progress??maxSteps} disabled={!current||!!joint} onChange={e=>{setPlaying(false);setProgress(+e.target.value)}}/>

      <div className="new-geometry-sequence-actions"><Button disabled={!current||!showWinding||!!joint} onClick={()=>{if(!playing&&(progress===null||progress>=maxSteps))setProgress(0);setPlaying(v=>!v);}}>{playing?<Pause size={15}/>:<Play size={15}/>}<span>{playing?'Pause':'Play winding'}</span></Button><Button variant="outline" onClick={()=>{setPlaying(false);setProgress(0)}} disabled={!current}>Ulang</Button><Button variant="ghost" onClick={()=>{setPlaying(false);setProgress(null)}} disabled={!current}>Lengkap</Button></div>

      <label htmlFor="ng-speed">Kecepatan<select id="ng-speed" aria-label="Kecepatan animasi winding" value={speed} onChange={e=>setSpeed(+e.target.value)}>{[1,3,6,12,24].map(s=><option key={s} value={s}>{s} langkah/detik</option>)}</select></label>

      <div className="new-geometry-legend"><span><i/>Winding terpasang</span><span><i className="live"/>Garis / ujung aktif</span><span><i className="anchors"/>Anchor boundary</span></div>

     </section>

     <details className="lab-extra-controls"><summary>Geometry layers</summary><label><input type="checkbox" checked={showBoundary} onChange={e=>setShowBoundary(e.target.checked)}/>Boundary A / B · tipis transparan</label><label><input type="checkbox" checked={showWinding} onChange={e=>{setShowWinding(e.target.checked);if(!e.target.checked)setPlaying(false)}}/>Spatial winding</label><label><input type="checkbox" checked={showAnchors} onChange={e=>setShowAnchors(e.target.checked)}/>Titik anchor</label></details>

     <div className="lab-results"><h3>Results <span>{selected?'('+selected.id+')':'(seluruh pavilion)'}</span></h3><div><span>Visual openness</span><progress max="100" aria-label="Openness konfigurasi aktif" value={current?(selected?current.openness.panels.find(p=>p.panel_id===selected.id)!.percent:current.openness.percent):0}/><b>{current?fmt(selected?current.openness.panels.find(p=>p.panel_id===selected.id)!.percent:current.openness.percent,2)+'%':'—'}</b></div><div><span>Panjang winding</span><b>{selected?fmt(selected.sleeved_winding.total_length_m,3)+' m':current?fmt(current.sleeved_winding.total_length_m,3)+' m':'—'}</b></div><div><span>Berat winding CFRP</span><b>{(selected?.sleeved_winding.material_metrics??current?.sleeved_winding.material_metrics)?fmt((selected?.sleeved_winding.material_metrics??current?.sleeved_winding.material_metrics)!.mass_kg,3)+' kg':'—'}</b></div><div><span>Total pavilion · winding</span><b>{current?.sleeved_winding.material_metrics?fmt(current.sleeved_winding.material_metrics.mass_kg,3)+' kg':'—'}</b></div><div><span>Jumlah putaran sleeve</span><b>{current?fmt((selected?.sleeved_winding??current.sleeved_winding).wrap_count,0):'—'}</b></div><div><span>Panjang putaran lokal</span><b>{current?fmt((selected?.sleeved_winding??current.sleeved_winding).local_wrap_length_m,3)+' m':'—'}</b></div><div><span>Total bentang pavilion</span><b>{current?fmt(current.total_segments,0):'—'}</b></div><div><span>Anchor terkunjungi</span><b>{first?`${first.visited_anchors}/${first.available_anchors}`:'—'}</b></div><div><span>FE / stress / displacement</span><b className="lab-pending">Belum dihitung</b></div></div>

     <Button className="lab-full-button" variant="outline" onClick={exportCurrent} disabled={!current}><Download size={16}/>Download konfigurasi</Button>

    </aside>

    <WindingPanelMetrics model={current} basis={source?.material_basis} selected={panel} onSelect={id=>{pick(id);viewer.current?.scrollIntoView({behavior:'smooth',block:'start'});}}/>

    <NewGeometryOpenness model={current} source={source} panel={panel} history={visibleIterations} onLoad={p=>{setAnchorDetail(false);setPlaying(false);setProgress(null);setPanel('ALL');setParameters({...p});viewer.current?.scrollIntoView({behavior:'smooth',block:'start'});}}/>

    <ModuleConnections hardware={current?.hardware}/>
    <section className="new-geometry-method" ref={method} aria-label="Sumber dan metode geometri baru"><h2>Geometri baru dari GH aktif</h2><p>Loft disimpan tetap. Slider panel membagi domain UV yang sama; batas panel dihitung pada permukaan native. Jarak boundary memakai sepuluh permukaan offset native GH, tanpa interpolasi bentuk offset. Seluruh tepi bawah panel pada batas UV tanah dipasang pada Z=0 di kedua boundary A dan B, termasuk titik offset yang semula terangkat. Aturan ini aktif pada setiap jumlah panel dan jarak boundary. Anchor dibagi menurut panjang batas panel; langkah indeks = shift + 1. Eksplorasi aktif memakai shift minimum 5 hingga floor(N/2).</p><p>Beberapa shift mengunjungi sebagian anchor. Web mempertahankan urutan itu dan menampilkan jumlah terkunjungi, tanpa menambahkan jalur penutup buatan. Setiap anchor yang dikunjungi mendapat satu lingkaran penuh pada radius 6,5 mm, diikuti bentang lurus antar titik kontak sleeve. Urutan dan posisi pusat anchor tetap berasal dari GH. Lingkaran ini merupakan jalur konseptual; transisi tangen, tumpukan serat dan gerak robot belum diselesaikan.</p><p className="new-geometry-unit-note">{source?.unit_note}</p><p>Data sleeve anchor dan baut antar-modul tetap tersimpan dalam ekspor konfigurasi dan paket GitHub. Lilitan lokal masuk panjang dan berat CFRP. Openness tetap memakai proyeksi bentang sumber dan footprint boundary; putaran lokal dan hardware belum masuk area tutupannya. Acuan Stuttgart memakai tepi komposit diperkuat dan sleeve aluminium lokal; rangka fabrikasinya dilepas. Material, section tepi dan kekakuan sambungan FE geometri baru belum ditetapkan.</p><p>Preset web: N29 / shift14 / jarak0.4 / 55 panel. Nilai shift17 pada snapshot GH tetap tercatat sebagai riwayat sumber; preset web dibatasi ke14 sesuai aturan ⌊N/2⌋. Data FE pavilion lama tetap berada pada opsi sebelumnya.</p><div className="new-geometry-provenance"><a href={NEW_GEOMETRY_SOURCE_URL} download="geometri-baru-source.json">Download sumber geometri</a><small>Snapshot GH: {source?.source_snapshot_sha256.slice(0,16)??'…'} · data GitHub · frontend Vercel</small></div></section>

   </div>

  </div>

 </div>;

}



