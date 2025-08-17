from fastapi import FastAPI
from fastapi.responses import Response
import requests, time
import threading
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI()

MONITOR_URL='http://localhost:8000/simulate_build'
OPTIMIZER_URL="http://localhost:8500/get_best_action"
RESPONDER_URL="http://localhost:8600/suggest_fix"

def autoops_loop(interval=10):
    while True:
        try:
            monitor_resp=requests.get(MONITOR_URL).json()
            print('[Monitor]->',monitor_resp)
            duration=monitor_resp['duration']
            
            if monitor_resp['status']=='failed':
                optimizer_resp=requests.post(
                    OPTIMIZER_URL,
                    json={'duration':duration,'success':0}
                ).json()
                print('[Optimizer]->',optimizer_resp)
                
                issue = monitor_resp.get("error", "unknown error")
                responder_resp=requests.post(
                    RESPONDER_URL,
                    json={'issue':issue}
                ).json()
                print('[Responder]->',responder_resp)
            else:
                print('[Monitor] Build secceeded. No action meeded')
        
        except Exception as e:
            print('[Controller] error:',e)
        
        time.sleep(interval)
        
@app.on_event('startup')
def start_loop():
    threading.Thread(target=autoops_loop,args=(10,),daemon=True).start()
    
@app.get('/')
def root():
    return {'status':'controller running (loop mode)'}