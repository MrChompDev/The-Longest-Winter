"""
Village scene - main gameplay view
"""
import pygame
import random
import math
import time
from settings import *
from systems.meters import MeterManager
from systems.tasks import TaskManager
from systems.escalation import EscalationManager
from scenes.minigames import create_minigame
from utils.audio import audio_manager
from utils.graphics import (draw_player_enhanced, draw_building_enhanced, 
                            draw_task_indicator, draw_meter_bar, draw_rounded_rect,
                            draw_gradient_rect)


class Player:
    """The Mayor character - Among Us style top-down"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = PLAYER_SIZE // 2
        
    def update(self, dt, keys):
        """Update player position with WASD"""
        # Reset velocity
        self.vx = 0
        self.vy = 0
        
        # WASD movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vy = PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        
        # Normalize diagonal movement
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.707  # 1/sqrt(2)
            self.vy *= 0.707
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Keep in bounds
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def get_nearby_building(self):
        """Get building within interaction range"""
        for building_key, building_info in BUILDINGS.items():
            bx, by = building_info['pos']
            dist = math.sqrt((self.x - bx)**2 + (self.y - by)**2)
            
            if dist < PLAYER_INTERACT_DISTANCE:
                return building_key, building_info
        return None, None
    
    def render(self, screen):
        """Render player - Enhanced Among Us style"""
        draw_player_enhanced(screen, self.x, self.y, self.radius)


class VillageScene:
    """Main gameplay scene"""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset the scene to initial state"""
        # Systems
        self.meter_manager = MeterManager()
        self.task_manager = TaskManager(self.meter_manager)
        self.escalation_manager = EscalationManager(self.meter_manager, self.task_manager)
        
        # Player starts at Town Hall
        town_hall_pos = BUILDINGS['TOWN_HALL']['pos']
        self.player = Player(town_hall_pos[0], town_hall_pos[1])
        
        # State
        self.start_time = time.time()
        self.current_minigame = None
        self.current_building = None
        self.is_in_minigame = False
        
        # Visual effects
        self.snow_particles = []
        for _ in range(150):
            self.snow_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(30, 80),
                'size': random.randint(1, 3)
            })
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Start Mainost music (louder)
        audio_manager.play_music('music', -1, 0.7)
    
    def update(self, dt, events):
        """Update village scene"""
        if self.is_in_minigame:
            return self._update_minigame(dt, events)
        else:
            return self._update_village(dt, events)
    
    def _update_village(self, dt, events):
        """Update main village gameplay"""
        # Update systems
        self.meter_manager.update(dt)
        
        # Check for critical systems and play warning
        critical_systems = self.meter_manager.get_critical_systems()
        if critical_systems and random.random() < 0.01:  # Occasional warning sound
            audio_manager.play_sound('warning', 0.3)
        
        self.task_manager.update(dt)
        elapsed = time.time() - self.start_time
        self.escalation_manager.update(elapsed)
        
        # Update player with WASD
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        
        # Update snow
        for particle in self.snow_particles:
            particle['y'] += particle['speed'] * dt
            if particle['y'] > SCREEN_HEIGHT:
                particle['y'] = -10
                particle['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Handle input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_e:
                    # Try to interact with nearby building
                    building_key, building_info = self.player.get_nearby_building()
                    if building_info:
                        tasks = self.task_manager.get_tasks_for_building(building_info['name'])
                        if tasks and building_info['system']:
                            # Start mini-game
                            self._start_minigame(building_info)
        
        # Check win/lose conditions
        elapsed = time.time() - self.start_time
        if elapsed >= WIN_TIME:
            return 'WIN'
        
        if self.meter_manager.get_collapsed_count() >= 2:
            return 'LOSE'
        
        return None
    
    def _start_minigame(self, building_info):
        """Start a mini-game"""
        system_type = building_info['system']
        escalation = self.meter_manager.meters[system_type].escalation_stage
        self.current_minigame = create_minigame(system_type, escalation)
        self.current_building = building_info
        self.is_in_minigame = True
    
    def _update_minigame(self, dt, events):
        """Update mini-game state"""
        if self.current_minigame:
            self.current_minigame.update(dt, events)
            
            if not self.current_minigame.active:
                # Mini-game finished
                if self.current_minigame.success:
                    # Restore meter
                    system_type = self.current_minigame.system_type
                    self.meter_manager.meters[system_type].restore(40)
                    
                    # Complete task
                    self.task_manager.complete_task(self.current_building['name'])
                
                # Return to game
                self.current_minigame = None
                self.current_building = None
                self.is_in_minigame = False
        
        return None
    
    def render(self, screen):
        """Render village scene"""
        screen.fill(COLOR_BG)
        
        if self.is_in_minigame:
            self._render_minigame(screen)
        else:
            self._render_village(screen)
    
    def _render_village(self, screen):
        """Render main village view - Enhanced top-down Among Us style"""
        # Enhanced background with gradient
        color1 = (35, 40, 55)
        color2 = (25, 30, 45)
        draw_gradient_rect(screen, color1, color2, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw floor tiles with better pattern
        for x in range(0, SCREEN_WIDTH, 60):
            for y in range(0, SCREEN_HEIGHT, 60):
                tile_variant = (x + y) % 180
                if tile_variant == 0:
                    tile_color = (50, 55, 70)
                elif tile_variant == 60:
                    tile_color = (45, 50, 65)
                else:
                    tile_color = (40, 45, 60)
                
                tile_rect = pygame.Rect(x, y, 60, 60)
                pygame.draw.rect(screen, tile_color, tile_rect)
                pygame.draw.rect(screen, (30, 35, 50), tile_rect, 1)
        
        # Draw paths/walkways between buildings with glow
        path_color = (70, 75, 90)
        glow_color = (80, 85, 100, 50)
        for bldg1_key, bldg1_info in BUILDINGS.items():
            for bldg2_key, bldg2_info in BUILDINGS.items():
                if bldg1_key < bldg2_key:
                    x1, y1 = bldg1_info['pos']
                    x2, y2 = bldg2_info['pos']
                    # Path glow
                    pygame.draw.line(screen, glow_color, (x1, y1), (x2, y2), 16)
                    # Path main
                    pygame.draw.line(screen, path_color, (x1, y1), (x2, y2), 12)
        
        # Draw buildings with enhanced graphics
        for building_key, building_info in BUILDINGS.items():
            x, y = building_info['pos']
            
            # Get meter for color
            meter = None
            if building_info['system']:
                meter = self.meter_manager.meters[building_info['system']]
            
            # Draw enhanced building
            draw_building_enhanced(screen, building_info, x, y, meter)
            
            # Building name with background
            name_surface = self.font_tiny.render(building_info['name'], True, (255, 255, 255))
            name_bg = pygame.Surface((name_surface.get_width() + 10, name_surface.get_height() + 4), pygame.SRCALPHA)
            draw_rounded_rect(name_bg, (0, 0, 0, 150), (0, 0, name_surface.get_width() + 10, name_surface.get_height() + 4), 3)
            w, h = building_info['size']
            screen.blit(name_bg, (x - name_bg.get_width() // 2, y + h//2 + 5))
            screen.blit(name_surface, (x - name_surface.get_width() // 2, y + h//2 + 7))
            
            # Enhanced task indicator
            tasks = self.task_manager.get_tasks_for_building(building_info['name'])
            if tasks:
                urgent_count = sum(1 for t in tasks if t.is_urgent())
                draw_task_indicator(screen, x + w//2 - 10, y - h//2 + 10, 
                                  urgent=urgent_count > 0, count=len(tasks))
        
        # Draw player
        self.player.render(screen)
        
        # Enhanced interaction prompt
        building_key, building_info = self.player.get_nearby_building()
        if building_info:
            prompt_text = "Press E or SPACE to interact"
            prompt_font = pygame.font.Font(None, 24)
            prompt = prompt_font.render(prompt_text, True, (255, 255, 255))
            
            # Background with rounded corners
            prompt_bg = pygame.Surface((prompt.get_width() + 30, prompt.get_height() + 16), pygame.SRCALPHA)
            draw_rounded_rect(prompt_bg, (40, 45, 60, 230), 
                            (0, 0, prompt.get_width() + 30, prompt.get_height() + 16), 8)
            
            # Border
            pygame.draw.rect(prompt_bg, COLOR_WARNING, 
                           (0, 0, prompt.get_width() + 30, prompt.get_height() + 16), 2, border_radius=8)
            
            prompt_x = self.player.x - (prompt.get_width() + 30) // 2
            prompt_y = self.player.y - 70
            
            screen.blit(prompt_bg, (prompt_x, prompt_y))
            screen.blit(prompt, (prompt_x + 15, prompt_y + 8))
        
        # Draw UI
        self._render_ui(screen)
        
        # Snow overlay
        self._render_snow(screen)
    
    def _render_minigame(self, screen):
        """Render current mini-game"""
        # Dark background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(COLOR_BG)
        overlay.set_alpha(220)
        screen.blit(overlay, (0, 0))
        
        if self.current_minigame:
            self.current_minigame.render(screen)
    
    def _render_ui(self, screen):
        """Render UI elements with enhanced graphics"""
        # Enhanced meters with gradients
        margin = 20
        meter_width = 220
        meter_height = 35
        
        meters_list = [
            ('HEAT', 'top-left', margin, margin),
            ('FOOD', 'top-right', SCREEN_WIDTH - meter_width - margin, margin),
            ('SANITY', 'bottom-left', margin, SCREEN_HEIGHT - meter_height - margin - 100),
            ('SAFETY', 'bottom-right', SCREEN_WIDTH - meter_width - margin, SCREEN_HEIGHT - meter_height - margin - 100),
        ]
        
        for name, pos, x, y in meters_list:
            meter = self.meter_manager.meters[name]
            
            # Label with shadow
            label = self.font_small.render(f"{name}", True, (255, 255, 255))
            shadow = self.font_small.render(f"{name}", True, (0, 0, 0))
            screen.blit(shadow, (x + 1, y - 21))
            screen.blit(label, (x, y - 22))
            
            # Enhanced meter bar
            draw_meter_bar(screen, x, y, meter_width, meter_height, 
                          meter.value, 100, meter.color)
            
            # Percentage text
            pct = self.font_small.render(f"{int(meter.value)}%", True, (255, 255, 255))
            screen.blit(pct, (x + meter_width + 5, y + meter_height // 2 - pct.get_height() // 2))
        
        # Enhanced timer with background
        elapsed = time.time() - self.start_time
        remaining = max(0, WIN_TIME - elapsed)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        timer_text = self.font.render(f"Until Dawn: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        
        # Background box
        timer_bg = pygame.Surface((timer_text.get_width() + 40, timer_text.get_height() + 20), pygame.SRCALPHA)
        draw_rounded_rect(timer_bg, (40, 45, 60, 200), 
                        (0, 0, timer_text.get_width() + 40, timer_text.get_height() + 20), 10)
        pygame.draw.rect(timer_bg, COLOR_SNOW, 
                       (0, 0, timer_text.get_width() + 40, timer_text.get_height() + 20), 2, border_radius=10)
        
        timer_x = SCREEN_WIDTH // 2 - (timer_text.get_width() + 40) // 2
        screen.blit(timer_bg, (timer_x, 10))
        screen.blit(timer_text, (timer_x + 20, 20))
        
        # Enhanced task count
        task_text = self.font_small.render(f"Active Tasks: {len(self.task_manager.active_tasks)}", True, (255, 255, 255))
        task_bg = pygame.Surface((task_text.get_width() + 24, task_text.get_height() + 12), pygame.SRCALPHA)
        draw_rounded_rect(task_bg, (40, 45, 60, 180), 
                        (0, 0, task_text.get_width() + 24, task_text.get_height() + 12), 6)
        
        task_x = SCREEN_WIDTH // 2 - (task_text.get_width() + 24) // 2
        screen.blit(task_bg, (task_x, 60))
        screen.blit(task_text, (task_x + 12, 66))
    
    def _render_snow(self, screen):
        """Render falling snow"""
        for particle in self.snow_particles:
            pygame.draw.circle(screen, COLOR_SNOW, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
