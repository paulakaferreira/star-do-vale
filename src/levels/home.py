from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame.sprite import Group
from pygame.surface import Surface

from src import support
from src.screen import virtual_screen

from .. import colors
from ..objects.collectable import Acerola, Collectable, Jabuticaba, Jaca
from ..objects.obstacle import Obstacle
from ..objects.tile import Tile
from ..player import Player
from ..settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from ..support import handle_sprite_position

if TYPE_CHECKING:
    from ..main import Game


def get_surfaces() -> dict[str, list[Surface]]:
    surfaces: dict[str, list[Surface]] = {"stumps": [], "trees": []}
    for key in surfaces.keys():
        full_path = "graphics/objects/" + key
        surfaces[key] = support.import_folder(full_path)
    return surfaces


class Level:
    collectables: list[Collectable] = []
    obstacles: list[Obstacle] = []
    tiles: dict[tuple[int, int], Tile]

    def __init__(self, game: Game) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_interactables: Group[Any] = Group()
        self.all_tiles: Group[Any] = Group()
        self.surfaces = get_surfaces()
        self.game = game
        self.setup()

    def setup(self) -> None:
        self.player = Player(
            (
                (SCREEN_WIDTH // 2 // TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2,
                (SCREEN_HEIGHT // 2 // TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2,
            ),
            self.all_interactables,
            "capybaba",
        )
        self.player.enter_level(self)

        self.setup_tiles()
        self.setup_obstacles()
        self.setup_collectables()

    def setup_obstacles(self) -> None:
        stump_image = self.surfaces["stumps"][0]
        self.stump = Obstacle(self.all_interactables, (320, 100), stump_image)
        self.obstacles = [self.stump]

    def setup_collectables(self) -> None:
        self.acerola = Acerola(self.all_interactables, (130, 30), self)
        self.jabuticaba = Jabuticaba(self.all_interactables, (70, 205), self)
        self.jaca = Jaca(self.all_interactables, (110, 150), self)
        self.collectables = [self.acerola, self.jabuticaba, self.jaca]

    def setup_tiles(self) -> None:
        self.tiles = {}
        area = [
            (x, y)
            for x in range(0, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE)
            for y in range(0, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE)
        ]
        for pos in area:
            self.tiles[pos] = Tile(self.all_tiles, pos, name="basic-sand")

    def run(self, dt: float) -> None:
        self.all_interactables.update(dt)

    def update_screen(self) -> None:
        virtual_screen.fill(colors.PASTEL_GREEN)
        sorted_sprites = handle_sprite_position(self.game)

        self.all_tiles.draw(virtual_screen)
        sorted_sprites.draw(virtual_screen)
