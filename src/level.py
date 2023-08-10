import pygame
from .player import Player
from . import settings
from . import colors


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
