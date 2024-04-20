from typing import Any

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group: Any, pos: tuple[int, int], image: Surface) -> None:
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()

    def get_hitbox(self) -> Rect:
        hitbox = self.rect.copy()
        hitbox.center = self.rect.center
        return hitbox