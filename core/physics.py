# core/physics.py
import math, random
from core.utils import clamp
import math
import random

def move_toward(agent, tx, ty, hunger_factor=1.0):
    dx = tx - agent.x
    dy = ty - agent.y
    dist = math.hypot(dx, dy)

    if dist < 1e-5:   # prevent division errors
        return

    base_speed = agent.genome["speed"]

    # minimum movement speed even when full
    speed = max(0.3, base_speed * hunger_factor)

    agent.x += (dx / dist) * speed
    agent.y += (dy / dist) * speed


def wander(agent, hunger_factor=1.0):
    agent.angle += random.uniform(-agent.turn_rate, agent.turn_rate)
    base_speed = agent.genome["speed"]
    min_speed = 0.4
    speed = max(min_speed, base_speed * 0.3 * hunger_factor)
    agent.x += math.cos(agent.angle) * speed
    agent.y += math.sin(agent.angle) * speed




def clamp_position(agent, W, H):
    agent.x = clamp(agent.x, 8, W - 8)
    agent.y = clamp(agent.y, 8, H - 8)
