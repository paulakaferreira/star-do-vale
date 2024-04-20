from typing import Any

import pygame
from pygame.sprite import Group

from src import colors, settings

from .objects import Obstacle


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites: Group[Any] = Group()
        self.setup()

    def setup(self) -> None:
        from .player import Player

        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites)
        self.player.enter_level(self)
        self.stump = Obstacle(self.all_sprites)
        self.obstacles = [self.stump]

    def run(self, dt: float) -> None:
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.update(dt)
