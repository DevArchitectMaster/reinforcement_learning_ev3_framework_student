import gym
from gym import spaces
import numpy as np
import logging

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self, pygame):
        super(CustomEnv,self).__init__()
        
        self.pygame = pygame
        self.car = pygame._car

        #self.action_space = spaces.Discrete(3)
        #self.observation_space = spaces.Box(np.array([0, 0, 0]), np.array([2, 2, 2]), dtype=np.int)
        
        # get action and observation-space from car?
        self.action_space = spaces.Discrete(self.car.action_space)
        self.observation_space = spaces.Box(np.array(self.car.observation_space[0]), 
                                            np.array(self.car.observation_space[1]), 
                                            dtype=np.int)
        
        #how many actions are possible?
        self.nActions = self.action_space.n
        #how many states exist in the observation space?
        self.nStates = 1
        high = self.observation_space.high
        low = self.observation_space.low
        for bounds_pair in zip(low, high): 
            num_states = bounds_pair[1] - bounds_pair[0] + 1
            self.nStates*=num_states

    def reset(self):
        self.car.reset()
        self.pygame.reset()
        obs = self.pygame.observe()
        return np.array(obs)

    def step(self, action):
        self.pygame.action(action)
        obs = np.array(self.pygame.observe())
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        info = {'prob':1}
        return obs, reward, done, info

    def render(self, mode="human", close=False):
        self.pygame.view()
