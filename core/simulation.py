# core/simulation.py
import random
import math
import numpy as np
from collections import deque, defaultdict

from config import (
    WORLD_W, WORLD_H, INITIAL_POP, NUM_PLANTS, HISTORY_SIZE,
    FOOD_VALUE, WATER_VALUE, MAX_ENERGY, MAX_WATER
)

from core.genome import random_genome_for_species, crossover, mutate
from core.organisms import Organism
from core.world import Plant
from core.physics import move_toward, wander, clamp_position

class Simulation:

    def __init__(self):
        self.pop_history = deque(maxlen=HISTORY_SIZE)
        self.speed_hist = deque(maxlen=HISTORY_SIZE)
        self.size_hist = deque(maxlen=HISTORY_SIZE)
        self.mutation_perf = defaultdict(lambda: {"offspring": 0, "mean_energy": 0})
        # Species population history
        self.species_history = {
            "red": deque(maxlen=HISTORY_SIZE),
            "green": deque(maxlen=HISTORY_SIZE),
            "blue": deque(maxlen=HISTORY_SIZE),
}


        self.reset()

    def reset(self):
        # plants
        self.plants = []
        for i in range(NUM_PLANTS):
            # half food, half water plants
            if i % 2 == 0:
                self.plants.append(Plant(
                    random.uniform(20, WORLD_W - 20),
                    random.uniform(20, WORLD_H - 20),
                    is_water=False
                ))
            else:
                self.plants.append(Plant(
                    random.uniform(20, WORLD_W - 20),
                    random.uniform(20, WORLD_H - 20),
                    is_water=True
                ))

        # initial agents: balanced mutation groups
        self.agents = []
        from config import MUTATION_TYPES
        species_list = ["red", "green", "blue"]
        per = INITIAL_POP // 3

        for sp in species_list:
            for _ in range(per):
                sex = random.choice(["male","female"])
                g = random_genome_for_species(sp, sex)
                self.agents.append(
                    Organism(
                        random.uniform(30, WORLD_W - 30),
                        random.uniform(30, WORLD_H - 30),
                        g
                    )
                )

        self.tick = 0

        self.pop_history = deque(maxlen=HISTORY_SIZE)
        self.speed_hist = deque(maxlen=HISTORY_SIZE)
        self.size_hist = deque(maxlen=HISTORY_SIZE)
        self.mutation_perf = defaultdict(lambda: {"offspring": 0, "mean_energy": 0})

    def step(self):
        self.tick += 1

        # --- update plants ---
        for p in self.plants:
            p.update()

        random.shuffle(self.agents)

        newborns = []
        alive = []

        for a in self.agents:

            # decrement cooldowns
            if a.repro_cooldown > 0:
                a.repro_cooldown -= 1
            if getattr(a, "eat_cooldown", 0) > 0:
                a.eat_cooldown -= 1
            if getattr(a, "drink_cooldown", 0) > 0:
                a.drink_cooldown -= 1

            # movement: decide target and move with hunger factor
            target = self.find_target(a)
            if target:
                move_toward(a, *target, hunger_factor=self.get_hunger_factor(a))
            else:
                wander(a, hunger_factor=self.get_hunger_factor(a))

            clamp_position(a, WORLD_W, WORLD_H)

            # --- EATING & DRINKING WITH CAPS + COOLDOWN + NUDGE ---
            # check nearby plants (small radius) and attempt eat/drink only if cooldown allows
            for p in self.plants:
                if abs(p.x - a.x) < 10 and abs(p.y - a.y) < 10:

                    # DRINK (water plants)
                    if p.is_water and a.water < MAX_WATER and a.drink_cooldown <= 0:
                        if p.take_water():
                            a.water = min(MAX_WATER, a.water + WATER_VALUE)
                            a.drink_cooldown = 6                # small cool-down (6 ticks)
                            # nudge away a little so they don't sit exactly on the plant
                            a.angle += random.uniform(0.6, 2.0)
                            break  # consumed something this tick -> stop checking other plants

                    # EAT (food plants)
                    elif (not p.is_water) and a.energy < MAX_ENERGY and a.eat_cooldown <= 0:
                        if p.take_food():
                            a.energy = min(MAX_ENERGY, a.energy + FOOD_VALUE)
                            a.eat_cooldown = 6                  # small cool-down (6 ticks)
                            # nudge away a little so they don't camp
                            a.angle += random.uniform(0.6, 2.0)
                            break  # consumed something this tick -> stop checking other plants

            # degrade resources (apply after eating so they don't immediately die)
            a.energy -= a.step_cost()
            a.water -= 0.02

            # reproduction (female seeks male of same species nearby)
            if (
                a.energy > a.genome["repro_energy_threshold"]
                and a.water > a.genome["repro_water_threshold"]
                and a.repro_cooldown <= 0
                and a.sex == "female"
            ):
                mate = self.find_mate_same_species(a)
                if mate and mate.sex == "male":
                    child_gen = mutate(crossover(a.genome, mate.genome))
                    newborns.append(
                        Organism(
                            (a.x + mate.x) / 2 + random.uniform(-5, 5),
                            (a.y + mate.y) / 2 + random.uniform(-5, 5),
                            child_gen,
                        )
                    )
                    # shared cost and cooldown
                    a.energy *= 0.6
                    mate.energy *= 0.6
                    a.water *= 0.6
                    mate.water *= 0.6
                    a.repro_cooldown = 20
                    mate.repro_cooldown = 20

            # age & death
            a.age += 1
            if a.age < a.genome["speed"] * 400 and a.energy > 0 and a.water > 0:
                alive.append(a)
            # else: organism removed (dies) and will not be added to alive

        # --- finalize new population ---
        self.agents = alive + newborns

        # --- Species population tracking ---
        counts = {"red": 0, "green": 0, "blue": 0}
        for a in self.agents:
            sp = a.species
            if sp in counts:
                counts[sp] += 1
        for sp in counts:
            self.species_history[sp].append(counts[sp])

        # --- existing global stats ---
        self.pop_history.append(len(self.agents))
        if self.agents:
            self.speed_hist.append(np.mean([ag.genome["speed"] for ag in self.agents]))
            self.size_hist.append(np.mean([ag.genome["size"] for ag in self.agents]))
        else:
            self.speed_hist.append(0)
            self.size_hist.append(0)


    def find_target(self, a):
        best = None
        best_d = 1e9

        for p in self.plants:

            # ---------------------------
            # IGNORE food if energy full
            # IGNORE water if hydration full
            # ---------------------------

            if p.is_water:
                if a.water >= MAX_WATER or p.water <= 0:
                    continue
            else:
                if a.energy >= MAX_ENERGY or p.food <= 0:
                    continue

            dx = p.x - a.x
            dy = p.y - a.y
            d2 = dx*dx + dy*dy

            if d2 < best_d and math.sqrt(d2) < a.genome["vision"]:
                best_d = d2
                best = (p.x, p.y)

        return best


    def find_mate_same_species(self, a):
        for b in self.agents:
            if b is a: continue
            if b.species != a.species: continue
            if b.sex == a.sex: continue
            if b.energy < b.genome["repro_energy_threshold"]: continue
            if b.water < b.genome["repro_water_threshold"]: continue

            dx = b.x - a.x
            dy = b.y - a.y
            if dx*dx + dy*dy < (a.genome["vision"] * 0.8)**2:
                return b
        return None


    def get_hunger_factor(self, a):
        # fullness values 0-1
        e = a.energy / MAX_ENERGY
        w = a.water  / MAX_WATER
        fullness = min(e, w)

        # hunger grows as fullness drops
        hunger = 1 - fullness

        # prevent too-low speeds (cause of stuck behavior)
        return max(0.5, hunger)


