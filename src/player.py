from typing import Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from src import settings
from src.level import Level

from .support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], group: Any) -> None:
        super().__init__(group)

        # Initialize animations
        self.animations: dict[str, list[Surface]] = {"up": [], "down": [], "left": [], "right": [], "down_idle": []}
        self.import_assets()
        self.status = "down_idle"
        self.animation_time: float = 0
        self.animation_speed = 4  # cycle through 4 sprites each second

        # general setup
        self.image: Surface = self.animations[self.status][self.animation_index]
        self.rect: Rect = self.image.get_rect(center=pos)

        # movement setup
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.hitbox_vertical_offset = 20
        self.level: Level | None = None

    @property
    def animation_index(self) -> int:
        return int(self.animation_time)

    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)
        self.animate(dt)

    def get_hitbox(self) -> Rect:
        return self.rect.scale_by(1 / 5, 1 / 10)

    def enter_level(self, level: Level) -> None:
        self.level = level

    def import_assets(self) -> None:
        for key in self.animations.keys():
            full_path = "graphics/character/" + key
            self.animations[key] = import_folder(full_path)

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        self.status = "down_idle"
        self.direction.y = 0
        self.direction.x = 0

        if keys[pygame.K_LEFT]:
            self.status = "left"
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.status = "right"
            self.direction.x = 1
        if keys[pygame.K_UP]:
            self.status = "up"
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.status = "down"
            self.direction.y = 1

    def predict_position(self, dt: float) -> Vector2:
        """Predict the next position without actually moving the player."""
        # normalize vector
        if self.direction.magnitude() > 0:  # checks if vector is not zero
            self.direction = self.direction.normalize()

        return self.pos + self.direction * self.speed * dt

    def predict_horizontal_hitbox(self, new_pos: Vector2) -> Rect:
        """Predict horizontal movement."""
        hitbox = self.get_hitbox()
        hitbox.center = (new_pos.x, self.pos.y + self.hitbox_vertical_offset)  # type: ignore
        return hitbox

    def predict_vertical_hitbox(self, new_pos: Vector2) -> Rect:
        """Predict vertical movement."""
        hitbox = self.get_hitbox()
        hitbox.center = (self.pos.x, new_pos.y + self.hitbox_vertical_offset)  # type: ignore
        return hitbox

    def check_horizontal_move(self, pos: Vector2) -> bool:
        return bool(pos.x <= (settings.SCREEN_WIDTH - 30) and (pos.x >= 30))

    def check_vertical_move(self, pos: Vector2) -> bool:
        return bool(pos.y <= (settings.SCREEN_HEIGHT - 40) and (pos.y >= 30))

    def move(self, dt: float) -> None:
        new_pos = self.predict_position(dt)

        future_horizontal_position = self.predict_horizontal_hitbox(new_pos)
        future_vertical_position = self.predict_vertical_hitbox(new_pos)

        if self.level is None:
            return

        horizontal_collisions = [
            obstacle for obstacle in self.level.obstacles if future_horizontal_position.colliderect(obstacle.hitbox)
        ]

        vertical_collisions = [
            obstacle for obstacle in self.level.obstacles if future_vertical_position.colliderect(obstacle.hitbox)
        ]

        if self.check_horizontal_move(new_pos) and len(horizontal_collisions) == 0:
            self.pos.x = new_pos.x

        if self.check_vertical_move(new_pos) and len(vertical_collisions) == 0:
            self.pos.y = new_pos.y

        self.rect.center = self.pos  # type: ignore

    def animate(self, dt: float) -> None:
        self.animation_time += self.animation_speed * dt
        if self.animation_time >= len(self.animations[self.status]):
            self.animation_time = 0
        self.image = self.animations[self.status][self.animation_index]
