import pygame
from random import randint, uniform
from os.path import join
from settings import *
from sprites import *
from ui import main_menu, difficulty_menu, game_over_menu

class Game:
    def __init__(self, difficulty='normal'):
        # pygame.init()  # Removed: handled in if __name__
        self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pong Wars")
        self.running = True

        # Load difficulty settings
        from settings import DIFFICULTY_PRESETS
        self.difficulty_settings = DIFFICULTY_PRESETS.get(difficulty, DIFFICULTY_PRESETS['normal'])

        # Sprite groups
        self.allSprites = pygame.sprite.Group()
        self.paddleSprites = pygame.sprite.Group()

        # Scoreboard manages scores
        self.scoreboard = Scoreboard()

        # Create the ball first so we can pass it to paddles for simple AI.
        # The paddle needs the ball reference to track the ball's position for AI logic (e.g., opponent movement).
        self.ball = Ball((self.allSprites,), POS['ball'], paddles=self.paddleSprites, scoreboard=self.scoreboard, difficulty_settings=self.difficulty_settings)
        # pass the ball instance into paddles so opponent AI can read ball.pos
        self.player = Paddle((self.allSprites, self.paddleSprites), POS['player'], is_player=True, ball=self.ball, difficulty_settings=self.difficulty_settings)
        self.opponent = Paddle((self.allSprites, self.paddleSprites), POS['opponent'], is_player=False, ball=self.ball, difficulty_settings=self.difficulty_settings)

        # Font (create once; render score surfaces each frame)
        self.font = pygame.font.Font(join("assets", "AlfaSlabOne-Regular.ttf"), 20)
        # launch once at start (preserve prior behavior)
        self.ball.launch()
        # middle line (create once; reuse each frame)
        self.middleLineColor = (*pygame.Color('white')[:3], 128)  # RGBA with alpha for transparency
        self.middleLineSurf = pygame.Surface((4, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.middleLineSurf.fill(self.middleLineColor)
        # second launch preserved from original behavior  # Removed: duplicate


    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Check for first-to-10 win condition
            if self.scoreboard.player >= 10:
                self.running = False
                return "Player"
            elif self.scoreboard.opponent >= 10:
                self.running = False
                return "Opponent"

            # Update the sprites once per frame
            self.allSprites.update(delta_time)

            # update score surfaces each frame so the display reflects changes
            self.playerScoreSurf = self.font.render(str(self.scoreboard.player), True, pygame.Color('white'))
            self.opponentScoreSurf = self.font.render(str(self.scoreboard.opponent), True, pygame.Color('white'))
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
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    while True:
        # Show main menu
        start_game = main_menu(screen, clock, title_text="Pong Wars")
        if not start_game:
            pygame.quit()
            break
        
        # Show difficulty selection menu
        difficulty = difficulty_menu(screen, clock)
        
        # Run the game and get the winner
        winner = Game(difficulty=difficulty).run()
        
        # Show game over menu
        play_again = game_over_menu(screen, clock, winner)
        if not play_again:
            pygame.quit()
            break
