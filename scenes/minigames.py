"""
Mini-game implementations for each building
"""
import random
import pygame
from settings import *
from utils.audio import audio_manager


class MiniGame:
    """Base class for mini-games"""
    
    def __init__(self, system_type, escalation_stage):
        self.system_type = system_type
        self.escalation_stage = escalation_stage
        self.active = True
        self.success = False
        self.progress = 0.0
    
    def update(self, dt, events):
        """Override in subclasses"""
        pass
    
    def render(self, screen):
        """Override in subclasses"""
        pass


class FurnaceGame(MiniGame):
    """Workshop - Keep needle in green zone"""
    
    def __init__(self, escalation_stage):
        super().__init__('HEAT', escalation_stage)
        self.needle_pos = 0.5  # 0-1
        self.target_min = 0.35  # Wider zone
        self.target_max = 0.65  # Wider zone
        self.drift_speed = FURNACE_DRIFT_SPEED * (1 + escalation_stage * 0.2)  # Less aggressive scaling
        self.drift_dir = random.choice([-1, 1])
        self.success_time = 0
        self.required_time = 8 - (escalation_stage * 1)  # Shorter time required
        self.control_strength = 1.5  # How responsive controls are
        
    def update(self, dt, events):
        if not self.active:
            return
        
        # Handle input - much more responsive
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.needle_pos -= self.drift_speed * dt * self.control_strength
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.needle_pos += self.drift_speed * dt * self.control_strength
        
        # Apply drift - much gentler
        self.needle_pos += self.drift_dir * self.drift_speed * dt * 0.5  # Half the drift
        
        # Random direction change - less frequent
        if random.random() < 0.01:  # Was 0.02, now half as often
            self.drift_dir *= -1
        
        # Clamp
        self.needle_pos = max(0, min(1, self.needle_pos))
        
        # Check if in zone
        if self.target_min <= self.needle_pos <= self.target_max:
            self.success_time += dt
            self.progress = self.success_time / self.required_time
            
            if self.success_time >= self.required_time:
                self.success = True
                self.active = False
                audio_manager.play_sound('success', 0.5)
        else:
            self.success_time = max(0, self.success_time - dt * 0.3)  # Slower decay
            self.progress = self.success_time / self.required_time
    
    def render(self, screen):
        # Draw furnace UI
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("FURNACE REGULATION", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, center_y - 200))
        
        # Instruction
        font_small = pygame.font.Font(None, 32)
        inst = font_small.render("Use A/D or Arrow Keys to keep needle in GREEN zone", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, center_y - 150))
        
        # Bar
        bar_width = 600
        bar_height = 60
        bar_x = center_x - bar_width // 2
        bar_y = center_y
        
        # Background
        pygame.draw.rect(screen, COLOR_UI_BG, (bar_x, bar_y, bar_width, bar_height))
        
        # Target zone
        zone_x = bar_x + int(self.target_min * bar_width)
        zone_width = int((self.target_max - self.target_min) * bar_width)
        pygame.draw.rect(screen, COLOR_SAFE, (zone_x, bar_y, zone_width, bar_height))
        
        # Needle
        needle_x = bar_x + int(self.needle_pos * bar_width)
        pygame.draw.line(screen, COLOR_ALERT, (needle_x, bar_y - 10), (needle_x, bar_y + bar_height + 10), 5)
        
        # Progress bar
        prog_y = center_y + 100
        pygame.draw.rect(screen, COLOR_UI_BG, (bar_x, prog_y, bar_width, 30))
        pygame.draw.rect(screen, COLOR_HEAT, (bar_x, prog_y, int(bar_width * self.progress), 30))
        
        # Progress text
        prog_text = font_small.render(f"Progress: {int(self.progress * 100)}%", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, prog_y + 40))


class SortingGame(MiniGame):
    """Farm - Sort crates correctly"""
    
    def __init__(self, escalation_stage):
        super().__init__('FOOD', escalation_stage)
        self.num_crates = 5 + escalation_stage
        self.crate_types = ['GRAIN', 'MEAT', 'VEGETABLES', 'PRESERVED']
        self.crates = []
        self.shelves = {t: pygame.Rect(0, 0, 0, 0) for t in self.crate_types}
        self.dragging = None
        self.sorted_count = 0
        self.setup_crates()
        
    def setup_crates(self):
        """Create random crates"""
        for i in range(self.num_crates):
            crate_type = random.choice(self.crate_types)
            x = 200 + (i % 5) * 120
            y = 400 + (i // 5) * 80
            self.crates.append({
                'type': crate_type,
                'rect': pygame.Rect(x, y, 100, 60),
                'sorted': False
            })
    
    def update(self, dt, events):
        if not self.active:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicking a crate
                for crate in self.crates:
                    if crate['rect'].collidepoint(mouse_pos) and not crate['sorted']:
                        self.dragging = crate
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    # Check if dropped on correct shelf
                    shelf = self.shelves[self.dragging['type']]
                    if shelf.colliderect(self.dragging['rect']):
                        self.dragging['sorted'] = True
                        self.sorted_count += 1
                        self.progress = self.sorted_count / self.num_crates
                        audio_manager.play_sound('success', 0.3)
                        
                        if self.sorted_count >= self.num_crates:
                            self.success = True
                            self.active = False
                    else:
                        audio_manager.play_sound('fail', 0.3)
                    
                    self.dragging = None
        
        # Drag crate with mouse
        if self.dragging:
            self.dragging['rect'].center = mouse_pos
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("SUPPLY SORTING", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 50))
        
        # Instruction
        font_small = pygame.font.Font(None, 28)
        inst = font_small.render("Drag crates to matching shelves", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 100))
        
        # Draw shelves
        shelf_y = 200
        shelf_width = 200
        shelf_height = 80
        spacing = 240
        start_x = center_x - (len(self.crate_types) * spacing) // 2
        
        for i, ctype in enumerate(self.crate_types):
            x = start_x + i * spacing
            rect = pygame.Rect(x, shelf_y, shelf_width, shelf_height)
            self.shelves[ctype] = rect
            
            pygame.draw.rect(screen, COLOR_UI_BG, rect)
            pygame.draw.rect(screen, COLOR_FOOD, rect, 3)
            
            label = font_small.render(ctype, True, COLOR_UI_TEXT)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
        
        # Draw crates
        for crate in self.crates:
            if not crate['sorted']:
                color = COLOR_FOOD if crate != self.dragging else COLOR_WARNING
                pygame.draw.rect(screen, color, crate['rect'])
                pygame.draw.rect(screen, COLOR_UI_TEXT, crate['rect'], 2)
                
                label = font_small.render(crate['type'][:4], True, COLOR_UI_TEXT)
                screen.blit(label, (crate['rect'].centerx - label.get_width() // 2, 
                                   crate['rect'].centery - label.get_height() // 2))
        
        # Progress
        prog_text = font_small.render(f"Sorted: {self.sorted_count}/{self.num_crates}", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, SCREEN_HEIGHT - 100))


class SimonSaysGame(MiniGame):
    """Church - Follow the flashing pattern (Simon Says style)"""
    
    def __init__(self, escalation_stage):
        super().__init__('SANITY', escalation_stage)
        self.sequence_length = 4 + escalation_stage
        self.colors = ['RED', 'BLUE', 'GREEN', 'YELLOW']
        self.sequence = [random.choice(self.colors) for _ in range(self.sequence_length)]
        self.player_input = []
        self.showing_sequence = True
        self.show_timer = 0
        self.show_index = 0
        self.button_positions = {
            'RED': (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60),
            'BLUE': (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 60),
            'GREEN': (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60),
            'YELLOW': (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 60),
        }
        self.button_colors = {
            'RED': (200, 50, 50),
            'BLUE': (50, 100, 200),
            'GREEN': (50, 180, 80),
            'YELLOW': (220, 200, 50),
        }
        
    def update(self, dt, events):
        if not self.active:
            return
        
        if self.showing_sequence:
            self.show_timer += dt
            if self.show_timer >= 0.6:
                self.show_timer = 0
                self.show_index += 1
                if self.show_index >= len(self.sequence):
                    self.showing_sequence = False
                    self.show_index = 0
        else:
            # Accept player input
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for color, pos in self.button_positions.items():
                        rect = pygame.Rect(pos[0], pos[1], 100, 100)
                        if rect.collidepoint(mouse_pos):
                            self.player_input.append(color)
                            audio_manager.play_sound('success', 0.2)
                            
                            # Check correctness
                            idx = len(self.player_input) - 1
                            if self.player_input[idx] != self.sequence[idx]:
                                # Wrong! Reset
                                audio_manager.play_sound('fail', 0.5)
                                self.player_input = []
                            elif len(self.player_input) == len(self.sequence):
                                # Success!
                                audio_manager.play_sound('success', 0.5)
                                self.success = True
                                self.active = False
                            
                            self.progress = len(self.player_input) / len(self.sequence)
                            break
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("PATTERN MEMORY", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 100))
        
        # Instruction
        font_small = pygame.font.Font(None, 28)
        if self.showing_sequence:
            inst = font_small.render("Watch the pattern...", True, COLOR_WARNING)
        else:
            inst = font_small.render("Repeat the pattern", True, COLOR_SAFE)
        screen.blit(inst, (center_x - inst.get_width() // 2, 150))
        
        # Draw buttons
        for color, pos in self.button_positions.items():
            base_color = self.button_colors[color]
            
            # Highlight during sequence
            if self.showing_sequence and self.show_index < len(self.sequence):
                if self.sequence[self.show_index] == color and self.show_timer < 0.3:
                    draw_color = tuple(min(255, c + 100) for c in base_color)
                else:
                    draw_color = base_color
            else:
                draw_color = base_color
            
            # Highlight on player click
            if not self.showing_sequence and self.player_input:
                if len(self.player_input) > 0 and self.player_input[-1] == color:
                    draw_color = tuple(min(255, c + 80) for c in base_color)
            
            pygame.draw.rect(screen, draw_color, (pos[0], pos[1], 100, 100), border_radius=10)
            pygame.draw.rect(screen, COLOR_UI_TEXT, (pos[0], pos[1], 100, 100), 3, border_radius=10)
        
        # Progress
        prog_text = font_small.render(f"Progress: {len(self.player_input)}/{len(self.sequence)}", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, SCREEN_HEIGHT - 100))


class SignalGame(MiniGame):
    """Watchtower - Match light patterns"""
    
    def __init__(self, escalation_stage):
        super().__init__('SAFETY', escalation_stage)
        self.pattern = [random.randint(0, 1) for _ in range(6)]
        self.player_pattern = [0] * 6
        self.time_limit = SIGNAL_MATCH_TIME - (escalation_stage * 2)
        self.time_remaining = self.time_limit
        
    def update(self, dt, events):
        if not self.active:
            return
        
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.active = False
            self.success = False
            audio_manager.play_sound('fail', 0.5)
            return
        
        # Check input
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check which light clicked
                center_x = SCREEN_WIDTH // 2 - 150
                y = SCREEN_HEIGHT // 2
                
                for i in range(6):
                    x = center_x + i * 60
                    rect = pygame.Rect(x, y, 50, 50)
                    if rect.collidepoint(mouse_pos):
                        self.player_pattern[i] = 1 - self.player_pattern[i]
                        break
        
        # Check if complete
        if self.player_pattern == self.pattern:
            self.success = True
            self.active = False
            audio_manager.play_sound('success', 0.5)
        
        # Update progress
        matches = sum(1 for i in range(6) if self.player_pattern[i] == self.pattern[i])
        self.progress = matches / 6
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("SIGNAL MATCHING", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 100))
        
        # Instruction
        font_small = pygame.font.Font(None, 28)
        inst = font_small.render("Match the pattern shown above", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 150))
        
        # Timer
        timer_text = font_small.render(f"Time: {int(self.time_remaining)}s", True, COLOR_WARNING)
        screen.blit(timer_text, (center_x - timer_text.get_width() // 2, 200))
        
        # Target pattern
        start_x = center_x - 150
        for i, val in enumerate(self.pattern):
            x = start_x + i * 60
            y = center_y - 100
            color = COLOR_SAFETY if val == 1 else COLOR_UI_BG
            pygame.draw.rect(screen, color, (x, y, 50, 50))
            pygame.draw.rect(screen, COLOR_UI_TEXT, (x, y, 50, 50), 2)
        
        # Player pattern
        for i, val in enumerate(self.player_pattern):
            x = start_x + i * 60
            y = center_y
            color = COLOR_SAFETY if val == 1 else COLOR_UI_BG
            pygame.draw.rect(screen, color, (x, y, 50, 50))
            pygame.draw.rect(screen, COLOR_UI_TEXT, (x, y, 50, 50), 2)
        
        # Progress
        prog_text = font_small.render(f"Match: {int(self.progress * 100)}%", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, center_y + 100))


class PipeRepairGame(MiniGame):
    """Alternative Workshop game - Connect pipes correctly"""
    
    def __init__(self, escalation_stage):
        super().__init__('HEAT', escalation_stage)
        self.grid_size = 4
        self.pipes = []
        self.correct_path = []
        self.player_clicks = []
        self.start_pos = (0, random.randint(0, self.grid_size - 1))
        self.end_pos = (self.grid_size - 1, random.randint(0, self.grid_size - 1))
        self.setup_puzzle()
        
    def setup_puzzle(self):
        """Create pipe puzzle"""
        # Simple path for player to find
        self.correct_path = [self.start_pos]
        current = self.start_pos
        
        while current[0] < self.end_pos[0]:
            # Move right
            current = (current[0] + 1, current[1])
            self.correct_path.append(current)
            
            # Sometimes move up or down
            if current != self.end_pos and random.random() < 0.3:
                if current[1] < self.end_pos[1]:
                    current = (current[0], current[1] + 1)
                elif current[1] > self.end_pos[1]:
                    current = (current[0], current[1] - 1)
                self.correct_path.append(current)
    
    def update(self, dt, events):
        if not self.active:
            return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                cell_size = 80
                start_x = SCREEN_WIDTH // 2 - (self.grid_size * cell_size) // 2
                start_y = SCREEN_HEIGHT // 2 - (self.grid_size * cell_size) // 2
                
                # Check which cell was clicked
                for row in range(self.grid_size):
                    for col in range(self.grid_size):
                        rect = pygame.Rect(start_x + col * cell_size, 
                                         start_y + row * cell_size,
                                         cell_size - 5, cell_size - 5)
                        if rect.collidepoint(mouse_pos):
                            cell = (col, row)
                            if cell == self.start_pos or (self.player_clicks and cell == self.player_clicks[-1]):
                                continue
                            
                            # Check if adjacent to last click
                            if not self.player_clicks:
                                if cell == self.start_pos:
                                    self.player_clicks.append(cell)
                                    audio_manager.play_sound('success', 0.2)
                            else:
                                last = self.player_clicks[-1]
                                if abs(cell[0] - last[0]) + abs(cell[1] - last[1]) == 1:
                                    self.player_clicks.append(cell)
                                    audio_manager.play_sound('success', 0.2)
                                    
                                    # Check if reached end
                                    if cell == self.end_pos:
                                        # Check if path is valid
                                        if set(self.player_clicks) == set(self.correct_path):
                                            self.success = True
                                            self.active = False
                                            audio_manager.play_sound('success', 0.5)
                                        else:
                                            audio_manager.play_sound('fail', 0.5)
                                            self.player_clicks = []
                                else:
                                    audio_manager.play_sound('fail', 0.3)
                            
                            self.progress = len(self.player_clicks) / len(self.correct_path)
                            break
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("PIPE REPAIR", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 80))
        
        # Instruction
        font_small = pygame.font.Font(None, 24)
        inst = font_small.render("Connect the pipes from START to END", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 130))
        
        # Draw grid
        cell_size = 80
        start_x = center_x - (self.grid_size * cell_size) // 2
        start_y = SCREEN_HEIGHT // 2 - (self.grid_size * cell_size) // 2
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                cell = (col, row)
                
                # Color based on state
                if cell == self.start_pos:
                    color = COLOR_SAFE
                elif cell == self.end_pos:
                    color = COLOR_ALERT
                elif cell in self.player_clicks:
                    color = COLOR_HEAT
                else:
                    color = COLOR_UI_BG
                
                pygame.draw.rect(screen, color, (x, y, cell_size - 5, cell_size - 5))
                pygame.draw.rect(screen, COLOR_UI_TEXT, (x, y, cell_size - 5, cell_size - 5), 2)
                
                # Labels
                if cell == self.start_pos:
                    label = font_small.render("START", True, COLOR_UI_TEXT)
                    screen.blit(label, (x + (cell_size - label.get_width()) // 2, 
                                      y + (cell_size - label.get_height()) // 2))
                elif cell == self.end_pos:
                    label = font_small.render("END", True, COLOR_UI_TEXT)
                    screen.blit(label, (x + (cell_size - label.get_width()) // 2,
                                      y + (cell_size - label.get_height()) // 2))
        
        # Progress
        prog_text = font_small.render(f"Progress: {int(self.progress * 100)}%", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, SCREEN_HEIGHT - 100))


class WordUnscrambleGame(MiniGame):
    """Church Alternative - Unscramble winter words"""
    
    def __init__(self, escalation_stage):
        super().__init__('SANITY', escalation_stage)
        self.words = ['WINTER', 'FROZEN', 'BLIZZARD', 'SHELTER', 'SURVIVAL', 'SNOWFALL', 'MAYOR', 'VILLAGE']
        self.target_word = random.choice(self.words)
        self.scrambled = list(self.target_word)
        random.shuffle(self.scrambled)
        self.scrambled = ''.join(self.scrambled)
        self.player_answer = ""
        self.time_limit = 15 - escalation_stage
        self.time_remaining = self.time_limit
        
    def update(self, dt, events):
        if not self.active:
            return
        
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.active = False
            self.success = False
            audio_manager.play_sound('fail', 0.5)
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_answer = self.player_answer[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.player_answer.upper() == self.target_word:
                        self.success = True
                        self.active = False
                        audio_manager.play_sound('success', 0.5)
                    else:
                        audio_manager.play_sound('fail', 0.5)
                        self.player_answer = ""
                elif event.unicode.isalpha() and len(self.player_answer) < len(self.target_word):
                    self.player_answer += event.unicode.upper()
                    audio_manager.play_sound('success', 0.1)
        
        self.progress = len(self.player_answer) / len(self.target_word)
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        font = pygame.font.Font(None, 48)
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font.render("WORD UNSCRAMBLE", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 100))
        
        # Timer
        timer_text = font_small.render(f"Time: {int(self.time_remaining)}s", True, COLOR_WARNING)
        screen.blit(timer_text, (center_x - timer_text.get_width() // 2, 160))
        
        # Scrambled word
        scrambled_text = font_large.render(self.scrambled, True, COLOR_SANITY)
        screen.blit(scrambled_text, (center_x - scrambled_text.get_width() // 2, center_y - 60))
        
        # Input box
        input_box = pygame.Rect(center_x - 200, center_y + 50, 400, 60)
        pygame.draw.rect(screen, COLOR_UI_BG, input_box)
        pygame.draw.rect(screen, COLOR_UI_TEXT, input_box, 3)
        
        answer_text = font.render(self.player_answer, True, COLOR_UI_TEXT)
        screen.blit(answer_text, (input_box.centerx - answer_text.get_width() // 2,
                                 input_box.centery - answer_text.get_height() // 2))
        
        # Instructions
        inst = font_small.render("Type the unscrambled word and press ENTER", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, center_y + 130))


class MazeEscapeGame(MiniGame):
    """Sanity Alternative - Navigate a simple maze"""
    
    def __init__(self, escalation_stage):
        super().__init__('SANITY', escalation_stage)
        self.grid_size = 7
        self.player_pos = [0, 0]
        self.exit_pos = [self.grid_size - 1, self.grid_size - 1]
        self.walls = self.generate_maze()
        
    def generate_maze(self):
        """Generate random walls"""
        walls = set()
        for _ in range(8 + random.randint(0, 5)):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if [x, y] != [0, 0] and [x, y] != self.exit_pos:
                walls.add((x, y))
        return walls
    
    def update(self, dt, events):
        if not self.active:
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                old_pos = self.player_pos.copy()
                
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player_pos[1] -= 1
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player_pos[1] += 1
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player_pos[0] -= 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player_pos[0] += 1
                
                # Check bounds
                if (self.player_pos[0] < 0 or self.player_pos[0] >= self.grid_size or
                    self.player_pos[1] < 0 or self.player_pos[1] >= self.grid_size or
                    tuple(self.player_pos) in self.walls):
                    self.player_pos = old_pos
                    audio_manager.play_sound('fail', 0.2)
                else:
                    audio_manager.play_sound('success', 0.1)
                
                # Check win
                if self.player_pos == self.exit_pos:
                    self.success = True
                    self.active = False
                    audio_manager.play_sound('success', 0.5)
                
                # Update progress
                dist_start = abs(0 - self.player_pos[0]) + abs(0 - self.player_pos[1])
                dist_end = abs(self.exit_pos[0] - self.player_pos[0]) + abs(self.exit_pos[1] - self.player_pos[1])
                max_dist = self.grid_size * 2 - 2
                self.progress = 1.0 - (dist_end / max_dist)
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        font = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)
        
        # Title
        title = font.render("MAZE ESCAPE", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 80))
        
        # Instructions
        inst = font_small.render("Use WASD to reach the EXIT", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 130))
        
        # Draw maze
        cell_size = 60
        start_x = center_x - (self.grid_size * cell_size) // 2
        start_y = center_y - (self.grid_size * cell_size) // 2
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                cell_x = start_x + x * cell_size
                cell_y = start_y + y * cell_size
                
                if (x, y) in self.walls:
                    color = (60, 60, 80)
                elif [x, y] == self.exit_pos:
                    color = COLOR_SAFE
                else:
                    color = COLOR_UI_BG
                
                pygame.draw.rect(screen, color, (cell_x, cell_y, cell_size - 2, cell_size - 2))
                pygame.draw.rect(screen, COLOR_UI_TEXT, (cell_x, cell_y, cell_size - 2, cell_size - 2), 1)
        
        # Draw player
        player_x = start_x + self.player_pos[0] * cell_size + cell_size // 2
        player_y = start_y + self.player_pos[1] * cell_size + cell_size // 2
        pygame.draw.circle(screen, COLOR_SNOW, (player_x, player_y), cell_size // 3)
        
        # Progress
        prog_text = font_small.render(f"Progress: {int(self.progress * 100)}%", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, SCREEN_HEIGHT - 80))


class ResourceCountGame(MiniGame):
    """Alternative Farm game - Count resources quickly"""
    
    def __init__(self, escalation_stage):
        super().__init__('FOOD', escalation_stage)
        self.resource_types = ['🌾', '🥕', '🥔', '🍖']
        self.target_resource = random.choice(self.resource_types)
        self.correct_count = random.randint(8, 15)
        self.items = []
        self.player_count = 0
        self.time_limit = 12 - escalation_stage
        self.time_remaining = self.time_limit
        self.setup_items()
        
    def setup_items(self):
        """Create random items"""
        # Add correct amount of target
        for _ in range(self.correct_count):
            self.items.append(self.target_resource)
        
        # Add distractors
        for _ in range(random.randint(10, 20)):
            other = random.choice([r for r in self.resource_types if r != self.target_resource])
            self.items.append(other)
        
        random.shuffle(self.items)
    
    def update(self, dt, events):
        if not self.active:
            return
        
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.active = False
            self.success = False
            audio_manager.play_sound('fail', 0.5)
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    digit = int(event.unicode) if event.unicode.isdigit() else 0
                    self.player_count = self.player_count * 10 + digit
                    self.player_count = min(99, self.player_count)
                    audio_manager.play_sound('success', 0.2)
                
                elif event.key == pygame.K_BACKSPACE:
                    self.player_count = self.player_count // 10
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Check answer
                    if self.player_count == self.correct_count:
                        self.success = True
                        self.active = False
                        audio_manager.play_sound('success', 0.5)
                    else:
                        audio_manager.play_sound('fail', 0.5)
                        self.player_count = 0
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("RESOURCE COUNT", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 50))
        
        # Instruction
        font_small = pygame.font.Font(None, 28)
        inst = font_small.render(f"How many {self.target_resource} are there? Type the number.", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 100))
        
        # Timer
        timer_text = font_small.render(f"Time: {int(self.time_remaining)}s", True, COLOR_WARNING)
        screen.blit(timer_text, (center_x - timer_text.get_width() // 2, 140))
        
        # Display items in grid
        font_items = pygame.font.Font(None, 36)
        items_per_row = 12
        item_spacing = 50
        start_y = 200
        
        for i, item in enumerate(self.items):
            row = i // items_per_row
            col = i % items_per_row
            x = center_x - (items_per_row * item_spacing) // 2 + col * item_spacing
            y = start_y + row * item_spacing
            
            item_text = font_items.render(item, True, COLOR_UI_TEXT)
            screen.blit(item_text, (x, y))
        
        # Player input
        input_box = pygame.Rect(center_x - 100, SCREEN_HEIGHT - 150, 200, 50)
        pygame.draw.rect(screen, COLOR_UI_BG, input_box)
        pygame.draw.rect(screen, COLOR_UI_TEXT, input_box, 3)
        
        answer_text = font.render(str(self.player_count) if self.player_count > 0 else "?", True, COLOR_UI_TEXT)
        screen.blit(answer_text, (input_box.centerx - answer_text.get_width() // 2,
                                 input_box.centery - answer_text.get_height() // 2))
        
        # Submit instruction
        submit_text = font_small.render("Press ENTER to submit", True, COLOR_UI_TEXT)
        screen.blit(submit_text, (center_x - submit_text.get_width() // 2, SCREEN_HEIGHT - 80))


class ReactionTestGame(MiniGame):
    """Watchtower Alternative - Click when color changes"""
    
    def __init__(self, escalation_stage):
        super().__init__('SAFETY', escalation_stage)
        self.rounds_needed = 5
        self.rounds_completed = 0
        self.waiting = True
        self.wait_time = random.uniform(1, 3)
        self.reaction_window = 0.8
        self.timer = 0
        self.showing_target = False
        
    def update(self, dt, events):
        if not self.active:
            return
        
        self.timer += dt
        
        if self.waiting:
            if self.timer >= self.wait_time:
                self.showing_target = True
                self.waiting = False
                self.timer = 0
        elif self.showing_target:
            if self.timer >= self.reaction_window:
                # Too slow!
                audio_manager.play_sound('fail', 0.5)
                self.active = False
                self.success = False
                return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if self.showing_target:
                    # Good reaction!
                    self.rounds_completed += 1
                    self.progress = self.rounds_completed / self.rounds_needed
                    audio_manager.play_sound('success', 0.3)
                    
                    if self.rounds_completed >= self.rounds_needed:
                        self.success = True
                        self.active = False
                    else:
                        self.showing_target = False
                        self.waiting = True
                        self.wait_time = random.uniform(1, 3)
                        self.timer = 0
                elif self.waiting:
                    # Clicked too early!
                    audio_manager.play_sound('fail', 0.5)
                    self.active = False
                    self.success = False
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        font = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font.render("REACTION TEST", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 100))
        
        # Instructions
        if self.waiting:
            inst = font_small.render("Wait for GREEN...", True, COLOR_WARNING)
        else:
            inst = font_small.render("CLICK NOW!", True, COLOR_SAFE)
        screen.blit(inst, (center_x - inst.get_width() // 2, 160))
        
        # Target circle
        if self.showing_target:
            color = COLOR_SAFE
        else:
            color = COLOR_ALERT
        
        pygame.draw.circle(screen, color, (center_x, center_y), 100)
        pygame.draw.circle(screen, COLOR_UI_TEXT, (center_x, center_y), 100, 5)
        
        # Progress
        prog_text = font_small.render(f"Round: {self.rounds_completed + 1}/{self.rounds_needed}", True, COLOR_UI_TEXT)
        screen.blit(prog_text, (center_x - prog_text.get_width() // 2, SCREEN_HEIGHT - 100))


class CodeBreakerGame(MiniGame):
    """Watchtower Alternative - Break the code sequence"""
    
    def __init__(self, escalation_stage):
        super().__init__('SAFETY', escalation_stage)
        self.code_length = 4
        self.code = [random.randint(0, 3) for _ in range(self.code_length)]
        self.attempts = []
        self.max_attempts = 8
        self.current_guess = []
        self.symbols = ['●', '■', '▲', '★']
        self.button_positions = []
        self.setup_buttons()
        
    def setup_buttons(self):
        center_x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 + 100
        spacing = 80
        start_x = center_x - (len(self.symbols) * spacing) // 2
        
        for i, symbol in enumerate(self.symbols):
            x = start_x + i * spacing
            self.button_positions.append((x, y, i))
    
    def check_guess(self, guess):
        """Return (correct_position, correct_symbol)"""
        correct_pos = sum(1 for i in range(len(guess)) if guess[i] == self.code[i])
        correct_sym = sum(min(guess.count(x), self.code.count(x)) for x in set(guess)) - correct_pos
        return correct_pos, correct_sym
    
    def update(self, dt, events):
        if not self.active:
            return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check symbol buttons
                for x, y, idx in self.button_positions:
                    if pygame.Rect(x, y, 60, 60).collidepoint(mouse_pos):
                        if len(self.current_guess) < self.code_length:
                            self.current_guess.append(idx)
                            audio_manager.play_sound('success', 0.2)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.current_guess:
                        self.current_guess.pop()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if len(self.current_guess) == self.code_length:
                        correct_pos, correct_sym = self.check_guess(self.current_guess)
                        self.attempts.append((self.current_guess.copy(), correct_pos, correct_sym))
                        
                        if correct_pos == self.code_length:
                            self.success = True
                            self.active = False
                            audio_manager.play_sound('success', 0.5)
                        elif len(self.attempts) >= self.max_attempts:
                            self.success = False
                            self.active = False
                            audio_manager.play_sound('fail', 0.5)
                        else:
                            self.current_guess = []
                        
                        self.progress = len(self.attempts) / self.max_attempts
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        font = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 24)
        font_symbol = pygame.font.Font(None, 40)
        
        # Title
        title = font.render("CODE BREAKER", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 50))
        
        inst = font_small.render("Crack the code! ● = right place, ○ = wrong place", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 100))
        
        # Previous attempts
        y = 150
        for guess, correct_pos, correct_sym in self.attempts[-5:]:
            x = center_x - 150
            for symbol_idx in guess:
                symbol_text = font_symbol.render(self.symbols[symbol_idx], True, COLOR_UI_TEXT)
                screen.blit(symbol_text, (x, y))
                x += 50
            
            # Feedback
            feedback = f"  ●{correct_pos} ○{correct_sym}"
            feedback_text = font_small.render(feedback, True, COLOR_SAFE if correct_pos > 0 else COLOR_WARNING)
            screen.blit(feedback_text, (x + 20, y + 5))
            y += 40
        
        # Current guess
        x = center_x - 100
        y = SCREEN_HEIGHT // 2
        for symbol_idx in self.current_guess:
            symbol_text = font.render(self.symbols[symbol_idx], True, COLOR_SAFETY)
            screen.blit(symbol_text, (x, y))
            x += 50
        
        # Symbol buttons
        for x, y, idx in self.button_positions:
            pygame.draw.rect(screen, COLOR_UI_BG, (x, y, 60, 60))
            pygame.draw.rect(screen, COLOR_UI_TEXT, (x, y, 60, 60), 2)
            
            symbol_text = font.render(self.symbols[idx], True, COLOR_UI_TEXT)
            screen.blit(symbol_text, (x + 15, y + 10))
        
        # Attempts remaining
        attempts_text = font_small.render(f"Attempts: {len(self.attempts)}/{self.max_attempts}", True, COLOR_UI_TEXT)
        screen.blit(attempts_text, (center_x - attempts_text.get_width() // 2, SCREEN_HEIGHT - 80))
    """Alternative Farm game - Count resources quickly"""
    
    def __init__(self, escalation_stage):
        super().__init__('FOOD', escalation_stage)
        self.resource_types = ['🌾', '🥕', '🥔', '🍖']
        self.target_resource = random.choice(self.resource_types)
        self.correct_count = random.randint(8, 15)
        self.items = []
        self.player_count = 0
        self.time_limit = 12 - escalation_stage
        self.time_remaining = self.time_limit
        self.setup_items()
        
    def setup_items(self):
        """Create random items"""
        # Add correct amount of target
        for _ in range(self.correct_count):
            self.items.append(self.target_resource)
        
        # Add distractors
        for _ in range(random.randint(10, 20)):
            other = random.choice([r for r in self.resource_types if r != self.target_resource])
            self.items.append(other)
        
        random.shuffle(self.items)
    
    def update(self, dt, events):
        if not self.active:
            return
        
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.active = False
            self.success = False
            audio_manager.play_sound('fail', 0.5)
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    digit = int(event.unicode) if event.unicode.isdigit() else 0
                    self.player_count = self.player_count * 10 + digit
                    self.player_count = min(99, self.player_count)
                    audio_manager.play_sound('success', 0.2)
                
                elif event.key == pygame.K_BACKSPACE:
                    self.player_count = self.player_count // 10
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Check answer
                    if self.player_count == self.correct_count:
                        self.success = True
                        self.active = False
                        audio_manager.play_sound('success', 0.5)
                    else:
                        audio_manager.play_sound('fail', 0.5)
                        self.player_count = 0
    
    def render(self, screen):
        center_x = SCREEN_WIDTH // 2
        
        # Title
        font = pygame.font.Font(None, 48)
        title = font.render("RESOURCE COUNT", True, COLOR_UI_TEXT)
        screen.blit(title, (center_x - title.get_width() // 2, 50))
        
        # Instruction
        font_small = pygame.font.Font(None, 28)
        inst = font_small.render(f"How many {self.target_resource} are there? Type the number.", True, COLOR_UI_TEXT)
        screen.blit(inst, (center_x - inst.get_width() // 2, 100))
        
        # Timer
        timer_text = font_small.render(f"Time: {int(self.time_remaining)}s", True, COLOR_WARNING)
        screen.blit(timer_text, (center_x - timer_text.get_width() // 2, 140))
        
        # Display items in grid
        font_items = pygame.font.Font(None, 36)
        items_per_row = 12
        item_spacing = 50
        start_y = 200
        
        for i, item in enumerate(self.items):
            row = i // items_per_row
            col = i % items_per_row
            x = center_x - (items_per_row * item_spacing) // 2 + col * item_spacing
            y = start_y + row * item_spacing
            
            item_text = font_items.render(item, True, COLOR_UI_TEXT)
            screen.blit(item_text, (x, y))
        
        # Player input
        input_box = pygame.Rect(center_x - 100, SCREEN_HEIGHT - 150, 200, 50)
        pygame.draw.rect(screen, COLOR_UI_BG, input_box)
        pygame.draw.rect(screen, COLOR_UI_TEXT, input_box, 3)
        
        answer_text = font.render(str(self.player_count) if self.player_count > 0 else "?", True, COLOR_UI_TEXT)
        screen.blit(answer_text, (input_box.centerx - answer_text.get_width() // 2,
                                 input_box.centery - answer_text.get_height() // 2))
        
        # Submit instruction
        submit_text = font_small.render("Press ENTER to submit", True, COLOR_UI_TEXT)
        screen.blit(submit_text, (center_x - submit_text.get_width() // 2, SCREEN_HEIGHT - 80))


# Factory function
def create_minigame(system_type, escalation_stage):
    """Create appropriate mini-game for system"""
    games = {
        'HEAT': [FurnaceGame, PipeRepairGame],
        'FOOD': [SortingGame, ResourceCountGame],
        'SANITY': [SimonSaysGame, WordUnscrambleGame, MazeEscapeGame],
        'SAFETY': [SignalGame, ReactionTestGame, CodeBreakerGame],
    }
    
    # Pick random variation if multiple exist
    game_list = games.get(system_type, [FurnaceGame])
    game_class = random.choice(game_list)
    return game_class(escalation_stage)
