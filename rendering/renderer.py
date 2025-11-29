# rendering/renderer.py

import pygame
from config import WORLD_W, WORLD_H

FRUIT_COLOR = (255,140,40)
WATER_COLOR = (80,180,255)
PLANT_COLOR = (40,130,40)

def draw_world(screen, sim):

    # draw plants
    for p in sim.plants:
        pygame.draw.circle(screen, PLANT_COLOR, (int(p.x), int(p.y)), 7)

        # draw fruits or water
        for i in range(p.food):
            pygame.draw.circle(screen, FRUIT_COLOR, (int(p.x + i*4), int(p.y - 10)), 4)

        for i in range(p.water):
            pygame.draw.circle(screen, WATER_COLOR, (int(p.x + i*4), int(p.y + 10)), 4)

    # draw organisms
    for a in sim.agents:
        draw_agent(screen, a)


def draw_agent(surface, agent):
    x, y = int(agent.x), int(agent.y)
    size = int(6 * agent.genome["size"])

    # Clamp color safely
    r = max(0, min(255, int(agent.genome["cr"] * 255)))
    g = max(0, min(255, int(agent.genome["cg"] * 255)))
    b = max(0, min(255, int(agent.genome["cb"] * 255)))
    color = (r, g, b)

    if agent.sex == "male":
        # DIAMOND
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y),
        ]
        pygame.draw.polygon(surface, color, points)
    else:
        # FEMALE CIRCLE
        pygame.draw.circle(surface, color, (x, y), size)
