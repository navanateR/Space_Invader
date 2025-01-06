import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

font = pygame.font.Font("Font/monogram.ttf", 40)
title_font = pygame.font.Font("Font/monogram.ttf", 80)

# Game text surfaces 
level_surface = font.render('LEVEL 01', False, YELLOW)
game_over_surface = title_font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)
start_text_surface = font.render("PRESS SPACE TO START", False, YELLOW)
title_surface = title_font.render("SPACE INVADERS", False, YELLOW)
level_complete_surface = title_font.render("LEVEL COMPLETE!", False, YELLOW)
next_level_surface = font.render("PRESS SPACE FOR NEXT LEVEL", False, YELLOW)
game_complete_surface = title_font.render("CONGRATULATIONS!", False, YELLOW)
quit_text_surface = font.render("PRESS Q TO QUIT", False, YELLOW)
return_home_surface = font.render("PRESS SHIFT TO TRY AGAIN", False, YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

# Event timers
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

def draw_home_screen():
    screen.fill(GREY)
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start_text_surface, (SCREEN_WIDTH // 2 - start_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text_surface, (SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


def draw_level_complete():
    screen.fill(GREY)
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    screen.blit(level_complete_surface,
                (SCREEN_WIDTH // 2 - level_complete_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(next_level_surface, (SCREEN_WIDTH // 2 - next_level_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text_surface, (SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


def draw_game_complete():
    screen.fill(GREY)
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    screen.blit(game_complete_surface,
                (SCREEN_WIDTH // 2 - game_complete_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start_text_surface, (SCREEN_WIDTH // 2 - start_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_text_surface, (SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Modified to only shoot when playing and adjust for fire rate multiplier
        if event.type == SHOOT_LASER and game.current_state == 'playing':
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.current_state == 'playing':
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

    keys = pygame.key.get_pressed()

    # Global quit option
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # State machine for game states
    if game.current_state == 'home':
        draw_home_screen()
        if keys[pygame.K_SPACE]:
            game.reset_game()


    elif game.current_state == 'playing':
        if not game.aliens_can_move:
            # Draw "Press SPACE to Start" message
            start_level_text = font.render("PRESS SPACE TO START", False, YELLOW)
            screen.blit(start_level_text,
                        (SCREEN_WIDTH // 2 - start_level_text.get_width() // 2,
                         SCREEN_HEIGHT // 2))

            # Check for space key to start level
            if keys[pygame.K_SPACE]:
                game.aliens_can_move = True

        # Normal gameplay updates

        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()
        game.check_level_complete()
        game.explosions_group.update()

        # Draw game screen

        screen.fill(GREY)
        pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)
        game.explosions_group.draw(screen)

        # Update level display
        level_surface = font.render(f'LEVEL {game.current_level:02d}', False, YELLOW)
        screen.blit(level_surface, (570, 740, 50, 50))

        # Draw lives and scores
        x = 50

        for life in range(game.lives):
            screen.blit(game.spaceship_group.sprite.image, (x, 745))

            x += 50

        screen.blit(score_text_surface, (50, 15, 50, 50))
        formatted_score = str(game.score).zfill(5)
        score_surface = font.render(formatted_score, False, YELLOW)
        screen.blit(score_surface, (50, 40, 50, 50))
        screen.blit(highscore_text_surface, (550, 15, 50, 50))
        formatted_highscore = str(game.highscore).zfill(5)
        highscore_surface = font.render(formatted_highscore, False, YELLOW)
        screen.blit(highscore_surface, (625, 40, 50, 50))

        # Draw game sprites

        game.spaceship_group.draw(screen)
        game.spaceship_group.sprite.lasers_group.draw(screen)

        for obstacle in game.obstacles:
            obstacle.blocks_group.draw(screen)

        game.aliens_group.draw(screen)
        game.alien_lasers_group.draw(screen)
        game.mystery_ship_group.draw(screen)

    elif game.current_state == 'game_over':
        screen.fill(GREY)
        pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
        screen.blit(game_over_surface,(SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        final_score_text = font.render(f"FINAL SCORE: {game.score}", False, YELLOW)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(return_home_surface,(SCREEN_WIDTH // 2 - return_home_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(quit_text_surface,(SCREEN_WIDTH // 2 - quit_text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            game.current_state = 'home'

    pygame.display.update()
    clock.tick(60)
