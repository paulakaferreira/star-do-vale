from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from PIL import Image
from pygame.sprite import Group
from pygame.surface import Surface

from src import support
from src.screen import virtual_screen

from .. import colors
<<<<<<<< HEAD:src/levels/level.py
from ..objects.collectables import Acerola, Collectable, Jabuticaba, Jaca
from ..objects.obstacles import Obstacle
from ..objects.tiles import TILE_MAP, Tile
========
from ..objects.collectable import Acerola, Collectable, Jabuticaba, Jaca
from ..objects.obstacle import Obstacle
from ..objects.tile import Tile
>>>>>>>> 425436c (refactor: add levels folder):src/levels/home.py
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

    def __init__(self, level_name: str, game: Game) -> None:
        self.level_name = level_name
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
        self.stump = Obstacle(self.all_interactables, (7, 2), stump_image)
        self.obstacles = [self.stump]

    def setup_collectables(self) -> None:
        self.acerola = Acerola(self.all_interactables, (3, 1), self)
        self.jabuticaba = Jabuticaba(self.all_interactables, (2, 4), self)
        self.jaca = Jaca(self.all_interactables, (7, 5), self)
        self.collectables = [self.acerola, self.jabuticaba, self.jaca]

<<<<<<<< HEAD:src/levels/level.py
    def setup_tiles(self) -> None:
        self.tiles = {}

        with Image.open(f"src/levels/{self.level_name}.png") as img:
            # Get image dimensions
            width, height = img.size
            assert width == 16
            assert height == 9

            pixels = img.load()

        for y in range(height):
            for x in range(width):
                grid_pos = (x, y)
                pixel = pixels[grid_pos]
                name = TILE_MAP[pixel[:3]]
                self.tiles[grid_pos] = Tile(self.all_tiles, grid_pos=grid_pos, name=name)
========
        # display tile
        area = [
            (x, y)
            for x in range(0, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE)
            for y in range(0, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE)
        ]
        for pos in area:
            Tile(self.all_tiles, pos, name="basic-sand")
>>>>>>>> 425436c (refactor: add levels folder):src/levels/home.py

    def run(self, dt: float) -> None:
        self.all_interactables.update(dt)

    def update_screen(self) -> None:
        virtual_screen.fill(colors.PASTEL_GREEN)
        sorted_sprites = handle_sprite_position(self.game)

        self.all_tiles.draw(virtual_screen)
        sorted_sprites.draw(virtual_screen)
