import pygame
from config import WIDTH, HEIGHT

def show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))

    while True:
        screen.fill((0, 0, 0))  
        road.draw(screen)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
        
        pygame.display.flip()