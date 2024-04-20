from typing import Any

import pygame
from pygame.sprite import Group
from pygame.surface import Surface

from src import colors, settings, support

from .objects import Obstacle


def get_surfaces() -> dict[str, list[Surface]]:
    surfaces: dict[str, list[Surface]] = {"stumps": [], "trees": []}
    for key in surfaces.keys():
        full_path = "graphics/objects/" + key
        surfaces[key] = support.import_folder(full_path)
    return surfaces


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites: Group[Any] = Group()
        self.surfaces = get_surfaces()
        self.setup()

    def setup(self) -> None:
        from .player import Player

        global surfaces
        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites)
        self.player.enter_level(self)

        # add stump
        stump_image = self.surfaces["stumps"][0]
        self.stump = Obstacle(self.all_sprites, (320, 100), stump_image)
        self.obstacles = [self.stump]

    def run(self, dt: float) -> None:
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.update(dt)
