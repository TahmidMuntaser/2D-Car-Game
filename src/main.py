import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  
road = Road(WIDTH, HEIGHT)
pygame.display.set_caption("2D Car Game")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    
    road.move()
    road.draw(screen)

    # screen.fill((0, 0, 0)) 
    pygame.draw.rect(screen, (100, 100, 150), (0, 0, WIDTH, HEIGHT), 5)
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = i.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            road.set_size(WIDTH, HEIGHT)
            
    pygame.display.flip()
pygame.quit()