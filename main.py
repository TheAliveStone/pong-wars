from os.path import join
import sys
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, SIZE, SPEED, COLORS

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Wars - Basic")
clock = pygame.time.Clock()

# simple helper
def clamp(val, a, b):
    return max(a, min(b, val))

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, is_left=True):
        super().__init__()
        w, h = SIZE['paddle']
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # draw shadow
        shadow = pygame.Rect(4, 4, w, h)
        pygame.draw.rect(self.image, COLORS['paddle shadow'], shadow, border_radius=6)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.Rect(0, 0, w, h), border_radius=6)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = SPEED['player'] if is_left else SPEED['opponent']
        self.is_left = is_left
        self.velocity = 0

    def update(self, dt):
        self.rect.y += int(self.velocity * dt)
        self.rect.y = clamp(self.rect.y, 0, WINDOW_HEIGHT - self.rect.height)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        w, h = SIZE['ball']
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        # shadow then ball
        pygame.draw.ellipse(self.image, COLORS['ball shadow'], pygame.Rect(4, 4, w, h))
        pygame.draw.ellipse(self.image, COLORS['ball'], pygame.Rect(0, 0, w, h - 2))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.speed = SPEED['ball']
        # start moving in a random-ish direction
        self.vel = pygame.math.Vector2(1, 0.25).normalize() * self.speed

    def update(self, dt):
        self.rect.centerx += int(self.vel.x * dt)
        self.rect.centery += int(self.vel.y * dt)
        # bounce off top/bottom only (no paddle collisions in this basic setup)
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.vel.y *= -1

    def reset(self, direction=1):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.vel = pygame.math.Vector2(direction, 0.25).normalize() * self.speed

# sprites
left_paddle = Paddle(40, WINDOW_HEIGHT // 2, is_left=True)
right_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2, is_left=False)
ball = Ball()

all_sprites = pygame.sprite.Group(left_paddle, right_paddle, ball)

# scores
score_left = 0
score_right = 0
font = pygame.font.SysFont(None, 96)

# game mode: 1 = single player (right is AI), 2 = two player
players = 1

def draw_translucent_score(surface, left, right):
    # translucent background for score
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    # small translucent bar behind the numbers
    bar_h = 140
    bar_rect = pygame.Rect(0, 20, WINDOW_WIDTH, bar_h)
    overlay.fill((0, 0, 0, 0))
    pygame.draw.rect(overlay, (0, 0, 0, 90), bar_rect)  # semi-transparent black
    # render scores
    left_surf = font.render(str(left), True, (255, 255, 255))
    right_surf = font.render(str(right), True, (255, 255, 255))
    # center left and right halves
    overlay.blit(left_surf, (WINDOW_WIDTH * 0.25 - left_surf.get_width() // 2, 20 + (bar_h - left_surf.get_height()) // 2))
    overlay.blit(right_surf, (WINDOW_WIDTH * 0.75 - right_surf.get_width() // 2, 20 + (bar_h - right_surf.get_height()) // 2))
    surface.blit(overlay, (0, 0))

running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                players = 1
            elif event.key == pygame.K_2:
                players = 2

    # input handling
    keys = pygame.key.get_pressed()
    # left paddle: W/S
    left_paddle.velocity = 0
    if keys[pygame.K_w]:
        left_paddle.velocity = -SPEED['player']
    elif keys[pygame.K_s]:
        left_paddle.velocity = SPEED['player']

    # right paddle: arrow keys for 2-player; AI if single player
    if players == 2:
        right_paddle.velocity = 0
        if keys[pygame.K_UP]:
            right_paddle.velocity = -SPEED['player']
        elif keys[pygame.K_DOWN]:
            right_paddle.velocity = SPEED['player']
    else:
        # simple AI: follow the ball's y position
        if ball.rect.centery < right_paddle.rect.centery - 10:
            right_paddle.velocity = -SPEED['opponent']
        elif ball.rect.centery > right_paddle.rect.centery + 10:
            right_paddle.velocity = SPEED['opponent']
        else:
            right_paddle.velocity = 0

    # update sprites
    all_sprites.update(dt)

    # scoring: when ball passes left or right edge
    if ball.rect.right < 0:
        score_right += 1
        ball.reset(direction=1)
    elif ball.rect.left > WINDOW_WIDTH:
        score_left += 1
        ball.reset(direction=-1)

    # draw background
    screen.fill(COLORS['bg'])

    # draw translucent score in background (so it appears behind paddles/ball)
    draw_translucent_score(screen, score_left, score_right)

    # draw sprites
    all_sprites.draw(screen)

    # simple HUD hint
    small = pygame.font.SysFont(None, 20)
    hint = small.render("Press 1 = single player, 2 = two player. Esc to quit.", True, (200, 200, 200))
    screen.blit(hint, (10, WINDOW_HEIGHT - 24))

    pygame.display.flip()

pygame.quit()
sys.exit()