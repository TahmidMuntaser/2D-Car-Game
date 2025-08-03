import pygame
import os 
import random
from config import WIDTH, HEIGHT, FPS

class EnemyCar:
    def __init__(self, screen_width, screen_height, car_number=2):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.car_number = car_number
        self.speed = random.randint(2, 5)
        self.update_road_boundaries()
        

    # road bondary calc
    def update_road_boundaries(self):
        border_percentage = 0.1
        self.road_left_border = int(self.screen_width * border_percentage)
        self.road_right_border = int(self.screen_width * border_percentage)
        
        
        
    def move(self):
        pass
    
    
    def draw(self, screen):
        pass
