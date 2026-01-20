import pygame
from settings import *
import random

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, position, is_player=False, ball=None):
        # add the sprite to any groups passed from Game
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

    # --- Paddle control helpers ---
    def set_ball(self, ball):
        """Attach or update reference to the ball used by AI."""
        self.ball = ball

    def handle_input(self):
        """Read keyboard and set vertical direction for player-controlled paddle."""
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    def ai_move(self):
        """Simple AI: follow the ball vertically if available."""
        if not self.ball:
            self.direction.y = 0
            return
        if self.ball.pos.y < self.pos.y:
            self.direction.y = -1
        elif self.ball.pos.y > self.pos.y:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, dt):
        """Apply movement based on current direction and speed, update rect."""
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self._clamp_to_window()

    def _clamp_to_window(self):
        """Ensure paddle stays within vertical window bounds."""
        half_h = self.rect.height // 2
        y = max(half_h, min(WINDOW_HEIGHT - half_h, self.rect.centery))
        self.rect.centery = y
        self.pos.y = float(self.rect.centery)

    def update(self, dt=0):
        if self.is_player:
            self.handle_input()
        else:
            self.ai_move()
        self.move(dt)


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, position, paddles=None, scoreboard=None):
        # add the sprite to any groups passed from Game
        super().__init__(*groups)

        # create a surface and fill it with the ball color
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        self.image.fill(pygame.Color(COLORS['ball']))
        self.direction = pygame.math.Vector2()
        self.speed = SPEED.get('ball', 300)
        # reference to paddle sprites group for collision checks
        self.paddles = paddles
        # optional scoreboard object (keeps backward compatibility with direct score attrs)
        self.scoreboard = scoreboard

        # keep numeric scores for compatibility with existing code
        self.playerScore = 0
        self.opponentScore = 0

        # ensure integer center coordinates (settings used / which may produce floats)
        cx, cy = position
        self.rect = self.image.get_rect(center=(int(cx), int(cy)))
        # float position for smooth sub-pixel movement
        self.pos = pygame.math.Vector2(self.rect.center)

    # --- Ball update helpers ---
    def update(self, dt=0):
        """High-level update: move, handle collisions and scoring."""
        self.update_position(dt)
        self.handle_wall_collisions()
        self.handle_out_of_bounds()
        self.handle_paddle_collision()

    def update_position(self, dt):
        """Move ball according to direction, speed and elapsed time."""
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def handle_wall_collisions(self):
        """Invert vertical direction when hitting top/bottom walls."""
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.direction.y *= -1

    def handle_out_of_bounds(self):
        """Detect left/right exit, update score(s) and relaunch from center."""
        if self.rect.left <= 0:
            # opponent scored — preserve old behavior (relaunch toward right)
            self.launch(direction_x=1)
            # keep both scoreboard and legacy attributes in sync
            self.opponentScore += 1
            if self.scoreboard and hasattr(self.scoreboard, "opponent_scored"):
                self.scoreboard.opponent_scored()
        elif self.rect.right >= WINDOW_WIDTH:
            # player scored — relaunch toward left
            self.launch(direction_x=-1)
            self.playerScore += 1
            if self.scoreboard and hasattr(self.scoreboard, "player_scored"):
                self.scoreboard.player_scored()

    def handle_paddle_collision(self):
        """Check for paddle collision and apply bounce, variation and speed increase."""
        if self.paddles and pygame.sprite.spritecollideany(self, self.paddles):
            self.bounce_horizontal()
            self.direction.y += random.uniform(-0.3, 0.3)  # small vertical variation
            # preserve original double-increment behavior (unchanged)
            self.speed = min(self.speed + 5, 600)
            self.speed += 5

    def bounce_horizontal(self):
        """Invert horizontal direction component."""
        self.direction.x *= -1

    def bounce_vertical(self):
        """Invert vertical direction component."""
        self.direction.y *= -1

    def increase_speed(self, amount=5, cap=600):
        """Increase speed with cap."""
        self.speed = min(self.speed + amount, cap)

    def reset_position(self):
        """Place ball at center without changing direction."""
        self.pos = pygame.math.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def attach_paddles(self, paddles):
        """Attach or update the paddle sprite group used for collision checks."""
        self.paddles = paddles

    def attach_scoreboard(self, scoreboard):
        """Attach or update scoreboard object; this is optional."""
        self.scoreboard = scoreboard

    def launch(self, direction_x=None, angle=None):
        """Reset position and set a normalized direction.
        direction_x: optional +1 (right) or -1 (left). If None, choose randomly.
        angle: optional vertical component (y). If None, pick small random variation.
        """
        self.reset_position()
        self.speed = SPEED.get('ball', 300)  # reset speed
        if direction_x is None:
            direction_x = random.choice((-1, 1))
        if angle is None:
            angle = random.uniform(-0.5, 0.5)
        self.direction = pygame.math.Vector2(direction_x, angle).normalize()
