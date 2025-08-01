import pygame
from config import HEIGHT, WIDTH

class Road:
    def __init__(self):
        self.image = pygame.image.load("assets/road1.png")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.y1 = 0
        self.y2 = -HEIGHT
        self.speed = 5 # 5 ppf
    
    def move(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT
            
            
    def draw(self, screen): 
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))
        