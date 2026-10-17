import {afterAll,expect,it} from 'vitest';
import fs from 'node:fs';
import {FULL_BASE_Z0_CONTRACT,newPanelBoundaries,generateNewGeometryCore,type NewGeometrySource,type NewGeometryParameters} from '../src/lib/new-geometry';
const source=JSON.parse(fs.readFileSync('public/new-geometry/source-v2.json','utf8')) as NewGeometrySource;
const dist=(a:readonly number[],b:readonly number[])=>Math.hypot(...a.map((v,k)=>v-b[k]));
const report:{panels:number;gap:number;ground_panels:number;ground_edges_both_layers:number}[]=[];
it('keeps the COMPLETE A and B base edges at Z=0 for all 650 panel-count/gap combinations',()=>{
 const unchanged=JSON.stringify(source);
 for(let n=36;n<=100;n++)for(let g=1;g<=10;g++){
  const pick={panels:n,gap:g/10},rows=newPanelBoundaries(source,pick),raw=newPanelBoundaries(source,pick,'SOURCE');let feet=0,edges=0;
  for(let i=0;i<rows.length;i++){
   const row=rows[i],floor=(j:number)=>Math.abs(row.uv[j][1])<1e-10||Math.abs(row.uv[j][1]-1)<1e-10;
   const baseEdges=row.uv.map((_,j)=>j).filter(j=>floor(j)&&floor((j+1)%row.uv.length)&&Math.abs(row.uv[j][1]-row.uv[(j+1)%row.uv.length][1])<1e-10);
   if(baseEdges.length)feet++;
   for(const layer of ['A','B'] as const){
    expect(row[layer][0]).toEqual(row[layer].at(-1));
    row.uv.forEach((_,j)=>{const q=row[layer][j],old=raw[i][layer][j];expect(q.slice(0,2)).toEqual(old.slice(0,2));if(floor(j))expect(q[2]).toBe(0);else expect(q).toEqual(old);expect(q[2]).toBeGreaterThanOrEqual(-1e-8);});
    for(const j of baseEdges){expect(row[layer][j][2]).toBe(0);expect(row[layer][j+1][2]).toBe(0);expect(dist(row[layer][j],row[layer][j+1])).toBeGreaterThan(1e-9);edges++;}
   }
  }
  expect(feet).toBeGreaterThan(0);report.push({panels:n,gap:g/10,ground_panels:feet,ground_edges_both_layers:edges});
 }
 expect(JSON.stringify(source)).toBe(unchanged);expect(report).toHaveLength(650);
},30000);
type NativeCase={parameters:NewGeometryParameters;A:number[][][];B:number[][][];winding:number[][][][];sleeved_panels:{total_length_m:number;mass_kg:number;visits:{center:number[];contact:number[]}[]}[]};
const native=JSON.parse(fs.readFileSync('public/new-geometry/full-base-z0-v1/native-cases.json','utf8')) as NativeCase[];
const comparisons:unknown[]=[];
it.each(native)('matches the independently computed full-base native GH boundaries, winding and sleeves: $parameters',c=>{
 const m=generateNewGeometryCore(source,c.parameters);let boundaryError=0,windingError=0,contactError=0,lengthError=0;
 expect(m.geometry_contract_id).toBe(FULL_BASE_Z0_CONTRACT);expect(m.panels).toHaveLength(c.A.length);
 m.panels.forEach((p,i)=>{
  for(const layer of ['A','B'] as const){expect(p[layer]).toHaveLength(c[layer][i].length);p[layer].forEach((q,j)=>boundaryError=Math.max(boundaryError,dist(q,c[layer][i][j])));}
  expect(p.segments).toHaveLength(c.winding[i].length);p.segments.forEach((s,j)=>{windingError=Math.max(windingError,dist(s.a,c.winding[i][j][0]),dist(s.b,c.winding[i][j][1]));});
  const r=c.sleeved_panels[i];expect(p.sleeved_winding.visits).toHaveLength(r.visits.length);p.sleeved_winding.visits.forEach((v,j)=>{contactError=Math.max(contactError,dist(v.center,r.visits[j].center),dist(v.contact,r.visits[j].contact));});lengthError=Math.max(lengthError,Math.abs(p.sleeved_winding.total_length_m-r.total_length_m));expect(Math.abs(p.sleeved_winding.material_metrics!.mass_kg-r.mass_kg)).toBeLessThan(1e-8);
 });
 expect(Math.max(boundaryError,windingError,contactError,lengthError)).toBeLessThan(1e-8);expect(m.FE_status).toBe('NOT_EVALUATED');comparisons.push({parameters:c.parameters,boundaryError,windingError,contactError,lengthError});
});
afterAll(()=>{fs.mkdirSync('reports/new-geometry/full-base-z0-v1',{recursive:true});fs.writeFileSync('reports/new-geometry/full-base-z0-v1/VERIFICATION.json',JSON.stringify({contract:FULL_BASE_Z0_CONTRACT,combinations:report,native_comparisons:comparisons,FE_run:false},null,2));});
