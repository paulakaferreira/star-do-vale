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
    def __init__(self, name: str, group: Any, pos: Any) -> None:
        super().__init__(group)
        self.name = name
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)

        # TODO: adapt for future objects
        full_path = f"graphics/fruit/{name}.png"
        self.surface = pygame.image.load(full_path).convert_alpha()
        self.image = self.surface
