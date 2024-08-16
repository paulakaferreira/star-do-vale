from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group
from pygame.surface import Surface

from src import settings

from .objects.collectables import Collectable
from .objects.tiles import Tile
from .settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from .support import import_folder

if TYPE_CHECKING:
    from .levels.level import Level

MAX_INVENTORY_CAPACITY = 32

DEFAULT_PLAYER_X = (SCREEN_WIDTH // 2 // TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
DEFAULT_PLAYER_Y = (SCREEN_HEIGHT // 2 // TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
DEFAULT_PLAYER_POS = (DEFAULT_PLAYER_X, DEFAULT_PLAYER_Y)


class Player(pygame.sprite.Sprite):
    def __init__(self, sprites_folder: str, pos: tuple[float, float] = DEFAULT_PLAYER_POS) -> None:
        _dummy_group: Group[Any] = Group()
        super().__init__(_dummy_group)
        # Initialize animations
        self.sprites_folder = sprites_folder
        self.animations: dict[str, list[Surface]] = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }
        self.animations.update({f"{k}_idle": [] for k in self.animations.keys()})

        self.import_assets()
        self.status = "down_idle"
        self.animation_time: float = 0
        self.animation_speed = 8  # cycle through 4 sprites each second
        self.status = "down_idle"

        # General setup
        self.image: Surface = self.animations[self.status][self.animation_index]
        self.rect: Rect = self.image.get_rect(center=pos)

        # Movement setup
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
        self.hitbox_vertical_offset = 0
        self.level: Level | None = None

        # Inventory
        self.inventory: list[Collectable] = []
        self.inventory_capactiy: int = 2

    @property
    def animation_index(self) -> int:
        return int(self.animation_time)

    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)
        self.animate(dt)
        self.plant()

    def get_hitbox(self) -> Rect:
        return self.rect.scale_by(1 / 5, 1 / 10)

    def enter_level(self, level: Level) -> None:
        self.level = level
        self.add(self.level.all_interactables)

    def import_assets(self) -> None:
        for key in self.animations.keys():
            full_path = f"graphics/{self.sprites_folder}/" + key
            self.animations[key] = import_folder(full_path)

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if not self.status.endswith("_idle"):
            self.status += "_idle"

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

        for collectable in self.level.collectables:
            if collectable.new_collision(self):
                if self.can_collect(collectable):
                    self.inventory.append(collectable.collect())
                else:
                    self.inventory_full_alert()

    def plant(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:  # TODO: modify once actions are established
            x_pos = self.pos.x
            y_pos = self.pos.y

            if self.status.startswith("left"):
                x_pos -= TILE_SIZE / 2
            elif self.status.startswith("right"):
                x_pos += TILE_SIZE / 2
            elif self.status.startswith("up"):
                y_pos -= TILE_SIZE / 2
            elif self.status.startswith("down"):
                y_pos += TILE_SIZE  # the hitbox should start from the feet, not the sprite center

            target_x: int = int(x_pos // TILE_SIZE)
            target_y: int = int(y_pos // TILE_SIZE)

            if 0 <= target_x < SCREEN_WIDTH and 0 <= target_y < SCREEN_HEIGHT:
                new_tile_pos = (target_x, target_y)
                if self.level is None:
                    return
                new_tile = Tile(self.level.all_tiles, grid_pos=new_tile_pos, name="treated-sand")
                self.level.all_tiles.add(new_tile)

    def inventory_full_alert(self) -> None:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("sounds/inventory_full.wav")
            pygame.mixer.music.play()
        except Exception:
            pass

    def animate(self, dt: float) -> None:
        self.animation_time += self.animation_speed * dt
        if self.animation_time >= len(self.animations[self.status]):
            self.animation_time = 0
        self.image = self.animations[self.status][self.animation_index]

    def can_collect(self, obj: Collectable) -> bool:
        return len(self.inventory) < self.inventory_capactiy

    def upgrade_inventory(self) -> None:
        if self.inventory_capactiy <= MAX_INVENTORY_CAPACITY:
            self.inventory_capactiy += 8
        # TODO: add pop-up message logic
