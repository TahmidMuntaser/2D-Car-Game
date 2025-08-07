import pygame
import sys
import os
from config import WIDTH, HEIGHT, FPS

class Button:
    """A simple button class for the menu"""
    
    def __init__(self, x, y, width, height, text, color, text_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        """Draw the button on screen"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)  # White border
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """Handle mouse events for the button"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class CarPreview:
    """Preview car selection"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_car = 3  # Default car
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
                    # Scale down for preview
                    scaled = pygame.transform.scale(original, (80, 100))
                    self.car_images[car_num] = scaled
        except Exception as e:
            print(f"Error loading car images: {e}")
            # Create fallback rectangles
            for car_num in range(3, 6):
                surface = pygame.Surface((80, 100))
                colors = {3: (255, 0, 0), 4: (0, 255, 0), 5: (0, 0, 255)}
                surface.fill(colors[car_num])
                self.car_images[car_num] = surface
    
    def draw(self, screen):
        """Draw car preview"""
        if self.current_car in self.car_images:
            screen.blit(self.car_images[self.current_car], (self.x, self.y))
            
        # Draw car number
        font = pygame.font.Font(None, 32)
        text = font.render(f"Car {self.current_car}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + 40, self.y + 120))
        screen.blit(text, text_rect)
    
    def next_car(self):
        """Switch to next car"""
        self.current_car = self.current_car + 1 if self.current_car < 5 else 3
    
    def prev_car(self):
        """Switch to previous car"""
        self.current_car = self.current_car - 1 if self.current_car > 3 else 5

class InitialWindow:
    """Main menu window for the 2D Car Game"""
    
    def __init__(self):
        pygame.init()
        self.window_width, self.window_height = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH,pygame.display.get_surface().get_height() if pygame.display.get_surface() else HEIGHT
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
        
        # Current selected car
        self.selected_car = 3
        
        # Car preview
        self.car_preview = CarPreview(self.window_width // 2 - 40, self.window_height // 2 - 100)
        
        # Create buttons
        self.create_buttons()
        
        # Game state
        self.show_options = False
        self.running = True
        self.start_game = False
        
    def create_buttons(self):
        """Create menu buttons"""
        button_width = pygame.display.get_surface().get_width() if pygame.display.get_surface() else WIDTH
        button_height = pygame.display.get_surface().get_height() if pygame.display.get_surface() else HEIGHT
        button_width = button_width * 0.3
        button_height = button_height * 0.07
        button_spacing = 20
        start_y = self.window_height // 2 - 50
        
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
        
        self.buttons['options'] = Button(
            self.window_width // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing),
            button_width, button_height, "Options",
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
        
        self.buttons['back'] = Button(
            self.window_width // 2 - button_width // 2, car_y + 120,
            button_width, button_height, "Back to Menu",
            (70, 70, 70), self.text_color, (100, 100, 100)
        )
        
        # Options buttons
        self.buttons['back_options'] = Button(
            self.window_width // 2 - button_width // 2, self.window_height // 2 + 100,
            button_width, button_height, "Back to Menu",
            (70, 70, 70), self.text_color, (100, 100, 100)
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
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 4))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.subtitle_font.render("Drive and Survive!", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, self.window_height // 4 + 50))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_main_menu(self):
        """Draw the main menu"""
        self.draw_background()
        self.draw_title()
        
        # Draw main menu buttons
        for button_name in ['new_game', 'change_car', 'options', 'quit']:
            self.buttons[button_name].draw(self.screen)
    
    def draw_car_selection(self):
        """Draw the car selection screen"""
        self.draw_background()
        
        # Title
        title_text = self.title_font.render("SELECT YOUR CAR", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 4))
        self.screen.blit(title_text, title_rect)
        
        # Car preview
        self.car_preview.current_car = self.selected_car
        self.car_preview.draw(self.screen)
        
        # Car selection buttons
        self.buttons['prev_car'].draw(self.screen)
        self.buttons['next_car'].draw(self.screen)
        self.buttons['back'].draw(self.screen)
        
        # Instructions
        instruction_text = self.subtitle_font.render("Use Previous/Next to choose your car", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 160))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_options(self):
        """Draw the options screen"""
        self.draw_background()
        
        # Title
        title_text = self.title_font.render("OPTIONS", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 3))
        self.screen.blit(title_text, title_rect)
        
        # Options info
        options_info = [
            "Game Controls:",
            "ARROW KEYS or WASD - Move car",
            "Numbers 3, 4, 5 - Change car during game",
            "ESC - Return to main menu",
            "",
            "Game Features:",
            "- Responsive car movement",
            "- Dynamic screen resizing",
            "- Multiple car models",
            "- Collision detection"
        ]
        
        y_offset = self.window_height // 2 - 80
        for i, info in enumerate(options_info):
            color = self.text_color if info.endswith(":") else (200, 200, 200)
            font = self.subtitle_font if info.endswith(":") else pygame.font.Font(None, 28)
            text = font.render(info, True, color)
            text_rect = text.get_rect(center=(self.window_width // 2, y_offset + i * 25))
            self.screen.blit(text, text_rect)
        
        # Back button
        self.buttons['back_options'].draw(self.screen)
    
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
            
            # Handle button clicks based on current state
            if self.show_options == "car_selection":
                self.handle_car_selection_events(event)
            elif self.show_options == "options":
                self.handle_options_events(event)
            else:
                self.handle_main_menu_events(event)
    
    def handle_main_menu_events(self, event):
        """Handle main menu events"""
        if self.buttons['new_game'].handle_event(event):
            self.start_game = True
            self.running = False
        elif self.buttons['change_car'].handle_event(event):
            self.show_options = "car_selection"
        elif self.buttons['options'].handle_event(event):
            self.show_options = "options"
        elif self.buttons['quit'].handle_event(event):
            self.running = False
    
    def handle_car_selection_events(self, event):
        """Handle car selection events"""
        if self.buttons['prev_car'].handle_event(event):
            if self.selected_car > 3:
                self.selected_car = self.selected_car - 1 
        elif self.buttons['next_car'].handle_event(event):
            if self.selected_car < 5:
                self.selected_car = self.selected_car + 1
        elif self.buttons['back'].handle_event(event):
            self.show_options = False
    
    def handle_options_events(self, event):
        """Handle options events"""
        if self.buttons['back_options'].handle_event(event):
            self.show_options = False
    
    def run(self):
        """Run the main menu"""
        while self.running:
            self.handle_events()
            
            # Draw current screen
            if self.show_options == "car_selection":
                self.draw_car_selection()
            elif self.show_options == "options":
                self.draw_options()
            else:
                self.draw_main_menu()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        if self.start_game:
            return self.selected_car  # Return selected car number for the game
        else:
            return None  # Return None to indicate quit

def show_main_menu():
    """Show the main menu and return the selected car number"""
    menu = InitialWindow()
    return menu.run()

if __name__ == "__main__":
    selected_car = show_main_menu()
    if selected_car:
        print(f"Starting game with car {selected_car}")
