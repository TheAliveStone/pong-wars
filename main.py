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
        
        # right paddle is player-controlled; left paddle is opponent (no keyboard input)
        self.player = Paddle((self.allSprites, self.paddleSprites), POS['player'], is_player=True)
        self.opponent = Paddle((self.allSprites, self.paddleSprites), POS['opponent'], is_player=False)
        self.ball = Ball(self.allSprites, POS['ball'])

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
            
            # Check out-of-bounds and relaunch only when a point is scored
            if self.ball.rect.left > WINDOW_WIDTH:
                self.ball.launch(direction_x=-1)
            elif self.ball.rect.right < 0:
                self.ball.launch(direction_x=1)

            # Draw everything
            self.displaySurface.fill(COLORS['bg'])
            self.allSprites.draw(self.displaySurface)
            pygame.display.flip()

        # Quit pygame
        pygame.quit()

if __name__ == '__main__':
    Game().run()
