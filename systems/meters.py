"""
Meter system - manages individual system meters (Heat, Food, Sanity, Safety)
"""
from settings import *


class Meter:
    """A single village system meter"""
    
    def __init__(self, name, drain_rate, color):
        self.name = name
        self.value = 100.0  # 0-100
        self.drain_rate = drain_rate
        self.color = color
        self.escalation_stage = 0
        
    def update(self, dt):
        """Drain meter over time"""
        # Apply escalation multiplier
        multiplier = 1.0 + (self.escalation_stage * 0.5)
        self.value -= self.drain_rate * dt * multiplier
        self.value = max(0, min(100, self.value))
        
        # Update escalation stage
        if self.value < ESCALATION_STAGE_3 * 100:
            self.escalation_stage = 3
        elif self.value < ESCALATION_STAGE_2 * 100:
            self.escalation_stage = 2
        else:
            self.escalation_stage = 1
    
    def restore(self, amount):
        """Restore meter value"""
        self.value = min(100, self.value + amount)
    
    def is_critical(self):
        """Check if meter is in critical state"""
        return self.value < 20
    
    def is_collapsed(self):
        """Check if system has collapsed"""
        return self.value <= 0


class MeterManager:
    """Manages all village system meters"""
    
    def __init__(self):
        self.meters = {
            'HEAT': Meter('Heat', HEAT_DRAIN_RATE, COLOR_HEAT),
            'FOOD': Meter('Food', FOOD_DRAIN_RATE, COLOR_FOOD),
            'SANITY': Meter('Sanity', SANITY_DRAIN_RATE, COLOR_SANITY),
            'SAFETY': Meter('Safety', SAFETY_DRAIN_RATE, COLOR_SAFETY),
        }
    
    def update(self, dt):
        """Update all meters"""
        for meter in self.meters.values():
            meter.update(dt)
    
    def get_collapsed_count(self):
        """Count how many systems have collapsed"""
        return sum(1 for m in self.meters.values() if m.is_collapsed())
    
    def get_critical_systems(self):
        """Get list of critical systems"""
        return [name for name, meter in self.meters.items() if meter.is_critical()]
