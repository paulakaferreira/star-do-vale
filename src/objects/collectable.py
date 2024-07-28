from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from src.objects.animation import AnimatedSprite

if TYPE_CHECKING:
    from ..level import Level
    from ..player import Player


class Collectable(AnimatedSprite):
    """
    Disappears when touched by player.
    """

    name: str
    price: int
    pos: Vector2
    image: Surface
    rect: Rect
    obj_type: str
    level: Level

    def __init__(self, group: Any, pos: tuple[int, int], level: Level) -> None:
        super().__init__(group)
        self.pos = Vector2(pos)
        img_path = f"graphics/fruit/{self.name}.png"
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()
        self.level = level
        self.in_collision = False

    def get_hitbox(self) -> Rect:
        hitbox = self.rect.copy()
        hitbox.center = self.rect.center
        return hitbox

    def new_collision(self, player: Player) -> bool:
        if pygame.sprite.collide_rect(player, self):
            if not self.in_collision:
                self.in_collision = True
                return True
            return False
        else:
            self.in_collision = False
            return False

    def collect(self) -> Collectable:
        self.level.collectables.remove(self)
        self.kill()
        self.collect_alert()
        return self

    def collect_alert(self) -> None:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("sounds/collect.wav")
            pygame.mixer.music.play()
        except Exception:
            pass


class Acerola(Collectable):
    def __init__(self, group: Any, pos: tuple[int, int], level: Level) -> None:
        self.name = "acerola"
        super().__init__(group, pos, level)
        self.type = "fruit"
        self.price = 6


class Jabuticaba(Collectable):
    def __init__(self, group: Any, pos: tuple[int, int], level: Level) -> None:
        self.name = "jabuticaba"
        super().__init__(group, pos, level)
        self.type = "fruit"
        self.price = 12


class Jaca(Collectable):
    def __init__(self, group: Any, pos: tuple[int, int], level: Level) -> None:
        self.name = "jaca"
        super().__init__(group, pos, level)
        self.type = "fruit"
        self.price = 12
