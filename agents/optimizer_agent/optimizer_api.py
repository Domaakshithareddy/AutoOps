from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from stable_baselines3 import DQN 
from agents.optimizer_agent.environment import BuildOptimizerEnv 

env=BuildOptimizerEnv()
model=DQN.load('agents/optimizer_agent/model/dqn_build_optimizer')

app=FastAPI()

class StateInput(BaseModel):
    duration: float
    success: int

@app.post('/get_best_action')
def get_best_action(state: StateInput):
    obs=np.array([state.duration,state.success],dtype=np.float32).reshape(1,-1)
    action=model.predict(obs,deterministic=True)[0]
    action_map={
        0:'default build',
        1:'use cache',
        2:'parallel build'
    }
    return {
        'action_id':int(action),
        'action_description': action_map[int(action)]
    }