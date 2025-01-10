import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)
WHITE = (255, 255, 255)

font = pygame.font.Font("Font/monogram.ttf", 40)
small_font = pygame.font.Font("Font/monogram.ttf", 34)
title_font = pygame.font.Font("Font/monogram.ttf", 80)

# Game text surfaces
level_surface = font.render('LEVEL 01', False, YELLOW)
game_over_surface = title_font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)
start_text_surface = font.render("PRESS SPACE TO START", False, YELLOW)
title_surface = title_font.render("SPACE INVADERS", False, YELLOW)
quit_text_surface = font.render("PRESS Q TO QUIT", False, YELLOW)
return_home_surface = font.render("PRESS SHIFT TO TRY AGAIN", False, YELLOW)
name_input_surface = font.render("ENTER 3 LETTERS/NUMBERS FOR LEADERBOARD", False, YELLOW)
leaderboard_title_surface = font.render("HIGH SCORES", False, YELLOW)
thanks_text_surface = font.render("thanks", False, YELLOW)
for_playing_surface = font.render("for playing!", False, YELLOW)
creator_text_surface = font.render("* navanateR", False, (WHITE))

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Python Space Invaders")
clock = pygame.time.Clock()
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Event timers
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 320)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))


def draw_home_screen():
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start_text_surface, (SCREEN_WIDTH // 2 - start_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text_surface, (SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


def show_thanks_screen():
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)

    screen.blit(thanks_text_surface,
                (SCREEN_WIDTH // 2 - thanks_text_surface.get_width() // 2,
                 SCREEN_HEIGHT // 2 - thanks_text_surface.get_height()))

    screen.blit(for_playing_surface,
                (SCREEN_WIDTH // 2 - for_playing_surface.get_width() // 2,
                 SCREEN_HEIGHT // 2))

    screen.blit(creator_text_surface,
                (SCREEN_WIDTH // 2 - creator_text_surface.get_width() // 2,
                 SCREEN_HEIGHT // 2 + creator_text_surface.get_height() * 2))

    pygame.display.update()
    pygame.time.wait(2000)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_thanks_screen()
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.current_state == 'playing' and game.aliens_can_move:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.current_state == 'playing' and game.aliens_can_move:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        if event.type == pygame.KEYDOWN and game.current_state == 'game_over' and game.name_input_active:
            if event.key == pygame.K_RETURN and len(game.name_input) == 3:
                game.submit_high_score(game.name_input)
                game.name_input_active = False
            elif event.key == pygame.K_BACKSPACE:
                game.name_input = game.name_input[:-1]
            elif len(game.name_input) < 3 and event.unicode.isalpha() or event.unicode.isnumeric():
                game.name_input += event.unicode.upper()

    keys = pygame.key.get_pressed()

    # Global quit option
    if keys[pygame.K_q]:
        show_thanks_screen()
        pygame.quit()
        sys.exit()

    # State machine for game states
    if game.current_state == 'home':
        draw_home_screen()
        if keys[pygame.K_SPACE]:
            game.reset_game()

    elif game.current_state == 'playing':
        screen.fill(GREY)
        pygame.draw.rect(screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, WHITE, (25, 730), (775, 730), 3)
        if not game.aliens_can_move:

            start_level_text = font.render(f"PRESS SPACE TO START LEVEL {game.current_level}", False, YELLOW)

            screen.blit(start_level_text,
                        (SCREEN_WIDTH // 2 - start_level_text.get_width() // 2,
                         SCREEN_HEIGHT // 1.5))

            # Allow movement between rounds
            game.spaceship_group.update()
            game.spaceship_group.draw(screen)
            if keys[pygame.K_SPACE]:
                game.aliens_can_move = True

        else:
            # Gameplay updates
            game.spaceship_group.update()
            game.move_aliens()
            game.alien_lasers_group.update()
            game.mystery_ship_group.update()
            game.check_for_collisions()
            game.check_level_complete()
            game.explosions_group.update()

            # Draw game elements
            game.explosions_group.draw(screen)
            game.spaceship_group.draw(screen)
            game.spaceship_group.sprite.lasers_group.draw(screen)

            for obstacle in game.obstacles:
                obstacle.blocks_group.draw(screen)

            game.aliens_group.draw(screen)
            game.alien_lasers_group.draw(screen)
            game.mystery_ship_group.draw(screen)

        # HUD 

        level_surface = font.render(f'LEVEL {game.current_level:02d}', False, YELLOW)
        screen.blit(level_surface, (570, 740, 50, 50))

        x = 50

        for life in range(game.lives):
            screen.blit(game.spaceship_group.sprite.image, (x, 745))

            x += 50

        screen.blit(score_text_surface, (50, 15, 50, 50))
        formatted_score = str(game.score).zfill(5)
        score_surface = font.render(formatted_score, False, YELLOW)
        screen.blit(score_surface, (50, 40, 50, 50))

        screen.blit(highscore_text_surface, (550, 15, 50, 50))

        if game.leaderboard.scores:
            highscore_initials = game.leaderboard.scores[0]["name"]
            initials_surface = small_font.render(highscore_initials, False, (255, 255, 255))  # White color
            formatted_highscore = str(game.highscore).zfill(5)
            highscore_surface = font.render(formatted_highscore, False, YELLOW)

            screen.blit(initials_surface, (575, 42.5, 50, 50))
            screen.blit(highscore_surface, (625, 40, 50, 50))

        # Draw Sprites

        game.spaceship_group.draw(screen)
        game.spaceship_group.sprite.lasers_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        game.aliens_group.draw(screen)
        game.alien_lasers_group.draw(screen)
        game.mystery_ship_group.draw(screen)

    elif game.current_state == 'game_over':
        screen.fill(GREY)
        pygame.draw.rect(screen, WHITE, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)

        if game.check_for_high_score() and not game.name_input_active and not hasattr(game, 'high_score_handled'):
            game.name_input_active = True
            game.name_input = ""
            game.high_score_handled = True

        if game.name_input_active:
            # Draw name input screen
            screen.blit(name_input_surface,
                        (SCREEN_WIDTH // 2 - name_input_surface.get_width() // 2,
                         SCREEN_HEIGHT // 2 - 100))
            name_surface = font.render(game.name_input + "_" * (3 - len(game.name_input)),
                                       False, WHITE)

            screen.blit(name_surface,
                        (SCREEN_WIDTH // 2 - name_surface.get_width() // 2,
                         SCREEN_HEIGHT // 2))
        else:
            screen.blit(game_over_surface,
                        (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2,
                         100))
            screen.blit(leaderboard_title_surface,
                        (SCREEN_WIDTH // 2 - leaderboard_title_surface.get_width() // 2,
                         200))

            # Leaderboard entries
            y_pos = 250

            for entry in game.leaderboard.scores:
                name_surface = font.render(entry['name'], False, WHITE)
                score_surface = font.render(f"{entry['score']:05d}", False, YELLOW)

                total_width = name_surface.get_width() + 20 + score_surface.get_width()  # 20 pixels spacing
                start_x = SCREEN_WIDTH // 2 - total_width // 2

                screen.blit(name_surface, (start_x, y_pos))
                screen.blit(score_surface, (start_x + name_surface.get_width() + 20, y_pos))
                y_pos += 50

            screen.blit(return_home_surface,
                        (SCREEN_WIDTH // 2 - return_home_surface.get_width() // 2,
                         y_pos + 50))
            screen.blit(quit_text_surface,
                        (SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2,
                         y_pos + 100))

            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                game.current_state = 'home'

    pygame.display.update()
    clock.tick(60)
