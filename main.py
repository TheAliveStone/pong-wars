import pygame

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Wars")

# Surface setup
paddle = pygame.Surface((10, 200)) # Create a surface of size 100x200
paddle.fill("white")  # Fill the surface with white color
ball = pygame.Surface((10, 10))  # Create a surface for the ball
ball.fill("white")  # Fill the ball surface with white color

# Keep the game running
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the display surface with a color
    display_surface.fill("black")  # Fill with black
    display_surface.blit(paddle, (10, 10))  # Draw the surface at position (100, 100)
    display_surface.blit(ball, (200, 200)) 

    # Update the display
    pygame.display.flip()

# Quit pygame    
pygame.quit()
