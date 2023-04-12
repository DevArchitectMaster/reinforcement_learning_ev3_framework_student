import json
from ev3_robot_offline import EV3Car

def load_policy(path_json):
    """load the policy json file

    Args:
        path_json (str): path to json file

    Returns:
        dict: policy dict: {state:action}
    
    """
    q_dict = {}
    with open(path_json, 'r') as f:
      q_dict = json.load(f)
      #f.close()
    return q_dict

def run_model(car, policy):
    """run the car with the given policy

    Args:
        car (EV3Car): car to drive given the policy
        policy (dict): policy
    """
    done=False
    while done==False:        
        #observe the current state
        state=car.observe()
        #select the best action; based on state
        action = greedy(policy, state)
        car.action(action)
            
def greedy(policy, s):
        '''
        Greedy policy
        return the best action corresponding to the state
        '''
        key = str(s[0])+' '+str(s[1])+' '+str(s[2])
        return policy[key]
             
if __name__ == '__main__':
    policy_file = 'policy_SARSA_test_1.json'
    policy = load_policy(policy_file)
    ev3 = EV3Car()
    run_model(car=ev3, policy=policy)
    