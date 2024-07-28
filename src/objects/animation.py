import math
from enum import Enum
from random import randint
from typing import Any, Callable

import pygame
from pygame.rect import FRect, Rect
from pygame.sprite import Sprite

SimpleTimeFunction = Callable[[float], tuple[float, float]]
ParametricTimeFunction = Callable[[Any, ...], SimpleTimeFunction]
TimeFunction = SimpleTimeFunction | ParametricTimeFunction


class Animation(Enum):
    IDLE = lambda t: (0, 0)  # noqa
    CIRCLE = lambda radius=32: lambda t: (radius * math.cos(t), radius * math.sin(t))  # noqa
    ERRATIC = lambda radius=32: lambda t: (randint(-radius, radius), randint(-radius, radius))  # noqa
    BOB = lambda radius=2: lambda t: (0, radius * math.sin(8 * t))  # noqa


class AnimatedSprite(Sprite):
    def __init__(
        self,
        *args: tuple[Any, ...],
        animation_function: Animation = Animation.BOB,
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self.animation_function = animation_function

    @property
    def displacement(self) -> tuple[float, float]:
        t = pygame.time.get_ticks() / 1000
        res = self.animation_function(t)  # type: ignore
        if isinstance(res, tuple):
            return res
        # allow sending parametric Animations
        return self.animation_function()(t)  # type: ignore

    @property
    def rect(self) -> FRect | Rect | None:
        return self.__rect.move(self.displacement)

    @rect.setter
    def rect(self, value: Rect) -> None:
        self.__rect = value
