import sys,json,time,clr,traceback
O=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs/NG07_BOUNDARY_GAP_N29_S14_P55_20261018'
r={}
try:
 clr.AddReference('Newtonsoft.Json')
 from Newtonsoft.Json import JsonConvert,JsonSerializerSettings,StringEscapeHandling
 settings=JsonSerializerSettings();settings.StringEscapeHandling=StringEscapeHandling.EscapeNonAscii
 for name in ['DIRECT_NATIVE_RAW','BEAM_STRESS_RAW']:
  path=O+'/V2/H020/NG07_H020_NATIVE_NINE_V2_G_'+name+'.json';data=json.load(open(path));t=time.time();encoded=JsonConvert.SerializeObject(data,settings);duration=time.time()-t;decoded=json.loads(str(encoded));assert decoded==data,'Serializer changed native values or structure';r[name]={'semantic_identity':True,'native_writer_seconds':duration,'characters':len(encoded)}
 r['status']='EXACT_JSON_ROUNDTRIP_VERIFIED'
except:r['error']=traceback.format_exc();r['status']='UNAVAILABLE_KEEP_ORIGINAL_EXPORTER'
with open(O+'/NATIVE_JSON_WRITER_AUDIT.json','w') as stream:json.dump(r,stream)
