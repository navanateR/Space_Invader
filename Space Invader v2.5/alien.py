import pygame, random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.colors = {
            3: (255, 255, 0),
            2: (255, 255, 0),
            1: (194, 181, 232)
        }
        self.color = self.colors[type]

    def update(self, direction):
        self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png")
        self.color = (255, 0, 0)

        x = random.choice([self.offset / 2, self.screen_width + self.offset - self.image.get_width()])

        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        self.rect.x += self.speed
        
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.image.load("Graphics/alien_explosion.png")
        colored_surface = pygame.Surface(self.image.get_size()).convert_alpha()
        colored_surface.fill(color)
        self.image.blit(colored_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = 10  # frames the explosion will last

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
