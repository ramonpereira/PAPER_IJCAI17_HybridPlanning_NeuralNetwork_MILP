from DeterministicMazeRemaster import DeterministicMazeRemaster
from RandomWalk import RandomWalk

def get_succesor_states(environment, state, visited):
    states = list()
    states.append((state[0], state[1]+0.3))  # Up
    states.append((state[0], state[1]-0.3))  # Down
    states.append((state[0]-0.3, state[1]))  # Left
    states.append((state[0]+0.3, state[1]))  # Right

    successor_states = list()
    for i in states:
        if verify_boundary(i, environment):
            successor_states.append(i)
    return successor_states

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
    initial_setting = {
        "maze"              : (0,0,10,10),                        #Continous state bound
        "start_state"       : (0,0),                              #Current State in X,Y and If in Jail
        "action_range"      : (-0.5,0.5),                         #The effective action range
        "goal_states"       : [(10,10)],                          #The goal state to finish running
        "jail_location"     : (-1,-1),                            #Jail location
        "obstacles"         : [], #[[(5,2),(5,5),(8,5),(8,2)]],   #Some obstacles that never crosspassing
        "muds"              : [], #[[(0,5),(0,10),(5,10),(5,5)]], #Mud area where movement is halfed
        "deadend_toleration": 2                                   #How many step left after getting into jail
    }

    environment = initial_setting.get('maze')
    initial_state = initial_setting.get('start_state')
    print initial_state
    print environment
    print get_succesor_states(environment, initial_state, False)
    

if __name__ == '__main__' :
    main()