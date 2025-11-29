# core/organisms.py
import random
import math
from core.utils import clamp
from config import FOOD_VALUE, WATER_VALUE, MAX_AGE

class Organism:
    next_id = 0

    def __init__(self, x, y, genome):
        self.id = Organism.next_id
        Organism.next_id += 1

        self.eat_cooldown = 0        # <-- add this
        self.drink_cooldown = 0
        
        self.x = x
        self.y = y

        self.age = 0
        self.energy = random.uniform(40, 80)
        self.water = random.uniform(40, 80)
        self.genome = genome

        self.repro_cooldown = 0
        self.children = 0
        self.parent_ids = ()

        self.angle = random.random() * math.tau
        self.turn_rate = 0.12

    @property
    def color(self):
        return (
            int(255 * clamp(self.genome["cr"], 0, 1)),
            int(255 * clamp(self.genome["cg"], 0, 1)),
            int(255 * clamp(self.genome["cb"], 0, 1)),
        )
    @property
    def species(self):
        return self.genome["species"]

    @property
    def sex(self):
        return self.genome["sex"]


    def radius(self):
        return int(4 + self.genome["size"] * 4)

    def step_cost(self):
        return self.genome["metabolism"] * self.genome["size"] * 0.05
