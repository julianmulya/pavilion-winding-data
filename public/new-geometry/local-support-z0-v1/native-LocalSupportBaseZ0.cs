// Keep the open-side slopes. Only its lowest complete panel edge becomes a flat foot.
class LocalBaseResult {
 public Grasshopper.DataTree<Curve> A=new Grasshopper.DataTree<Curve>(),B=new Grasshopper.DataTree<Curve>(),Ground=new Grasshopper.DataTree<Curve>(),OpenProfile=new Grasshopper.DataTree<Curve>();
 public Grasshopper.DataTree<Mesh> Highlight=new Grasshopper.DataTree<Mesh>(),SlopeHighlight=new Grasshopper.DataTree<Mesh>();
 public string Meta,Report;
}
class LocalBaseEdge {public int Panel,Edge;public double Lo,Hi,Mean,MidDistance;}
List<Curve> LBcurves(int i){return Component.Params.Input[i].VolatileData.AllData(true).Select(g=>(Curve)g.ScriptVariable()).ToList();}
string LBn(double x){return x.ToString("R",System.Globalization.CultureInfo.InvariantCulture);}
string LBxyz(Point3d p){return "["+LBn(p.X)+","+LBn(p.Y)+","+LBn(p.Z)+"]";}
Mesh LBhighlight(Point3d a,Point3d b){return Mesh.CreateFromCylinder(new Cylinder(new Circle(new Plane(a,b-a),.012),a.DistanceTo(b)),1,12);}
LocalBaseResult LocalBase(){
 var r=new LocalBaseResult();var aa=LBcurves(0);var bb=LBcurves(1);var uvc=LBcurves(2);double tol=1e-10;
 if(aa.Count!=bb.Count||aa.Count!=uvc.Count)throw new Exception("A/B/UV panel ownership mismatch");
 double lowV=uvc.Min(c=>c.GetBoundingBox(true).Min.Y),highV=uvc.Max(c=>c.GetBoundingBox(true).Max.Y),midU=(uvc.Min(c=>c.GetBoundingBox(true).Min.X)+uvc.Max(c=>c.GetBoundingBox(true).Max.X))/2;
 var UV=new List<Polyline>();var PA=new List<Polyline>();var PB=new List<Polyline>();var candidates=new List<LocalBaseEdge>();var below=new List<double>();
 for(int p=0;p<aa.Count;p++){
  Polyline uv,a,b;if(!uvc[p].TryGetPolyline(out uv)||!aa[p].TryGetPolyline(out a)||!bb[p].TryGetPolyline(out b)||!a.IsClosed||!b.IsClosed||a.Count!=uv.Count||b.Count!=uv.Count)throw new Exception("Native polygon/UV vertex mismatch");
  UV.Add(uv);PA.Add(a);PB.Add(b);
  for(int j=0;j<uv.Count-1;j++){
   if(Math.Abs(uv[j].Y-highV)<tol&&a[j].Z<-tol)below.Add(uv[j].X);
   if(Math.Abs(uv[j].Y-highV)<tol&&Math.Abs(uv[j+1].Y-highV)<tol&&Math.Abs(uv[j].X-uv[j+1].X)>tol)candidates.Add(new LocalBaseEdge{Panel=p,Edge=j,Lo=Math.Min(uv[j].X,uv[j+1].X),Hi=Math.Max(uv[j].X,uv[j+1].X),Mean=(a[j].Z+a[j+1].Z)/2,MidDistance=Math.Abs((uv[j].X+uv[j+1].X)/2-midU)});
  }
 }
 if(candidates.Count<3)throw new Exception("Open-side profile requires at least three panel edges");
 candidates.Sort((a,b)=>Math.Abs(a.Mean-b.Mean)>tol?a.Mean.CompareTo(b.Mean):Math.Abs(a.MidDistance-b.MidDistance)>tol?a.MidDistance.CompareTo(b.MidDistance):a.Panel!=b.Panel?a.Panel.CompareTo(b.Panel):a.Edge.CompareTo(b.Edge));
 var selected=candidates[0];double lo=selected.Lo,hi=selected.Hi;foreach(var u in below){lo=Math.Min(lo,u);hi=Math.Max(hi,u);}
 var rows=new List<string>();var profile=new List<string>();int edges=0,openFeet=0,openElevated=0,moved=0,floorPanels=0;double minBefore=Double.PositiveInfinity,minAfter=Double.PositiveInfinity,maxGround=0,maxXY=0,total=0,maxOpen=0;
 for(int p=0;p<aa.Count;p++){
  var uv=UV[p];var mask=uv.Select(q=>Math.Abs(q.Y-lowV)<tol||(Math.Abs(q.Y-highV)<tol&&q.X>=lo-tol&&q.X<=hi+tol)).ToArray();var groundPairs=new List<int>();bool ownerGround=false;
  for(int j=0;j<uv.Count-1;j++)if(mask[j]&&mask[j+1]&&Math.Abs(uv[j].Y-uv[j+1].Y)<tol&&uv[j].DistanceTo(uv[j+1])>tol){groundPairs.Add(j);ownerGround=true;if(Math.Abs(uv[j].Y-highV)<tol)openFeet++;}
  if(ownerGround)floorPanels++;
  for(int layer=0;layer<2;layer++){
   var original=layer==0?PA[p]:PB[p];var pts=new List<Point3d>();
   for(int j=0;j<original.Count;j++){
    var q=original[j];minBefore=Math.Min(minBefore,q.Z);if(mask[j]){if(q.Z!=0)moved++;q.Z=0;maxGround=Math.Max(maxGround,Math.Abs(q.Z));}
    maxXY=Math.Max(maxXY,Math.Max(Math.Abs(q.X-original[j].X),Math.Abs(q.Y-original[j].Y)));minAfter=Math.Min(minAfter,q.Z);pts.Add(q);
   }
   var result=new PolylineCurve(pts);if(!result.IsValid||!result.IsClosed)throw new Exception("Invalid corrected boundary");(layer==0?r.A:r.B).Add(result,new Grasshopper.Kernel.Data.GH_Path(0));
   foreach(int j in groundPairs){
    if(pts[j].Z!=0||pts[j+1].Z!=0||pts[j].DistanceTo(pts[j+1])<=tol)throw new Exception("Incomplete ground edge");
    var line=new LineCurve(pts[j],pts[j+1]);var path=new Grasshopper.Kernel.Data.GH_Path(p,layer);r.Ground.Add(line,path);total+=line.GetLength();edges++;
    if(Math.Abs(uv[j].Y-highV)<tol)r.Highlight.Add(LBhighlight(pts[j],pts[j+1]),path);
   }
   for(int j=0;j<uv.Count-1;j++)if(Math.Abs(uv[j].Y-highV)<tol&&Math.Abs(uv[j+1].Y-highV)<tol){
    bool foot=mask[j]&&mask[j+1];var path=new Grasshopper.Kernel.Data.GH_Path(p,layer);r.OpenProfile.Add(new LineCurve(pts[j],pts[j+1]),path);maxOpen=Math.Max(maxOpen,Math.Max(pts[j].Z,pts[j+1].Z));
    if(!foot){r.SlopeHighlight.Add(LBhighlight(pts[j],pts[j+1]),path);if(layer==0)openElevated++;}
    profile.Add("{\"panel\":\"P"+(p+1).ToString("000")+"\",\"layer\":\""+(layer==0?"A":"B")+"\",\"edge\":"+j+",\"ground\":"+(foot?"true":"false")+",\"u\":["+LBn(uv[j].X)+","+LBn(uv[j+1].X)+"],\"a\":"+LBxyz(pts[j])+",\"b\":"+LBxyz(pts[j+1])+",\"source_a\":"+LBxyz(original[j])+",\"source_b\":"+LBxyz(original[j+1])+"}");
   }
  }
  if(groundPairs.Count>0)rows.Add("{\"panel\":\"P"+(p+1).ToString("000")+"\",\"ground_edge_indices\":["+String.Join(",",groundPairs)+"]}");
 }
 if(minAfter<-1e-8||openFeet<1||openFeet>=candidates.Count||openElevated<2)throw new Exception("Local support must keep elevated open-side slopes and at least one flat foot");
 r.Meta="{\"contract\":\"GH_LOCAL_SUPPORT_BASE_Z0_V1\",\"panels\":"+aa.Count+",\"selected_open_panel\":\"P"+(selected.Panel+1).ToString("000")+"\",\"support_u_interval\":["+LBn(lo)+","+LBn(hi)+"],\"open_edge_count\":"+candidates.Count+",\"open_ground_panels\":"+openFeet+",\"open_elevated_edges\":"+openElevated+",\"max_open_elevation_m\":"+LBn(maxOpen)+",\"ground_panels\":"+floorPanels+",\"ground_edges_both_layers\":"+edges+",\"max_abs_ground_Z_m\":"+LBn(maxGround)+",\"max_XY_change_m\":"+LBn(maxXY)+",\"minimum_Z_before_m\":"+LBn(minBefore)+",\"minimum_Z_after_m\":"+LBn(minAfter)+",\"moved_vertex_occurrences\":"+moved+",\"ground_length_owner_sum_m\":"+LBn(total)+",\"ground_panel_details\":["+String.Join(",",rows)+"],\"open_profile_edges\":["+String.Join(",",profile)+"]}";
 r.Report="SISI TERBUKA \\_/ | ALAS LOKAL Z=0\nSelected foot: P"+(selected.Panel+1).ToString("000")+"; "+openFeet+" complete open-side support panels.\n"+openElevated+" open-side edges retain their rise.\nBoth A and B foot edges are exactly Z=0.\nShared UV corner corrections also reach adjacent panels.\nMain loft, X/Y and all non-foot vertices unchanged.\nYellow = rising open edge; orange = local foot (display only).\nGeometry only; no Analyze.";
 return r;
}
