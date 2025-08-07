import pygame
from config import WIDTH, HEIGHT, FPS
from road import Road
from main_car import MainCar
from enemy_car import EnemyCar
from game_over import show_game_over
from initial_window import show_main_menu

def start_game(selected_car=3):
    """Start the main game with the selected car"""
    # Don't call pygame.init() again as it's already initialized by the menu
    current_width, current_height = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH,pygame.display.get_surface().get_height() if pygame.display.get_surface() else HEIGHT
    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)  
    road = Road(current_width, current_height)
    pygame.display.set_caption("2D Car Game")

    # Create car at bottom center, accounting for road borders
    road_border = road.get_road_borders()
    car_start_x = (current_width - MainCar.get_default_car_width()) // 2
    height = current_height
    car_start_y = height - MainCar.get_default_car_height() - 10  # 10px margin from bottom
    car = MainCar(car_start_x, car_start_y, car_number=selected_car)
    enemy_car = EnemyCar(current_width, current_height)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        
        # Handle events
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.VIDEORESIZE:
                current_width, current_height = i.size
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                road.set_size(current_width, current_height)
                car.update_screen_size(current_width, current_height)  # Update car boundaries
                enemy_car.update_screen_size(current_width, current_height)
            elif i.type == pygame.KEYDOWN:
                # Change car model with number keys
                if i.key == pygame.K_1:
                    car.change_car(3)
                elif i.key == pygame.K_2:
                    car.change_car(4)
                elif i.key == pygame.K_3:
                    car.change_car(5)
                elif i.key == pygame.K_ESCAPE:
                    # Return to main menu
                    running = False
                    return True  # Indicate we want to return to menu
        
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

        if main_rect.colliderect(enemy_rect):
            # Show game over screen and check if player wants to continue
            game_over_result = show_game_over(screen, road, car, enemy_car, car_start_x, car_start_y)
            if not game_over_result:
                running = False
                return True  # Return to main menu

        # Draw border
        pygame.draw.rect(screen, (100, 100, 150), (0, 0, current_width, current_height), 5)
                
        pygame.display.flip()
    
    return False  # Exit completely

def main():
    """Main function that handles the game loop and menu"""
    while True:
        # Show main menu and get selected car
        selected_car = show_main_menu()
        
        if selected_car is None:
            # User quit from menu
            break
        
        # Start the game with selected car
        return_to_menu = start_game(selected_car)
        
        if not return_to_menu:
            # User quit from game
            break
    
    pygame.quit()

if __name__ == "__main__":
    main()