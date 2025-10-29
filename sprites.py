import pygame
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, position, is_player=False, ball=None):
        # add the sprite to any groups passed from Game()
        super().__init__(*groups)

        # create a surface and fill it with the paddle color
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['paddle']))
        self.is_player = is_player
        # reference to the Ball instance (may be None)
        self.ball = ball      
        self.direction = pygame.math.Vector2()
        # choose speed based on side (player on right gets player speed)
        cx, cy = position
        if cx > WINDOW_WIDTH / 2:
            self.speed = SPEED.get('player', 300)
        else:
            self.speed = SPEED.get('opponent', 300)

        self.rect = self.image.get_rect(center=(int(cx), int(cy)))
        # float position for smooth sub-pixel movement
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt=0):
        if self.is_player:
            keys = pygame.key.get_pressed()
            self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        else:
            # simple default opponent AI: follow the ball if available
            if self.ball:
                if self.ball.pos.y < self.pos.y:
                    self.direction.y = -1
                elif self.ball.pos.y > self.pos.y:
                    self.direction.y = 1
                else:
                    self.direction.y = 0
            else:
                # fallback: no movement if we don't have a ball reference
                self.direction.y = 0

        self.pos.y += self.direction.y * self.speed * dt
        # sync integer rect for rendering / collision
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, position, paddles=None):
        # add the sprite to any groups passed from Game()
        super().__init__(*groups)
 
        # create a surface and fill it with the ball color
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['ball']))
        self.direction = pygame.math.Vector2()
        self.speed = SPEED.get('ball', 300)
        # reference to paddle sprites group for collision checks
        self.paddles = paddles
 
        # ensure integer center coordinates (settings used / which may produce floats)
        cx, cy = position
        self.rect = self.image.get_rect(center=(int(cx), int(cy)))
        # float position for smooth sub-pixel movement
        self.pos = pygame.math.Vector2(self.rect.center)
 
    def update(self, dt=0):
        # update float position
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.direction.y *= -1
        # ball went off left/right -> relaunch from center toward appropriate side
        if self.rect.left <= 0:
            self.launch(direction_x=1)
        elif self.rect.right >= WINDOW_WIDTH:
            self.launch(direction_x=-1)
        # collide with any paddle in the paddle group
        if self.paddles and pygame.sprite.spritecollideany(self, self.paddles):
            self.direction.x *= -1
        
        

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
