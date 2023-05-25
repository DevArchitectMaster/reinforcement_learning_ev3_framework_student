import logging
import json
from ev3_robot_car import EV3Car as Car

if __name__ == '__main__':
        
    actions_dict = {
        0: {'speed' : 20},
        1: {'angle' : -45},
        2: {'angle' : 45},
        3: {'speed' : -20},

        4: {'angle' : 90},
        5: {'angle' : 180},
        6: {'angle' : 270},
        7: {'angle' : 360}
    }
    
    ev3 = Car(actions=actions_dict)

    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(json.dumps(actions_dict, indent=4))
        print("\n\n")
        input_value = int(input("Waehlen Sie die Aktion aus: [0,1,2,3] & '-1' (for exit):\n"))

        if input_value == -1:
            logging.warning("exit by user")
            print("\n\n")
            break
        
        if input_value in actions_dict:
            print("\n")
            logging.warning("#####################################################################")
            logging.warning("input_value: '%s'", input_value)
            logging.warning("actions_dict[input_value]: '%s'", actions_dict[input_value])
            logging.warning("#####################################################################")
            print("\n")

            ev3.action(input_value)
        else:
            logging.error("404 - action '%s' not found", input_value)
    
    exit(0)