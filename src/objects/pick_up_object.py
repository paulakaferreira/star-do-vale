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
    pos: pygame.math.Vector2
    image: Surface
    rect: Rect
    obj_type: str

    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)
        img_path = f"graphics/fruit/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()

    def get_hitbox(self) -> Rect:
        hitbox = self.rect.copy()
        hitbox.center = self.rect.center
        return hitbox


class Acerola(PickUpObject):
    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        self.name = "acerola"
        super().__init__(group, pos)
        self.type = "fruit"
        self.price = 6


class Jabuticaba(PickUpObject):
    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        self.name = "jabuticaba"
        super().__init__(group, pos)
        self.type = "fruit"
        self.price = 12


class Jaca(PickUpObject):
    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        self.name = "jaca"
        super().__init__(group, pos)
        self.type = "fruit"
        self.price = 12
