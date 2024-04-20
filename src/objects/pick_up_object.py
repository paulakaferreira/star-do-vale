from typing import Any

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from src import support


class PickUpObject(pygame.sprite.Sprite):
    """
    Creates Object with no hitbox.
    Contain only one surface.
    Should disapear once touched by the first player.
    """
    name: str
    price: int
    pos: tuple[int, int]
    image: Surface

    def __init__(self, group: Any) -> None:
        super().__init__(group)


class Acerola(PickUpObject):
    
    def __init__(self, group: Any, pos: tuple[int, int]) -> None:
        super().__init__(group)
        self.name = "acerola"
        self.price = 6
        self.pos = pygame.math.Vector2(pos)
        img_path = f"graphics/fruit/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
