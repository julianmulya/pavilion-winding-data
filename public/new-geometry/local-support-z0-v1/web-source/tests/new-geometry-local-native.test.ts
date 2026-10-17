import fs from 'node:fs';import {afterAll,expect,it} from 'vitest';
import {generateNewGeometryCore,LOCAL_SUPPORT_Z0_CONTRACT,type NewGeometrySource,type NewGeometryParameters} from '../src/lib/new-geometry';
const source=JSON.parse(fs.readFileSync('public/new-geometry/source-v2.json','utf8')) as NewGeometrySource;
type NativeCase={parameters:NewGeometryParameters;ground:{selected_open_panel:string;open_ground_panels:number;open_elevated_edges:number};A:number[][][];B:number[][][];winding:number[][][][];sleeved_panels:{total_length_m:number;mass_kg:number;visits:{center:number[];contact:number[]}[]}[]};
const cases=JSON.parse(fs.readFileSync('public/new-geometry/local-support-z0-v1/native-cases.json','utf8')) as NativeCase[];
const dist=(a:readonly number[],b:readonly number[])=>Math.hypot(...a.map((v,k)=>v-b[k]));const comparisons:unknown[]=[];
it.each(cases)('matches native C# local-support boundaries, ordered winding and sleeves: $parameters',c=>{
 const model=generateNewGeometryCore(source,c.parameters);let boundaryError=0,windingError=0,contactError=0,lengthError=0;
 expect(model.geometry_contract_id).toBe(LOCAL_SUPPORT_Z0_CONTRACT);expect(model.panels).toHaveLength(c.A.length);
 model.panels.forEach((p,i)=>{
  for(const layer of ['A','B'] as const){expect(p[layer]).toHaveLength(c[layer][i].length);p[layer].forEach((q,j)=>boundaryError=Math.max(boundaryError,dist(q,c[layer][i][j])));}
  expect(p.segments).toHaveLength(c.winding[i].length);p.segments.forEach((s,j)=>windingError=Math.max(windingError,dist(s.a,c.winding[i][j][0]),dist(s.b,c.winding[i][j][1])));
  const native=c.sleeved_panels[i];expect(p.sleeved_winding.visits).toHaveLength(native.visits.length);p.sleeved_winding.visits.forEach((v,j)=>contactError=Math.max(contactError,dist(v.center,native.visits[j].center),dist(v.contact,native.visits[j].contact)));lengthError=Math.max(lengthError,Math.abs(p.sleeved_winding.total_length_m-native.total_length_m));expect(Math.abs(p.sleeved_winding.material_metrics!.mass_kg-native.mass_kg)).toBeLessThan(1e-8);
 });
 expect(Math.max(boundaryError,windingError,contactError,lengthError)).toBeLessThan(1e-8);expect(c.ground.open_ground_panels).toBeGreaterThanOrEqual(1);expect(c.ground.open_elevated_edges).toBeGreaterThanOrEqual(2);expect(model.FE_status).toBe('NOT_EVALUATED');
 comparisons.push({parameters:c.parameters,selected_panel:c.ground.selected_open_panel,boundaryError,windingError,contactError,lengthError});
});
afterAll(()=>{fs.mkdirSync('reports/new-geometry/local-support-z0-v1',{recursive:true});fs.writeFileSync('reports/new-geometry/local-support-z0-v1/NATIVE_COMPARISON.json',JSON.stringify({contract:LOCAL_SUPPORT_Z0_CONTRACT,comparisons,FE_run:false},null,2));});
