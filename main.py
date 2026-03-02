"""
THE LONGEST WINTER
Main game file with scene management
"""
import pygame
import sys
from settings import *
from scenes.village import VillageScene
from utils.helpers import draw_text_centered, Button
from utils.audio import audio_manager


class Game:
    """Main game controller"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("THE LONGEST WINTER")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = 'MENU'  # MENU, PLAYING, WIN, LOSE
        
        # Scenes
        self.village_scene = VillageScene()
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 72)
        
        # Snow particles (for menu/end screens)
        import random
        self.menu_snow = []
        for _ in range(100):
            self.menu_snow.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(30, 80),
                'size': random.randint(1, 3)
            })
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update based on state
            if self.state == 'MENU':
                self.update_menu(dt, events)
            elif self.state == 'PLAYING':
                self.update_playing(dt, events)
            elif self.state in ['WIN', 'LOSE']:
                self.update_endgame(dt, events)
            
            # Render
            self.render()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def update_menu(self, dt, events):
        """Update menu state"""
        # Update menu snow
        for particle in self.menu_snow:
            particle['y'] += particle['speed'] * dt
            if particle['y'] > SCREEN_HEIGHT:
                particle['y'] = -10
                import random
                particle['x'] = random.randint(0, SCREEN_WIDTH)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_game()
    
    def start_game(self):
        """Start a new game"""
        self.state = 'PLAYING'
        self.village_scene.reset()
    
    def update_playing(self, dt, events):
        """Update main gameplay"""
        result = self.village_scene.update(dt, events)
        
        if result == 'WIN':
            self.state = 'WIN'
        elif result == 'LOSE':
            self.state = 'LOSE'
    
    def update_endgame(self, dt, events):
        """Update end game state"""
        # Update menu snow
        for particle in self.menu_snow:
            particle['y'] += particle['speed'] * dt
            if particle['y'] > SCREEN_HEIGHT:
                particle['y'] = -10
                import random
                particle['x'] = random.randint(0, SCREEN_WIDTH)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'MENU'
    
    def render(self):
        """Render current state"""
        self.screen.fill(COLOR_BG)
        
        if self.state == 'MENU':
            self.render_menu()
        elif self.state == 'PLAYING':
            self.village_scene.render(self.screen)
        elif self.state in ['WIN', 'LOSE']:
            self.render_endgame()
    
    def render_menu(self):
        """Render menu screen"""
        # Title
        draw_text_centered(self.screen, "THE LONGEST WINTER", self.font_large, COLOR_SNOW, 200)
        
        # Subtitle
        draw_text_centered(self.screen, "A Top-Down Thriller", self.font, COLOR_SNOW_DARK, 300)
        
        # Instructions
        instructions = [
            "You are the last mayor of a frozen village",
            "Use WASD to move around the village",
            "Press E or SPACE near buildings to work",
            "Keep all systems running until dawn",
            "If TWO systems collapse, you lose"
        ]
        
        y = 380
        for i, inst in enumerate(instructions):
            color = COLOR_ALERT if i == 4 else COLOR_UI_TEXT
            draw_text_centered(self.screen, inst, self.font_small, color, y)
            y += 35
        
        # Start
        draw_text_centered(self.screen, "Press SPACE to begin", self.font, COLOR_WARNING, 600)
        
        # Snow
        self.render_snow()
    
    def render_endgame(self):
        """Render win/lose screen"""
        if self.state == 'WIN':
            draw_text_centered(self.screen, "YOU SURVIVED", self.font_large, COLOR_SAFE, 250)
            draw_text_centered(self.screen, "Dawn has broken", self.font, COLOR_SNOW, 350)
        else:
            draw_text_centered(self.screen, "SYSTEMS FAILED", self.font_large, COLOR_ALERT, 250)
            draw_text_centered(self.screen, "The village is lost", self.font, COLOR_SNOW_DARK, 350)
        
        # Time survived
        import time
        if hasattr(self.village_scene, 'start_time'):
            elapsed = time.time() - self.village_scene.start_time
            time_text = f"Time: {int(elapsed)}s / {WIN_TIME}s"
            draw_text_centered(self.screen, time_text, self.font, COLOR_UI_TEXT, 420)
        
        # Restart
        draw_text_centered(self.screen, "Press SPACE to return to menu", self.font, COLOR_WARNING, 550)
        
        # Snow
        self.render_snow()
    
    def render_snow(self):
        """Render falling snow for menu/end screens"""
        for particle in self.menu_snow:
            pygame.draw.circle(self.screen, COLOR_SNOW, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])


if __name__ == '__main__':
    game = Game()
    game.run()
