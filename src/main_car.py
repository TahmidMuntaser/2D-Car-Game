import pygame
import os
from config import WIDTH, HEIGHT

class MainCar:
    """Main player car class with image loading and movement controls"""
    
    def __init__(self, x, y, car_number=5):
        """
        Initialize the main player car
        Args:
            x (int): Starting x position
            y (int): Starting y position
            car_number (int): Car image number (1-5)
        """
        self.x = x
        self.y = y
        self.car_number = 2
        self.speed = 5
        
        # Screen boundaries (will be updated by the game)
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        
        # Calculate responsive road boundaries based on screen width
        self.update_road_boundaries()
        
        # Load car image
        self.load_car_image()
        
        # Create collision rectangle
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
    
    def update_road_boundaries(self):
        """Calculate road boundaries based on screen size"""
        # Make borders proportional to screen width (8-12% of screen width)
        border_percentage = 0.1  # 10% of screen width for borders
        self.road_left_border = int(self.screen_width * border_percentage)
        self.road_right_border = int(self.screen_width * border_percentage)
        
        # Ensure minimum and maximum border sizes
        self.road_left_border = max(30, min(self.road_left_border, 80))
        self.road_right_border = max(30, min(self.road_right_border, 80))
    
    def load_car_image(self):
        """Load the car image from assets folder and remove white background"""
        try:
            # Get the path to the assets folder
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            assets_path = os.path.join(current_dir, "assets", f"car{self.car_number}.png")
            
            # Load the original image
            original = pygame.image.load(assets_path).convert_alpha()
            print(f"Original image size: {original.get_size()}")
            
            # Try multiple methods to remove background
            # Method 1: Aggressive pixel-by-pixel removal
            cleaned_surface = pygame.Surface(original.get_size(), pygame.SRCALPHA)
            cleaned_surface.fill((0, 0, 0, 0))  # Fill with transparent
            
            pixels_kept = 0
            pixels_removed = 0
            
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
                        pixels_kept += 1
                    else:
                        pixels_removed += 1
            
            print(f"Pixels kept: {pixels_kept}, Pixels removed: {pixels_removed}")
            
            # Make car wider for better visibility and gameplay
            # Car should be about 18-20% of road width for good proportions
            road_width = self.screen_width - (2 * int(self.screen_width * 0.1))  # Total road width
            car_width = int(road_width * 0.3)  # 30% of road width (wider than before)

            # Ensure reasonable size limits
            car_width = max(70, min(car_width, 200))  # Between 70-200 pixels (wider range)
            car_height = int(car_width * 1.3)  # Height is 1.3x width (better car proportions)
            
            self.image = pygame.transform.scale(cleaned_surface, (car_width, car_height))
            
            # Get dimensions
            self.width = car_width
            self.height = car_height
            
            print(f"Road width: {road_width}, Car size: {car_width}x{car_height}")
            
        except Exception as e:
            print(f"Error loading car image: {e}")
            # Create a fallback rectangle if image loading fails
            self.width = 60
            self.height = 100
            self.image = None
            self.fallback_color = (255, 0, 0)  # Red color as fallback for debugging
    
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
        old_x_ratio = self.x / max(1, self.screen_width) if self.screen_width > 0 else 0.5
        old_y_ratio = self.y / max(1, self.screen_height) if self.screen_height > 0 else 0.8
        
        self.screen_width = width
        self.screen_height = height
        
        # Recalculate road boundaries for new screen size
        self.update_road_boundaries()
        
        # Reload car image with new responsive size
        self.load_car_image()
        
        # Maintain relative position on screen
        self.x = int(old_x_ratio * self.screen_width)
        self.y = int(old_y_ratio * self.screen_height)
        
        # Ensure car stays within new boundaries
        if self.x < self.road_left_border:
            self.x = self.road_left_border
        elif self.x > self.screen_width - self.width - self.road_right_border:
            self.x = self.screen_width - self.width - self.road_right_border
            
        if self.y < 0:
            self.y = 0
        elif self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
            
        self.update_position()
        
        print(f"Screen resized to {width}x{height}, borders: {self.road_left_border}/{self.road_right_border}, car: {self.width}x{self.height}")
    
    def handle_input(self, keys):
        """Handle keyboard input for car movement"""
        # Reset movement flags
        self.moving_left = False
        self.moving_right = False
        
        # Check for key presses and move accordingly
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left()
            self.moving_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right()
            self.moving_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move_down()
    
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
        self.x = x
        self.y = y
        self.update_position()
    
    def change_car(self, car_number):
        """Change to a different car model"""
        if 1 <= car_number <= 5:
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


def test_main_car():
    """Test function to demonstrate the MainCar class"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Car Test")
    clock = pygame.time.Clock()
    
    # Create main car at bottom center
    car = MainCar(WIDTH // 2 - 40, HEIGHT - 150, car_number=1)
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Change car model with number keys
                if event.key == pygame.K_1:
                    car.change_car(1)
                elif event.key == pygame.K_2:
                    car.change_car(2)
                elif event.key == pygame.K_3:
                    car.change_car(3)
                elif event.key == pygame.K_4:
                    car.change_car(4)
                elif event.key == pygame.K_5:
                    car.change_car(5)
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        car.handle_input(keys)
        
        # Update
        car.update_position()
        
        # Draw
        screen.fill((50, 50, 50))  # Dark gray background
        car.draw(screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "Use ARROW KEYS or WASD to move",
            "Press 1-5 to change car model",
            f"Current car: car{car.car_number}.png",
            f"Position: {car.get_center()}"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    # Run the test when this file is executed directly
    test_main_car()
