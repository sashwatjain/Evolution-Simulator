# rendering/graphs.py

import pygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io

from config import HISTORY_SIZE, MUTATION_TYPES

def render_stats(sim, width, height):

    fig = plt.figure(figsize=(width/100, height/100), dpi=100)
    gs = fig.add_gridspec(4,1, height_ratios=[1,1,1,1])

    # 1. Population
    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(sim.pop_history, linewidth=2)
    ax1.set_title("Population")

    # 2. Avg Speed & Size
    ax2 = fig.add_subplot(gs[1,0])
    ax2.plot(sim.speed_hist, label="avg speed")
    ax2.plot(sim.size_hist, label="avg size")
    ax2.legend()
    ax2.set_title("Traits")

    # 3. Mutation performance
    ax3 = fig.add_subplot(gs[2,0])
    mut = ["gaussian", "salt_and_pepper", "drift"]
    offs = [sim.mutation_perf[m]["offspring"] for m in mut]
    ax3.bar(mut, offs)
    ax3.set_title("Mutation Strategy Offspring Count")

    # 4. Species populations
    ax4 = fig.add_subplot(gs[3,0])
    ax4.plot(sim.species_history["red"], color="red", label="Red")
    ax4.plot(sim.species_history["green"], color="green", label="Green")
    ax4.plot(sim.species_history["blue"], color="blue", label="Blue")
    ax4.set_title("Species Population Over Time")
    ax4.legend()

    plt.tight_layout()


    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return pygame.image.load(buf, "stats.png")
