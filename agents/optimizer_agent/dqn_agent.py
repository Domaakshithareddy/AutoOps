from stable_baselines3 import DQN
from environment import BuildOptimizerEnv

env=BuildOptimizerEnv()

model=DQN('MlpPolicy',env,verbose=1)
model.learn(total_timesteps=10000)
model.save('agents/optimizer_agent/model/dqn_build_optimizer')

print('Training complete. Model saved.')