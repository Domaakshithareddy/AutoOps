from fastapi import FastAPI, Response
from prometheus_client import Counter,Gauge,generate_latest,CONTENT_TYPE_LATEST
import random
import time

app=FastAPI()

BUILD_TOTAL=Counter("build_total","Total number of simulated builds")
BUILD_FAILURES=Counter("build_failures","Total failed builds")
BUILD_DURATION=Gauge("build_duration_seconds","Duration of each build")

@app.get('/simulate_build')

def simulate_build():
    BUILD_TOTAL.inc()
    duration=round(random.uniform(1.0,3.0),2)
    BUILD_DURATION.set(duration)
    time.sleep(duration)
    
    if random.random()<0.3:
        BUILD_FAILURES.inc()
        return {"status":"failed","duration":duration}
    return {"status":"success","duration":duration}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)