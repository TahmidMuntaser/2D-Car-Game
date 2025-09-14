import pygame
import os 
import random
from config import WIDTH, HEIGHT, FPS

class EnemyCar:
    def __init__(self, screen_width, screen_height, car_number=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.car_number = car_number
        self.speed = random.randint(2, 5) 
        # self.width = 60   
        # self.height = 100
        self.update_road_boundaries()
        self.load_car_image()
        self.spawn()


     

    # road bondary calc
    def update_road_boundaries(self):
        border_percentage = 0.1
        self.road_left_border = int(self.screen_width * border_percentage)
        self.road_right_border = int(self.screen_width * border_percentage)
        
        
    # load car img
    def load_car_image(self):
        try:
            # load img
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(current_dir, "assets", f"car{self.car_number}.png")
            original = pygame.image.load(path).convert_alpha()
            
            # rm white bg 
            cleaned_surface = pygame.Surface(original.get_size(), pygame.SRCALPHA)
            for x in range(original.get_width()):
                for y in range(original.get_height()):
                    pixel = original.get_at((x, y))
                    r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3] if len(pixel) > 3 else 255
                    is_background = (
                        r >= 255 and g >= 255 and b >= 255 or
                        r > 240 and g > 240 and b > 240 or
                        (r > 220 and g > 220 and b > 220 and abs(r-g) < 20 and abs(g-b) < 20) or
                        a < 10
                    )
                    if not is_background:
                        cleaned_surface.set_at((x, y), pixel)
            
            # calc car size
            road_width = self.screen_width - (2 * int(self.screen_width * 0.1)) 
            car_width = int(road_width * 0.25)
            car_width = max(60, min(car_width, 250))
            car_height = int(car_width * 1.3)
            
            self.image = pygame.transform.scale(cleaned_surface, (car_width, car_height))
            self.image = pygame.transform.rotate(self.image, 180)
            self.width = car_width
            self.height = car_height
            # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
        except Exception as e:
            self.image = None
            self.width = 60
            self.height = 100
            self.fallback_color = (0, 255, 0)
            
    def update_speed(self, score):
       
        if score < 10:
            self.speed = random.randint(4, 6)
        elif score < 20:
            self.speed = random.randint(5, 7)
        elif score < 35:
            self.speed = random.randint(7, 9)
        else:
            self.speed = random.randint(9, 12)
        
    
    def spawn(self, score=0):
        road_width = self.screen_width - (self.road_left_border + self.road_right_border)
        self.x = random.randint(self.road_left_border, self.road_left_border + road_width - self.width)
        self.y = -self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # set speed based on score
        self.update_speed(score)

        
        
        
    def move(self, score=0):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > self.screen_height:
            self.spawn(score) 
        
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.fallback_color, self.rect)
            
            
            
    # upd screen size 
    def update_screen_size(self, width, height):
        # old car position 
        old_center_x_ratio = (self.x + self.width // 2 - self.road_left_border) / (
            self.screen_width - self.road_left_border - self.road_right_border)
        distance_from_top = self.y
        
        # upd new screen size 
        self.screen_width = width
        self.screen_height = height
        self.update_road_boundaries()
        self.load_car_image()
        
        # recalculate position
        new_road_width = self.screen_width - (self.road_left_border + self.road_right_border)
        self.x = int(self.road_left_border + old_center_x_ratio * new_road_width - self.width // 2)
        self.y = distance_from_top
        
        # boundary check 
        self.x = max(self.road_left_border, min(self.x, self.screen_width - self.road_right_border - self.width))
        # collision rectangle 
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def get_rect(self):
        return self.rect


