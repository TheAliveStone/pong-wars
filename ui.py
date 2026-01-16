import sys
import pygame
from os.path import join
from settings import COLORS

def _load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont(None, size)

def main_menu(screen, clock, title_text="Pong Wars"):
    """Blocking menu. Returns True to start the game, False to quit."""
    pygame.event.clear()
    title_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 96)
    small_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 28)

    w, h = screen.get_size()
    start_btn = pygame.Rect(0, 0, 320, 72)
    start_btn.center = (w // 2, h // 2 + 40)
    quit_btn = pygame.Rect(0, 0, 160, 56)
    quit_btn.center = (w // 2, h // 2 + 130)

    hover_color = pygame.Color("white")
    base_color = pygame.Color("#86D3FF")
    text_color = pygame.Color("white")

    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if start_btn.collidepoint((mx, my)):
                    return True
                if quit_btn.collidepoint((mx, my)):
                    return False

        mx, my = pygame.mouse.get_pos()
        is_hover_start = start_btn.collidepoint((mx, my))
        is_hover_quit = quit_btn.collidepoint((mx, my))

        # Draw
        screen.fill(COLORS.get('bg', '#000000'))
        # Title
        title_surf = title_font.render(title_text, True, text_color)
        title_rect = title_surf.get_rect(center=(w // 2, h // 2 - 80))
        screen.blit(title_surf, title_rect)

        # Subtitle / hint
        hint = small_font.render("Press Enter / Click Start to play — Esc to quit", True, text_color)
        hint_rect = hint.get_rect(center=(w // 2, h // 2 - 20))
        screen.blit(hint, hint_rect)

        # Start button
        pygame.draw.rect(screen, hover_color if is_hover_start else base_color, start_btn, border_radius=8)
        start_text = small_font.render("START", True, pygame.Color("black") if is_hover_start else pygame.Color("white"))
        start_rect = start_text.get_rect(center=start_btn.center)
        screen.blit(start_text, start_rect)

        # Quit button
        pygame.draw.rect(screen, hover_color if is_hover_quit else base_color, quit_btn, border_radius=8)
        quit_text = small_font.render("QUIT", True, pygame.Color("black") if is_hover_quit else pygame.Color("white"))
        quit_rect = quit_text.get_rect(center=quit_btn.center)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()