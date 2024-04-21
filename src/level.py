from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame.sprite import Group
from pygame.surface import Surface

from src import settings, support

from . import colors
from .objects.collectable import Acerola, Collectable, Jabuticaba, Jaca
from .objects.obstacle import Obstacle
from .player import Player
from .support import handle_sprite_position

if TYPE_CHECKING:
    from .main import Game


def get_surfaces() -> dict[str, list[Surface]]:
    surfaces: dict[str, list[Surface]] = {"stumps": [], "trees": []}
    for key in surfaces.keys():
        full_path = "graphics/objects/" + key
        surfaces[key] = support.import_folder(full_path)
    return surfaces


class Level:
    collectables: list[Collectable] = []
    obstacles: list[Obstacle] = []

    def __init__(self, game: Game) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites: Group[Any] = Group()
        self.surfaces = get_surfaces()
        self.game = game
        self.setup()

    def setup(self) -> None:
        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites, "capybaba")
        self.player.enter_level(self)

        # add stump
        stump_image = self.surfaces["stumps"][0]
        self.stump = Obstacle(self.all_sprites, (320, 100), stump_image)
        self.obstacles = [self.stump]

        # add fruit
        self.acerola = Acerola(self.all_sprites, (130, 30), self)
        self.jabuticaba = Jabuticaba(self.all_sprites, (70, 205), self)
        self.jaca = Jaca(self.all_sprites, (110, 150), self)
        self.collectables = [self.acerola, self.jabuticaba, self.jaca]

    def run(self, dt: float) -> None:
        self.all_sprites.update(dt)

    def update_screen(self, screen: Surface) -> None:
        screen.fill(colors.PASTEL_GREEN)
        sorted_sprites = handle_sprite_position(self.game)

        sorted_sprites.draw(screen)
