import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road
from main_car import MainCar
from enemy_car import EnemyCar
from game_over import show_game_over
from initial_window import show_main_menu  # Menu screen

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
    car_start_y = current_height - car.height - 10  # 10px margin from bottom
    
    # Set the car to the correct position
    car.set_position(car_start_x, car_start_y)
    
    enemy_car = EnemyCar(current_width, current_height)
    clock = pygame.time.Clock()

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
                car_start_y = current_height - car.height - 10
            elif i.type == pygame.KEYDOWN:
                # Change car model with number keys
                if i.key == pygame.K_1:
                    car.change_car(3)
                elif i.key == pygame.K_2:
                    car.change_car(4)
                elif i.key == pygame.K_3:
                    car.change_car(5)
                elif i.key == pygame.K_ESCAPE:
                    return True  # Return to main menu

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

        # Check for collisions
        inflate_w = int(car.width * 0.45)
        inflate_h = int(car.height * 0.05)
        main_rect = car.get_rect().inflate(-inflate_w, -inflate_h)

        inflate_w_enemy = int(enemy_car.width * 0.45)
        inflate_h_enemy = int(enemy_car.height * 0.05)
        enemy_rect = enemy_car.get_rect().inflate(-inflate_w_enemy, -inflate_h_enemy)

        # pygame.draw.rect(screen, (255, 0, 0), main_rect, 2)
        # pygame.draw.rect(screen, (0, 255, 0), enemy_rect, 2)

        if main_rect.colliderect(enemy_rect):
            # print("💥 Collision detected!")
            game_over_result = show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y)
            if not game_over_result:
                return True  # Return to main menu

        pygame.display.flip()

    return False  # Exit game

def main():
    pygame.init()
    while True:
        # Show main menu and get selected car
        selected_car = show_main_menu()
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
    pygame.quit()

if __name__ == "__main__":
    main()
