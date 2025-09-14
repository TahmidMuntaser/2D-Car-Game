import pygame

def check_collision(screen, car, enemy_car, draw_debug=False):
    
    # Create masks
    car_mask = pygame.mask.from_surface(car.image)
    enemy_mask = pygame.mask.from_surface(enemy_car.image)
    
    # Calculate the offset
    offset = (int(enemy_car.x - car.x), int(enemy_car.y - car.y))
    
    # if draw_debug:
    #     # Convert each mask to a visible surface to help with debugging
    #     car_mask_surface = car_mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    #     enemy_mask_surface = enemy_mask.to_surface(setcolor=(0, 255, 0, 255), unsetcolor=(0, 0, 0, 0))
        
    #     # Set black as transparent so only the mask shows
    #     car_mask_surface.set_colorkey((0, 0, 0))
    #     enemy_mask_surface.set_colorkey((0, 0, 0))
        
    #     # Blit the mask surfaces using the object's x, y positions
    #     screen.blit(car_mask_surface, (car.x, car.y))
    #     screen.blit(enemy_mask_surface, (enemy_car.x, enemy_car.y))
    
    
    # Use mask overlap to detect collision with the calculated offset
    return car_mask.overlap(enemy_mask, offset) is not None 