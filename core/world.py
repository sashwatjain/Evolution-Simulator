# core/world.py
import random, math
from core.utils import clamp
from config import WORLD_W, WORLD_H, WATER_SPAWN_RATE, FRUIT_SPAWN_RATE

class Plant:
    def __init__(self, x, y, is_water=False):
        self.x = x
        self.y = y
        self.is_water = is_water

        self.capacity = random.randint(2, 4)
        self.food = 0
        self.water = 0

    def update(self):
        if not self.is_water:
            # spawn fruits
            if self.food < self.capacity and random.random() < FRUIT_SPAWN_RATE:
                self.food += 1
        else:
            # spawn water droplets
            if self.water < self.capacity and random.random() < WATER_SPAWN_RATE:
                self.water += 1

    def take_food(self):
        if self.food > 0:
            self.food -= 1
            return True
        return False

    def take_water(self):
        if self.water > 0:
            self.water -= 1
            return True
        return False
