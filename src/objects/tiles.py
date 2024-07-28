from typing import Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from src.settings import HALF_TILE, TILE_SIZE

TILE_MAP = {
    (217, 160, 102): "basic-sand",
    (106, 190, 48): "leaf-soil",
    (99, 155, 255): "water",
}


class Tile(pygame.sprite.Sprite):
    """
    Sprites with no hitbox.
    Player should not walk behind it.
    """

    name: str
    pos: Vector2
    image: Surface
    rect: Rect
    tile_type: str  # TODO: create child to make use of this

    def __init__(
        self,
        group: Any,
        name: str,
        grid_pos: tuple[int, int] | None = None,
        left_top: tuple[float, float] | None = None,
    ) -> None:
        super().__init__(group)
        assert (grid_pos or left_top) and not (grid_pos and left_top), "Only `grid_pos` or `left_top` must be declared"

        if left_top:
            pos = left_top[0] + HALF_TILE, left_top[1] + HALF_TILE
        if grid_pos:
            pos = grid_pos[0] * TILE_SIZE + HALF_TILE, grid_pos[1] * TILE_SIZE + HALF_TILE

        self.pos = Vector2(pos)
        self.name = name
        img_path = f"graphics/tiles/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
