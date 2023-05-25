import sys
import os

from datetime import datetime
import logging, logging.config
import logger
import json

import numpy as np
import gym
from reinforcement_agents.agents import TemporalDifferenceLearning as TDL
from sim_world.envs.car_0.ev3_sim_car import SimCar as Car
from sim_world.envs.pygame_0.ev3_sim_pygame_2d_V2 import PyGame2D as Simulation

# only for lecturer otherwise comment out the following line
#os.chdir(os.getcwd() + ".\student\simulation")

def load_policy(policy_as_json):
    """load the policy json file

    Args:
        policy_as_json (str): path to json file

    Returns:
        dict: policy dict: {state:action}
    
    """
    __policy = {}
    with open(policy_as_json, 'r') as __f:
      __policy = json.load(__f)
    return __policy

def run_model(env, policy, states_list):
    """run the car with the given policy

    Args:
        car (SimCar): car to drive given the policy
        policy (dict): policy
    """
    __state = env.reset()

    __done = False
    while (__done == False):
        # preprocessing of the measured values
        __preprocessed_state = preprocessing_observations(observations=__state, states_list=states_list)

        # select the best action; based on state
        __action = greedy(policy=policy, state=__preprocessed_state)
        __state, __reward, __done, __info = env.step(__action)
            
def greedy(policy, state):
    '''
    Greedy policy

    return the best action corresponding to the state
    '''
    __key = str(state[0]) + ' ' + str(state[1]) + ' ' + str(state[2])
    return policy[__key]

def preprocessing_observations(observations, states_list):
    # states_list = [['west'], ['north'], ['east']] 
    __car_X = 50
    __car_size = 24 # cm
    __resize_factor = __car_X / __car_size
    __obs_discrete = []

    for __observation in observations:
        if (__observation < ((__car_size * __resize_factor) * 1.8)):
            # obstacle detected
            __value = states_list[1][1]
            if (__observation < ((__car_size * __resize_factor) * 0.6)):
                # close obstacle detected
                __value = states_list[1][0]
        else:
            # no obstacle detected
            __value = states_list[1][2]
        __obs_discrete.append(__value)   
    logger.debug('OBSERVATION DISCRETE \'%s\'', str(__obs_discrete))
    return __obs_discrete

def train_model(env, agent, states_list, file_path, file_prefix, file_suffix, q_table=None):
    """train the agent in the given env

    Args:
        env (gym.Env): gym.Env to train in 
        agent (agent): reinforcement agent to train
        file_prefix (strings): #TODO
        file_suffix (strings): #TODO
        q_table (np.array, optional): q_table used for init. Defaults to None.
    """
    __observation_space_nums = __get_observation_space_num(env=env, states_list=states_list)
    if (not (q_table is None)):
        agent.actionValueTable = q_table
        logger.info('USE GIVEN Q-TABLE')

    __reward_sums, __evst, __actionValueTable_history = _runExperiment_NStep(agent_nEpisodes=agent_nEpisodes, env=env, agent=agent, states_list=states_list, observation_space_num=__observation_space_nums)
    
    np.save(file_path + file_prefix + 'q-table' + file_suffix + '.npy', __actionValueTable_history[-1])
    np.save(file_path + file_prefix + 'reward_sums' + file_suffix + '.npy', __reward_sums)

    # create argmax policy; store as json
    __json_path = file_path + file_prefix + 'policy' + file_suffix + '.json'
    __q_policy = __convert_q_table_to_policy(q_table=__actionValueTable_history[-1], observation_space_num=__observation_space_nums)
    __store_dict_as_json(dict_data=__q_policy, file_name=__json_path)

def test_model(env, agent, states_list, file_path, file_prefix, file_suffix, q_table=None):
    # load rewards and q-table
    __rewards = read_numpy_data(numpy_file=file_path + file_prefix + 'reward_sums' + file_suffix)
    logger.debug('rewards loaded = \'%s\'', str(__rewards))
    __q_data = read_numpy_data(numpy_file=file_path + file_prefix + 'q-table' + file_suffix)

    # test the q-table
    __reward_sums, __episodesvstimesteps = _test_q_table(q_table=__q_data, env=env, states_list=states_list, agent_nEpisodes=10)
    logger.debug('reward sums = \'%s\'', str(__reward_sums))

################################################################
### Additional functions only for the simulation environment ###
################################################################

def _runExperiment_NStep(agent_nEpisodes, env, agent, states_list, observation_space_num):
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
    if (__e % 100 == 0):
      logger.info('Episode: %s', str(__e))
      
    __state = env.reset()

    # preprocessing of the measured values
    __state = preprocessing_observations(observations=__state, states_list=states_list)

    # transform to 1d-coodinates
    __state = __convert_3d_to_1d(state_3d=__state, observation_space_num=observation_space_num)
    __action = agent.selectAction(__state)    
    __done = False
    __experiences = [{}]
    __reward_sums.append(0.0)
    while (not __done):
      __timesteps += 1
      __experiences[-1]['state'] = __state
      __experiences[-1]['action'] = __action
      __experiences[-1]['done'] = __done
      
      __new_state, __reward, __done, __info = env.step(__action)

      # preprocessing of the measured values
      __new_state = preprocessing_observations(observations=__new_state, states_list=states_list)
      
      # transform to 1d-coodinates
      __new_state = __convert_3d_to_1d(state_3d=__new_state, observation_space_num=observation_space_num)   

      __new_action = agent.selectAction(__new_state)
      
      __xp = {}
      __xp['state'] = __new_state
      __xp['reward'] = __reward
      __xp['done'] = __done
      __xp['action'] = __new_action
      __experiences.append(__xp)
      
      agent.update(__experiences[-2:])
      
      if (agent.getName() == "SARSA"):
        __action = __new_action
      else:
        __action = agent.selectAction(__new_state)
      
      __state = __new_state
      
      __reward_sums[-1] += __reward

      if (__e % 50 == 0):
          env.render()
    __episodesvstimesteps.append([__e, __timesteps])

    # store table data
    if (__e % 50 == 0):
        if (agent.getName() == 'Double Q-Learning'):
          __avg_action_table = np.mean(np.array([agent.actionValueTable_1.copy(), agent.actionValueTable_2.copy()]), axis=0)
          __actionValueTable_history.append(__avg_action_table.copy())
        else:
          __actionValueTable_history.append(agent.actionValueTable.copy())

    if (__e % 100 == 0):
        __title = agent.getName() + ' Episode:' + str(__e)
        logger.debug('%s | reward_sums = \'%s\'', str(__title), str(__reward_sums[-1]))
      
  return __reward_sums, np.array(__episodesvstimesteps), __actionValueTable_history

def _test_q_table(q_table, env, states_list, agent_nEpisodes):
  """test the given q-table under an greedy policy (argmax)

  Args:
      q_table (np.array): q_table to test
      env (gym.Env): gym Environment to test the agent in
      agent_nEpisodes (int): number of episodes

  Returns:
      reward_sums (list): sum of rewards per Episode
      episodesvstimesteps (np.array): steps per episode
  """
  __observation_space_nums = __get_observation_space_num(env=env, states_list=states_list)

  __reward_sums = []
  __episodesvstimesteps = []
  for __e in range(agent_nEpisodes):
      __timesteps = 0
          
      __state = env.reset()

      # preprocessing of the measured values
      __state = preprocessing_observations(observations=__state, states_list=states_list)

      __q_table_index = __convert_3d_to_1d(state_3d=__state, observation_space_num=__observation_space_nums)
      #__action = agent.selectAction(__state)
      __action = np.argmax(q_table[__q_table_index]) 
      __done = False
      __reward_sums.append(0.0)
      while (not __done):
          __timesteps += 1
          
          __experiences = [{}]
          __experiences[-1]['state'] = __state
          __experiences[-1]['action'] = __action
          __experiences[-1]['done'] = __done
          
          __new_state, __reward, __done, __info = env.step(__action)

          # preprocessing of the measured values
          __new_state = preprocessing_observations(observations=__new_state, states_list=states_list)

          # transform to 1d-coodinates
          __new_state = __convert_3d_to_1d(state_3d=__new_state, observation_space_num=__observation_space_nums)

          #new_action = agent.selectAction(new_state)
          __action = np.argmax(q_table[__new_state]) 

          __state = __new_state
          
          if (__e % 1 == 0):
              env.render()

          #episodesvstimesteps.append([e,timesteps])
          __reward_sums[-1] += __reward
      __episodesvstimesteps.append([__e, __timesteps])

  return __reward_sums, np.array(__episodesvstimesteps)

def __get_observation_space_num(env, states_list):
    """get the number of steps per dimenion of the observation space

    Args:
        env (gym.Env): env to obtain the observation from

    Returns:
        list: number of steps per observation dimension
    """
    # how many states per dimension exist?
    __observation_space_nums = [len(states_list[0]), len(states_list[1]), len(states_list[2])]
    return __observation_space_nums

def __convert_q_table_to_policy(q_table, observation_space_num):
    """convert the q-table to a greedy policy lookup dictionary

    Args:
        q_table (np.array): q-table to create the policy
        observation_space_num (): #TODO

    Returns:
        dict: greedy policy dict {state:action}
    """
    __policy_dict = {}
    for __i, __state in enumerate(q_table):
        __skey = ___convert_1d_to_3d(state_1d=__i, observation_space_num=observation_space_num)
        __skey = str(__skey[0]) + ' ' + str(__skey[1]) + ' ' + str(__skey[2])
        __action = int(np.argmax(__state))
        __policy_dict.update({__skey : __action})
    return __policy_dict

def __store_dict_as_json(dict_data, file_name):
    """save a given dict as json file

    Args:
        dict_data (dict): dict to save
        file_name (str): path of the .json file
    """
    with open(file_name, 'w') as __f:
        json.dump(dict_data, __f)

def __convert_3d_to_1d(state_3d, observation_space_num):
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

def ___convert_1d_to_3d(state_1d, observation_space_num):
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

def read_numpy_data(numpy_file):
    """load numpy data

    Args:
        file (str): path to file

    Returns:
        np.array: loaded data
    """
    __data = np.load(numpy_file + '.npy')
    return __data

################################################################
###                          M A I N                         ###
################################################################
             
if __name__ == '__main__':
    ROOT_FILE_PATH = "../model_storage/"

    current_datetimestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists(ROOT_FILE_PATH + current_datetimestamp):
        os.makedirs(ROOT_FILE_PATH + current_datetimestamp)
    CURRENT_FILE_PATH = ROOT_FILE_PATH + current_datetimestamp + "/"

    # logger config
    # https://docs.python.org/3/library/logging.html#logrecord-attributes   
    logger = logger.createLogger(config="../logging.conf.json", logger_name="__main__", logfile=CURRENT_FILE_PATH + 'logfile.log')

    logger.info('START SIMULATION')
    
    ###############################################################
    ############################ SETUP ############################

    TRAIN_MODEL = True
    RETRAIN_MODEL = True
    TEST_MODEL = True
    RUN_MODEL = True  

    # manual path
    #CURRENT_FILE_PATH = ""

    ######################### ENVIRONMENT #########################

    MAP = './sim_world/race_tracks/1.PNG'
    MAP_START_COORDINATES = (90, 550)
    MAP_CHECK_POINT_LIST= [(290, 550), (670, 250), (1210, 160)]

    CAR_ENERGY_START = 1000
    CAR_ENERGY_MAX = 1000

    # States & Actions
    nStates = 27
    # states_list = [['west'], ['north'], ['east']]
    states_list = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    actions_dict = {
        0: {'speed' : 20, 'energy' : -10},
        1: {'angle' : -45, 'energy' : -10},
        2: {'angle' : 45, 'energy' : -10},
        3: {'speed' : -20, 'energy' : -10}
    }
    nActions = len(actions_dict)

    sim_car = Car(actions_dict = actions_dict, car_file = './sim_world/envs/Lego-Robot.png', energy = CAR_ENERGY_START, energy_max = CAR_ENERGY_MAX)
    sim_pygame = Simulation(map_file_path = MAP, car = sim_car,  start_coordinates = MAP_START_COORDINATES, checkpoints_list = MAP_CHECK_POINT_LIST)
    env = gym.make("Robot_Simulation_Pygame-v2", pygame = sim_pygame)

    ###############################################################
    ######################### MODEL ###############################

    agent_exerciseID = 0
    agent_nExperiments = 1
    agent_nEpisodes = 10000

    # Agent
    agent_alpha = 0.2
    agent_gamma = 0.9

    agent_n_steps = 20
    
    # Policy
    policy_epsilon = 0.1

    #env.render()
    
    # Agent
    agent = TDL.SARSA(nStates, nActions, agent_alpha, agent_gamma, epsilon=policy_epsilon)
    #agent = TDL.nStepTreeBackup(nStates, nActions, agent_alpha, agent_gamma, epsilon=policy_epsilon, n=agent_n_steps)
    logger.info('AGENT \'%s\' SELECTED', str(agent.getName()))

    file_prefix = ''
    file_suffix = '_' + agent.getName() + '_' + current_datetimestamp

    ######################### AGENT TRAIN #########################

    if (TRAIN_MODEL):
        logger.info('TRAIN AGENT [%s]', str(CURRENT_FILE_PATH))
        train_model(env=env, agent=agent, file_path=CURRENT_FILE_PATH, file_prefix=file_prefix, file_suffix=file_suffix, states_list=states_list)
        logger.info('FINISH TRAINING OF AGENT')

    ######################### AGENT TRAIN #########################

    if (RETRAIN_MODEL):
        q_data_file = CURRENT_FILE_PATH + file_prefix + 'q-table' + file_suffix
        rewards_file = CURRENT_FILE_PATH + file_prefix + 'reward_sums' + file_suffix
        # manual path
        #q_data_file = ""
        #rewards_file= ""

        # load rewards and q-table
        rewards = read_numpy_data(rewards_file)
        logger.debug('rewards loaded = \'%s\'', str(rewards))
        logger.info('LOADING TRAININGSDATA \'%s\'', str(q_data_file))
        q_data = read_numpy_data(numpy_file=q_data_file)

        logger.info('RETRAIN AGENT WITH \'%s\' [%s]', str(q_data_file), str(CURRENT_FILE_PATH))
        train_model(env=env, agent=agent, states_list=states_list, file_path=CURRENT_FILE_PATH, file_prefix=file_prefix, file_suffix=file_suffix, q_table=q_data)
        logger.info('FINISH RETRAINING OF AGENT')

    ######################### AGENT TEST ##########################

    if (TEST_MODEL):
        logger.info('TEST AGENT [%s]', str(CURRENT_FILE_PATH))
        test_model(env=env, agent=agent, states_list=states_list, file_path=CURRENT_FILE_PATH, file_prefix=file_prefix, file_suffix=file_suffix)
        logger.info('FINISH TESTING OF AGENT')

    ######################### AGENT RUN ###########################

    if (RUN_MODEL):
        policy_file = CURRENT_FILE_PATH + file_prefix + 'policy' + file_suffix + '.json'
        # manual path
        #policy_file = "../model_storage/policy_SARSA.json"

        logger.info('LOADING POLICY \'%s\'', str(policy_file))
        policy = load_policy(policy_as_json=policy_file)
        logger.info('RUN AGENT WITH \'%s\' [%s]', str(policy_file), str(CURRENT_FILE_PATH))
        run_model(env=env, policy=policy, states_list=states_list)
        logger.info('FINISH RUNNING OF AGENT')
    
    ###############################################################

    logger.info('EXIT SIMULATION')