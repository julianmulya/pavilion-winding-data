from pathlib import Path
import os,json,time,subprocess,uuid,sys,ctypes,shutil
B=Path(r'C:/Users/Acer/Documents/Codex/2026-10-04/be');R=B/'outputs/NG10_REINFORCEMENT_FROM_BATCH500_20261018';W=B/'work/sleeve_sequence/ng10';RHINO=r'C:/Program Files/Rhino 7/System/Rhino.exe'
state={'status':'STARTING','reviewed':[],'pid':os.getpid(),'native_only':True,'baseline_batch_paused':True}
def save():
 state['updated_unix']=time.time();(R/'PROGRESS.json').write_text(json.dumps(state,indent=2))
class MEM(ctypes.Structure):_fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),('total',ctypes.c_ulonglong),('available',ctypes.c_ulonglong),('page',ctypes.c_ulonglong),('availpage',ctypes.c_ulonglong),('virtual',ctypes.c_ulonglong),('availvirtual',ctypes.c_ulonglong),('extended',ctypes.c_ulonglong)]
for mode in ['REPEAT','NEW_ANCHOR','AB_SHIFT6']:
 folder=R/mode
 if (folder/'REVIEW_COMPLETE.json').exists():state['reviewed'].append(mode);continue
 if (folder/'INPUT_COMPLETE.json').exists():state.update(status='HOLD_EXISTING_FROZEN_INPUT_NO_REPLAY',variant=mode);save();sys.exit(1)
 mem=MEM();mem.length=ctypes.sizeof(mem);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem));state['available_bytes']=mem.available
 if mem.available<3000000000 or shutil.disk_usage(R).free<10*1024**3:state.update(status='HOLD_RESOURCE',variant=mode);save();sys.exit(1)
 req={'variant':mode,'nonce':str(uuid.uuid4())};(R/'ACTIVE_REQUEST.json').write_text(json.dumps(req));env=os.environ.copy();env['NG10_NONCE']=req['nonce'];si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=7;macro='_Karamba3DGetLicense _Grasshopper _-RunPythonScript '+str(W/'worker.py').replace('\\','/');proc=subprocess.Popen('"'+RHINO+'" /nosplash /runscript="'+macro+'"',env=env,startupinfo=si);state.update(status='RUNNING',variant=mode,worker_pid=proc.pid);save();start=time.time()
 while proc.poll() is None:
  try:ws=json.loads((R/'WORKER_STATE.json').read_text())
  except:ws={}
  if ws.get('pid')==proc.pid:
   state['worker']=ws;save()
   if ws.get('phase') in ['HOLD','LICENSE_HOLD']:state['status']=ws['phase'];save();sys.exit(1)
  if time.time()-start>1800:state['status']='HOLD_TIMEOUT_NO_REPLAY';save();sys.exit(1)
  time.sleep(3)
 complete=folder/('NG10_'+mode+'_NATIVE_NINE_V2_COMPLETE.json')
 if not complete.exists():state['status']='HOLD_PROCESS_ENDED_INCOMPLETE';state['exit_code']=proc.returncode;save();sys.exit(1)
 review=subprocess.run([sys.executable,str(W/'review_native.py'),str(folder)],capture_output=True,text=True);(folder/'REVIEW_STDOUT.log').write_text(review.stdout);(folder/'REVIEW_STDERR.log').write_text(review.stderr)
 if review.returncode:state['status']='HOLD_REVIEW';save();sys.exit(1)
 state['reviewed'].append(mode);save()
state['status']='THREE_CANDIDATES_NATIVE_REVIEWED';save()
