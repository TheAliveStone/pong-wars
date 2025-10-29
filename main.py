import pygame
from random import randint, uniform
from os.path import join
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pong Wars")
        self.running = True

        # Sprite groups
        self.allSprites = pygame.sprite.Group()
        self.paddleSprites = pygame.sprite.Group()
        
        # Create the ball first so we can pass it to paddles for simple AI
        self.ball = Ball((self.allSprites,), POS['ball'], paddles=self.paddleSprites)
        # pass the ball instance into paddles so opponent AI can read ball.pos
        self.player = Paddle((self.allSprites, self.paddleSprites), POS['player'], is_player=True, ball=self.ball)
        self.opponent = Paddle((self.allSprites, self.paddleSprites), POS['opponent'], is_player=False, ball=self.ball)

        # launch once at start
        self.ball.launch()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the sprites
            self.allSprites.update(dt)

            # Draw everything
            self.displaySurface.fill(COLORS['bg'])
            self.allSprites.draw(self.displaySurface)
            pygame.display.flip()

        # Quit pygame
        pygame.quit()

if __name__ == '__main__':
    Game().run()
