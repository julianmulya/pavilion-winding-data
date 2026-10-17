// Geometry only. Native Karamba components create elements, assemble and analyze.
class NFResult {
 public Grasshopper.DataTree<object> Meshes=new Grasshopper.DataTree<object>(),Axes=new Grasshopper.DataTree<object>(),Names=new Grasshopper.DataTree<object>(),Height=new Grasshopper.DataTree<object>(),IndexMap=new Grasshopper.DataTree<object>(),AssemblyPts=new Grasshopper.DataTree<object>(),FrameLines=new Grasshopper.DataTree<object>(),FrameNames=new Grasshopper.DataTree<object>(),LinkLines=new Grasshopper.DataTree<object>(),LinkNames=new Grasshopper.DataTree<object>(),SupportP=new Grasshopper.DataTree<object>(),LoadP=new Grasshopper.DataTree<object>(),LoopP=new Grasshopper.DataTree<object>();
 public Grasshopper.DataTree<object> FramePts=new Grasshopper.DataTree<object>();public string Meta,Report;
}
List<Point3d> nfPoints=new List<Point3d>();Dictionary<string,List<int>> nfGrid=new Dictionary<string,List<int>>();
string NFkey(Point3d p){return Math.Round(p.X/1e-8)+","+Math.Round(p.Y/1e-8)+","+Math.Round(p.Z/1e-8);}
int NFfind(Point3d p){long x=(long)Math.Round(p.X/1e-8),y=(long)Math.Round(p.Y/1e-8),z=(long)Math.Round(p.Z/1e-8);for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++)for(int c=-1;c<=1;c++){List<int> ids;if(nfGrid.TryGetValue((x+a)+","+(y+b)+","+(z+c),out ids))foreach(var i in ids)if(nfPoints[i].DistanceTo(p)<1e-8)return i;}return -1;}
int NFframe(Point3d p){int i=NFfind(p);if(i>=0)return i;i=nfPoints.Count;nfPoints.Add(p);string k=NFkey(p);if(!nfGrid.ContainsKey(k))nfGrid[k]=new List<int>();nfGrid[k].Add(i);return i;}
string NFn(double x){return x.ToString("R",System.Globalization.CultureInfo.InvariantCulture);}
string NFxyz(Point3d p){return "["+NFn(p.X)+","+NFn(p.Y)+","+NFn(p.Z)+"]";}
List<Curve> NFcurves(int index){return Component.Params.Input[index].VolatileData.AllData(true).Select(g=>((Grasshopper.Kernel.Types.GH_Curve)g).Value).ToList();}
List<List<Point3d>> NFanchors(int index){var t=Component.Params.Input[index].VolatileData;var r=new List<List<Point3d>>();for(int i=0;i<t.PathCount;i++)r.Add(t.get_Branch(i).Cast<Grasshopper.Kernel.Types.IGH_Goo>().Select(g=>((Grasshopper.Kernel.Types.GH_Point)g).Value).ToList());return r;}
NFResult BuildNativeFEGeometry(){
 nfPoints.Clear();nfGrid.Clear();var r=new NFResult();var A=NFcurves(0);var B=NFcurves(1);var aa=NFanchors(2);var ab=NFanchors(3);var tr=Component.Params.Input[4].VolatileData;
 if(A.Count!=B.Count||A.Count!=tr.PathCount||A.Count!=aa.Count||A.Count!=ab.Count)throw new Exception("Native owner tree mismatch");
 int ns=2,nw=2;double width=.02,thick=.000981747704,radius=.0065;
 var polygons=new List<Polyline[]>();var spans=new List<List<Line>>();var normals=new List<Vector3d>();var contactIndices=new List<List<int>>();int wraps=0;
 for(int p=0;p<A.Count;p++){
  Polyline a,b;if(!A[p].TryGetPolyline(out a)||!B[p].TryGetPolyline(out b))throw new Exception("Native polygon required");polygons.Add(new[]{a,b});
  var normal=Vector3d.Zero;for(int j=0;j<a.Count-1;j++)normal+=Vector3d.CrossProduct(new Vector3d(a[j]),new Vector3d(a[j+1]));if(!normal.Unitize())throw new Exception("Panel normal undefined");normals.Add(normal);
  foreach(var pl in new[]{a,b})foreach(var q in pl)NFframe(q);foreach(var q in aa[p])NFframe(q);foreach(var q in ab[p])NFframe(q);
  var lines=new List<Line>();foreach(Grasshopper.Kernel.Types.IGH_Goo g in tr.get_Branch(p)){var v=g.ScriptVariable();Curve c=v as Curve;Line line=v is Line?(Line)v:new Line(c.PointAtStart,c.PointAtEnd);if(line.Length<1e-8)throw new Exception("Zero transfer");lines.Add(line);}spans.Add(lines);
 }
 // Each transfer starts at one visited sleeve contact. The closed sequence uses it once.
 for(int p=0;p<A.Count;p++){
  var ids=new List<int>();var visited=new HashSet<int>();var anchors=aa[p].Concat(ab[p]).ToList();
  for(int j=0;j<spans[p].Count;j++){
   var line=spans[p][j];if(line.To.DistanceTo(spans[p][(j+1)%spans[p].Count].From)>1e-8)throw new Exception("Transfer sequence is not closed");
   var q=line.From;int a=Enumerable.Range(0,anchors.Count).OrderBy(i=>anchors[i].DistanceTo(q)).First();
   if(Math.Abs(anchors[a].DistanceTo(q)-radius)>1e-8||!visited.Add(a))throw new Exception("Sleeve contact ownership mismatch");
   int index=NFframe(q);ids.Add(index);r.LinkLines.Add(new Line(anchors[a],q),new Grasshopper.Kernel.Data.GH_Path(0));r.LinkNames.Add("NG_LINK_P"+(p+1).ToString("000")+"_V"+(j+1).ToString("000"),new Grasshopper.Kernel.Data.GH_Path(0));r.LoopP.Add(anchors[a],new Grasshopper.Kernel.Data.GH_Path(0));wraps++;
  }contactIndices.Add(ids);
 }
 int frameCount=nfPoints.Count,frameSegments=0,groundEdges=0;var groundNodes=new HashSet<int>();var loadNodes=new HashSet<int>();double zmin=nfPoints.Min(q=>q.Z),zmax=nfPoints.Max(q=>q.Z);double boundaryLength=0;
 var distinct=new HashSet<string>();
 for(int p=0;p<polygons.Count;p++)for(int layer=0;layer<2;layer++){
  var pl=polygons[p][layer];int part=0;
  for(int j=0;j<pl.Count-1;j++){
   Point3d a=pl[j],b=pl[j+1];Vector3d d=b-a;double L=d.Length;if(L<1e-8)continue;
   var stations=new List<Tuple<double,int>>();for(int i=0;i<frameCount;i++){double t=((nfPoints[i]-a)*d)/(L*L);if(t>=-1e-8&&t<=1+1e-8&&nfPoints[i].DistanceTo(a+d*t)<1e-8)stations.Add(Tuple.Create(Math.Max(0,Math.Min(1,t)),i));}stations.Sort((u,v)=>u.Item1.CompareTo(v.Item1));
   bool ground=Math.Abs(a.Z)<1e-8&&Math.Abs(b.Z)<1e-8;if(ground){groundEdges++;foreach(var s in stations)groundNodes.Add(s.Item2);}
   for(int k=0;k<stations.Count-1;k++){int i=stations[k].Item2,h=stations[k+1].Item2;if(i==h)continue;var line=new Line(nfPoints[i],nfPoints[h]);r.FrameLines.Add(line,new Grasshopper.Kernel.Data.GH_Path(0));r.FrameNames.Add("NG_EDGE_P"+(p+1).ToString("000")+"_"+(layer==0?"A":"B")+"_S"+(++part).ToString("000"),new Grasshopper.Kernel.Data.GH_Path(0));frameSegments++;boundaryLength+=line.Length;distinct.Add(Math.Min(i,h)+","+Math.Max(i,h));}
  }
  // Lateral load locations: actual original-A polygon vertices in upper 75% of pavilion.
  if(layer==0)foreach(var q in pl)if(q.Z>zmin+.25*(zmax-zmin))loadNodes.Add(NFfind(q));
 }
 if(groundNodes.Count<3||groundEdges==0)throw new Exception("No distributed Z=0 ground-boundary support chain");
 foreach(var i in groundNodes.OrderBy(i=>i))r.SupportP.Add(nfPoints[i],new Grasshopper.Kernel.Data.GH_Path(0));
 foreach(var i in loadNodes.OrderBy(i=>i)){if(i<0)throw new Exception("Load station unmapped");r.LoadP.Add(nfPoints[i],new Grasshopper.Kernel.Data.GH_Path(0));}
 foreach(var q in nfPoints){r.AssemblyPts.Add(q,new Grasshopper.Kernel.Data.GH_Path(0,0));r.FramePts.Add(q,new Grasshopper.Kernel.Data.GH_Path(0));}
 int master=frameCount,count=0,triangles=0;double total=0;var records=new List<string>();
 for(int p=0;p<spans.Count;p++){
  var path=new Grasshopper.Kernel.Data.GH_Path(p,0);var patch=new Mesh();patch.Vertices.UseDoublePrecisionVertices=true;var routes=new List<string>();
  for(int s=0;s<spans[p].Count;s++){
   Line line=spans[p][s];var dir=line.Direction;dir.Unitize();var across=Vector3d.CrossProduct(normals[p],dir);if(!across.Unitize())throw new Exception("Ribbon axis undefined");int start=patch.Vertices.Count,faceBegin=patch.Faces.Count;
   for(int j=0;j<=ns;j++)for(int c=0;c<=nw;c++){
    Point3d q=line.PointAt((double)j/ns)+across*(((double)c/nw-.5)*width);patch.Vertices.Add(q);int index;
    if((j==0||j==ns)&&c==nw/2)index=contactIndices[p][j==0?s:(s+1)%spans[p].Count];else{index=master++;r.AssemblyPts.Add(q,new Grasshopper.Kernel.Data.GH_Path(1,p));}
    r.IndexMap.Add(index,path);
   }
   for(int j=0;j<ns;j++)for(int c=0;c<nw;c++){int k=start+j*(nw+1)+c,h=k+nw+1;patch.Faces.AddFace(k,h,h+1);patch.Faces.AddFace(k,h+1,k+1);r.Axes.Add(dir,path);r.Axes.Add(dir,path);}
   routes.Add("{\"strand\":"+s+",\"face_begin\":"+faceBegin+",\"face_count\":"+(2*ns*nw)+",\"length_m\":"+NFn(line.Length)+",\"start\":"+NFxyz(line.From)+",\"end\":"+NFxyz(line.To)+"}");total+=line.Length;count++;
  }
  patch.Normals.ComputeNormals();string name="NG_P"+(p+1).ToString("000")+"_F0";r.Meshes.Add(patch,path);r.Names.Add(name,path);r.Height.Add(thick*100,path);triangles+=patch.Faces.Count;
  records.Add("{\"name\":\""+name+"\",\"panel\":"+p+",\"family\":0,\"faces\":"+patch.Faces.Count+",\"routes\":["+String.Join(",",routes)+"]}");
 }

 // Reinforcement geometry uses only native RhinoCommon and explicit native node ownership.
 int[] targetPanels=new int[]{23,32,33};int[][] repeated=new int[][]{new int[]{26,1},new int[]{13,19},new int[]{16,24}};
 double addedLength=0;int addedFaces=0;var turnNodes=new List<int>();var additionRecords=new List<string>();
 for(int ti=0;ti<targetPanels.Length;ti++){
  int p=targetPanels[ti];var basePath=new Grasshopper.Kernel.Data.GH_Path(p,0);var path=new Grasshopper.Kernel.Data.GH_Path(p,1);
  Mesh original=(Mesh)r.Meshes.Branch(basePath)[0];var originalMap=r.IndexMap.Branch(basePath).Select(x=>Convert.ToInt32(x)).ToList();
  var patch=new Mesh();patch.Vertices.UseDoublePrecisionVertices=true;var routes=new List<string>();
  var lines=new List<Line>();var starts=new List<int>();var ends=new List<int>();var originalStrands=new List<int>();
  if(false){foreach(int strand in repeated[ti]){lines.Add(spans[p][strand]);starts.Add(originalMap[strand*9+1]);ends.Add(originalMap[strand*9+7]);originalStrands.Add(strand);}}
  else{
   int pv=repeated[ti][0]*9+4;Point3d pivot=original.Vertices.Point3dAt(pv);int pivotIndex=originalMap[pv];
   int ai=-1,bi=-1;double best=-1;
   for(int a=0;a<spans[p].Count;a++)for(int b=0;b<spans[p].Count;b++){
    var qa=spans[p][a].From;var qb=spans[p][b].From;
    bool aLayer=aa[p].Any(q=>Math.Abs(q.DistanceTo(qa)-radius)<1e-8),bLayer=ab[p].Any(q=>Math.Abs(q.DistanceTo(qb)-radius)<1e-8);
    if(!aLayer||!bLayer)continue;double score=Vector3d.CrossProduct(qa-pivot,qb-pivot).Length;
    if(score>best){best=score;ai=a;bi=b;}
   }
   if(ai<0||bi<0||best<1e-8)throw new Exception("No valid new anchor distribution triangle");
   Point3d a0=spans[p][ai].From,b0=spans[p][bi].From;
   int aIndex=contactIndices[p][ai],bIndex=contactIndices[p][bi];
   lines.Add(new Line(a0,pivot));starts.Add(aIndex);ends.Add(pivotIndex);originalStrands.Add(-1);
   lines.Add(new Line(pivot,b0));starts.Add(pivotIndex);ends.Add(bIndex);originalStrands.Add(-1);
   lines.Add(new Line(b0,a0));starts.Add(bIndex);ends.Add(aIndex);originalStrands.Add(-1);
  }
  for(int s=0;s<lines.Count;s++){
   Line line=lines[s];Vector3d dir=line.Direction;dir.Unitize();int start=patch.Vertices.Count,faceBegin=patch.Faces.Count;
   var across=Vector3d.CrossProduct(normals[p],dir);if(!across.Unitize())throw new Exception("Additional ribbon axis undefined");
   for(int j=0;j<=ns;j++)for(int c=0;c<=nw;c++){
    Point3d q;int index;
    if(false){int vi=originalStrands[s]*9+j*3+c;q=original.Vertices.Point3dAt(vi);index=originalMap[vi];}
    else{q=line.PointAt((double)j/ns)+across*(((double)c/nw-.5)*width);if((j==0||j==ns)&&c==1)index=j==0?starts[s]:ends[s];else{index=master++;r.AssemblyPts.Add(q,new Grasshopper.Kernel.Data.GH_Path(2,p));}}
    patch.Vertices.Add(q);r.IndexMap.Add(index,path);
   }
   for(int j=0;j<ns;j++)for(int c=0;c<nw;c++){int k=start+j*3+c,h=k+3;patch.Faces.AddFace(k,h,h+1);patch.Faces.AddFace(k,h+1,k+1);r.Axes.Add(dir,path);r.Axes.Add(dir,path);}
   turnNodes.Add(starts[s]);if(false)turnNodes.Add(ends[s]);
   routes.Add("{\"strand\":"+s+",\"face_begin\":"+faceBegin+",\"face_count\":8,\"length_m\":"+NFn(line.Length)+",\"start\":"+NFxyz(line.From)+",\"end\":"+NFxyz(line.To)+"}");addedLength+=line.Length;
  }
  patch.Normals.ComputeNormals();string name="NG_P"+(p+1).ToString("000")+"_F1";r.Meshes.Add(patch,path);r.Names.Add(name,path);r.Height.Add(thick*100,path);addedFaces+=patch.Faces.Count;
  records.Add("{\"name\":\""+name+"\",\"panel\":"+p+",\"family\":1,\"faces\":"+patch.Faces.Count+",\"routes\":["+String.Join(",",routes)+"]}");
 }
 triangles+=addedFaces;total+=addedLength;count+=false?6:9;

 double loopLength=wraps*2*Math.PI*radius;
 r.Meta="{\"schema\":\"GH_NEW_NATIVE_FE_GEOMETRY/1\",\"panels\":"+A.Count+",\"explicit_master_nodes\":"+master+",\"frame_seed_nodes\":"+frameCount+",\"triangles\":"+triangles+",\"strands\":"+count+",\"frame_segments\":"+frameSegments+",\"distinct_frame_segments\":"+distinct.Count+",\"equivalent_sleeve_links\":"+wraps+",\"wrap_count\":"+wraps+",\"ground_edges\":"+groundEdges+",\"support_count\":"+groundNodes.Count+",\"load_nodes\":"+loadNodes.Count+",\"zmin_m\":"+NFn(zmin)+",\"zmax_m\":"+NFn(zmax)+",\"transfer_length_m\":"+NFn(total)+",\"local_wrap_length_m\":"+NFn(loopLength)+",\"boundary_length_m\":"+NFn(boundaryLength)+",\"width_m\":"+NFn(width)+",\"thickness_m\":"+NFn(thick)+",\"records\":["+String.Join(",",records)+"]}";
 r.Meta=r.Meta.Substring(0,r.Meta.Length-1)+",\"reinforcement_mode\":\"NEW_ANCHOR\",\"additional_transfer_length_m\":"+NFn(addedLength)+",\"reinforcement_turn_nodes\":["+String.Join(",",turnNodes)+"],\"additional_turn_count\":"+turnNodes.Count+"}";
 r.Report="NATIVE C# GLOBAL FE GEOMETRY / ANALYZE NOT RUN\n"+A.Count+" panels; "+count+" straight sleeve-contact spans; "+triangles+" shell triangles.\n"+frameSegments+" owner boundary beam segments; "+wraps+" local equivalent sleeve links.\n"+groundNodes.Count+" translation supports on "+groundEdges+" ground boundary edges at Z=0.\n"+loadNodes.Count+" lateral stations, total 1 kN per direction.\nLocal circles supply lumped self-weight only; contact/bolt stress excluded.\nSource loft, panels, anchor sequence and physical sleeve routes unchanged.";
 return r;
}
