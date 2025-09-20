import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        # add the sprite to any groups passed from Game()
        super().__init__(groups)

        # create a surface and fill it with the paddle color
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['paddle']))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # ensure integer center coordinates (settings used / which may produce floats)
        cx, cy = position
        self.frect = self.image.get_frect(center=(cx, cy))

    def update(self, dt=0):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.frect.y += self.direction.y * self.speed * dt

