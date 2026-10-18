# -*- coding: utf-8 -*-
import os,json,time,traceback,sys
import System,Rhino,Grasshopper as gh,clr
clr.AddReference('KarambaCommon');import feb
ROOT=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/outputs/NG10_REINFORCEMENT_FROM_BATCH500_20261018';W=r'C:/Users/Acer/Documents/Codex/2026-10-04/be/work/sleeve_sequence/ng10'
request=json.load(open(ROOT+'/ACTIVE_REQUEST.json'));assert os.environ.get('NG10_NONCE')==request['nonce'] and Rhino.RhinoDoc.ActiveDoc.Objects.Count==0
state={'pid':os.getpid(),'variant':request['variant'],'phase':'ENTERED','time_unix':time.time()}
def report():
 with open(ROOT+'/WORKER_STATE.json','w') as stream:json.dump(state,stream)
report()
try:
 env={'VARIANT':request['variant'],'RUN_ROOT':ROOT,'FORCE_DETAIL':True};state['phase']='PREPARE';report();execfile(W+'/prepare.py',env)
 folder=ROOT+'/'+request['variant'];assert os.path.exists(folder+'/INPUT_COMPLETE.json'),'Preparation incomplete'
 license=str(feb.LicenseValidation.instance().license_info().license_type());state['license']=license
 if license=='lic_trial':state['phase']='LICENSE_HOLD';report()
 else:
  state['phase']='NATIVE_ANALYZE_AND_EXPORT';report();execfile(W+'/run_native_once.py',env);complete=folder+'/NG10_'+request['variant']+'_NATIVE_NINE_V2_COMPLETE.json';assert os.path.exists(complete),'Native result incomplete';state['phase']='COMPLETE';state['complete']=complete;report()
except:state['phase']='HOLD';state['error']=traceback.format_exc();report()
finally:
 state['ended_unix']=time.time();report()
 if state['phase']=='COMPLETE' and os.environ.get('NG10_NONCE')==request['nonce'] and Rhino.RhinoDoc.ActiveDoc.Objects.Count==0:System.Diagnostics.Process.GetCurrentProcess().Kill()
