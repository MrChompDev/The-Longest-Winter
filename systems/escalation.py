"""
Escalation system - handles progressive difficulty scaling
"""
from settings import *


class EscalationManager:
    """Manages game-wide escalation and difficulty scaling"""
    
    def __init__(self, meter_manager, task_manager):
        self.meter_manager = meter_manager
        self.task_manager = task_manager
        self.global_stage = 1
        
    def update(self, elapsed_time):
        """Update escalation based on time and system states"""
        # Calculate global escalation stage
        critical_count = len(self.meter_manager.get_critical_systems())
        collapsed_count = self.meter_manager.get_collapsed_count()
        
        # Determine global stage
        if collapsed_count >= 1:
            self.global_stage = 3
        elif critical_count >= 2:
            self.global_stage = 3
        elif critical_count >= 1:
            self.global_stage = 2
        else:
            self.global_stage = 1
        
        # Adjust task spawning based on escalation
        if self.global_stage == 3:
            self.task_manager.max_tasks = 5
            self.task_manager.min_tasks = 3
        elif self.global_stage == 2:
            self.task_manager.max_tasks = 4
            self.task_manager.min_tasks = 2
        else:
            self.task_manager.max_tasks = 3
            self.task_manager.min_tasks = 2
    
    def get_environmental_effects(self):
        """Get current environmental effects based on system states"""
        effects = {
            'vision_reduction': 0,
            'movement_penalty': 0,
            'ui_distortion': False,
            'phantom_tasks': False
        }
        
        # Heat effects
        heat_meter = self.meter_manager.meters['HEAT']
        if heat_meter.is_critical():
            effects['vision_reduction'] = 0.3
            effects['movement_penalty'] = 0.2
        
        # Food effects
        food_meter = self.meter_manager.meters['FOOD']
        if food_meter.is_critical():
            effects['movement_penalty'] += 0.15
        
        # Sanity effects
        sanity_meter = self.meter_manager.meters['SANITY']
        if sanity_meter.is_critical():
            effects['ui_distortion'] = True
        
        # Safety effects
        safety_meter = self.meter_manager.meters['SAFETY']
        if safety_meter.is_critical():
            effects['phantom_tasks'] = True
        
        return effects
    
    def get_minigame_difficulty(self, system_type):
        """Get difficulty modifier for a specific system's mini-game"""
        meter = self.meter_manager.meters[system_type]
        return meter.escalation_stage
