import pygame

def check_collision(screen, car, enemy_car, draw_debug=False):
    
    # create car masks
    car_mask = pygame.mask.from_surface(car.image)
    enemy_mask = pygame.mask.from_surface(enemy_car.image)
    
    # get rects 
    car_rect = car.image.get_rect(topleft=(car.x, car.y))
    enemy_rect = enemy_car.image.get_rect(topleft=(enemy_car.x, enemy_car.y))
    
    offset = (enemy_rect.x - car_rect.x, enemy_rect.y - car_rect.y)
    
    # if draw_debug:
    #     car_outline = car_mask.outline()
    #     enemy_outline = enemy_mask.outline()

        
    #     car_outline = [(p[0] + car_rect.x, p[1] + car_rect.y) for p in car_outline]
    #     enemy_outline = [(p[0] + enemy_rect.x, p[1] + enemy_rect.y) for p in enemy_outline]

    #     if len(car_outline) > 2:
    #         pygame.draw.polygon(screen, (255, 0, 0), car_outline, 2)
    #     if len(enemy_outline) > 2:
    #         pygame.draw.polygon(screen, (0, 255, 0), enemy_outline, 2)
    
    # Actual collision check      
    return car_mask.overlap(enemy_mask, offset) is not None