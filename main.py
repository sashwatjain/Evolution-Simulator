# main.py

import pygame, sys, time
from config import SCREEN_W, SCREEN_H, WORLD_W, WORLD_H, FPS, FAST_FORWARD_MULT
from core.simulation import Simulation
from rendering.renderer import draw_world
from rendering.graphs import render_stats

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Evolution Simulator")
clock = pygame.time.Clock()

sim = Simulation()
paused = False
fast = False

last_graph_time = 0
graph_surf = None

font = pygame.font.SysFont("Arial", 18)

while True:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                paused = not paused
            if ev.key == pygame.K_f:
                fast = not fast
            if ev.key == pygame.K_r:
                sim.reset()

    # update simulation
    if not paused:
        steps = FAST_FORWARD_MULT if fast else 1
        for _ in range(steps):
            sim.step()

    # draw world
    screen.fill((18,18,28))
    world_area = screen.subsurface((0,0,WORLD_W,WORLD_H))
    world_area.fill((22,22,34))
    draw_world(world_area, sim)

    # draw UI panel
    ui_area = screen.subsurface((WORLD_W, 0, SCREEN_W-WORLD_W, SCREEN_H))
    ui_area.fill((12,12,16))

    info = [
        f"Tick: {sim.tick}",
        f"Population: {len(sim.agents)}",
        f"Paused: {paused}",
        f"Fast: {fast}",
        "SPACE: pause  |  F: fast-forward  |  R: reset"
    ]

    y = 20
    for line in info:
        surf = font.render(line, True, (255,255,255))
        ui_area.blit(surf, (10, y))
        y += 24

    # render graph occasionally
    if time.time() - last_graph_time > 0.8:
        graph_surf = render_stats(sim, SCREEN_W-WORLD_W-20, SCREEN_H//2)
        last_graph_time = time.time()

    if graph_surf:
        ui_area.blit(graph_surf, (10, 200))

    pygame.display.flip()
    clock.tick(FPS)
