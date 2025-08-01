import pygame
from config import HEIGHT, WIDTH

class Road:
    def __init__(self, width , height):
        self.original_image = pygame.image.load("assets/road1.png")
        self.set_size(width, height)
        self.y1 = 0
        self.y2 = -height
        self.speed = 5 # 5 ppf
        
    def set_size(self, width , height):
        self.width  = width
        self.height = height
        self.image = pygame.transform.scale(self.original_image, (width, height)) 
        self.y1 = 0
        self.y2 = -height

    def move(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        if self.y1 >= self.height:
            self.y1 = -self.height
        if self.y2 >= self.height:
            self.y2 = -self.height
            
            
    def draw(self, screen): 
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))
        