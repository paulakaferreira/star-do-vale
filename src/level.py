import pygame

from . import colors, settings
from .objects import Obstacle
from .player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites)
        self.player.enter_level(self)
        self.stump = Obstacle(self.all_sprites)
        self.obstacles = [self.stump]

    def run(self, dt):
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.update(dt)
