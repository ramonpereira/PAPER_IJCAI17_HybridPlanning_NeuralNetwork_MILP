from DeterministicMazeRemaster import DeterministicMazeRemaster
from RandomWalk import RandomWalk
import numpy as np

def approximated_transition_fuction(state, action):
    new_state = (0, 0)  
    return new_state

def true_transition_fuction(state, action):
    a_x = action[0]
    a_y = action[1]
    s_x = state[0]
    s_y = state[1]
    distances = np.sqrt(np.power(s_x-5,2)+np.power(s_y-5,2))
    scalefactor = 2.0/(1.0+np.exp(-2*distances))-0.99
    
    return s_x + (a_x*scalefactor), s_y + (a_y*scalefactor)

def get_succesor_states(environment, state, action_range):
    states = list()
    possible_directions = np.transpose([np.tile(action_range, len(action_range)), np.repeat(action_range, len(action_range))])
    length = len(possible_directions)
    for i in range(length):
        x = state[0] + possible_directions[i][0]
        y = state[1] + possible_directions[i][1]
        possible_state = (x, y)
        if verify_boundary(possible_state, environment):
            states.append(possible_state)

    return states

def verify_boundary(state, environment):
    x = state[0]
    y = state[1]

    minx = environment[0]
    miny = environment[1]

    maxx = environment[2]
    maxy = environment[3]

    if x < minx:
        return False
    elif y < miny:
        return False
    elif x >= maxx:
        return False
    elif y >= maxy:
        return False

    return True

def get_estimate(initial_state, goal_state):
    return 0

def main():
    task_setting = {
        "environment"        : (0,0,10,10),                        # Continous state bound
        "initial_state"      : (0,0),                              # Initial State in X, Y
        "action_range"       : [1, -1, 0.5, -0.5],                 # Action range
        "goal_state"         : [(10,10)],                          # Goal State in X, Y
        "obstacles"          : [], #[[(5,2),(5,5),(8,5),(8,2)]],   # Some obstacles that never crosspassing
    }

    environment = task_setting.get('environment')
    initial_state = task_setting.get('initial_state')
    action_range = task_setting.get('action_range')
    np_action_range = np.array(action_range)
    #action_test = (1.0,0.4862182908564383)
    #state_test = (0.0,0.0)    
    #print true_transition_fuction(state_test, action_test)
    print get_succesor_states(environment, initial_state, np_action_range)

if __name__ == '__main__' :
    main()