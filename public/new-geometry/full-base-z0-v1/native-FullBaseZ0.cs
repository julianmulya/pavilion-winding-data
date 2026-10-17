// Native geometry rule: the complete UV perimeter edge of BOTH owner boundaries is ground.
class FullBaseResult {
 public Grasshopper.DataTree<Curve> A=new Grasshopper.DataTree<Curve>(),B=new Grasshopper.DataTree<Curve>(),Ground=new Grasshopper.DataTree<Curve>();
 public Grasshopper.DataTree<Mesh> Highlight=new Grasshopper.DataTree<Mesh>();
 public string Meta,Report;
}
List<Curve> FBcurves(int i){return Component.Params.Input[i].VolatileData.AllData(true).Select(g=>(Curve)g.ScriptVariable()).ToList();}
string FBn(double x){return x.ToString("R",System.Globalization.CultureInfo.InvariantCulture);}
FullBaseResult FullBase(){
 var r=new FullBaseResult();var aa=FBcurves(0);var bb=FBcurves(1);var uv=FBcurves(2);var panelRows=new List<string>();
 if(aa.Count!=bb.Count||aa.Count!=uv.Count)throw new Exception("A/B/UV panel ownership mismatch");
 double lo=uv.Min(c=>c.GetBoundingBox(true).Min.Y),hi=uv.Max(c=>c.GetBoundingBox(true).Max.Y),tol=1e-10;
 int floorPanels=0,edges=0,moved=0;double minBefore=Double.PositiveInfinity,minAfter=Double.PositiveInfinity,maxGround=0,maxXY=0,total=0;
 for(int p=0;p<aa.Count;p++){
  Polyline up;if(!uv[p].TryGetPolyline(out up)||!up.IsClosed)throw new Exception("Closed UV cell required");
  var mask=up.Select(q=>Math.Abs(q.Y-lo)<tol||Math.Abs(q.Y-hi)<tol).ToArray();var groundPairs=new List<int>();
  for(int j=0;j<up.Count-1;j++)if(mask[j]&&mask[j+1]&&Math.Abs(up[j].Y-up[j+1].Y)<tol&&up[j].DistanceTo(up[j+1])>tol)groundPairs.Add(j);
  if(groundPairs.Count>0)floorPanels++;
  int groundVertices=0;
  for(int layer=0;layer<2;layer++){
   Polyline pl;if(!(layer==0?aa[p]:bb[p]).TryGetPolyline(out pl)||!pl.IsClosed||pl.Count!=up.Count)throw new Exception("Native A/B vertex order differs from UV cell");
   var pts=new List<Point3d>();
   for(int j=0;j<pl.Count;j++){
    var q=pl[j];minBefore=Math.Min(minBefore,q.Z);
    if(mask[j]){if(q.Z!=0)moved++;q.Z=0;groundVertices++;maxGround=Math.Max(maxGround,Math.Abs(q.Z));}
    maxXY=Math.Max(maxXY,Math.Max(Math.Abs(q.X-pl[j].X),Math.Abs(q.Y-pl[j].Y)));minAfter=Math.Min(minAfter,q.Z);pts.Add(q);
   }
   var result=new PolylineCurve(pts);if(!result.IsValid||!result.IsClosed)throw new Exception("Invalid corrected boundary");
   (layer==0?r.A:r.B).Add(result,new Grasshopper.Kernel.Data.GH_Path(0));
   foreach(int j in groundPairs){
    if(pts[j].Z!=0||pts[j+1].Z!=0)throw new Exception("Partial ground edge forbidden");
    var line=new LineCurve(pts[j],pts[j+1]);if(line.GetLength()<=tol)throw new Exception("Collapsed ground edge");
    var path=new Grasshopper.Kernel.Data.GH_Path(p,layer);r.Ground.Add(line,path);total+=line.GetLength();edges++;
    var cyl=new Cylinder(new Circle(new Plane(pts[j],pts[j+1]-pts[j]),.012),line.GetLength());r.Highlight.Add(Mesh.CreateFromCylinder(cyl,1,12),path);
   }
  }
  if(groundPairs.Count>0)panelRows.Add("{\"panel\":\"P"+(p+1).ToString("000")+"\",\"ground_edge_indices\":["+String.Join(",",groundPairs)+"],\"ground_vertices_both_layers\":"+groundVertices+"}");
 }
 if(minAfter<-1e-8)throw new Exception("An interior source vertex remains below ground: "+FBn(minAfter));
 r.Meta="{\"contract\":\"GH_FULL_BASE_Z0_V1\",\"panels\":"+aa.Count+",\"ground_panels\":"+floorPanels+",\"ground_edges_both_layers\":"+edges+",\"max_abs_ground_Z_m\":"+FBn(maxGround)+",\"max_XY_change_m\":"+FBn(maxXY)+",\"minimum_Z_before_m\":"+FBn(minBefore)+",\"minimum_Z_after_m\":"+FBn(minAfter)+",\"moved_vertex_occurrences\":"+moved+",\"ground_length_owner_sum_m\":"+FBn(total)+",\"ground_panel_details\":["+String.Join(",",panelRows)+"]}";
 r.Report="SELURUH ALAS PANEL A + B PADA Z=0\n"+floorPanels+" ground panels / "+edges+" complete owner edges.\nAll endpoints of the two owner base edges are exactly Z=0.\nGround mask comes from UV perimeter, not negative height alone.\nX/Y and all other polygon vertices preserved; main loft unchanged.\nLive rule follows panel count and boundary gap.\nGeometry only. Historical FE does not apply to this correction.";
 return r;
}
