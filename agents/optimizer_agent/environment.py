import gymnasium as gym
import numpy as np
from gymnasium import spaces

class BuildOptimizerEnv(gym.Env):
    def __init__(self):
        super(BuildOptimizerEnv,self).__init__()
        
        self.action_space=spaces.Discrete(3)
        
        self.observation_space=spaces.Box(low=0,high=10,shape=(2,),dtype=np.float32)
        
        self.state=None
        self.prev_duration=3.0
        self.prev_success=1
        
    def step(self,action):
        if action==0:
            duration=np.random.uniform(2.5,3.5)
            success=np.random.rand()>0.3
        elif action==1:
            duration=np.random.uniform(1.5,2.8)
            success=np.random.rand()>0.2
        else:
            duration=np.random.uniform(1.0,2.5)
            success=np.random.rand()>0.4
            
        reward=-duration
        if not success:
            reward-=5

        self.state=np.array([duration,int(success)],dtype=np.float32)
        done=False
        
        return self.state,reward,done,False,{}
    
    def reset(self,*,seed=None,options=None):
        super().reset(seed=seed)
        self.state=np.array([3.0,1],dtype=np.float32)
        return self.state,{}
    
    def render(self,mode='human'):
        print(f'Build Duration:{self.state[0]:.2f}s, Success: {bool(self.state[1])}')