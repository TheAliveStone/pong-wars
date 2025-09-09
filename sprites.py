import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        # add the sprite to any groups passed from Game()
        super().__init__(*groups)

        # create a surface and fill it with the paddle color
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['paddle']))

        # ensure integer center coordinates (settings used / which may produce floats)
        cx, cy = POS['player']
        self.rect = self.image.get_rect(center=(int(cx), int(cy)))

    def update(self, dt=0):
        # minimal update signature to match allSprites.update(dt) call
        pass