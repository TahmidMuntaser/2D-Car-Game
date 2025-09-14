import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road
from main_car import MainCar
from enemy_car import EnemyCar
from game_over import show_game_over
from initial_window import show_main_menu  # Menu screen
from score import Score
from collision import check_collision


def start_game(selected_car=3):
    # Get the actual current screen size (which might have been resized during game over)
    current_surface = pygame.display.get_surface()
    current_width = current_surface.get_width() if current_surface else WIDTH
    current_height = current_surface.get_height() if current_surface else HEIGHT

    # Ensure the screen is properly set to the current size
    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    pygame.display.set_caption("2D Car Game")

    road = Road(current_width, current_height)

    # Create car first with temporary position
    car = MainCar(0, 0, car_number=selected_car)
    
    # Now calculate proper starting position based on actual car size after initialization
    car_start_x = (current_width - car.width) // 2
    car_start_y = current_height - car.height
    
    # Set the car to the correct position
    car.set_position(car_start_x, car_start_y)
    
    enemy_car = EnemyCar(current_width, current_height)
    clock = pygame.time.Clock()
    score = Score()

    running = True
    while running:
        clock.tick(FPS)

        # Handle events
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return False  # Exit game
            elif i.type == pygame.VIDEORESIZE:
                current_width, current_height = i.size
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                road.set_size(current_width, current_height)
                car.update_screen_size(current_width, current_height)  # Update car boundaries
                enemy_car.update_screen_size(current_width, current_height)
                # Update car start position for when game over occurs
                car_start_x = (current_width - car.width) // 2
                car_start_y = current_height - car.height
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    return True  # Return to main menu

        # Handle car input
        keys = pygame.key.get_pressed()
        car.handle_input(keys)
        car.update_position()
        
        # Score update
        score.update()
        
        
        # Draw everything
        road.move()
        road.draw(screen)
        car.draw(screen)
        enemy_car.move(score.get_score())
        enemy_car.draw(screen)
        
        # Draw score text
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Score: {score.get_score()}", True, (255, 255, 255))
        
        # Background box
        box_rect = pygame.Rect(20, 15, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(screen, (25, 25, 25), box_rect, border_radius=8)
        
        # Draw text
        screen.blit(score_text, (30, 20))
        
        # Collision check 
        if check_collision(screen, car, enemy_car, draw_debug=True):
            game_over_result = show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y, score.get_score())

            if game_over_result == "retry":
                score.reset()
            elif game_over_result == "menu":
                return True
            else:
                return False

        pygame.display.flip()

    return False  # Exit game

def main():
    pygame.init()
    last_car = 3
    while True:
        # Show main menu and get selected car
        selected_car = show_main_menu(last_car)
        if selected_car is None:
            # User quit from menu
            break
        elif selected_car is False:
            # Something went wrong, but don't start game
            break
        else:
            # User selected a car, start the game
            return_to_menu = start_game(selected_car)
            if not return_to_menu:
                # User quit from game
                break
            last_car = selected_car  # Remember the last selected car
    pygame.quit()

if __name__ == "__main__":
    main()
