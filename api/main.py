from fastapi import FastAPI
from agents.responder_agent import responder

app = FastAPI(title="AutoOps API")

# Include your responder routes
app.include_router(responder.router)

@app.get("/")
async def root():
    return {"message": "AutoOps API is running"}
