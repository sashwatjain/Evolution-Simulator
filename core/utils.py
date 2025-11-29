# core/utils.py
import random
import math

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def dist_sq(a, b):
    return (a.x - b.x)**2 + (a.y - b.y)**2

def rand_color():
    return random.random(), random.random(), random.random()
