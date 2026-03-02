"""
Enhanced graphics and visual effects
"""
import pygame
import math
from settings import *


def draw_rounded_rect(surface, color, rect, radius=10):
    """Draw a rounded rectangle"""
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2*radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2*radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)


def draw_shadow(surface, rect, offset=5, alpha=100):
    """Draw a shadow behind a rect"""
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shadow.fill((0, 0, 0, alpha))
    surface.blit(shadow, (rect.x + offset, rect.y + offset))


def draw_gradient_rect(surface, color1, color2, rect, vertical=True):
    """Draw a gradient filled rectangle"""
    x, y, w, h = rect
    if vertical:
        for i in range(h):
            ratio = i / h
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
    else:
        for i in range(w):
            ratio = i / w
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (x + i, y), (x + i, y + h))


def draw_glow(surface, pos, radius, color, intensity=255):
    """Draw a glowing circle effect"""
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(radius, 0, -2):
        alpha = int((i / radius) * intensity)
        pygame.draw.circle(glow_surface, (*color, alpha), (radius, radius), i)
    surface.blit(glow_surface, (pos[0] - radius, pos[1] - radius))


def draw_particles(surface, particles, color=COLOR_SNOW):
    """Draw snow or other particles with glow"""
    for particle in particles:
        x, y = int(particle['x']), int(particle['y'])
        size = particle['size']
        # Main particle
        pygame.draw.circle(surface, color, (x, y), size)
        # Subtle glow
        if size > 1:
            glow_color = (*color[:3], 100)
            pygame.draw.circle(surface, glow_color, (x, y), size + 1)


def draw_meter_bar(surface, x, y, width, height, value, max_value, color, bg_color=COLOR_UI_BG):
    """Draw an enhanced meter bar with gradient and glow"""
    # Background
    bg_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, bg_color, bg_rect, 5)
    
    # Fill with gradient
    if value > 0:
        fill_width = int((value / max_value) * width)
        fill_rect = pygame.Rect(x, y, fill_width, height)
        
        # Gradient from darker to lighter
        color_dark = tuple(max(0, c - 40) for c in color)
        draw_gradient_rect(surface, color_dark, color, fill_rect)
        
        # Glow on critical
        if value < max_value * 0.3:
            glow_intensity = int(abs(math.sin(pygame.time.get_ticks() / 300)) * 100)
            pygame.draw.rect(surface, (*COLOR_ALERT, glow_intensity), fill_rect, 2)
    
    # Border
    pygame.draw.rect(surface, (200, 200, 200), bg_rect, 2, border_radius=5)
    
    # Shine effect
    shine = pygame.Surface((width, height // 3), pygame.SRCALPHA)
    shine.fill((255, 255, 255, 30))
    surface.blit(shine, (x, y))


def draw_button_3d(surface, rect, color, text, font, pressed=False):
    """Draw a 3D-looking button"""
    offset = 2 if pressed else 0
    
    # Shadow
    shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
    draw_rounded_rect(surface, (0, 0, 0, 100), shadow_rect, 8)
    
    # Button body
    button_rect = pygame.Rect(rect.x + offset, rect.y + offset, rect.width, rect.height)
    color_light = tuple(min(255, c + 30) for c in color)
    color_dark = tuple(max(0, c - 30) for c in color)
    draw_gradient_rect(surface, color_light, color_dark, button_rect)
    
    # Border
    border_color = tuple(max(0, c - 50) for c in color)
    pygame.draw.rect(surface, border_color, button_rect, 3, border_radius=8)
    
    # Text
    text_surface = font.render(text, True, (255, 255, 255))
    text_pos = (button_rect.centerx - text_surface.get_width() // 2,
                button_rect.centery - text_surface.get_height() // 2)
    surface.blit(text_surface, text_pos)


def draw_player_enhanced(surface, x, y, radius=20):
    """Draw an enhanced Among Us style player"""
    # Shadow
    shadow_surf = pygame.Surface((radius * 3, radius * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, radius * 3, radius * 2))
    surface.blit(shadow_surf, (int(x - radius * 1.5), int(y + radius * 0.7)))
    
    # Body outline (darker)
    body_outline = tuple(max(0, c - 40) for c in COLOR_SNOW)
    pygame.draw.circle(surface, body_outline, (int(x), int(y - 5)), radius + 2)
    pygame.draw.rect(surface, body_outline, 
                    (int(x - radius), int(y - 5), radius * 2, radius + 5))
    pygame.draw.circle(surface, body_outline, (int(x), int(y + radius)), radius + 2)
    
    # Body main
    pygame.draw.circle(surface, COLOR_SNOW, (int(x), int(y - 5)), radius)
    pygame.draw.rect(surface, COLOR_SNOW, 
                    (int(x - radius + 2), int(y - 5), (radius - 2) * 2, radius))
    pygame.draw.circle(surface, COLOR_SNOW, (int(x), int(y + radius - 5)), radius)
    
    # Visor with shine
    visor_color = (60, 120, 200)
    visor_rect = pygame.Rect(int(x - radius * 0.6), int(y - 12), int(radius * 1.2), 10)
    pygame.draw.ellipse(surface, visor_color, visor_rect)
    
    # Visor shine
    shine_rect = pygame.Rect(visor_rect.x + 2, visor_rect.y + 1, visor_rect.width // 2, 4)
    pygame.draw.ellipse(surface, (120, 180, 255, 150), shine_rect)
    
    # Backpack detail
    pack_color = tuple(max(0, c - 20) for c in COLOR_SNOW)
    pygame.draw.circle(surface, pack_color, (int(x + radius * 0.6), int(y)), int(radius * 0.4))


def draw_building_enhanced(surface, building_info, x, y, meter=None):
    """Draw an enhanced building with details"""
    w, h = building_info['size']
    base_color = building_info['color']
    
    # Adjust color based on meter
    if meter:
        if meter.is_collapsed():
            base_color = COLOR_ALERT
        elif meter.is_critical():
            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() / 500))
            base_color = tuple(int(c * (0.7 + pulse * 0.3)) for c in COLOR_WARNING)
    
    # Shadow
    shadow_rect = pygame.Rect(x - w//2 + 5, y - h//2 + 5, w, h)
    pygame.draw.rect(surface, (0, 0, 0, 80), shadow_rect, border_radius=5)
    
    # Building body with gradient
    building_rect = pygame.Rect(x - w//2, y - h//2, w, h)
    color_light = tuple(min(255, c + 20) for c in base_color)
    color_dark = tuple(max(0, c - 20) for c in base_color)
    draw_gradient_rect(surface, color_light, color_dark, building_rect)
    
    # Roof
    roof_color = tuple(max(0, c - 40) for c in base_color)
    roof_points = [
        (x - w//2 - 5, y - h//2),
        (x, y - h//2 - 15),
        (x + w//2 + 5, y - h//2)
    ]
    pygame.draw.polygon(surface, roof_color, roof_points)
    pygame.draw.polygon(surface, (0, 0, 0, 100), roof_points, 2)
    
    # Windows with glow
    window_color = (255, 255, 200, 200)
    window_glow = (255, 255, 150, 100)
    
    if building_info['name'] == 'Town Hall':
        # Multiple windows
        for wx in [-30, 0, 30]:
            for wy in [-20, 10]:
                window_rect = pygame.Rect(x + wx - 8, y + wy - 6, 16, 12)
                pygame.draw.rect(surface, window_glow, 
                               pygame.Rect(window_rect.x - 2, window_rect.y - 2, 
                                         window_rect.width + 4, window_rect.height + 4))
                pygame.draw.rect(surface, window_color, window_rect)
    else:
        # Regular windows
        for wx in [-15, 15]:
            window_rect = pygame.Rect(x + wx - 8, y - 10, 16, 12)
            pygame.draw.rect(surface, window_glow, 
                           pygame.Rect(window_rect.x - 2, window_rect.y - 2, 
                                     window_rect.width + 4, window_rect.height + 4))
            pygame.draw.rect(surface, window_color, window_rect)
    
    # Door
    door_rect = pygame.Rect(x - 12, y + h//2 - 25, 24, 25)
    door_color = tuple(max(0, c - 60) for c in base_color)
    pygame.draw.rect(surface, door_color, door_rect, border_radius=3)
    pygame.draw.rect(surface, (0, 0, 0, 150), door_rect, 2, border_radius=3)
    
    # Door knob
    pygame.draw.circle(surface, (200, 180, 100), (x + 8, y + h//2 - 12), 3)
    
    # Border
    border_color = tuple(max(0, c - 50) for c in base_color)
    pygame.draw.rect(surface, border_color, building_rect, 3, border_radius=5)


def draw_task_indicator(surface, x, y, urgent=False, count=1):
    """Draw an enhanced task indicator with pulsing animation"""
    import time
    pulse = abs(math.sin(time.time() * 3))
    base_radius = 10
    radius = base_radius + int(pulse * 5)
    
    # Glow
    color = COLOR_ALERT if urgent else COLOR_WARNING
    draw_glow(surface, (x, y), radius + 10, color, intensity=100)
    
    # Main indicator
    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, (255, 255, 255), (x, y), radius, 2)
    
    # Count
    if count > 1:
        font = pygame.font.Font(None, 20)
        text = font.render(str(count), True, (255, 255, 255))
        surface.blit(text, (x - text.get_width()//2, y - text.get_height()//2))
