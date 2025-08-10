import pygame
from config import WIDTH, HEIGHT

def show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    bg_color = (30, 30, 50)         # Dark blue-gray
    button_color = (70, 130, 180)   # Steel blue
    button_hover_color = (100, 149, 237)  # Cornflower blue
    text_color = (255, 255, 255)    # White
    
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    again = small_font.render("Try Again", True, text_color)
    quit_text = small_font.render("Quit", True, text_color)
    
    # again_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50)
    # quit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50)

    while True:
        width, height = screen.get_size()
        # rectangle for buttons
        again_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
        quit_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)
        
        screen.fill(bg_color)  
        
        # road.draw(screen)
        line_color = (100, 100, 120)
        for i in range(0, height + 50, 50):
            y = (i + pygame.time.get_ticks() // 10) % (height + 50)
            pygame.draw.rect(screen, line_color, (width // 2 - 5, y, 10, 30))
        
        screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2 - game_over_text.get_height()//2-60)) #gameover
        
        # draw rectengles 
        
        mouse_pos = pygame.mouse.get_pos()
        # Try Again button with hover
        if again_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, again_rect)
        else:
            pygame.draw.rect(screen, button_color, again_rect)
        # Add white border
        pygame.draw.rect(screen, (255, 255, 255), again_rect, 3)

        # Quit button with hover
        if quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, quit_rect)
        else:
            pygame.draw.rect(screen, button_color, quit_rect)
        # Add white border
        pygame.draw.rect(screen, (255, 255, 255), quit_rect, 3)
        

        # draw text on rectangles
        screen.blit(again, again.get_rect(center=again_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
                
        pygame.display.flip()
        
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:   
                pygame.quit()
                exit()
                
            elif i.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(i.size, pygame.RESIZABLE)
                road.set_size(i.size[0], i.size[1])
                car.update_screen_size(i.size[0], i.size[1])
                enemy_car.update_screen_size(i.size[0], i.size[1])
                
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if again_rect.collidepoint(i.pos):
                    enemy_car.spawn()
                    # car position 
                    width, height = screen.get_size()
                    car_start_x = (width - car.width)//2
                    car_start_y = height - car.height - 10
                    car.set_position(car_start_x, car_start_y)
                    return True
                
                elif quit_rect.collidepoint(i.pos):
                    pygame.quit()
                    exit()
                
