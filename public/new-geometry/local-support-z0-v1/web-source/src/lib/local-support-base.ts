export const LOCAL_SUPPORT_Z0_CONTRACT='GH_LOCAL_SUPPORT_BASE_Z0_V1';
type Point=[number,number,number];
type Panel={id:string;uv:[number,number][];A:Point[];B:Point[]};
const tol=1e-10;
// Select one complete lowest panel edge. Additional below-floor source vertices
// only extend its local interval; high portions of the open boundary stay intact.
export function localSupportInterval(panels:Panel[]){
 const edges=panels.flatMap((p,index)=>p.uv.flatMap((q,j)=>{
  const next=(j+1)%p.uv.length,w=p.uv[next];
  return Math.abs(q[1]-1)<tol&&Math.abs(w[1]-1)<tol&&Math.abs(q[0]-w[0])>tol?[{panel:p.id,index,edge:j,lo:Math.min(q[0],w[0]),hi:Math.max(q[0],w[0]),mean_z:(p.A[j][2]+p.A[next][2])/2,mid_distance:Math.abs((q[0]+w[0])/2-.5)}]:[];
 }));
 if(!edges.length)throw Error('Batas sisi terbuka tidak ditemukan.');
 edges.sort((a,b)=>Math.abs(a.mean_z-b.mean_z)>tol?a.mean_z-b.mean_z:Math.abs(a.mid_distance-b.mid_distance)>tol?a.mid_distance-b.mid_distance:a.index-b.index||a.edge-b.edge);
 const selected=edges[0],below=panels.flatMap(p=>p.uv.flatMap((q,j)=>Math.abs(q[1]-1)<tol&&p.A[j][2]<-tol?[q[0]]:[]));
 return {selected_panel:selected.panel,selected_edge:selected.edge,lo:Math.min(selected.lo,...below),hi:Math.max(selected.hi,...below),open_edge_count:edges.length};
}
export function applyLocalSupportBase<T extends Panel>(panels:T[]){
 const interval=localSupportInterval(panels);
 const ground=([u,v]:[number,number])=>Math.abs(v)<tol||(Math.abs(v-1)<tol&&u>=interval.lo-tol&&u<=interval.hi+tol);
 return panels.map(p=>{
  const adjust=(layer:'A'|'B')=>p[layer].map((q,j)=>ground(p.uv[j%p.uv.length])?[q[0],q[1],0] as Point:q);
  return {...p,A:adjust('A'),B:adjust('B')};
 });
}
