from ev3dev2.motor import MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import InfraredSensor
import logging

class MotorTank:
    def __init__(self, output1, output2, **kwargs):
        """2 Motors driving like a tank

        Args:
            output1 (str): port for motor 1
            output2 (str): port for motor 2
        """
        logging.info('CREATE MOTOR TANK (%s, %s)', output1, output2)
        # create the MoveTank object
        self.tank=MoveTank(output1, output2)

    def drive(self,action_params):
        """drive the tank given the params in dict

        Args:
            action_params (dict):  {'left_speed':int, 'right_speed':int, 'rotations':float},
        """
        logging.info('MOTOR TANK DRIVE , %s', action_params)
        self.tank.on_for_rotations(**action_params)

class SensorUltrasonic:
    def __init__(self, port, **kwargs):
        """Ultrasonic Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR ULTRASONIC (%s)', port)
        self.port = port
        # Connect ultrasonic and touch sensors to any sensor port
        self.us = UltrasonicSensor(port)
        # Put the US sensor into distance mode.
        self.us.mode="US-DIST-CM"
        #units = us.units
        #reports 'cm' even though the sensor measures 'mm'

    def read(self):
        """read the distance value

        Returns:
            float: distance
        """
        distance = self.us.value() # mm
        distance/=10  # convert mm to cm
        distance = round(distance,1)
        return distance


class SensorInfrared:
    def __init__(self, port, max_cm=70, **kwargs):
        """Ultrasonic Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR INFRARED (%s)', port)
        self.port = port
        # Connect ultrasonic and touch sensors to any sensor port
        self.ir = InfraredSensor(port)
        # Put the US sensor into distance mode.
        self.ir.mode='IR-PROX'
        self.IR_MAX_DIST = max_cm #according to lego 50-70 cm

    def read(self):
        """read the distance value

        Returns:
            float: distance
        """
        distance = self.ir.value() #100%value
        #calc cm value from percentage distance
        distance = (distance/100)* self.IR_MAX_DIST #cm
        distance = round(distance,1)
        return distance


class EV3Car:
    def __init__(self):
        """Create the EV3 Car with its sensors and motors
        """
        #logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.car_size = 24 #cm        
        self.inputs = {}
        self.outputs = {}
        self.actions_dict = {
            0: {'left_speed':20, 'right_speed':20, 'rotations':0.5},
            1: {'left_speed':-20, 'right_speed':20, 'rotations':0.25},
            2: {'left_speed':20, 'right_speed':-20, 'rotations':0.25},
        }   
        self.init_robot_input_and_output()
        
    def init_robot_input_and_output(self):
        """create the input and outputs which are given to the agent
        """
        #init sensors
        inputs = {}
        #ultrasonic left/west
        sensor_pos = 'west'
        sensor = SensorUltrasonic('in1', )
        inputs.update({sensor_pos: sensor})
        #ultrasonic right/east
        sensor_pos = 'east'
        sensor = SensorUltrasonic('in4')
        inputs.update({sensor_pos: sensor})
        #infrared up/north
        sensor_pos = 'north'
        sensor = SensorInfrared('in2')
        inputs.update({sensor_pos: sensor})
        #update inputs
        self.inputs = inputs

        #init motors
        outputs={}
        motor = MotorTank('outA', 'outB')
        #use the group name to identify the motors in the actions later..
        outputs.update({'tank1': motor})
        #update outputs
        self.outputs = outputs

    def observe(self):
        """read the sensors, create a state

        Returns:
            list: current state of the Car
        """
        #multiple measurements with average values per sensor; round to 1 decimal value
        observations = [0,0,0]
        observations[0] = self.inputs['west'].read()
        observations[1] = self.inputs['north'].read()
        observations[2] = self.inputs['east'].read()
        #discretize sensor values
        obs_discrete = []
        logging.info('OBSERVATION RAW %s',str(observations))

        for obs in observations:
            if(obs < ((self.car_size) * 1.8)):
                val = 1 # obstacle detected
                if(obs < ((self.car_size) * 0.6)):
                    val = 0 # close obstacle detected
            else:
                val = 2 
            obs_discrete.append(val)   
        logging.info('OBSERVATION DISCRETE %s',str(obs_discrete))
        return tuple(obs_discrete)

    def action(self,action):
        """perform the given action

        Args:
            action (int): numerical representation of the action
        """
        logging.info("ACTION: %s",action)
        action_params = self.actions_dict[action]
        self.outputs['tank1'].drive(action_params)


            

