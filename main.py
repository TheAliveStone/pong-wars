import pygame

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong Wars")

# Keep the game running
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the display surface with a color
    display_surface.fill("blue")  # Fill with blue

    # Update the display
    pygame.display.flip()

# Quit pygame    
pygame.quit()