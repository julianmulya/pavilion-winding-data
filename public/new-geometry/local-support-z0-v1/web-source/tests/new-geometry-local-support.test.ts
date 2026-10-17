import fs from 'node:fs';import {afterAll,expect,it} from 'vitest';
import {newPanelBoundaries,type NewGeometrySource} from '../src/lib/new-geometry';
import {localSupportInterval,LOCAL_SUPPORT_Z0_CONTRACT} from '../src/lib/local-support-base';
const source=JSON.parse(fs.readFileSync('public/new-geometry/source-v2.json','utf8')) as NewGeometrySource;
const report:unknown[]=[];
it('retains both rising open-side slopes and at least one full A/B support panel in every design combination',()=>{
 const snapshot=JSON.stringify(source);
 for(let n=36;n<=100;n++)for(let step=1;step<=10;step++){
  const pick={panels:n,gap:step/10},raw=newPanelBoundaries(source,pick,'SOURCE'),rows=newPanelBoundaries(source,pick),interval=localSupportInterval(raw);let feet=0,slopes=0,unchangedElevated=0;
  const shared=new Map<string,number[]>();
  rows.forEach((p,index)=>{
   for(const layer of ['A','B'] as const)p.uv.forEach(([u,v],j)=>{
    const point=p[layer][j],old=raw[index][layer][j],ground=Math.abs(v)<1e-10||(Math.abs(v-1)<1e-10&&u>=interval.lo-1e-10&&u<=interval.hi+1e-10);
    expect(point.slice(0,2)).toEqual(old.slice(0,2));if(ground)expect(point[2]).toBe(0);else expect(point).toEqual(old);expect(point[2]).toBeGreaterThanOrEqual(-1e-8);
    const key=layer+'/'+u.toFixed(8)+'/'+v.toFixed(8),existing=shared.get(key);if(existing)expect(Math.hypot(...point.map((x,k)=>x-existing[k]))).toBeLessThan(1e-8);else shared.set(key,point);
    if(Math.abs(v-1)<1e-10&&old[2]>.5&&!ground){expect(point[2]).toBe(old[2]);unchangedElevated++;}
   });
   p.uv.forEach(([u,v],j)=>{const next=(j+1)%p.uv.length;if(Math.abs(v-1)>1e-10||Math.abs(p.uv[next][1]-1)>1e-10)return;
    const foot=u>=interval.lo-1e-10&&u<=interval.hi+1e-10&&p.uv[next][0]>=interval.lo-1e-10&&p.uv[next][0]<=interval.hi+1e-10;
    if(foot){feet++;for(const layer of ['A','B'] as const){expect(p[layer][j][2]).toBe(0);expect(p[layer][next][2]).toBe(0);expect(Math.hypot(...p[layer][j].map((x,k)=>x-p[layer][next][k]))).toBeGreaterThan(.01);}}
    else {slopes++;expect(Math.max(p.A[j][2],p.A[next][2],p.B[j][2],p.B[next][2])).toBeGreaterThan(0);}
   });
  });
  expect(feet).toBeGreaterThanOrEqual(1);expect(feet).toBeLessThan(interval.open_edge_count);expect(slopes).toBeGreaterThanOrEqual(2);expect(unchangedElevated).toBeGreaterThan(0);
  report.push({parameters:pick,selected_panel:interval.selected_panel,support_u_interval:[interval.lo,interval.hi],open_support_panels:feet,open_rising_edges:slopes,unchanged_elevated_vertices:unchangedElevated});
 }
 expect(report).toHaveLength(650);expect(JSON.stringify(source)).toBe(snapshot);
},30000);
afterAll(()=>{const dir='reports/new-geometry/local-support-z0-v1';fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(dir+'/VERIFICATION.json',JSON.stringify({contract:LOCAL_SUPPORT_Z0_CONTRACT,combinations:report,FE_run:false},null,2));});
