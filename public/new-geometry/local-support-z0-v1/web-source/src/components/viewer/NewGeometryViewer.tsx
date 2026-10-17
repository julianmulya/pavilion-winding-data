import {useEffect,useRef,useState} from 'react';
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import type {NewGeometryModel} from '../../lib/new-geometry';
import {addModuleHardware,clipHardwareLine} from './module-hardware-meshes';
import {sleeveStepPoint,sleeveStepPoints} from '../../lib/sleeved-winding';
type Props={model:NewGeometryModel;panel:string;joint:string|null;anchorDetail?:boolean;progress:number|null;view:'perspective'|'top'|'front'|'right';reset:number;showAnchors:boolean;showSleeves:boolean;showBolts:boolean;showBoundary:boolean;showWinding:boolean;onSelect:(id:string)=>void};
type WindingDraw={line:THREE.LineSegments;ends:number[]};
function clear(group:THREE.Group){group.traverse(o=>{if(o instanceof THREE.Mesh||o instanceof THREE.Line||o instanceof THREE.Points){o.geometry.dispose();for(const m of Array.isArray(o.material)?o.material:[o.material])m.dispose();if(o instanceof THREE.InstancedMesh)o.dispose();}});group.clear();}
export default function NewGeometryViewer(props:Props){
 const host=useRef<HTMLDivElement>(null),state=useRef<{renderer:THREE.WebGLRenderer;scene:THREE.Scene;camera:THREE.PerspectiveCamera;controls:OrbitControls;geometry:THREE.Group;heads:THREE.Group;winding:WindingDraw[];box:THREE.Box3;invalidate:()=>void;fit:()=>void}|null>(null),latest=useRef(props),[error,setError]=useState('');
 useEffect(()=>{latest.current=props;});
 useEffect(()=>{
  const container=host.current;if(!container)return;let renderer:THREE.WebGLRenderer;
  try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});}catch{setError('WebGL tidak tersedia. Ekspor geometri tetap dapat diunduh.');return;}
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));container.append(renderer.domElement);renderer.domElement.setAttribute('aria-label','Geometri baru interaktif dari Grasshopper');
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(38,1,.001,2000);camera.up.set(0,0,1);
  const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.08;
  const geometry=new THREE.Group(),heads=new THREE.Group();scene.add(geometry,heads);scene.add(new THREE.HemisphereLight(0xffffff,0x9ba89f,2));const keyLight=new THREE.DirectionalLight(0xffffff,2.3);keyLight.position.set(5,-7,10);scene.add(keyLight);
  const floor=new THREE.GridHelper(24,24,0xc4cec4,0xe1e5dc);floor.name='ground-grid';floor.rotateX(Math.PI/2);floor.position.z=-.02;scene.add(floor);
  let dirty=true;const invalidate=()=>{dirty=true;};controls.addEventListener('change',invalidate);
  const e={renderer,scene,camera,controls,geometry,heads,winding:[] as WindingDraw[],box:new THREE.Box3(),invalidate,fit:()=>{}};state.current=e;
  e.fit=()=>{if(e.box.isEmpty())return;const center=e.box.getCenter(new THREE.Vector3()),size=e.box.getSize(new THREE.Vector3()),radius=Math.max(size.length()/2,.1),v=latest.current.view,direction=(latest.current.anchorDetail&&v==='perspective'?(()=>{const r=(latest.current.model.panels.find(p=>p.id===latest.current.panel)??latest.current.model.panels[0]).sleeved_winding.visits[0];return new THREE.Vector3(...r.x).multiplyScalar(1.5).addScaledVector(new THREE.Vector3(...r.y),-.7).addScaledVector(new THREE.Vector3(...r.axis),.35);})():v==='top'?new THREE.Vector3(0,-.0001,1):v==='front'?new THREE.Vector3(0,1,.0001):v==='right'?new THREE.Vector3(1,0,.0001):new THREE.Vector3(1,1.6,.9)).normalize(),right=new THREE.Vector3().crossVectors(camera.up,direction).normalize(),up=new THREE.Vector3().crossVectors(direction,right).normalize(),tan=Math.tan(THREE.MathUtils.degToRad(camera.fov/2));let distance=.1;for(const x of [e.box.min.x,e.box.max.x])for(const y of [e.box.min.y,e.box.max.y])for(const z of [e.box.min.z,e.box.max.z]){const d=new THREE.Vector3(x,y,z).sub(center);distance=Math.max(distance,Math.abs(d.dot(up))/tan+d.dot(direction),Math.abs(d.dot(right))/(tan*camera.aspect)+d.dot(direction));}camera.position.copy(center).addScaledVector(direction,distance*1.16);camera.near=Math.max(.0001,radius/1000);camera.far=Math.max(100,radius*100);camera.updateProjectionMatrix();controls.target.copy(center);controls.update();invalidate();};
  const resize=()=>{const r=container.getBoundingClientRect();renderer.setSize(r.width,r.height);camera.aspect=r.width/Math.max(1,r.height);camera.updateProjectionMatrix();e.fit();};const observer=new ResizeObserver(resize);observer.observe(container);resize();
  let start=[0,0];const down=(ev:PointerEvent)=>{start=[ev.clientX,ev.clientY];};const pick=(ev:PointerEvent)=>{if(Math.hypot(ev.clientX-start[0],ev.clientY-start[1])>4)return;const rect=container.getBoundingClientRect(),ray=new THREE.Raycaster();ray.params.Line.threshold=.06;ray.setFromCamera(new THREE.Vector2((ev.clientX-rect.left)/rect.width*2-1,-(ev.clientY-rect.top)/rect.height*2+1),camera);const hit=ray.intersectObjects(geometry.children.filter(o=>o.userData.panel),false)[0];if(hit)latest.current.onSelect(hit.object.userData.panel);};
  const lost=(ev:Event)=>{ev.preventDefault();setError('Konteks WebGL terputus. Muat ulang untuk memulihkan visual.');};renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointerup',pick);renderer.domElement.addEventListener('webglcontextlost',lost);
  renderer.setAnimationLoop(()=>{controls.update();if(dirty){renderer.render(scene,camera);dirty=false;}});
  return()=>{observer.disconnect();renderer.setAnimationLoop(null);controls.removeEventListener('change',invalidate);controls.dispose();renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointerup',pick);renderer.domElement.removeEventListener('webglcontextlost',lost);clear(geometry);clear(heads);floor.geometry.dispose();(floor.material as THREE.Material).dispose();renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();state.current=null;};
 },[]);
 useEffect(()=>{
  const e=state.current;if(!e)return;clear(e.geometry);clear(e.heads);e.winding=[];const floor=e.scene.getObjectByName('ground-grid');if(floor)floor.visible=!props.anchorDetail;e.box.makeEmpty();
  const joint=props.model.hardware.joints.find(j=>j.id===props.joint),anchor=props.anchorDetail?(props.model.panels.find(p=>p.id===props.panel)??props.model.panels[0]).sleeved_winding.visits[0]:null,focus=anchor?.center??joint?.bolts[0]?.center??(joint?joint.a.map((v,k)=>(v+joint.b[k])*.5):null),size=anchor?.06:.18,detailBox=focus?new THREE.Box3().setFromCenterAndSize(new THREE.Vector3(...focus),new THREE.Vector3(size,size,size)):null;
  const panels=props.model.panels.filter(p=>joint?joint.owners.includes(p.id):props.panel==='ALL'||p.id===props.panel);
  for(const p of panels){
   for(const points of [p.A,p.B])for(const point of points)e.box.expandByPoint(new THREE.Vector3(...point));
   if(props.showBoundary){const pos:number[]=[];for(const loop of [p.A,p.B])for(let j=0;j<loop.length-1;j++){const points=detailBox?clipHardwareLine(loop[j],loop[j+1],detailBox):[loop[j],loop[j+1]];if(points)pos.push(...points[0],...points[1]);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));const line=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0x89958b,transparent:true,opacity:.6}));line.userData.panel=p.id;e.geometry.add(line);}
   if(props.showWinding){const positions:number[]=[],ends=[0],route=p.sleeved_winding;for(const step of route.steps){const points=sleeveStepPoints(route,step);for(let i=1;i<points.length;i++){const line=detailBox?clipHardwareLine(points[i-1],points[i],detailBox):[points[i-1],points[i]];if(line)positions.push(...line[0],...line[1]);}ends.push(positions.length/3);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));const line=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0x374b42,transparent:true,opacity:props.panel==='ALL'?.66:.9,depthTest:!props.anchorDetail}));e.winding.push({line,ends});e.geometry.add(line);}
   if(props.showAnchors&&!joint){const g=new THREE.BufferGeometry().setFromPoints([...p.anchorsA,...p.anchorsB].filter(p=>!detailBox||detailBox.containsPoint(new THREE.Vector3(...p))).map(p=>new THREE.Vector3(...p)));e.geometry.add(new THREE.Points(g,new THREE.PointsMaterial({color:0x517c66,size:props.anchorDetail?.0007:props.panel==='ALL'?.016:.025,sizeAttenuation:true})));}
  }
  addModuleHardware(e.geometry,props.model.hardware,{panel:props.panel,joint:props.joint,showSleeves:props.showSleeves||!!anchor,showBolts:props.showBolts,showBoundary:props.showBoundary,box:detailBox});
  if(detailBox)e.box.copy(detailBox);
  e.renderer.domElement.dataset.config=props.model.id;e.renderer.domElement.dataset.panels=String(props.model.panels.length);e.renderer.domElement.dataset.segments=String(props.model.total_segments);e.renderer.domElement.dataset.scope=props.panel;e.renderer.domElement.dataset.source=props.model.source_sha256;
  e.fit();e.invalidate();
  e.renderer.domElement.dataset.hardwareContract=props.model.hardware.contract.id;e.renderer.domElement.dataset.sleeves=String(props.model.hardware.counts.winding_sleeves);e.renderer.domElement.dataset.moduleBolts=String(props.model.hardware.counts.module_bolts);e.renderer.domElement.dataset.joint=props.joint??'';
  e.renderer.domElement.dataset.windingContract=props.model.sleeved_winding.contract.id;e.renderer.domElement.dataset.wraps=String(props.model.sleeved_winding.wrap_count);e.renderer.domElement.dataset.anchorDetail=anchor?.id??'';
 },[props.model,props.panel,props.joint,props.anchorDetail,props.showAnchors,props.showSleeves,props.showBolts,props.showBoundary,props.showWinding]);
 useEffect(()=>{state.current?.fit();},[props.view,props.reset]);
 useEffect(()=>{
  const e=state.current;if(!e)return;clear(e.heads);
  for(const {line,ends} of e.winding)line.geometry.setDrawRange(0,props.progress===null?Infinity:ends[Math.min(Math.floor(props.progress),ends.length-1)]);
  if(props.progress!==null&&props.showWinding&&!props.joint){for(const p of props.model.panels.filter(p=>props.panel==='ALL'||p.id===props.panel)){
   const route=p.sleeved_winding,index=Math.min(Math.floor(props.progress),route.steps.length-1),s=route.steps[index];if(!s)continue;const completed=Math.floor(props.progress)>=route.steps.length,part=completed?1:Math.min(1,props.progress-index),point=new THREE.Vector3(...sleeveStepPoint(route,s,part));
   if(!completed){const g=new THREE.BufferGeometry().setFromPoints(sleeveStepPoints(route,s,part).map(p=>new THREE.Vector3(...p)));e.heads.add(new THREE.Line(g,new THREE.LineBasicMaterial({color:0xdc752c,depthTest:!props.anchorDetail})));}
   const g=new THREE.BufferGeometry().setFromPoints([point]);const head=new THREE.Points(g,new THREE.PointsMaterial({color:0xf0872e,size:props.anchorDetail?.0015:props.panel==='ALL'?.065:.035,sizeAttenuation:true,depthTest:false}));head.renderOrder=10;e.heads.add(head);
  }}
  e.renderer.domElement.dataset.progress=props.progress===null?'all':props.progress.toFixed(3);e.invalidate();
 },[props.progress,props.model,props.panel,props.anchorDetail,props.showWinding,props.showBoundary,props.showAnchors]);
 return <div ref={host} className="lab-viewport new-geometry-viewport" role="img" aria-label="Geometri baru · winding per panel">{error&&<p role="alert">{error}</p>}</div>;
}
