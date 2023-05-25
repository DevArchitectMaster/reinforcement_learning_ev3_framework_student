import pygame
import math
import numpy as np
import logging

logger = logging.getLogger(__name__ + '.SimCar')

class _BlueprintDistanceMeasure(): ### Additional function only for the simulation environment ###
    def __init__(self, car, radar_beams, radar_detect_angle, beam_degree, max_len, env_map):
        #TODO remove dict
        __positions_dict = {
            'north' : 0,
            'north-east' : 45,
            'east' : 90,
            'south-east' : 135,
            'south' : 180,
            'south-west' : 225,
            'west' : 270,
            'north-west' : 315
        }
        self.radar_beams = radar_beams
        self.radar_detect_angle = radar_detect_angle
        self.degree = __positions_dict[beam_degree]
        self.max_len=max_len * car.resize_factor
        self.car = car
        self.env_map = env_map   

    def check_beam(self, degree):
        """get the length of a single degree

        Args:
            degree (int): degree of the beam

        Returns:
            float: x, y, distance
        """
        __len = 0
        __x = int(self.car._center[0] + math.cos(math.radians(360 - (self.car._angle + degree))) * __len)
        __y = int(self.car._center[1] + math.sin(math.radians(360 - (self.car._angle + degree))) * __len)

        while __len < self.max_len: #TODO separate check if coords in map
            __len = __len + 1
            __x = int(self.car._center[0] + math.cos(math.radians(360 - (self.car._angle + degree))) * __len)
            __y = int(self.car._center[1] + math.sin(math.radians(360 - (self.car._angle + degree))) * __len)
            
            if((__x < 0) or (__x>= (self.env_map.get_size())[0]) or  (__y < 0) or (__y>= (self.env_map.get_size())[1])):
                break
            elif(self.env_map.get_at((__x, __y)) == (255, 255, 255, 255)):
                break
        __dist = int(math.sqrt(math.pow(__x - self.car._center[0], 2) + math.pow(__y - self.car._center[1], 2)))
        return __x,__y, __dist

    def get_distance(self):
        """get the distance from the current position to the wall
        """
        __beam_angle = self.radar_detect_angle/(self.radar_beams - 1)

        __beam_list = []
        __dist_list = []
        for __beam in range(self.radar_beams):
            __beam_degree = self.degree - self.radar_detect_angle / 2 + __beam * __beam_angle
            #TODO: noch benötigt?
            #print(beam, beam_angle, beam_degree)
            #specific angles per beam
            #if beam==0 or beam==self.radar_beams-1:
            #    max_len = self.max_len
            #else: 
            #    max_len = self.max_len
            __x, __y, __dist = self.check_beam(__beam_degree)
            __beam_list.append((__x,__y))
            __dist_list.append(__dist)

        __beams = np.array(__beam_list)
        __min_idx = np.array(__dist_list).argmin()
        __x = __beams[__min_idx,0]
        __y = __beams[__min_idx,1]
        __dist = int(math.sqrt(math.pow(__x - self.car._center[0], 2) + math.pow(__y - self.car._center[1], 2)))

        if(__dist > self.max_len):
            __dist=self.max_len
        self.car._radars.append([(__x, __y), __dist])
        self.car._radars_for_draw.append( __beam_list)

        return __dist

class MotorTank:
    def __init__(self, car, **kwargs):
        """2 Motors driving like a tank

        Args:
            agent (Car): Owner of the MotorTank
            kwargs (dict): additonal arguments
        """
        logger.debug('CREATE MOTOR TANK')
        self.agent = car
        self.param_dict = {
            'speed' : self.agent.add_speed,
            'angle' : self.agent.add_angle,
            'energy' : self.agent.add_energy
        }
        self.variance = (kwargs['variance'])

    def drive(self, action_params):
        """drive the tank given the params in dict

        Args:
            action_params (dict):  {'speed':int} or {'angle':int}
        """
        logger.debug('MOTOR TANK DRIVE \'%s\'', action_params)
        #TODO CHECK
        for __param in action_params.items():
            __set_value = __param[1]
            #add variance to set speed and angle
            if(__param[0] == 'speed' or __param[0] == 'angle'):
                __set_value = __set_value + np.random.uniform(self.variance* - 1, self.variance)
            self.param_dict[__param[0]](__set_value)

class SensorUltrasonic(_BlueprintDistanceMeasure):
    def __init__(self, car, position, max_cm,  **kwargs):
        """Ultrasonic Sensor Object

        Args:
            car (Car): Owner of the sensor
            position (str): position of the sensor (north, west, south, east)
            max_cm (int): max range to measure in
            kwargs (dict): additonal arguments
        """
        logger.debug('CREATE SENSOR ULTRASONIC')
        _BlueprintDistanceMeasure.__init__(self, car, radar_beams = 5, radar_detect_angle = 30, beam_degree = position, max_len = max_cm, env_map = kwargs['env_map'])
        self.variance = (kwargs['variance'] / 100) * max_cm

    def read(self):
        """read the distance to the next object/wall

        Returns:
           float: distance value
        """
        __distance = self.get_distance()
        __variance_err = np.random.uniform(self.variance * -1, self.variance)
        __distance += __variance_err
        logger.debug('ULTRASONIC SENSOR READ \'%s\'', __distance)
        return __distance

class SensorInfrared(_BlueprintDistanceMeasure):
    def __init__(self, car, position, max_cm,  **kwargs):
        """Infrared Sensor Object

        Args:
            agent (Car): Owner of the sensor
            position (str): position of the sensor (north, west, south, east)
            max_cm (int): max range to measure in
            kwargs (dict): additonal arguments
        """
        logger.debug('CREATE SENSOR INFRARED')
        _BlueprintDistanceMeasure.__init__(self, car, radar_beams = 5, radar_detect_angle = 30, beam_degree = position, max_len = max_cm, env_map = kwargs['env_map'])
        self.variance = (kwargs['variance'] / 100) * max_cm

    def read(self):
        """read the distance to the next object/wall

        Returns:
           float: distance value
        """
        __distance = self.get_distance()
        __variance_err = np.random.uniform(self.variance * -1, self.variance)
        __distance+=__variance_err
        logger.debug('INFRARED SENSOR READ \'%s\'', __distance)
        return __distance

class SimCar:
    def __init__(self, actions_dict, car_file, energy, energy_max):
        """SimCar object

        Args:
            car_file (str): path to car image
            energy (int): energy value at start
            energy_max (int): maximum energy value
        """
        self._map = None # init map and sensors by env

        #TODO: Car Eigenschaften rauslösen
        self.car_X = 50
        self.car_Y = 50
        self.car_size = 24 # cm
        self.resize_factor = self.car_X / self.car_size

        self._surface = pygame.image.load(car_file)
        self._surface = pygame.transform.scale(self._surface, (self.car_X, self.car_Y))
        self._rotate_surface = self._surface
        
        self._angle = 0
        self._speed = 0
        self._is_alive = True
        self._is_crashed = False
        
        # for drawing the distance beams
        self._radars = []
        self._radars_for_draw = []

        self.energy = energy
        self.energy_max = energy_max
        
        self.inputs = {}
        self.__min_observation = 0
        self.__max_observation_Ultrasonic = 100
        self.__max_observation_Infrared = 100
        self.__max_observation_max = max(self.__max_observation_Ultrasonic, self.__max_observation_Infrared)
        self.observation_space = ([self.__min_observation, self.__min_observation, self.__min_observation], [self.__max_observation_Ultrasonic, self.__max_observation_Infrared, self.__max_observation_Ultrasonic])
        self.observation = []

        self.outputs = {}
        self.actions_dict = actions_dict
        self.action_space = len(self.actions_dict.keys())
        self._last_action = 0

    def init_robot_input_and_output(self):
        """create the input and outputs which are given to the agent
        """
        sensor_variance = 2

        # init sensors
        inputs = {}

        # ultrasonic left/west
        sensor_pos = 'west'
        sensor = SensorUltrasonic(self, position = sensor_pos, max_cm = self.__max_observation_Ultrasonic, variance = sensor_variance, env_map = self._map)
        inputs.update({sensor_pos : sensor})
        
        # ultrasonic right/east
        sensor_pos = 'east'
        sensor = SensorUltrasonic(self, position = sensor_pos, max_cm = self.__max_observation_Ultrasonic, variance = sensor_variance, env_map = self._map)
        inputs.update({sensor_pos : sensor})

        # infrared up/north
        sensor_pos = 'north'
        sensor = SensorInfrared(self, position = sensor_pos, max_cm = self.__max_observation_Infrared, variance = sensor_variance, env_map = self._map)
        inputs.update({sensor_pos : sensor})

        self.inputs = inputs

        # init motors
        outputs={}
        
        motor = MotorTank(self, variance=sensor_variance)
        # use the group name to identify the motors in the actions later
        outputs.update({'tank1' : motor})

        self.outputs = outputs

    def observe(self):
        """read the sensors

        Returns:
            list: current measurement / observation of the Car
        """
        observations = [0,0,0]
        observations[0] = self.inputs['west'].read()
        observations[1] = self.inputs['north'].read()
        observations[2] = self.inputs['east'].read()
        
        obs_evaluated = []
        logger.debug('OBSERVATION RAW \'%s\'', str(observations))
        for obs in observations:
            if(obs < self.__min_observation):
                obs = self.__min_observation
            elif(obs > self.__max_observation_max):
                obs = self.__max_observation_max
            #TODO: convert from discrete values to continuous values
            obs = int(obs)
            obs_evaluated.append(obs)
        logger.debug('OBSERVATION EVALUATED \'%s\'', str(obs_evaluated))
        self.observation =  tuple(obs_evaluated)

    def action(self, action):
        """execute the given action

        Args:
            action (int): numerical representation of the action to execute

        Returns:
            int: executed action
        """
        action_params = self.actions_dict[action]
        self.outputs['tank1'].drive(action_params) 
        self._last_action = action
        self._update_status()
        logger.debug('ACTION SELECTED: \'%s\'', action)
        return action
    
    ################################################################
    ### Additional functions only for the simulation environment ###
    ################################################################

    def set_map(self, map):
        """set the map for ev3-car

        Args:
            map (image): map image file
        """
        self._map = map

    def set_start_position(self, position):
        """set the position of the robot

        Args:
            position (tuple): coordinates (current position) of the robot
        """
        self._pos = list(position)
        self._center = [self._pos[0] + self.car_X / 2, self._pos[1] + self.car_Y / 2]

    def add_speed(self, speed):
        """add speed to the current speed value

        Args:
            speed (int): value to add
        """
        self._speed += speed

    def add_angle(self, angle):
        """add angle degrees to the current angle value

        Args:
            angle (int): value to add
        """
        self._angle += angle
        self._angle = round(self._angle%360, 2) #roundend degrees
        
    def add_energy(self, energy):
        """add energy to the current energy value

        Args:
            energy (int): energy to add
        """
        self.energy += energy   
   
    def _update_status(self):
        """update the environment after each action/step
        """
        self._pos[0] += math.cos(math.radians(360 - self._angle)) * self._speed
     
        #self.distance += self.speed
        #self.time_spent += 1
        self._pos[1] += math.sin(math.radians(360 - self._angle)) * self._speed
  
        # calculate 4 collision points
        self._center = [int(self._pos[0]) + self.car_X / 2, int(self._pos[1]) + self.car_Y / 2]
        len = 20
        left_top = [self._center[0] + math.cos(math.radians(360 - (self._angle + 30))) * len, self._center[1] + math.sin(math.radians(360 - (self._angle + 30))) * len]
        right_top = [self._center[0] + math.cos(math.radians(360 - (self._angle + 150))) * len, self._center[1] + math.sin(math.radians(360 - (self._angle + 150))) * len]
        left_bottom = [self._center[0] + math.cos(math.radians(360 - (self._angle + 210))) * len, self._center[1] + math.sin(math.radians(360 - (self._angle + 210))) * len]
        right_bottom = [self._center[0] + math.cos(math.radians(360 - (self._angle + 330))) * len, self._center[1] + math.sin(math.radians(360 - (self._angle + 330))) * len]
        self._four_points = [left_top, right_top, left_bottom, right_bottom]
        
        if(self.energy <=0):
            #print("NO ENERGY")
            self._is_alive = False

    def reset(self):
        """reset the car status
        """
        self.energy = self.energy_max
        self._angle = 0
        self._speed = 0
        self._is_alive = True
        self._is_crashed = False
        self._last_action = 0