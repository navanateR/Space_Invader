import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien, MysteryShip, Explosion
from laser import Laser
from leaderboard import Leaderboard

class Game:
    def __init__(self, screen_width, screen_height, offset):
        # Initialize basic properties
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # Initialize leaderboard first, before any references to it
        self.leaderboard = Leaderboard()
        self.highscore = self.get_current_highscore()

        # Initialize game objects
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()

        # Initialize game state variables
        self.lives = 3
        self.score = 0
        self.explosions_group = pygame.sprite.Group()
        self.current_state = 'home'
        self.alien_speed = 1
        self.alien_fire_rate = 1.0
        self.current_level = 1
        self.aliens_can_move = False
        self.name_input = ""
        self.name_input_active = False
        self.current_highscore = self.get_current_highscore()

        # Load sounds
        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def get_current_highscore(self):
        """Get the current highest score from the leaderboard"""
        if self.leaderboard.scores:
            return self.leaderboard.scores[0]["score"]
        return 0

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x=x, y=y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        if self.aliens_can_move:
            self.aliens_group.update(self.aliens_direction * self.alien_speed)
            alien_sprites = self.aliens_group.sprites()
            for alien in alien_sprites:
                if alien.rect.right >= self.screen_width + self.offset / 2:
                    self.aliens_direction = -1
                    self.alien_move_down(2)
                elif alien.rect.left <= self.offset / 2:
                    self.aliens_direction = 1
                    self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_can_move and self.aliens_group.sprites() and random.random() < self.alien_fire_rate:
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_for_collisions(self):
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.explosion_sound.play()
                    for alien in aliens_hit:
                        self.explosions_group.add(Explosion(alien.rect.center, alien.color))
                        self.score += alien.type * 100
                        if self.score > self.current_highscore:
                            self.current_highscore = self.score
                        laser_sprite.kill()

                mystery_hit = pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True)
                if mystery_hit:
                    self.explosions_group.add(
                        Explosion(mystery_hit[0].rect.center, mystery_hit[0].color))
                    self.score += 500
                    self.explosion_sound.play()
                    if self.score > self.current_highscore:
                        self.current_highscore = self.score
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def check_level_complete(self):
        if len(self.aliens_group.sprites()) == 0:
            self.current_level += 1
            self.alien_speed += 0.2
            self.alien_fire_rate += 0.1
            self.start_new_level()

    def check_for_high_score(self):
        return self.leaderboard.check_high_score(self.score)

    def submit_high_score(self, name):
        self.leaderboard.add_score(name.upper(), self.score)

    def game_over(self):
        """Handle game over state"""
        self.current_state = 'game_over'

    def reset_game(self):
        """Reset the game to initial state"""
        self.score = 0
        self.lives = 3
        self.alien_speed = 1
        self.alien_fire_rate = 1.0
        self.current_state = 'playing'
        self.obstacles = self.create_obstacles()
        self.start_new_level()
        self.aliens_can_move = False
        self.current_level = 1
        self.highscore = self.get_current_highscore()
        self.current_highscore = self.get_current_highscore()

    def start_new_level(self):
        """Initialize a new level"""
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.mystery_ship_group.empty()
        self.explosions_group.empty()
        self.spaceship_group.sprite.reset()
        self.obstacles = self.create_obstacles()
        self.create_aliens()
        self.aliens_can_move = False
