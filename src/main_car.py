import pygame
import os
from config import WIDTH, HEIGHT

class MainCar:
    """Main player car class with image loading and movement controls"""
    
    def __init__(self, x, y, car_number=5):
        self.x, self.y, self.car_number, self.speed = x, y, car_number, 5
        self.screen_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH
        self.screen_height = pygame.display.get_surface().get_height() if pygame.display.get_surface() else HEIGHT

        # Calculate responsive road boundaries based on screen width
        self.update_road_boundaries()
        
        # Load car image
        self.load_car_image()
        
        # Create collision rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_road_boundaries(self):
        b = int(self.screen_width * 0.1)
        self.road_left_border = self.road_right_border = b

    def _car_size(self):
        road_w = self.screen_width - 2 * int(self.screen_width * 0.1)
        w = max(60, min(int(road_w * 0.25), 250))
        return w, int(w * 1.3)

    def load_car_image(self):
        try:
            # Get the path to the assets folder
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            assets_path = os.path.join(current_dir, "assets", f"car{self.car_number}.png")
            
            # Load the original image
            original = pygame.image.load(assets_path).convert_alpha()
                        
            # Try multiple methods to remove background
            # Method 1: Aggressive pixel-by-pixel removal
            cleaned_surface = pygame.Surface(original.get_size(), pygame.SRCALPHA)
            cleaned_surface.fill((0, 0, 0, 0))  # Fill with transparent
            for x in range(original.get_width()):
                for y in range(original.get_height()):
                    pixel = original.get_at((x, y))
                    r, g, b, a = pixel[0], pixel[1], pixel[2], pixel[3] if len(pixel) > 3 else 255
                    # Multiple conditions to detect background
                    is_background = False
                    # Pure white
                    if r >= 255 and g >= 255 and b >= 255:
                        is_background = True
                    # Near white (very light colors)
                    elif r > 240 and g > 240 and b > 240:
                        is_background = True
                    # Light gray/off-white
                    elif r > 220 and g > 220 and b > 220 and abs(r-g) < 20 and abs(g-b) < 20:
                        is_background = True
                    # Already transparent
                    elif a < 10:
                        is_background = True
                    
                    if not is_background:
                        cleaned_surface.set_at((x, y), pixel)
            car_width, car_height = self._car_size()
            self.image = pygame.transform.scale(cleaned_surface, (car_width, car_height))
            self.width, self.height = car_width, car_height
        except Exception as e:
            # Create a fallback rectangle if image loading fails
            self.width, self.height = 60, 100
            self.image = None
            self.fallback_color = (255, 0, 0)  # Red color as fallback for debugging
    
    # @staticmethod          check later
    def get_default_car_height():
        """Get default car height for initial positioning"""
        screen_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH
        road_width = screen_width - (2 * int(screen_width * 0.1))
        #car_width and car_height
        car_width = max(60, min(int(road_width * 0.25), 200))
        return int(car_width * 1.3)

    # @staticmethod          check later
    def get_default_car_width():
        screen_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH
        road_width = screen_width - (2 * int(screen_width * 0.1))
        return max(60, min(int(road_width * 0.25), 200))

    def move_left(self):
        """Move car left with road boundary checking"""
        # Road has borders, so we need to stay within the road area
        if self.x > self.road_left_border:
            self.x -= self.speed
            self.rect.x = self.x

    def move_right(self):
        """Move car right with road boundary checking"""
        # Road has borders, so we need to stay within the road area
        if self.x < self.screen_width - self.width - self.road_right_border:
            self.x += self.speed
            self.rect.x = self.x

    def move_up(self):
        """Move car up with boundary checking"""
        if self.y > 0:
            self.y -= self.speed
            self.rect.y = self.y

    def move_down(self):
        """Move car down with boundary checking"""
        if self.y < self.screen_height - self.height:
            self.y += self.speed
            self.rect.y = self.y
    
    def update_screen_size(self, width, height):
        """Update screen dimensions when window is resized"""
        # Calculate current position as percentages of the old screen
        old_width, old_height = self.screen_width, self.screen_height
        old_road_width = old_width - (2 * int(old_width * 0.1))
        car_center_x = self.x + getattr(self, 'width', 60) // 2
        old_left_border = int(old_width * 0.1)
        x_ratio_in_road = (car_center_x - old_left_border) / old_road_width if old_road_width > 0 else 0.5
        old_car_height = getattr(self, 'height', 100)
        
        # Calculate available space for car movement (screen height - car height)
        old_available_space = old_height - old_car_height
        
        if old_available_space > 0:
            # Calculate ratio where 0.0 = top, 1.0 = bottom
            y_ratio = self.y / old_available_space
        else:
            y_ratio = 0.0  # Default to top if no space available
        
        # Clamp the ratio to valid range
        y_ratio = max(0.0, min(1.0, y_ratio))
        self.screen_width, self.screen_height = width, height
        # Recalculate road boundaries for new screen size
        self.update_road_boundaries()
        # Reload car image with new responsive size
        self.load_car_image()
        self.rect.size = (self.width, self.height)
        # Calculate new horizontal position within the new road area
        new_road_width = self.screen_width - (2 * self.road_left_border)
        new_center_x = self.road_left_border + (x_ratio_in_road * new_road_width)
        self.x = int(new_center_x - self.width // 2)
        # Calculate new vertical position using ratio
        new_available_space = self.screen_height - self.height
        self.y = int(y_ratio * new_available_space) if new_available_space > 0 else 0
        # Ensure car stays within valid boundaries
        min_x = self.road_left_border
        max_x = self.screen_width - self.road_right_border - self.width
        
        if max_x >= min_x:  # Valid road area exists
            if self.x < min_x:
                self.x = min_x
            elif self.x > max_x:
                self.x = max_x
        else:  # Road too narrow, center horizontally
            self.x = (self.screen_width - self.width) // 2
        
        # Check vertical boundaries
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height
            
        self.update_position()
        
        print(f"Screen resized from {old_width}x{old_height} to {width}x{height}")
        print(f"Car positioned at ({self.x}, {self.y}), y-ratio: {y_ratio:.3f}")
    
    def handle_input(self, keys):
        """Handle keyboard input for car movement"""
        # Check for key presses and move accordingly
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.move_right()
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.move_down()
    
    def update_position(self):
        """Update the collision rectangle position"""
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """Draw the car on the screen"""
        if self.image:
            # Draw the car image
            screen.blit(self.image, (self.x, self.y))
        else:
            # Fallback: draw a colored rectangle if image failed to load
            pygame.draw.rect(screen, self.fallback_color, self.rect)
            
            # Add some basic car details for fallback
            # Windshield
            windshield_rect = pygame.Rect(self.x + 15, self.y + 15, self.width - 30, 30)
            pygame.draw.rect(screen, (173, 216, 230), windshield_rect)
            
            # Headlights
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 20, self.y + 10), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.width - 20, self.y + 10), 5)
    
    def get_rect(self):
        """Return the collision rectangle"""
        return self.rect

    def get_center(self):
        """Get the center position of the car"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def set_position(self, x, y):
        """Set the car position"""
        self.x, self.y = x, y
        self.update_position()

    def change_car(self, car_number):
        """Change to a different car model"""
        if 3 <= car_number <= 5:
            self.car_number = car_number
            self.load_car_image()
            print(f"Changed to car{car_number}.png")

    def get_info(self):
        """Get car information"""
        return {
            "position": (self.x, self.y),
            "size": (self.width, self.height),
            "car_number": self.car_number,
            "speed": self.speed
        }


# def test_main_car():
#     """Test function to demonstrate the MainCar class"""
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Main Car Test")
#     clock = pygame.time.Clock()
    
#     # Create main car at bottom center
#     car = MainCar(WIDTH // 2 - 40, HEIGHT - 150, car_number=1)
    
#     # Game loop
#     running = True
#     while running:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.KEYDOWN:
        #         # Change car model with number keys
        #         if event.key == pygame.K_1:
        #             car.change_car(1)
        #         elif event.key == pygame.K_2:
        #             car.change_car(2)
        #         elif event.key == pygame.K_3:
        #             car.change_car(3)
        #         elif event.key == pygame.K_4:
        #             car.change_car(4)
        #         elif event.key == pygame.K_5:
        #             car.change_car(5)
        
    #     # Handle continuous key presses
    #     keys = pygame.key.get_pressed()
    #     car.handle_input(keys)
        
    #     # Update
    #     car.update_position()
        
    #     # Draw
    #     screen.fill((50, 50, 50))  # Dark gray background
    #     car.draw(screen)
        
    #     # Draw instructions
    #     font = pygame.font.Font(None, 24)
    #     instructions = [
    #         "Use ARROW KEYS or WASD to move",
    #         "Press 1-5 to change car model",
    #         f"Current car: car{car.car_number}.png",
    #         f"Position: {car.get_center()}"
    #     ]
        
    #     for i, instruction in enumerate(instructions):
    #         text = font.render(instruction, True, (255, 255, 255))
    #         screen.blit(text, (10, 10 + i * 25))
        
    #     pygame.display.flip()
    #     clock.tick(60)
    
    # pygame.quit()


# if __name__ == "__main__":
#     # Run the test when this file is executed directly
#     test_main_car()
