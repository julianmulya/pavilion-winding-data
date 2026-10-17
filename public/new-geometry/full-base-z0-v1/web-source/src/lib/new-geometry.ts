import {Vector3,Vector4} from 'three';
import {calcSurfacePoint} from 'three/addons/curves/NURBSUtils.js';
import {divideClosed,sequence} from './generator';
import {NEW_GEOMETRY_SOURCE_SHA256,NEW_GEOMETRY_SOURCE_URL} from './new-geometry-pin';
import {buildModuleHardware} from './module-hardware';
import {buildSleevedWinding,SLEEVED_WINDING_CONTRACT} from './sleeved-winding';
export type XYZ=[number,number,number];
type UV=[number,number];
export type NewGeometryParameters={anchors:number;shift:number;gap:number;panels:number};
export type NativeSurface={type:'NurbsSurface';degree:[number,number];counts:[number,number];knotsU:number[];knotsV:number[];domains:[[number,number],[number,number]];points:[number,number,number,number][][];crc:number};
export type WindingMaterialBasis={id:string;units:'m';metres_per_source_unit:1;width_mm:number;thickness_mm:number;density_kg_m3:number;passes_already_in_equivalent_section:1;gravity_m_s2:number;scope:string;section_basis:string};
export type NewGeometrySource={schema:'pavilion.active-gh-parametric/1';id:string;name:string;source_filename:string;source_snapshot_sha256:string;coordinate_units:'GH_SOURCE_UNIT'|'m';unit_note:string;material_basis?:WindingMaterialBasis;native_defaults:NewGeometryParameters;web_defaults:NewGeometryParameters;surface_A:NativeSurface;native_offset_surfaces:{gap:number;surface:NativeSurface}[];results:{stress:null;displacement:null;mass:null;utilization:null;safety:null;historical_result_attachment:false}};
export const newMaxShift=(anchors:number)=>Math.floor(anchors/2);
export const NEW_MIN_SHIFT=5;
// Historical source comparisons retain their original domain; active exploration uses this narrower design rule.
export function validateNewDesignParameters(p:NewGeometryParameters){validateNewParameters(p);if(p.shift<NEW_MIN_SHIFT)throw Error('Winding shift minimum 5; maksimum floor(N/2).');}
export function isNewDesignParameters(p:NewGeometryParameters){try{validateNewDesignParameters(p);return true;}catch{return false;}}
export function validateNewParameters(p:NewGeometryParameters){
 if(!Number.isInteger(p.anchors)||p.anchors<10||p.anchors>50||!Number.isInteger(p.shift)||p.shift<0||p.shift>newMaxShift(p.anchors)||!Number.isInteger(p.panels)||p.panels<36||p.panels>100||!Number.isFinite(p.gap)||Math.abs(p.gap*10-Math.round(p.gap*10))>1e-9||p.gap<.1||p.gap>1)throw Error('Parameter di luar domain geometri baru. Shift maksimum = floor(N/2).');
}
function validateSurface(s:NativeSurface){
 if(s?.type!=='NurbsSurface'||s.counts?.length!==2||s.degree?.length!==2||s.domains?.length!==2)throw Error('Permukaan native GH tidak valid.');
 if(s.points.length!==s.counts[0]||s.points.some(row=>row.length!==s.counts[1]||row.some(p=>p.length!==4||p.some(v=>!Number.isFinite(v))||p[3]<=0)))throw Error('Control points native tidak valid.');
 for(const [knots,n,d] of [[s.knotsU,s.counts[0],s.degree[0]],[s.knotsV,s.counts[1],s.degree[1]]] as const){if(knots.length!==n+d-1||knots.some((v,i)=>!Number.isFinite(v)||(i>0&&v<knots[i-1])))throw Error('Knot native GH tidak valid.');}
}
export function validateNewSource(s:NewGeometrySource){
 if(s?.schema!=='pavilion.active-gh-parametric/1'||!['GH_SOURCE_UNIT','m'].includes(s.coordinate_units)||!/^[a-f0-9]{64}$/.test(s.source_snapshot_sha256))throw Error('Kontrak geometri baru tidak sesuai.');
 if(s.coordinate_units==='m')windingMaterialMetrics(0,s.material_basis);
 validateSurface(s.surface_A);validateNewParameters(s.web_defaults);
 if(s.native_offset_surfaces.length!==10||new Set(s.native_offset_surfaces.map(x=>Math.round(x.gap*10))).size!==10)throw Error('Offset GH tidak lengkap.');
 for(let i=1;i<=10;i++){const row=s.native_offset_surfaces.find(x=>Math.abs(x.gap-i/10)<1e-9);if(!row)throw Error('Offset GH hilang.');validateSurface(row.surface);}
 if(Object.entries(s.results).some(([key,value])=>key==='historical_result_attachment'?value!==false:value!==null))throw Error('Geometri baru belum memiliki hasil FE.');
 return s;
}
export async function loadNewGeometrySource(signal:AbortSignal){
 const r=await fetch(NEW_GEOMETRY_SOURCE_URL,{signal});if(!r.ok)throw Error('Sumber geometri baru belum tersedia.');
 const b=await r.arrayBuffer(),sha=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),v=>v.toString(16).padStart(2,'0')).join('');
 if(sha!==NEW_GEOMETRY_SOURCE_SHA256)throw Error('Identitas sumber geometri berubah; visual ditahan.');
 return validateNewSource(JSON.parse(new TextDecoder().decode(b)));
}
// Direct port of the active GH panel-layout helpers. No panel removal or remesh.
function clip(poly:UV[],nx:number,ny:number,c:number):UV[]{
 if(!poly.length)return [];const out:UV[]=[];let a=poly.at(-1)!,da=nx*a[0]+ny*a[1]-c;
 for(const b of poly){const db=nx*b[0]+ny*b[1]-c;if((da<=0)!==(db<=0)){const t=da/(da-db);out.push([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]);}if(db<=0)out.push(b);a=b;da=db;}
 const clean:UV[]=[];for(const p of out)if(!clean.length||Math.hypot(p[0]-clean.at(-1)![0],p[1]-clean.at(-1)![1])>1e-12)clean.push(p);
 if(clean.length>1&&Math.hypot(clean[0][0]-clean.at(-1)![0],clean[0][1]-clean.at(-1)![1])<=1e-12)clean.pop();return clean;
}
export function panelLayout(n:number){
 const rows=Math.max(1,Math.min(n,Math.round(Math.sqrt(n/Math.sqrt(.75))))),base=Math.floor(n/rows),extra=n%rows,seeds:UV[]=[];
 for(let row=0;row<rows;row++){const columns=base+(row<extra?1:0);for(let col=0;col<columns;col++)seeds.push([(col+.5+.5*(row%2))/(columns+.5),(row+.5)/rows]);}
 return seeds.map(([x,y],i)=>{let poly:UV[]=[[0,0],[1,0],[1,1],[0,1]];for(let j=0;j<seeds.length;j++)if(i!==j){const[u,v]=seeds[j];poly=clip(poly,u-x,v-y,(u*u+v*v-x*x-y*y)*.5);}return poly;});
}
const evaluators=new WeakMap<NativeSurface,(uv:UV)=>XYZ>();
export function surfaceEvaluator(s:NativeSurface){
 let fn=evaluators.get(s);if(fn)return fn;
 // Rhino stores two fewer exterior knots than the standard knot convention.
 const ku=[s.knotsU[0],...s.knotsU,s.knotsU.at(-1)!],kv=[s.knotsV[0],...s.knotsV,s.knotsV.at(-1)!];
 const cp=s.points.map(row=>row.map(p=>new Vector4(...p))),target=new Vector3();
 fn=([u,v]:UV)=>{const U=s.domains[0][0]+u*(s.domains[0][1]-s.domains[0][0]),V=s.domains[1][0]+v*(s.domains[1][1]-s.domains[1][0]);calcSurfacePoint(s.degree[0],s.degree[1],ku,kv,cp,U,V,target);return [target.x,target.y,target.z];};
 evaluators.set(s,fn);return fn;
}
export const FULL_BASE_Z0_CONTRACT='GH_FULL_BASE_Z0_V1';
export type NewBoundaryPolicy=typeof FULL_BASE_Z0_CONTRACT|'SOURCE';
export function newPanelBoundaries(s:NewGeometrySource,pick:Pick<NewGeometryParameters,'gap'|'panels'>,policy:NewBoundaryPolicy=FULL_BASE_Z0_CONTRACT){
 const offset=s.native_offset_surfaces.find(o=>Math.abs(o.gap-pick.gap)<1e-9);if(!offset)throw Error('Jarak boundary harus memakai station offset native GH.');
 const A=surfaceEvaluator(s.surface_A),B=surfaceEvaluator(offset.surface);
 return panelLayout(pick.panels).map((uv,i)=>{const loop=[...uv,uv[0]];
  // Ground the entire perimeter edge on BOTH layers, including raised offset vertices.
  // Interior vertices and the underlying native loft remain unchanged.
  const onGround=([,v]:UV)=>Math.abs(v)<1e-10||Math.abs(v-1)<1e-10;
  const evaluate=(fn:(q:UV)=>XYZ)=>loop.map(q=>{const p=fn(q);return policy===FULL_BASE_Z0_CONTRACT&&onGround(q)?[p[0],p[1],0] as XYZ:p;});
  return {id:`P${String(i+1).padStart(3,'0')}`,source_index:i,A:evaluate(A),B:evaluate(B),uv};});
}
const length=(a:readonly number[],b:readonly number[])=>Math.hypot(...a.map((v,k)=>v-b[k]));
export function windingMaterialMetrics(length_m:number,basis:WindingMaterialBasis|undefined){
 if(!basis||basis.units!=='m'||basis.metres_per_source_unit!==1||basis.passes_already_in_equivalent_section!==1||!Number.isFinite(length_m)||length_m<0||[basis.width_mm,basis.thickness_mm,basis.density_kg_m3,basis.gravity_m_s2].some(v=>!Number.isFinite(v)||v<=0))throw Error('Basis massa winding atau satuan meter tidak valid.');
 // Equivalent section already contains its one spatial pass: do not multiply it twice.
 const area_m2=basis.width_mm*basis.thickness_mm*1e-6,linear_mass_kg_per_m=area_m2*basis.density_kg_m3,mass_kg=length_m*linear_mass_kg_per_m;
 return {basis_id:basis.id,scope:'SPATIAL_CFRP_WINDING_ONLY' as const,length_m,volume_m3:length_m*area_m2,linear_mass_kg_per_m,mass_kg,weight_N:mass_kg*basis.gravity_m_s2,method:'GEOMETRY_ESTIMATE_NOT_FE' as const};
}
export function generateNewGeometryCore(s:NewGeometrySource,p:NewGeometryParameters,policy:NewBoundaryPolicy=FULL_BASE_Z0_CONTRACT){
 validateNewParameters(p);let windingLength=0;
 const panels=newPanelBoundaries(s,p,policy).map(panel=>{
  const anchorsA=divideClosed(panel.A,p.anchors) as XYZ[],anchorsB=divideClosed(panel.B,p.anchors) as XYZ[];
  // Native P is the OFFSET B boundary; native Lower is ORIGINAL A.
  const segments=sequence(anchorsB,anchorsA,p.shift),panelLength=segments.reduce((sum,line)=>sum+length(line.a,line.b),0);windingLength+=panelLength;
  const visited=new Set(segments.flatMap(line=>[`${line.from_layer}:${line.from_index}`,`${line.to_layer}:${line.to_index}`]));
  const sleeved_winding=buildSleevedWinding({...panel,segments});
  return {...panel,anchorsA,anchorsB,segments,winding_length_source_units:panelLength,winding_length_m:s.coordinate_units==='m'?panelLength:null,material_metrics:s.coordinate_units==='m'?windingMaterialMetrics(panelLength,s.material_basis):null,sleeved_winding:{...sleeved_winding,material_metrics:s.coordinate_units==='m'?windingMaterialMetrics(sleeved_winding.total_length_m,s.material_basis):null},visited_anchors:visited.size,available_anchors:2*p.anchors};
 });
 const total_length_m=panels.reduce((n,v)=>n+v.sleeved_winding.total_length_m,0),sleeved_winding={contract:SLEEVED_WINDING_CONTRACT,total_length_m,local_wrap_length_m:panels.reduce((n,v)=>n+v.sleeved_winding.local_wrap_length_m,0),transfer_length_m:panels.reduce((n,v)=>n+v.sleeved_winding.transfer_length_m,0),wrap_count:panels.reduce((n,v)=>n+v.sleeved_winding.wrap_count,0),material_metrics:s.coordinate_units==='m'?windingMaterialMetrics(total_length_m,s.material_basis):null};
 return {id:`${s.id}/${policy===FULL_BASE_Z0_CONTRACT?FULL_BASE_Z0_CONTRACT+'/':''}N${p.anchors}/S${p.shift}/HS${p.gap.toFixed(1)}/P${p.panels}`,source_sha256:s.source_snapshot_sha256,geometry_contract_id:policy,parameters:{...p},panels,sleeved_winding,winding_length_source_units:windingLength,winding_length_m:s.coordinate_units==='m'?windingLength:null,material_metrics:s.coordinate_units==='m'?windingMaterialMetrics(windingLength,s.material_basis):null,total_segments:panels.reduce((n,v)=>n+v.segments.length,0),FE_status:'NOT_EVALUATED' as const,stress:null,displacement:null,mass:null,utilization:null,initial_strain:false};
}
export function generateNewGeometry(s:NewGeometrySource,p:NewGeometryParameters,policy:NewBoundaryPolicy=FULL_BASE_Z0_CONTRACT){const model=generateNewGeometryCore(s,p,policy);return {...model,hardware:buildModuleHardware(model.panels)};}
export type NewGeometryCore=ReturnType<typeof generateNewGeometryCore>;
export type NewGeometryModel=ReturnType<typeof generateNewGeometry>;
