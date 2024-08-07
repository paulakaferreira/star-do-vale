from typing import Any

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from src.settings import HALF_TILE, TILE_SIZE


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group: Any, grid_pos: tuple[int, int], image: Surface) -> None:
        super().__init__(group)
        pos = grid_pos[0] * TILE_SIZE + HALF_TILE, grid_pos[1] * TILE_SIZE + HALF_TILE
        self.pos = pygame.math.Vector2(pos)
        self.image = image
        self.rect: Rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()

    def get_hitbox(self) -> Rect:
        hitbox = self.rect.copy()
        hitbox.center = self.rect.center
        return hitbox
