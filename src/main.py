import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road
from main_car import MainCar
from enemy_car import EnemyCar

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  
road = Road(WIDTH, HEIGHT)
pygame.display.set_caption("2D Car Game")

# Create car at bottom center, accounting for road borders
road_border = road.get_road_borders()
car_start_x = (pygame.display.get_surface().get_width() -MainCar.get_default_car_width()) // 2 
height=pygame.display.get_surface().get_height() if pygame.display.get_surface() else HEIGHT
car_start_y = height - MainCar.get_default_car_height() - 10  # 10px margin from bottom
car = MainCar(car_start_x, car_start_y, car_number=3)
enemy_car = EnemyCar(WIDTH, HEIGHT)
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    
    # Handle events
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = i.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            road.set_size(WIDTH, HEIGHT)
            car.update_screen_size(WIDTH, HEIGHT)  # Update car boundaries
            enemy_car.update_screen_size(WIDTH, HEIGHT)

        
        elif i.type == pygame.KEYDOWN:
            # Change car model with number keys
            if i.key == pygame.K_3:
                car.change_car(3)
            elif i.key == pygame.K_4:
                car.change_car(4)
            elif i.key == pygame.K_5:
                car.change_car(5)
    
    # Handle car input
    keys = pygame.key.get_pressed()
    car.handle_input(keys)
    car.update_position()
    
    # Draw everything
    road.move()
    road.draw(screen)
    car.draw(screen)
    enemy_car.move()
    enemy_car.draw(screen)

    # Draw border
    pygame.draw.rect(screen, (100, 100, 150), (0, 0, WIDTH, HEIGHT), 5)
            
    pygame.display.flip()
pygame.quit()