import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, position, isplayer=False):
        # add the sprite to any groups passed from Game()
        super().__init__(*groups)

        # create a surface and fill it with the paddle color
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['paddle']))
        self.isplayer = isplayer      
        self.direction = pygame.math.Vector2()
        # choose speed based on side (player on right gets player speed)
        cx, cy = position
        if cx > WINDOW_WIDTH / 2:
            self.speed = SPEED.get('player', 300)
        else:
            self.speed = SPEED.get('opponent', 300)

        # ensure integer center coordinates (settings used / which may produce floats)
        # integer rect used by pygame's drawing/collision APIs
        self.rect = self.image.get_rect(center=(int(cx), int(cy)))
        # float position for smooth sub-pixel movement
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt=0):
        if self.is_player:
            keys = pygame.key.get_pressed()
            self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        else:
            # simple default: no movement for opponent (replace with AI later)
            self.direction.y = 0

        self.pos.y += self.direction.y * self.speed * dt
        # sync integer rect for rendering / collision
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        # add the sprite to any groups passed from Game()
        super().__init__(*groups)

        # create a surface and fill it with the ball color
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['ball']))
        self.direction = pygame.math.Vector2()
        self.speed = SPEED.get('ball', 300)

        # ensure integer center coordinates (settings used / which may produce floats)
        # integer rect used by pygame's drawing/collision APIs
        cx, cy = position
        self.rect = self.image.get_rect(center=(int(cx), int(cy)))
        # float position for smooth sub-pixel movement
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt=0):
        # update float position
        self.pos += self.direction * self.speed * dt
        # sync integer rect for rendering / collision
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def launch(self, direction_x=None, angle=None):
        """Reset position and set a normalized direction.
        direction_x: optional +1 (right) or -1 (left). If None, choose randomly.
        angle: optional vertical component (y). If None, pick small random variation.
        """
        self.pos = pygame.math.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        import random
        if direction_x is None:
            direction_x = random.choice((-1, 1))
        if angle is None:
            angle = random.uniform(-0.5, 0.5)
        self.direction = pygame.math.Vector2(direction_x, angle).normalize()
