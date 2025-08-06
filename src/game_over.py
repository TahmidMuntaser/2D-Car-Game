import pygame
from config import WIDTH, HEIGHT

def show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    again = small_font.render("Try Again", True, (255, 255, 255))
    quit_text = small_font.render("Quit", True, (255, 255, 255))
    
    # rectangle for buttons
    again_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
    quit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50)

    while True:
        screen.fill((0, 0, 0))  
        road.draw(screen)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
        
        # draw rectengles 
        pygame.draw.rect(screen, (0, 128, 0), again_rect)
        pygame.draw.rect(screen, (128, 0, 0), quit_rect)

        # draw text on rectangles
        screen.blit(again, (again_rect.x + 50, again_rect.y + 10))
        screen.blit(quit_text, (quit_rect.x + 70, quit_rect.y + 10))
        
        pygame.display.flip()