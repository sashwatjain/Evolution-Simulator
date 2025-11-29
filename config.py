SCREEN_W = 1400
SCREEN_H = 800

WORLD_W = 1000
WORLD_H = 800

FPS = 60

INITIAL_POP = 90             # better for 3 species (30 each)
NUM_PLANTS = 70              # more plants → stable early game

# Resource spawn rates
FRUIT_SPAWN_RATE = 0.020     # strong improvement
WATER_SPAWN_RATE  = 0.025    # must be close to fruit rate

FAST_FORWARD_MULT = 10

# Resource value per consumption
FOOD_VALUE = 100.0            # balanced
WATER_VALUE = 75.0           # vital for survival

# Lifespan
MAX_AGE = 1000                # speed * 600 = excellent balance

# Mutation types
MUTATION_TYPES = ["gaussian", "salt_and_pepper", "drift"]

HISTORY_SIZE = 500
GRID_CELL = 60

MAX_ENERGY = 120.0
MAX_WATER = 90.0

# Species config (tuned for stability + fair competition)

SPECIES = {
    "red": {
        "base_color": (255, 50, 50),
        "default_genome": {
            "speed": 1.6,
            "size": 1.1,
            "metabolism": 0.18,           # lower so red survives better
            "vision": 140,                # slightly higher vision
            "repro_energy_threshold": 55, # reduced threshold
            "repro_water_threshold": 35,  # easier reproduction
            "mutation_rate": 0.8
        }
    },

    "green": {
        "base_color": (50, 255, 50),
        "default_genome": {
            "speed": 1.5,                 # slightly reduced → fairness
            "size": 1.4,                  # heavier, but survives if food is good
            "metabolism": 0.15,           # must remain low
            "vision": 160,                # excellent detection
            "repro_energy_threshold": 50,
            "repro_water_threshold": 30,
            "mutation_rate": 0.3
        }
    },

    "blue": {
        "base_color": (50, 120, 255),
        "default_genome": {
            "speed": 1.8,
            "size": 0.9,
            "metabolism": 0.25,           # medium drain
            "vision": 150,
            "repro_energy_threshold": 55, # lowered → earlier reproduction
            "repro_water_threshold": 35,
            "mutation_rate": 0.4
        }
    }
}

