import pygame
from config import WIDTH, HEIGHT, FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Game")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    screen.fill((50, 50, 50)) 
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            
            
    pygame.display.flip()
pygame.quit()