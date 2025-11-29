import random
from core.utils import clamp
from config import MUTATION_TYPES, SPECIES

GENE_SCHEMA = [
    ("speed", (0.2, 3.5)),
    ("size", (0.4, 3.0)),
    ("metabolism", (0.3, 2.5)),
    ("vision", (20, 150)),
    ("repro_energy_threshold", (60, 220)),
    ("repro_water_threshold", (30, 160)),
    ("mutation_rate", (0.005, 0.20)),
]


# -------------------------------------------------------
#  NEW GENOME: correctly initialize mutation_type + color
# -------------------------------------------------------
def random_genome_for_species(species_name, sex):
    base = SPECIES[species_name]["default_genome"]
    g = base.copy()

    # Color inherited from species
    g["cr"] = SPECIES[species_name]["base_color"][0] / 255
    g["cg"] = SPECIES[species_name]["base_color"][1] / 255
    g["cb"] = SPECIES[species_name]["base_color"][2] / 255

    # ensure color genes clamped
    g["cr"] = clamp(g["cr"], 0.0, 1.0)
    g["cg"] = clamp(g["cg"], 0.0, 1.0)
    g["cb"] = clamp(g["cb"], 0.0, 1.0)

    g["species"] = species_name
    g["sex"] = sex

    # --- CRITICAL FIX: ALWAYS give mutation_type ---
    g["mutation_type"] = random.choice(MUTATION_TYPES)

    return g


# -------------------------------------------------------
#  CROSSOVER: blend numeric + color, inherit categorical
# -------------------------------------------------------
def crossover(g1, g2):
    child = {}

    for key in g1:

        if key in ("species", "mutation_type"):
            child[key] = random.choice([g1[key], g2[key]])
            continue

        if key == "sex":
            continue  # assign after

        if key in ("cr", "cg", "cb"):
            child[key] = (g1[key] + g2[key]) / 2
            continue

        # numeric genes
        v1 = g1[key]
        v2 = g2[key]

        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            child[key] = (v1 + v2) / 2
        else:
            child[key] = random.choice([v1, v2])

    # assign sex
    child["sex"] = random.choice(["male", "female"])

    # ensure mutation_type exists
    if "mutation_type" not in child:
        child["mutation_type"] = random.choice(MUTATION_TYPES)

    # ensure color clamped
    for c in ("cr", "cg", "cb"):
        child[c] = clamp(child[c], 0.0, 1.0)

    return child


# -------------------------------------------------------
#  MUTATION: safe bounded mutation + color clamping
# -------------------------------------------------------
def mutate(genome):
    mtype = genome["mutation_type"]
    mr = genome["mutation_rate"]

    new = genome.copy()

    # numeric genes
    for key, (lo, hi) in GENE_SCHEMA:
        if random.random() > mr:
            continue

        if mtype == "gaussian":
            delta = random.gauss(0, (hi - lo) * 0.05)
            new[key] = clamp(new[key] + delta, lo, hi)

        elif mtype == "salt_and_pepper":
            if random.random() < 0.2:
                new[key] = random.uniform(lo, hi)
            else:
                delta = random.gauss(0, (hi - lo) * 0.02)
                new[key] = clamp(new[key] + delta, lo, hi)

        elif mtype == "drift":
            drift_amount = (hi - lo) * 0.015
            direction = random.choice([-1, 1])
            new[key] = clamp(new[key] + drift_amount * direction, lo, hi)

    # small chance to flip mutation strategy
    if random.random() < mr * 0.08:
        new["mutation_type"] = random.choice(MUTATION_TYPES)

    # color mutation
    if random.random() < mr:
        new["cr"] += random.gauss(0, 0.03)
    if random.random() < mr:
        new["cg"] += random.gauss(0, 0.03)
    if random.random() < mr:
        new["cb"] += random.gauss(0, 0.03)

    # --- CRITICAL FIX: clamp color safely ---
    new["cr"] = clamp(new["cr"], 0.0, 1.0)
    new["cg"] = clamp(new["cg"], 0.0, 1.0)
    new["cb"] = clamp(new["cb"], 0.0, 1.0)

    return new
