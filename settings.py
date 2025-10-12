import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
SIZE = {'paddle': (40, 100), 'ball': (30, 30)}
POS = {
    'ball': (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
    'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2),
    'opponent': (50, WINDOW_HEIGHT / 2)  # <-- 50 is near the left edge
}
SPEED = {'player': 500, 'opponent': 250, 'ball': 450}
COLORS = {
    'paddle': '#86D3FF',         # soft sky-cyan (main)
    'paddle shadow': '#1F6BAA',  # deeper blue for shadow
    'ball': '#D5FBFF',           # very bright cyan (ball)
    'ball shadow': '#2BB1E6',    # saturated blue-teal for glow/shadow
    'bg': '#0B3B5A'              # dark ocean blue (background base)
}
