"""
Task system - manages task queue and spawning
"""
import random
import time
from settings import *


class Task:
    """A single task that needs to be completed"""
    
    def __init__(self, system_type, building_name, urgency=1):
        self.system_type = system_type  # HEAT, FOOD, SANITY, SAFETY
        self.building_name = building_name
        self.urgency = urgency  # 1-3
        self.spawn_time = time.time()
        self.age = 0
    
    def update(self, dt):
        """Update task age"""
        self.age = time.time() - self.spawn_time
    
    def is_urgent(self):
        """Check if task has become urgent"""
        return self.age > 30 or self.urgency >= 3


class TaskManager:
    """Manages the task queue and spawning"""
    
    def __init__(self, meter_manager):
        self.meter_manager = meter_manager
        self.active_tasks = []
        self.next_spawn_time = time.time() + random.uniform(2, 4)
        self.min_tasks = 2
        self.max_tasks = 4
        
    def update(self, dt):
        """Update all tasks and spawn new ones"""
        # Update existing tasks
        for task in self.active_tasks:
            task.update(dt)
        
        # Spawn new tasks if needed
        current_time = time.time()
        if current_time >= self.next_spawn_time:
            if len(self.active_tasks) < self.max_tasks:
                self._spawn_task()
            self.next_spawn_time = current_time + random.uniform(TASK_SPAWN_MIN, TASK_SPAWN_MAX)
        
        # Ensure minimum tasks
        while len(self.active_tasks) < self.min_tasks:
            self._spawn_task()
    
    def _spawn_task(self):
        """Spawn a new task based on system states"""
        # Weight by which systems are lowest
        weights = {}
        for name, meter in self.meter_manager.meters.items():
            if meter.value > 0:  # Don't spawn tasks for collapsed systems
                # Lower value = higher weight
                weights[name] = max(1, int((100 - meter.value) / 10))
        
        if not weights:
            return
        
        # Select system
        systems = list(weights.keys())
        system_weights = list(weights.values())
        system_type = random.choices(systems, weights=system_weights)[0]
        
        # Find building for this system
        building_name = None
        for bldg, info in BUILDINGS.items():
            if info['system'] == system_type:
                building_name = info['name']
                break
        
        if building_name:
            urgency = self.meter_manager.meters[system_type].escalation_stage
            task = Task(system_type, building_name, urgency)
            self.active_tasks.append(task)
    
    def complete_task(self, building_name):
        """Complete a task at the given building"""
        for task in self.active_tasks[:]:
            if task.building_name == building_name:
                self.active_tasks.remove(task)
                return task
        return None
    
    def get_tasks_for_building(self, building_name):
        """Get all tasks for a specific building"""
        return [t for t in self.active_tasks if t.building_name == building_name]
