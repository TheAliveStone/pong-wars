import sys
import pygame
from os.path import join
from settings import COLORS

def _load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont(None, size)

def difficulty_menu(screen, clock):
    """Blocking difficulty menu. Returns 'easy', 'normal', or 'hard'."""
    pygame.event.clear()
    title_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 48)
    small_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 28)

    w, h = screen.get_size()
    easy_btn = pygame.Rect(0, 0, 200, 60)
    easy_btn.center = (w // 2 - 250, h // 2 + 40)
    normal_btn = pygame.Rect(0, 0, 200, 60)
    normal_btn.center = (w // 2, h // 2 + 40)
    hard_btn = pygame.Rect(0, 0, 200, 60)
    hard_btn.center = (w // 2 + 250, h // 2 + 40)

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
                if event.key == pygame.K_ESCAPE:
                    return 'normal'  # Default to normal if ESC
                if event.key == pygame.K_1:
                    return 'easy'
                if event.key == pygame.K_2:
                    return 'normal'
                if event.key == pygame.K_3:
                    return 'hard'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if easy_btn.collidepoint((mx, my)):
                    return 'easy'
                if normal_btn.collidepoint((mx, my)):
                    return 'normal'
                if hard_btn.collidepoint((mx, my)):
                    return 'hard'

        mx, my = pygame.mouse.get_pos()
        is_hover_easy = easy_btn.collidepoint((mx, my))
        is_hover_normal = normal_btn.collidepoint((mx, my))
        is_hover_hard = hard_btn.collidepoint((mx, my))

        # Draw
        screen.fill(COLORS.get('bg', '#000000'))
        # Title
        title_surf = title_font.render("Select Difficulty", True, text_color)
        title_rect = title_surf.get_rect(center=(w // 2, h // 2 - 80))
        screen.blit(title_surf, title_rect)

        # Hint
        hint = small_font.render("Use arrow keys (1, 2, 3) or click", True, text_color)
        hint_rect = hint.get_rect(center=(w // 2, h // 2 - 20))
        screen.blit(hint, hint_rect)

        # Easy button
        pygame.draw.rect(screen, hover_color if is_hover_easy else base_color, easy_btn, border_radius=8)
        easy_text = small_font.render("EASY", True, pygame.Color("black") if is_hover_easy else pygame.Color("white"))
        easy_rect = easy_text.get_rect(center=easy_btn.center)
        screen.blit(easy_text, easy_rect)

        # Normal button
        pygame.draw.rect(screen, hover_color if is_hover_normal else base_color, normal_btn, border_radius=8)
        normal_text = small_font.render("NORMAL", True, pygame.Color("black") if is_hover_normal else pygame.Color("white"))
        normal_rect = normal_text.get_rect(center=normal_btn.center)
        screen.blit(normal_text, normal_rect)

        # Hard button
        pygame.draw.rect(screen, hover_color if is_hover_hard else base_color, hard_btn, border_radius=8)
        hard_text = small_font.render("HARD", True, pygame.Color("black") if is_hover_hard else pygame.Color("white"))
        hard_rect = hard_text.get_rect(center=hard_btn.center)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

def game_over_menu(screen, clock, winner):
    """Blocking game over menu. Returns True to play again, False to return to main menu."""
    pygame.event.clear()
    title_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 96)
    small_font = _load_font(join("assets", "AlfaSlabOne-Regular.ttf"), 28)

    w, h = screen.get_size()
    play_again_btn = pygame.Rect(0, 0, 300, 72)
    play_again_btn.center = (w // 2, h // 2 + 40)
    main_menu_btn = pygame.Rect(0, 0, 300, 72)
    main_menu_btn.center = (w // 2, h // 2 + 130)

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
                if play_again_btn.collidepoint((mx, my)):
                    return True
                if main_menu_btn.collidepoint((mx, my)):
                    return False

        mx, my = pygame.mouse.get_pos()
        is_hover_play_again = play_again_btn.collidepoint((mx, my))
        is_hover_main_menu = main_menu_btn.collidepoint((mx, my))

        # Draw
        screen.fill(COLORS.get('bg', '#000000'))
        # Winner title
        winner_text = f"{winner} Wins!"
        winner_surf = title_font.render(winner_text, True, text_color)
        winner_rect = winner_surf.get_rect(center=(w // 2, h // 2 - 100))
        screen.blit(winner_surf, winner_rect)

        # Subtitle
        hint = small_font.render("First to 10 points!", True, text_color)
        hint_rect = hint.get_rect(center=(w // 2, h // 2 - 20))
        screen.blit(hint, hint_rect)

        # Play Again button
        pygame.draw.rect(screen, hover_color if is_hover_play_again else base_color, play_again_btn, border_radius=8)
        play_again_text = small_font.render("PLAY AGAIN", True, pygame.Color("black") if is_hover_play_again else pygame.Color("white"))
        play_again_rect = play_again_text.get_rect(center=play_again_btn.center)
        screen.blit(play_again_text, play_again_rect)

        # Main Menu button
        pygame.draw.rect(screen, hover_color if is_hover_main_menu else base_color, main_menu_btn, border_radius=8)
        main_menu_text = small_font.render("MAIN MENU", True, pygame.Color("black") if is_hover_main_menu else pygame.Color("white"))
        main_menu_rect = main_menu_text.get_rect(center=main_menu_btn.center)
        screen.blit(main_menu_text, main_menu_rect)

        pygame.display.flip()

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