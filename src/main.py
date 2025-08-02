import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road
from main_car import MainCar

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  
road = Road(WIDTH, HEIGHT)
pygame.display.set_caption("2D Car Game")

# Create car at bottom center, accounting for road borders
road_border = road.get_road_borders()
car_start_x = WIDTH // 2 - 40  # Will be adjusted by car's responsive sizing
car_start_y = HEIGHT - 150
car = MainCar(car_start_x, car_start_y, car_number=1)
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
    
    # Handle car input
    keys = pygame.key.get_pressed()
    car.handle_input(keys)
    car.update_position()
    
    # Draw everything
    road.move()
    road.draw(screen)
    
    # Draw car on top of road
    car.draw(screen)

    # Draw border
    pygame.draw.rect(screen, (100, 100, 150), (0, 0, WIDTH, HEIGHT), 5)
            
    pygame.display.flip()
pygame.quit()