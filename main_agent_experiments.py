import os
import numpy as np
import gym
from reinforcement_agents.agents import TemporalDifferenceLearning as TDL
import sim_world # import ensures that the gym environment for the Robot-Simulation is registered
from sim_world.envs.car_0.ev3_sim_car import Car
from sim_world.envs.pygame_0.ev3_sim_pygame_2d_V2 import PyGame2D
import logging
import json

# only for lecturer otherwise comment out the following line
os.chdir(os.getcwd() + ".\_student_version")

def runExperiment_NStep(agent_nEpisodes, env, agent, observation_space_num):
  """Train and test the agent in the given Environment for the given Episodes.
     Function for N-Step agents.

    Args:
        agent_nEpisodes (int): number of Episoeds to train
        env (gym env): Evironment to train/test the agent in
        agent (agent): the agent to train
        observation_space_num (list): number of states per dimenson of observation

    Returns:
        list: reward_sums
        list: episodesvstimesteps 
        list: actionValueTable_history
  """
  __reward_sums = []
  __episodesvstimesteps = []
  __actionValueTable_history = []
  for __e in range(agent_nEpisodes):
    __timesteps = 0
    if(__e % 100 == 0):
      print("Episode: ", __e)
      
    __state = env.reset()
    # transform to 1d-coodinates
    __state = convert_3d_to_1d(__state, observation_space_num)
    __action = agent.selectAction(__state)    
    __done = False
    __experiences = [{}]
    __reward_sums.append(0.0)
    while not __done:
      __timesteps += 1
      __experiences[-1]['state'] = __state
      __experiences[-1]['action'] = __action
      __experiences[-1]['done'] = __done
      
      __new_state, __reward, __done, __info = env.step(__action)
      
      # transform to 1d-coodinates
      __new_state = convert_3d_to_1d(__new_state, observation_space_num)   
      #print("State:", state, "Action: ", env.actionMapping[action][1], "Reward: ", reward, "New state:", new_state, "done:", done)
      
      __new_action = agent.selectAction(__new_state)
      
      __xp = {}
      __xp['state'] = __new_state
      __xp['reward'] = __reward
      __xp['done'] = __done
      __xp['action'] = __new_action
      __experiences.append(__xp)
      
      agent.update(__experiences[-2:])
      
      if(agent.getName() == "SARSA"):
        __action = __new_action
      else:
        __action = agent.selectAction(__new_state)
      
      __state = __new_state
      
      __reward_sums[-1] += __reward

      if(__e % 50) == 0:
          env.render()
    __episodesvstimesteps.append([__e, __timesteps])

    # store table data
    if(__e % 50 == 0):
        if(agent.getName() == 'Double Q-Learning'):
          avg_action_table = np.mean(np.array([agent.actionValueTable_1.copy(), agent.actionValueTable_2.copy()]), axis=0)
          __actionValueTable_history.append(avg_action_table.copy())
        else:
          __actionValueTable_history.append(agent.actionValueTable.copy())

    if(__e % 100 == 0):
        title = agent.getName() + ' Episode:' + str(__e)
        print(title, 'reward_sums=', __reward_sums[-1])

      
  return __reward_sums, np.array(__episodesvstimesteps), __actionValueTable_history

def test_q_table(q_table, env, agent_nEpisodes):
  """test the given q-table under an greedy policy (argmax)

  Args:
      q_table (np.array): q_table to test
      env (gym.Env): gym Environment to test the agent in
      agent_nEpisodes (int): number of episodes

  Returns:
      reward_sums (list): sum of rewards per Episode
      episodesvstimesteps (np.array): steps per episode
  """
  __observation_space_nums = _get_observation_space_num(env)

  __reward_sums = []
  __episodesvstimesteps = []
  for __e in range(agent_nEpisodes):
      __timesteps = 0
          
      __state = env.reset()
      __q_table_index = convert_3d_to_1d(__state, __observation_space_nums)
      #__action = agent.selectAction(state)
      __action = np.argmax(q_table[__q_table_index]) 
      __done = False
      __reward_sums.append(0.0)
      while not __done:
          __timesteps += 1
          
          __experiences = [{}]
          __experiences[-1]['state'] = __state
          __experiences[-1]['action'] = __action
          __experiences[-1]['done'] = __done
          
          __new_state, __reward, __done, __info = env.step(__action)

          # transform to 1d-coodinates
          __new_state = convert_3d_to_1d(__new_state, __observation_space_nums)

          #new_action = agent.selectAction(new_state)
          __action = np.argmax(q_table[__new_state]) 
          

          __state = __new_state
          
          if(__e % 1 == 0):
              env.render()

          #episodesvstimesteps.append([e,timesteps])
          __reward_sums[-1] += __reward
      __episodesvstimesteps.append([__e, __timesteps])

  return __reward_sums, np.array(__episodesvstimesteps)

def train_agent(env, agent, file_prefix, file_suffix, __q_table=None,):
    """train the agent in the given env

    Args:
        env (gym.Env): gym.Env to train in 
        agent (agent): reinforcement agent to train
        file_prefix (strings): #TODO
        file_suffix (strings): #TODO
        q_table (np.array, optional): q_table used for init. Defaults to None.
    """
    __observation_space_nums = _get_observation_space_num(env)
    if (not (__q_table is None)):
        agent.actionValueTable = __q_table
        logging.info('USE GIVEN Q-TABLE')

    __reward_sums, __evst, __actionValueTable_history = runExperiment_NStep(agent_nEpisodes, env, agent, __observation_space_nums)

    
    np.save(file_prefix + 'q-table' + file_suffix + '.npy', __actionValueTable_history[-1])
    np.save(file_prefix + 'reward_sums' + file_suffix + '.npy', __reward_sums)

    # create argmax policy; store as json
    __json_path = file_prefix + 'policy' + file_suffix + '.json'
    __q_policy = convert_q_table_to_policy(__actionValueTable_history[-1], __observation_space_nums)
    store_dict_as_json(__q_policy, __json_path)

def _get_observation_space_num(env):
    """get the number of steps per dimenion of the observation space

    Args:
        env (gym.Env): env to obtain the observation from
    Returns:
        list: number of steps per observation dimension
    """
    # how many states per dimension exist?
    __observation_space_nums = []
    __high = env.observation_space.high
    __low = env.observation_space.low
    for __bounds_pair in zip(__low, __high): 
        __num_states = __bounds_pair[1] - __bounds_pair[0] + 1
        __observation_space_nums.append(__num_states)
    return __observation_space_nums

def convert_3d_to_1d(state_3d, observation_space_num):
  """convert 3d States to 1d States

  Args:
      state_3d (list): 3d state
      observation_space_num (list): list of stages per observation dimension

  Returns:
      state_1d (int): 1d state
  """
  __x_len = observation_space_num[2]
  __y_len = observation_space_num[1]
  __z_len = observation_space_num[0]

  __x = state_3d[2]
  __y = state_3d[1]
  __z = state_3d[0]
  # ravel
  __state_1d = __x + (__y * __x_len) + (__z * __x_len * __y_len)
  return __state_1d

def convert_1d_to_3d(state_1d, observation_space_num):
  """convert 1d States to 3d States

  Args:
      state_1d (int): 1d state
      observation_space_num (list): list of stages per observation dimension

  Returns:
      state_3d (tupel): 3d state
  """
  __x_len = observation_space_num[2]
  __y_len = observation_space_num[1]
  __z_len = observation_space_num[0]

  # unravel
  __x = state_1d % __x_len
  __y = (state_1d // __x_len) % __y_len
  __z = ((state_1d // __x_len) // __y_len) % __z_len

  return (__z, __y, __x)

def read_numpy_data(file):
  """load numpy data

  Args:
      file (str): path to file

  Returns:
      np.array: loaded data
  """
  __data = np.load(file + '.npy')
  return __data

def convert_q_table_to_policy(q_table, observation_space_num):
    """convert the q-table to a greedy policy lookup dictionary

    Args:
        q_table (np.array): q-table to create the policy
        observation_space_num (): #TODO

    Returns:
        dict: greedy policy dict {state:action}
    """
    __policy_dict = {}
    for __i, __state in enumerate(q_table):
        __skey = convert_1d_to_3d(__i, observation_space_num)
        __skey = str(__skey[0]) + ' ' + str(__skey[1]) + ' ' + str(__skey[2])
        __action = int(np.argmax(__state))
        __policy_dict.update({__skey : __action})
    return __policy_dict

def store_dict_as_json(dict_data, file_name):
    """save a given dict as json file

    Args:
        dict_data (dict): dict to save
        file_name (str): path of the .json file
    """
    with open(file_name, 'w') as __f:
        json.dump(dict_data, __f)



if __name__ == '__main__':
    
    ######################### ENVIRONMENT #########################

    MAP = './sim_world/race_tracks/1.PNG'
    #MAP = './sim_world/race_tracks/4.PNG'

    MAP_START_COORDINATES = (90, 550)
    MAP_CHECK_POINT_LIST= [(290, 550), (670, 250), (1210, 160)]


    CAR_ENERGY_START = 1000
    CAR_ENERGY_MAX = 1000
    
    logging.basicConfig(format = '%(levelname)s:%(message)s', level=logging.INFO)
    sim_car = Car(car_file = './sim_world/envs/Lego-Robot.png', energy = CAR_ENERGY_START, energy_max = CAR_ENERGY_MAX)
    sim_pygame = PyGame2D(map_file_path = MAP, car = sim_car,  start_coordinates = MAP_START_COORDINATES, checkpoints_list = MAP_CHECK_POINT_LIST)
    env = gym.make("Robot_Simulation_Pygame-v2", pygame = sim_pygame)
    
    
    ######################### AGENT TRAIN #########################
    
    agent_exerciseID = 0
    agent_nExperiments = 1
    agent_nEpisodes = 2000

    # Agent
    agent_alpha = 0.2 
    agent_gamma = 0.9

    agent_n_steps = 20
    
    # Policy
    policy_epsilon = 0.1

    #env.render()
        
    agent = TDL.SARSA(env.nStates, env.nActions, agent_alpha, agent_gamma, epsilon=policy_epsilon)
    #agent = TDL.nStepTreeBackup(env.nStates, env.nActions, agent_alpha, agent_gamma, epsilon=policy_epsilon, n=agent_n_steps)

    file_prefix = 'q_tables_storage/'
    file_suffix = '_' + agent.getName() + '_test_1'

    #train_agent(env, agent, file_prefix, file_suffix)
    # quit()
    

    ######################### AGENT/Q-TABLE TEST #########################

    # load rewards and q-table
    rewards = read_numpy_data(file_prefix + 'reward_sums' + file_suffix)
    print(rewards)
    q_data = read_numpy_data(file_prefix + 'q-table' + file_suffix)

    # retrain agent
    #train_agent(env, agent, file_prefix, file_suffix, q_table=q_data)


    # test the q-table
    reward_sums, episodesvstimesteps = test_q_table(q_data, env, agent_nEpisodes = 10)
    print(reward_sums)