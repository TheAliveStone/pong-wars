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
        
        # Create the ball first so we can pass it to paddles for simple AI.
        # The paddle needs the ball reference to track the ball's position for AI logic (e.g., opponent movement).
        self.ball = Ball((self.allSprites,), POS['ball'], paddles=self.paddleSprites)
        # pass the ball instance into paddles so opponent AI can read ball.pos
        self.player = Paddle((self.allSprites, self.paddleSprites), POS['player'], is_player=True, ball=self.ball)
        self.opponent = Paddle((self.allSprites, self.paddleSprites), POS['opponent'], is_player=False, ball=self.ball)

        # Font (create once; render score surfaces each frame)
        self.font = pygame.font.Font(join("assets", "AlfaSlabOne-Regular.ttf"), 20)
        # launch once at start
        self.ball.launch()

        # Middle line (create once; reuse each frame)
        self.middleLineColor = (*pygame.Color('white')[:3], 128)  # RGBA with alpha for transparency
        self.middleLineSurf = pygame.Surface((4, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.middleLineSurf.fill(self.middleLineColor)
        self.ball.launch()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the sprites once per frame
            self.allSprites.update(delta_time)

            # update score surfaces each frame so the display reflects changes
            self.playerScoreSurf = self.font.render(str(self.ball.playerScore), True, pygame.Color('white'))
            self.opponentScoreSurf = self.font.render(str(self.ball.opponentScore), True, pygame.Color('white'))
            self.opponentScoreRect = self.opponentScoreSurf.get_rect(midtop=(WINDOW_WIDTH * 3 // 4, 10))
            self.playerScoreRect = self.playerScoreSurf.get_rect(midtop=(WINDOW_WIDTH // 4, 10))
            self.middleLineSurf.fill(self.middleLineColor)

            # Draw everything
            self.displaySurface.fill(COLORS['bg'])
            self.allSprites.draw(self.displaySurface)
            self.displaySurface.blit(self.playerScoreSurf, self.playerScoreRect)
            self.displaySurface.blit(self.opponentScoreSurf, self.opponentScoreRect)
            self.displaySurface.blit(self.middleLineSurf, (WINDOW_WIDTH // 2 - 2, 0))
            pygame.display.flip()

        # Quit pygame
        pygame.quit()

if __name__ == '__main__':
    Game().run()
