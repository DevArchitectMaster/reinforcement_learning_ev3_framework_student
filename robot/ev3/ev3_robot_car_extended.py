# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html

from ev3dev2.motor import MoveTank

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sensor.lego import SoundSensor
from ev3dev2.sensor.lego import LightSensor

import logging
import math



# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html#move-tank
class MotorTank:
    def __init__(self, output1, output2, **kwargs):
        """two Motors driving like a tank

        Args:
            output1 (str): port for motor 1
            output2 (str): port for motor 2
        """
        logging.info('CREATE MOTOR TANK (%s, %s)', output1, output2)
        # create the MoveTank object
        self.tank = MoveTank(output1, output2)

    def drive(self, action_params):
        """drive the tank given the params in dict

        Args:
            action_params (dict):  {'speed':int} or {'angle':int}
        """
        def drive_degrees(action_params):
            """drive the tank given the params in dict

            Args:
                action_params (dict):  {'speed':int} or {'angle':int}
            """
            logging.info('MOTOR TANK DRIVE , %s', action_params)

            __speed = 20
            __speed_negativ = __speed * (-1)
            # radius = 2,75 | 5/2 => perimeter = 17,27
            __perimeter = 17.27
            for [__action_key, __action_value] in action_params.items():
                if(__action_key == 'speed'):
                    __one_cm = 360 / __perimeter
                    __distance = __action_value * __one_cm
                    self.tank.on_for_degrees(__speed, __speed, __distance)
                elif(__action_key == 'angle'):
                    __radian_measure = __action_value * 2
                    self.tank.on_for_degrees(__speed, __speed_negativ, __radian_measure)

        def drive_rotations(action_params):
            """drive the tank given the params in dict
            Args:
                action_params (dict):  {'speed':int} or {'angle':int}
            """
            logging.info('MOTOR TANK DRIVE , %s', action_params)
            __speed = 20
            __speed_negativ = __speed * (-1)
            # radius = 2,75 | 5/2 => perimeter = 17,27
            __perimeter = 17.27
            for __action_key, __action_value in action_params.items():
                if(__action_key == 'speed'):
                    __distance = __action_value / __perimeter
                    self.tank.on_for_rotations(__speed, __speed, __distance)
                elif(__action_key == 'angle'):
                    __rotations = (__action_value * 2) / 360
                    self.tank.on_for_rotations(__speed, __speed_negativ, __rotations)


        logging.info('MOTOR TANK DRIVE , %s', action_params)
        drive_degrees(action_params)
        #drive_rotations(action_params)



# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html#ultrasonic-sensor
class SensorUltrasonic:
    def __init__(self, port, **kwargs):
        """Ultrasonic Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR ULTRASONIC (%s)', port)
        self.port = port
        # Connect ultrasonic sensors to any sensor port
        self.us = UltrasonicSensor(port)
        # Put the US sensor into distance mode.
        self.us.mode = "US-DIST-CM"
        #units = us.units
        #reports 'cm' even though the sensor measures 'mm'

    def read(self):
        """read the distance value

        Returns:
            float: distance
        """
        distance = self.us.value() # mm
        distance /= 10  # convert mm to cm
        distance = round(distance,1)
        return distance



# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html#infrared-sensor
class SensorInfrared:
    def __init__(self, port, max_cm=70, **kwargs):
        """Infrared Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR INFRARED (%s)', port)
        self.port = port
        # Connect infrared sensors to any sensor port
        self.ir = InfraredSensor(port)
        # Put the US sensor into distance mode.
        self.ir.mode = 'IR-PROX'
        self.IR_MAX_DIST = max_cm #according to lego 50-70 cm

    def read(self):
        """read the distance value

        Returns:
            float: distance
        """
        distance = self.ir.value() #100%value
        #calc cm value from percentage distance
        distance = (distance/100) * self.IR_MAX_DIST #cm
        distance = round(distance, 1)
        return distance



########################################################################################################################################################################################################

# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#touch-sensor
class SensorTouch:
    def __init__(self, port, **kwargs):
        """Touch Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR TOUCH (%s)', port)
        self.port = port
        # Connect touch sensors to any sensor port
        self.touch = TouchSensor(port)
        # Put the touch sensor into button state.
        self.touch.mode = 'TOUCH'
        

    def read(self):
        """read the state of the sensor

        Returns:
            boolean: is pressed
        """
        return self.touch.is_pressed()
    


# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#color-sensor
class SensorColor:
    def __init__(self, port, **kwargs):
        """Color Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR COLOR (%s)', port)
        self.port = port
        # Connect color sensors to any sensor port
        self.color = ColorSensor(port)
        # Color. All LEDs rapidly cycling, appears white.
        self.color.mode = 'COL-COLOR'

    def read(self):
        """read color detected by the sensor, categorized by overall value.

        Returns:
            int: color number [0: No color | 1: Black | 2: Blue | 3: Green | 4: Yellow | 5: Red | 6: White | 7: Brown]
        """
        return self.color.color()
    


# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#gyro-sensor
class SensorGyro:
    def __init__(self, port, **kwargs):
        """Gyro Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR GYRO (%s)', port)
        self.port = port
        # Connect gyro sensors to any sensor port
        self.gyro = GyroSensor(port)
        # Raw sensor value
        self.gyro.mode = 'GYRO-FAS'
        # Angle and rotational speed
        #self.gyro.mode = 'GYRO-G&A'

    def read(self):
        """read the angle and rotational speed value

        Returns:
            dict: angle and rotational speed
        """
        gyro_dict = self.gyro.value()
        return gyro_dict



# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#sound-sensor
class SensorSound:
    def __init__(self, port, max_cm=70, **kwargs):
        """Sound Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR SOUND (%s)', port)
        self.port = port
        # Connect sound sensors to any sensor port
        self.sound = SoundSensor(port)
        # Sound pressure level. Flat weighting
        self.sound.mode = 'DB'

    def read(self):
        """read the sound pressure level, as a percent. Uses a flat weighting

        Returns:
            float: sound pressure level
        """
        sound_pressure_level = self.sound.value() * self.sound._scale('DB')
        return sound_pressure_level



# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/sensors.html#light-sensor
class LightInfrared:
    def __init__(self, port, **kwargs):
        """Light Sensor Object

        Args:
            port (str): port where the sensor is connected
        """
        logging.info('CREATE SENSOR LIGHT (%s)', port)
        self.port = port
        # Connect light sensors to any sensor port
        self.light = LightSensor(port)
        # Reflected light. LED on
        self.light.mode = 'REFLECT'

    def read(self):
        """read the the reflected light intensity, as a percentage

        Returns:
            float: reflected light intensity
        """
        reflected_light_intensity = self.light.value() * self.light._scale('REFLECT')
        return reflected_light_intensity

########################################################################################################################################################################################################



class EV3Car:
    def __init__(self, actions):
        """Create the EV3 Car with its sensors and motors
        """
        #logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.car_size = 24 #cm
        self.inputs = {}
        self.outputs = {}
        self.actions_dict = actions
        self.init_robot_input_and_output()
        
    def init_robot_input_and_output(self):
        """create the input and outputs which are given to the agent
        """
        #init sensors
        inputs = {}
        #ultrasonic left/west
        sensor_pos = 'west'
        sensor = SensorUltrasonic('in1')
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
        outputs = {}
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
        __min_observation = 0
        __max_observation = 70

        observations = [0,0,0]
        observations[0] = self.inputs['west'].read()
        observations[1] = self.inputs['north'].read()
        observations[2] = self.inputs['east'].read()
        #discretize sensor values
        obs_evaluated = []
        logging.info('OBSERVATION RAW %s',str(observations))
        for obs in observations:
            if(obs < __min_observation):
                obs = __min_observation
            elif(obs > __max_observation):
                obs = __max_observation
            obs_evaluated.append(obs)
        logging.debug('OBSERVATION EVALUATED %s', str(obs_evaluated))
        return tuple(obs_evaluated)

    def action(self, action):
        """perform the given action

        Args:
            action (int): numerical representation of the action to execute
        """
        logging.info("ACTION: %s", action)
        action_params = self.actions_dict[action]
        self.outputs['tank1'].drive(action_params)