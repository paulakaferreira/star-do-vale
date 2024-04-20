from typing import Any

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class PickUpObject(pygame.sprite.Sprite):
    """
    Disappears when touched by player.
    """

    name: str
    price: int
    pos: tuple[int, int]
    image: Surface
    rect: Rect

    def __init__(self, group: Any) -> None:
        super().__init__(group)

    def kill(self):
        self.kill()

    def get_hitbox(self) -> Rect:
        hitbox = self.rect.copy()
        hitbox.center = self.rect.center
        return hitbox


class Acerola(PickUpObject):
    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        super().__init__(group)
        self.name = "acerola"
        self.price = 6
        self.pos = pygame.math.Vector2(pos)
        img_path = f"graphics/fruit/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()
