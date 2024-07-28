from typing import Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface


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

    def __init__(self, group: Any, pos: tuple[float, float], name: str) -> None:
        super().__init__(group)
        self.pos = Vector2(pos)
        self.name = name
        img_path = f"graphics/tiles/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
