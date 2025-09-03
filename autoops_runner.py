import subprocess
import time
import requests
import os
import signal

monitor_proc=subprocess.Popen(['python','-m','uvicorn','agents.monitor_agent.monitor_agent:app','--port','8000'])
optimizer_proc=subprocess.Popen(['python','-m','uvicorn','agents.optimizer_agent.optimizer_api:app','--port','8500'])
responder_proc=subprocess.Popen(['python','-m','uvicorn','agents.responder_agent.responder:app','--port','8600'])

time.sleep(8)

controller_proc=subprocess.Popen(['python', '-m', 'uvicorn', 'api.main:app', '--port', '9000'])
time.sleep(3)

print('Executing AutoOps pipeline...')
response=requests.get('http://localhost:9000/run_autoops').json()
print("\n=== AutoOps Pipeline Output ===")
print(response)
print("================================")

for p in (monitor_proc,optimizer_proc,responder_proc,controller_proc):
    p.send_signal(signal.SIGINT)
    
print('All background services stopped.')



# Change main.py code for a single point runner:

# from fastapi import FastAPI
# import requests

# app = FastAPI()

# MONITOR_URL   = "http://localhost:8000/simulate_build"
# OPTIMIZER_URL = "http://localhost:8500/get_best_action"
# RESPONDER_URL = "http://localhost:8600/suggest_fix"

# @app.get("/run_autoops")
# def run_autoops():
#     monitor_resp = requests.get(MONITOR_URL).json()
#     print("[Monitor] ->", monitor_resp)

#     if monitor_resp["status"] == "success":
#         return {
#             "status": "success",
#             "message": "Build completed successfully. No action needed."
#         }

#     duration = monitor_resp["duration"]
#     optimizer_resp = requests.post(
#         OPTIMIZER_URL,
#         json={"duration": duration, "success": 0}
#     ).json()
#     print("[Optimizer] ->", optimizer_resp)

#     issue = "build failure due to memory limits"
#     responder_resp = requests.post(
#         RESPONDER_URL,
#         json={"issue": issue}
#     ).json()
#     print("[Responder] ->", responder_resp)

#     return {
#         "status": "failed",
#         "optimizer_action": optimizer_resp,
#         "fix_suggestion": responder_resp
#     }

# @app.get("/")
# def root():
#     return {"status": "controller ready"}
