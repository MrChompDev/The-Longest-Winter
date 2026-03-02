"""
Utility functions and helpers
"""
import pygame
from settings import *


def draw_text_centered(screen, text, font, color, y):
    """Draw centered text at given y position"""
    text_surface = font.render(text, True, color)
    x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
    screen.blit(text_surface, (x, y))
    return text_surface


def draw_text(screen, text, font, color, x, y):
    """Draw text at given position"""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    return text_surface


def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t


def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


class Button:
    """Simple button helper"""
    
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
    
    def update(self, mouse_pos):
        """Update button state"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            return True
        return False
    
    def render(self, screen):
        """Render button"""
        color = COLOR_WARNING if self.hovered else COLOR_UI_BG
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_UI_TEXT, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, COLOR_UI_TEXT)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))
