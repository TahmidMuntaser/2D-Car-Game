import pygame
import sys
import os
from config import WIDTH, HEIGHT, FPS

class Button:
    """A simple button class for the menu"""
    
    def __init__(self, x, y, width, height, text, color, text_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text, self.color, self.text_color, self.hover_color = text, color, text_color, hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        """Draw the button on screen"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)  # White border
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))
    
    def handle_event(self, event):
        """Handle mouse events for the button"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

class CarPreview:
    """Preview car selection"""
    def __init__(self, x, y):
        self.x, self.y, self.current_car = x, y, 3
        self.car_images = {}
        self.load_car_images()
        
    def load_car_images(self):
        """Load preview images for cars"""
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for car_num in range(3, 6):  # Cars 3, 4, 5
                assets_path = os.path.join(current_dir, "assets", f"car{car_num}.png")
                if os.path.exists(assets_path):
                    original = pygame.image.load(assets_path).convert_alpha()
                    self.car_images[car_num] = pygame.transform.scale(original, (80, 100))
        except Exception as e:
            print(f"Error loading car images: {e}")
            colors = {3: (255, 0, 0), 4: (0, 255, 0), 5: (0, 0, 255)}
            for car_num in range(3, 6):
                surface = pygame.Surface((80, 100))
                surface.fill(colors[car_num])
                self.car_images[car_num] = surface
    
    def draw(self, screen):
        """Draw car preview"""
        if self.current_car in self.car_images:
            screen.blit(self.car_images[self.current_car], (self.x, self.y))
        font_size = max(24, min(40, int(screen.get_height() * 0.04)))
        font = pygame.font.Font(None, font_size)
        text = font.render(f"Car {self.current_car}", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(self.x + 40, self.y + 120)))

class InitialWindow:
    """Main menu window for the 2D Car Game"""
    def __init__(self):
        pygame.init()
        # Get current screen size or use defaults
        current_surface = pygame.display.get_surface()
        self.window_width = current_surface.get_width() if current_surface else WIDTH
        self.window_height = current_surface.get_height() if current_surface else HEIGHT
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("2D Car Game - Main Menu")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.bg_color = (30, 30, 50)  # Dark blue-gray
        self.button_color = (70, 130, 180)  # Steel blue
        self.button_hover_color = (100, 149, 237)  # Cornflower blue
        self.text_color = (255, 255, 255)  # White
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        
        # Game state
        self.selected_car = 3
        self.show_options = False
        self.running = True
        self.start_game = False
        self.quit_game = False
        
        # Car preview and buttons
        self.car_preview = CarPreview(self.window_width // 2 - 40, self.window_height // 2 - 100)
        self.create_buttons()
        
    def create_buttons(self):
        """Create menu buttons with optimized positioning"""
        # Responsive button sizing
        button_width = min(250, int(self.window_width * 0.35))  # Max 250px, 35% of screen width
        button_height = max(50, int(self.window_height * 0.08))  # Min 50px, 8% of screen height
        button_spacing = max(15, int(self.window_height * 0.025))  # Min 15px, 2.5% of screen height
        
        # Center buttons vertically, starting a bit above center
        total_buttons = 4  # new_game, change_car, instructions, quit
        total_height = (total_buttons * button_height) + ((total_buttons - 1) * button_spacing)
        start_y = (self.window_height - total_height) // 2 + int(self.window_height * 0.1)
        
        self.buttons = {}
        
        # Main menu buttons
        self.buttons['new_game'] = Button(
            self.window_width // 2 - button_width // 2, start_y,
            button_width, button_height, "New Game",
            self.button_color, self.text_color, self.button_hover_color
        )
        
        self.buttons['change_car'] = Button(
            self.window_width // 2 - button_width // 2, start_y + button_height + button_spacing,
            button_width, button_height, "Change Car",
            self.button_color, self.text_color, self.button_hover_color
        )
        
        self.buttons['instructions'] = Button(
            self.window_width // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing),
            button_width, button_height, "Instructions",
            self.button_color, self.text_color, self.button_hover_color
        )
        
        self.buttons['quit'] = Button(
            self.window_width // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing),
            button_width, button_height, "Quit",
            (180, 70, 70), self.text_color, (200, 90, 90)  # Red color for quit
        )
        
        # Car selection buttons
        car_button_width = 150
        car_button_height = 40
        car_y = self.window_height // 2 + 60
        
        self.buttons['prev_car'] = Button(
            self.window_width // 2 - 200, car_y,
            car_button_width, car_button_height, "Previous",
            self.button_color, self.text_color, self.button_hover_color
        )
        
        self.buttons['next_car'] = Button(
            self.window_width // 2 + 50, car_y,
            car_button_width, car_button_height, "Next",
            self.button_color, self.text_color, self.button_hover_color
        )
    
    def draw_background(self):
        """Draw animated background"""
        self.screen.fill(self.bg_color)
        # Draw some road-like lines for visual appeal
        line_color = (100, 100, 120)
        for i in range(0, self.window_height + 50, 50):
            y = (i + pygame.time.get_ticks() // 10) % (self.window_height + 50)
            pygame.draw.rect(self.screen, line_color, (self.window_width // 2 - 5, y, 10, 30))
    
    def draw_title(self):
        """Draw the game title"""
        title_text = self.title_font.render("2D CAR GAME", True, self.text_color)
        #
        self.screen.blit(title_text, title_text.get_rect(center=(self.window_width // 2, self.window_height // 4)))
        subtitle_text = self.subtitle_font.render("Drive and Survive!", True, (200, 200, 200))
        self.screen.blit(subtitle_text, subtitle_text.get_rect(center=(self.window_width // 2, self.window_height // 4 + 50)))
    
    def draw_main_menu(self):
        self.draw_background()
        self.draw_title()
        for btn in ['new_game', 'change_car', 'instructions', 'quit']: self.buttons[btn].draw(self.screen)
    
    def draw_car_selection(self):
        self.draw_background()
        title_size, instruction_size, small_text_size = max(48, min(72, int(self.window_height * 0.08))), max(24, min(36, int(self.window_height * 0.04))), max(20, min(28, int(self.window_height * 0.03)))
        title_font = pygame.font.Font(None, title_size)
        title_text = title_font.render("SELECT YOUR CAR", True, self.text_color)
        self.screen.blit(title_text, title_text.get_rect(center=(self.window_width // 2, self.window_height // 5)))
        self.car_preview.current_car = self.selected_car
        self.car_preview.draw(self.screen)
        
        # Car selection buttons
        self.buttons['prev_car'].draw(self.screen)
        self.buttons['next_car'].draw(self.screen)
        
        # Instructions with proper spacing
        instruction_font = pygame.font.Font(None, instruction_size)
        small_font = pygame.font.Font(None, small_text_size)
        
        # Split long instruction text if needed
        instruction_y = self.window_height // 2 + 140
        
        if self.window_width < 600:
            # For smaller screens, split the instruction into two lines
            instruction_text1 = instruction_font.render("Use Previous/Next buttons", True, (200, 200, 200))
            instruction_text2 = instruction_font.render("or Arrow Keys to choose your car", True, (200, 200, 200))
            
            instruction_rect1 = instruction_text1.get_rect(center=(self.window_width // 2, instruction_y))
            instruction_rect2 = instruction_text2.get_rect(center=(self.window_width // 2, instruction_y + instruction_size + 5))
            
            self.screen.blit(instruction_text1, instruction_rect1)
            self.screen.blit(instruction_text2, instruction_rect2)
            esc_y = instruction_y + (instruction_size + 5) * 2 + 10
        else:
            # For larger screens, keep it on one line
            instruction_text = instruction_font.render("Use Previous/Next or Arrow Keys to choose your car", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(center=(self.window_width // 2, instruction_y))
            self.screen.blit(instruction_text, instruction_rect)
            esc_y = instruction_y + instruction_size + 15
        
        # ESC instruction
        esc_text = small_font.render("Press ESC to return to main menu", True, (150, 150, 150))
        esc_rect = esc_text.get_rect(center=(self.window_width // 2, esc_y))
        self.screen.blit(esc_text, esc_rect)
    
    def draw_instructions(self):
        """Draw the instructions screen"""
        self.draw_background()
        
        # Responsive font sizes based on screen height
        title_size = max(48, min(72, int(self.window_height * 0.08)))
        header_size = max(28, min(40, int(self.window_height * 0.045)))
        text_size = max(20, min(30, int(self.window_height * 0.035)))
        
        # Title
        title_font = pygame.font.Font(None, title_size)
        title_text = title_font.render("GAME INSTRUCTIONS", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 6))
        self.screen.blit(title_text, title_rect)
        
        # Instructions info
        instructions_info = [
            ("GAME CONTROLS:", "header"),
            ("ARROW KEYS or WASD - Move your car", "text"),
            ("LEFT/RIGHT ARROWS - Change car in selection", "text"),
            ("Numbers 1, 2, 3 - Change car model during game", "text"),
            ("ESC - Return to main menu", "text"),
            ("", "empty"),
            ("GAME OBJECTIVES:", "header"),
            ("- Avoid colliding with enemy cars", "text"),
            ("- Survive as long as possible", "text"),
            ("- Use responsive controls to navigate", "text"),
            ("", "empty"),
            ("FEATURES:", "header"),
            ("- Dynamic screen resizing support", "text"),
            ("- Multiple car models to choose from", "text"),
            ("- Realistic collision detection", "text"),
            ("- Smooth car movement and controls", "text")
        ]
        
        # Calculate optimal spacing based on screen size
        available_height = self.window_height - (self.window_height // 6) - 100  # Space after title and bottom margin
        total_text_lines = len([info for info in instructions_info if info[1] != "empty"])
        line_spacing = min(max(20, available_height // (total_text_lines + 2)), text_size + 8)
        
        # Starting position
        y_start = self.window_height // 6 + title_size + 30
        current_y = y_start
        
        # Create fonts
        header_font = pygame.font.Font(None, header_size)
        text_font = pygame.font.Font(None, text_size)
        
        for info_text, info_type in instructions_info:
            if info_type == "empty":
                current_y += line_spacing // 2  # Half spacing for empty lines
                continue
            
            if info_type == "header":
                color = self.text_color
                font = header_font
                current_y += line_spacing // 4  # Extra space before headers
            else:
                color = (200, 200, 200)
                font = text_font
            
            # Check if text fits on screen, truncate if necessary
            max_width = self.window_width - 40  # 20px margin on each side
            text_surface = font.render(info_text, True, color)
            
            if text_surface.get_width() > max_width:
                # Truncate text if it's too long
                words = info_text.split()
                truncated_text = ""
                for word in words:
                    test_text = truncated_text + word + " "
                    if font.size(test_text)[0] <= max_width - 20:  # Leave some buffer
                        truncated_text = test_text
                    else:
                        truncated_text = truncated_text.rstrip() + "..."
                        break
                text_surface = font.render(truncated_text, True, color)
            
            # Check if we have enough vertical space
            if current_y + line_spacing > self.window_height - 50:
                # Add "..." if we run out of space
                dots_surface = text_font.render("... (press ESC to return)", True, (150, 150, 150))
                dots_rect = dots_surface.get_rect(center=(self.window_width // 2, self.window_height - 30))
                self.screen.blit(dots_surface, dots_rect)
                break
            self.screen.blit(text_surface, text_surface.get_rect(center=(self.window_width // 2, current_y)))
            current_y += line_spacing

    def handle_events(self):
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.VIDEORESIZE:
                # Handle window resize
                self.window_width, self.window_height = event.size
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.create_buttons()  # Recreate buttons for new size
                self.car_preview = CarPreview(self.window_width // 2 - 40, self.window_height // 2 - 100)
            
            # Handle ESC key - return to main menu from any sub-screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.show_options:  # If in any sub-screen
                    self.show_options = False  # Return to main menu
                    continue  # Skip other event handling
            
            # Handle button clicks based on current state
            if self.show_options == "car_selection":
                self.handle_car_selection_events(event)
            elif self.show_options != "instructions":  # Only handle main menu if not in instructions
                self.handle_main_menu_events(event)
    
    def handle_main_menu_events(self, event):
        """Handle main menu events"""
        if self.buttons['new_game'].handle_event(event):
            self.start_game = True
            self.running = False
        elif self.buttons['change_car'].handle_event(event):
            self.show_options = "car_selection"
        elif self.buttons['instructions'].handle_event(event):
            self.show_options = "instructions"
        elif self.buttons['quit'].handle_event(event):
            self.quit_game = True
            self.running = False  # Quit the game

    def handle_car_selection_events(self, event):
        """Handle car selection events"""
        # Handle button clicks
        if self.buttons['prev_car'].handle_event(event):
            self.selected_car = max(3, self.selected_car - 1)
        elif self.buttons['next_car'].handle_event(event):
            self.selected_car = min(5, self.selected_car + 1)
        
        # Handle arrow keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Left arrow - previous car
                self.selected_car = max(3, self.selected_car - 1)
            elif event.key == pygame.K_RIGHT:  # Right arrow - next car
                self.selected_car = min(5, self.selected_car + 1)
    
    def handle_instructions_events(self, event):
        """Handle instructions events - ESC key handled globally"""
        # No specific event handling needed for instructions screen
        # ESC key is handled globally in handle_events method
        pass
    
    def run(self):
        """Run the main menu"""
        while self.running:
            self.handle_events()
            
            # Draw current screen
            if self.show_options == "car_selection":
                self.draw_car_selection()
            elif self.show_options == "instructions":
                self.draw_instructions()
            else:
                self.draw_main_menu()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        if self.start_game:
            return self.selected_car  # Return selected car number for the game
        elif self.quit_game:
            return None  # Return None to indicate user wants to quit
        else:
            return False  # Return False to indicate no car selected

def show_main_menu():
    """Show the main menu and return the selected car number"""
    menu = InitialWindow()
    return menu.run()

if __name__ == "__main__":
    selected_car = show_main_menu()
    if selected_car:
        print(f"Starting game with car {selected_car}")
