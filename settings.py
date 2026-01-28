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

# Difficulty presets: tune these values to taste
DIFFICULTY_PRESETS = {
    'easy': {
        'player': 500,        # player speed (unchanged)
        'opponent': 200,      # slower opponent
        'ball': 350,          # slower initial ball
        'paddle_height': 140, # bigger paddles for player/opponent
        'ai_error': 0.25,     # large AI error (makes opponent miss)
        'ball_accel': 3       # smaller speed increment on bounce
    },
    'normal': {
        'player': 500,
        'opponent': 250,
        'ball': 450,
        'paddle_height': 100,
        'ai_error': 0.10,
        'ball_accel': 5
    },
    'hard': {
        'player': 500,
        'opponent': 330,      # faster opponent
        'ball': 520,          # faster initial ball
        'paddle_height': 80,  # smaller paddles
        'ai_error': 0.02,     # very small AI error
        'ball_accel': 8       # stronger speed increase on bounce
    }
}