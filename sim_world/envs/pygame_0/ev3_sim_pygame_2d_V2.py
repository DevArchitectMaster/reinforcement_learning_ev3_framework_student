import pygame
import math
import logging

class PyGame2D:
    def __init__(self, map_file_path, car, start_coordinates, checkpoints_list):
        """Create the Game Environment

        Args:
            map_file_path (str): path to the map image.png
            car (Car): car object that navigates through the world
            start_coordinates (tuple): start position of the car
            checkpoints_list (list): A list of checkpoints to reach (min. 2 checkpoints in list)
        """
        MAP_CHECKPOINT_RADIUS = 50
        self._map_screen_width = 1280
        self._map_screen_height = 720
        
        # pygame initalization
        pygame.init()
        self.__pygame_screen = pygame.display.set_mode((self._map_screen_width, self._map_screen_height))
        self.__pygame_clock = pygame.time.Clock()
        self.__pygame_font_info = pygame.font.SysFont("Arial", 20)
        self.__pygame_game_speed = 60
        self.__pygame_mode = 0
        
        # map data 
        self._map = pygame.image.load(map_file_path)
        self._map_checkpoint_list = checkpoints_list
        self._map_current_checkpoint = 0
        self._map_checkpoint_radius = MAP_CHECKPOINT_RADIUS
        self._map_check_flag = False
        self._map_goal_reached = False

        # car data  
        self._car = car
        self._car_energy_max = car.energy_max  
        self._car_start_pos = start_coordinates
        self._car.set_start_position(self._car_start_pos)
        self._car.set_map(self._map)
        self._car.init_robot_input_and_output() # update map for sensors
    
    def reset(self):
        self._map_current_checkpoint = 0
        self._map_check_flag = False
        self._map_goal_reached = False
        self._car.set_start_position(self._car_start_pos)

    def _check_collision(self):
        """check if the Car hitbox touches obstacle pixels
        """
        for __p in self._car._four_points:
            if((__p[0] >= 0) and (__p[0] <= (self._map.get_size())[0]) and (__p[1] >= 0) and (__p[1] <= (self._map.get_size())[1])):
                if(self._map.get_at((int(__p[0]), int(__p[1]))) == (255, 255, 255, 255)):
                    self._car._is_alive = False
                    self._car.energy = 0
                    self._car._is_crashed = True
                    break
   
    def _check_checkpoint(self):
        """check if the Car touches a checkpoint, touched checkpoints will be removed
        """
        __p = self._map_checkpoint_list[self._map_current_checkpoint]
        __dist = self._get_distance(__p, self._car._center)
        if(__dist < self._map_checkpoint_radius):
            self._map_current_checkpoint += 1
            self._map_check_flag = True

            if(self._car.energy > self._car_energy_max):
                self.energy=self._car_energy_max
            if(self._map_current_checkpoint >= len(self._map_checkpoint_list)):
                self._map_current_checkpoint = 0
                self._map_goal_reached = True
            else:
                self._map_goal_reached = False

    def _draw(self):
        """draw the objects on the screen
        """
        self.__pygame_screen.blit(self._car._rotate_surface, self._car._pos)

    def _draw_collision_hitbox(self):
        """draw the Car hitbox on the screen
        """
        for __i in range(4):
            __x = int(self._car._four_points[__i][0])
            __y = int(self._car._four_points[__i][1])
            pygame.draw.circle(self.__pygame_screen, (255, 0, 0, 255), (__x, __y), 5)

    def _draw_radar(self):
        """draw the radar objects on the screen
        """
        for __radar_beams in self._car._radars_for_draw:
            __poly_coords = [self._car._center] + __radar_beams
            pygame.draw.polygon(self.__pygame_screen, (0, 155, 155), __poly_coords)
            
        for __r in self._car._radars:
            __pos, __dist = __r
            pygame.draw.line(self.__pygame_screen, (0, 255, 0), self._car._center, __pos, 1)
            pygame.draw.circle(self.__pygame_screen, (0, 255, 0), __pos, 5)

    def action(self, action):
        """perform the given action

        Args:
            action (int): numerical representation of the action
        """
        logging.debug("ACTION: %s",action)
        # execute desired car action, calc new car coordinates
        self._car.action(action)
        
        # update the car on the screen
        self._car._rotate_surface = self._rot_center(self._car._surface, self._car._angle)

        # check for collisions, rewards in environment
        self._check_collision()
        self._check_checkpoint()

        # clear measurements and drawing lists for radars
        self._car._radars.clear()
        self._car._radars_for_draw.clear()

        # set speed to 0 (Markov Decision Process)
        self._car._speed=0

    def evaluate(self):
        """evaluate the rewards

        Returns:
            int: reward value given the current state/action
        """
        # reward for distance from goal (= last checkpoint)
        if self._get_distance(self._car._center, self._map_checkpoint_list[-1]) != 0:
            __reward = 0.1*(self._get_distance(self._car_start_pos, self._map_checkpoint_list[-1]) / self._get_distance(self._car._center, self._map_checkpoint_list[-1]))
        else:
            __reward = 0

        if(self._map_check_flag):
            self._map_check_flag = False
            __reward += 1000
            #print("Checkpoint num:", self.car.current_check , "/", len(check_point))

        if(self._car._is_crashed == True):
            __reward+=-100
        return __reward
        
    def is_done(self):
        """check if the Car is still alive
            all checkpoints reached or obstacle returns False

        Returns:
           bool: is (episode) done aka. end of episode
        """
        if((not self._car._is_alive) or self._map_goal_reached):
            self._map_current_checkpoint = 0
            return True
        return False

    def observe(self):
        """#get the env observation
        """
        self._car.observe()
        return self._car.observation

    def _draw_info_text(self, info_str, text_center):
        """draw the info_str to the text_center coordinates

        Args:
            info_str (str): text to draw
            text_center (tuple): (x,y) where to draw
        """
        __text = self.__pygame_font_info.render(info_str, True, (255, 0, 0))
        __text_rect = __text.get_rect()
        __text_rect.center = text_center
        self.__pygame_screen.blit(__text, __text_rect)

    def view(self):
        """show the current environment and its Car
        """
        # draw game
        for __event in pygame.event.get():
            if(__event.type == pygame.QUIT):
                done = True
            elif(__event.type == pygame.KEYDOWN):
                if(__event.key == pygame.K_m):
                    self.__pygame_mode += 1
                    self.__pygame_mode = self.__pygame_mode % 3
                if(__event.key == pygame.K_ESCAPE):
                    #pygame.QUIT
                    logging.info("SIMULATION KILLED BY USER")
                    exit()
                    
        self.__pygame_screen.blit(self._car._map, (0, 0))

        if(self.__pygame_mode == 1):
            self.__pygame_screen.fill((0, 0, 0))

        for __checkp in self._map_checkpoint_list:
            pygame.draw.circle(self.__pygame_screen, (55, 55, 55), __checkp, self._map_checkpoint_radius, 1)
        
        # highlight the current checkpoint to reach
        pygame.draw.circle(self.__pygame_screen, (255, 255, 0), self._map_checkpoint_list[self._map_current_checkpoint], self._map_checkpoint_radius, 3)

        self._draw_collision_hitbox()
        self._draw_radar()
        self._draw()

        # print radar values on screen
        __info_str = 'Observation: '
        for __i, __r in enumerate(self._car.observation):
             __info_str += str(__r) + ', '
        __text_center = (self._map_screen_width / 4, 40)
        self._draw_info_text(__info_str,__text_center)

       
        __info_str = "Action:" + str(self._car._last_action)
        __text_center = (self._map_screen_width / 4, 70)
        self._draw_info_text(__info_str,__text_center)
       

        __info_str = "ENERGY:" + str(self._car.energy) + "   Angle:" + str(self._car._angle) + " Speed:" + str(self._car._speed)
        __text_center = (self._map_screen_width / 4, 10)
        self._draw_info_text(__info_str,__text_center)

        
        __info_str = "Press 'm' to change view mode"
        __text_center = (self._map_screen_width / 2, 10)
        self._draw_info_text(__info_str,__text_center)

        __info_str = "Press 'ESC' to kill the simulation"
        __text_center = (self._map_screen_width / 2, 30)
        self._draw_info_text(__info_str,__text_center)

        pygame.display.flip()
        self.__pygame_clock.tick(self.__pygame_game_speed)

    def _get_distance(self, p1, p2):
        """calculate the euclidain distance of two points

        Args:
            p1 (list): coordinates of point 1
            p2 (list): coordinates of point 2

        Returns:
            float: distance between p1 and p2
        """
        return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))

    def _rot_center(self, image, angle):
        """rotate the given image by the given angle

        Args:
            image (image): image object to rotate
            angle (int): angle for rotation

        Returns:
        image: rotated image object
        """
        __orig_rect = image.get_rect()
        __rot_image = pygame.transform.rotate(image, angle)
        __rot_rect = __orig_rect.copy()
        __rot_rect.center = __rot_image.get_rect().center
        __rot_image = __rot_image.subsurface(__rot_rect).copy()
        return __rot_image