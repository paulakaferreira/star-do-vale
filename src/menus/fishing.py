from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame
from pygame import Event

from src.screen import virtual_screen

if TYPE_CHECKING:
    pass


class Fishing:
    def __init__(self) -> None:
        self.fish = Fish()  # type: ignore
        self.bobber = Bobber()  # type: ignore
        self.progression_bar = ProgressionBar(self.fish, self.bobber)

    def handle_event(self, event: Event) -> None:
        self.progression_bar.handle_event(event)
        self.bobber.handle_event(event)
        self.fish.handle_event(event)

    def run(self, time_delta: float) -> None:
        self.progression_bar.run(time_delta)
        self.bobber.run(time_delta)
        self.fish.run(time_delta)


class FishingElement:
    def __init__(self) -> None:
        self.sprite = pygame.image.load("graphics/menus/bobber/fish.png").convert_alpha()
        screen = virtual_screen
        self.initial_pos = (screen.get_width() / 2, screen.get_height() / 2)
        self.pos = self.initial_pos
        self.show = False
        self.speed: float = 0
        self.max_speed: float = 6
        self.reel_acceleration: float = 2
        self.buoyancy: float = 0.25
        self.height = 100
        self.min_position: float = (screen.get_height() - self.height) / 2
        self.max_position: float = (screen.get_height() + self.height) / 2
        self.speed_count = 0
        self.initial_pos = (self.initial_pos[0], self.max_position)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.show = not self.show
                self.reset()

    def cap_position(self, pos_y: float, height: float = 0) -> float:
        if pos_y > self.max_position:
            pos_y = self.max_position
            self.speed = 0
        if pos_y < self.min_position:
            pos_y = self.min_position
            self.speed = 0
        return pos_y

    def update_position(self, time_delta: float) -> None:
        pos = self.pos
        dy = self.speed  # self.speed * time_delta
        if dy:
            self.pos = (pos[0], self.cap_position(pos[1] + dy))

    def movement(self, time_delta: float) -> None:
        pass

    def get_topleft(self) -> tuple[float, float]:
        w, h = self.sprite.get_size()
        return (self.pos[0] - 2 / 2, self.pos[1] - h / 2)

    def run(self, time_delta: float) -> None:
        surface = virtual_screen
        if self.show:
            self.movement(time_delta)
            surface.blit(self.sprite, self.get_topleft())

    def reset(self) -> None:
        self.pos = self.initial_pos
        self.speed = 0


class ProgressionBar(FishingElement):
    def __init__(self, fish: Fish, bobber: Bobber) -> None:
        super().__init__()
        screen = virtual_screen
        self.fish = fish
        self.bobber = bobber
        self.initial_value: float = 25
        self.value: float = self.initial_value
        self.max_value: float = 100
        self.width = 20
        self.height = 200
        self.x_offset = 40
        self.color = (0, 255, 0)  # Green color
        self.background_color = (255, 0, 0)  # Red color
        self.pos = (
            screen.get_width() / 2 + self.x_offset,
            (screen.get_height() - self.height) / 2,
        )  # Adjust the position as needed
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.container_radius = 2
        self.container_rect = pygame.Rect(
            self.pos[0] - self.container_radius,
            self.pos[1] - self.container_radius,
            self.width + 2 * self.container_radius,
            self.height + 2 * self.container_radius,
        )
        self.catch_speed = 10
        self.flee_speed = 10

    def reset(self) -> None:
        pass

    def evaluate_progress(self, time_delta: float) -> None:
        if abs(self.bobber.pos[1] - self.fish.pos[1]) < (self.bobber.reel_window + self.fish.sprite.get_height()) / 2:
            self.value += self.catch_speed * time_delta
        else:
            self.value -= self.flee_speed * time_delta
        if self.value < 0:
            self.value = 0
        if self.value > self.max_value:
            self.value = self.max_value

        if self.value == self.max_value:
            self.finish(success=True)

        if self.value == 0:
            self.finish(success=False)

    def finish(self, success: bool) -> None:
        if success:
            print("Fishing: 🐟 Ganhou um peixe!")
        else:
            print("Fishing: ❌ Ihhh... ruindade!")
        self.fish.show = False
        self.bobber.show = False
        self.show = False
        self.value = self.initial_value

    def run(self, time_delta: float) -> None:
        surface = virtual_screen
        if self.show is False:
            return

        self.evaluate_progress(time_delta)

        pygame.draw.rect(surface, (0, 0, 0), self.container_rect, 2)
        pygame.draw.rect(surface, self.background_color, self.rect)
        filled_height = int((self.value / self.max_value) * self.height)
        filled_rect = pygame.Rect(self.pos[0], self.pos[1] + self.height - filled_height, self.width, filled_height)
        pygame.draw.rect(surface, self.color, filled_rect)


class Fish(FishingElement):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)
        self.sprite = pygame.image.load("graphics/menus/bobber/fish.png").convert_alpha()

    def movement(self, time_delta: float) -> None:
        if not hasattr(self, "change_behavior_countdown"):
            self.change_behavior_countdown = random.randint(20, 40)
            self.speed = random.randint(-4, 4)

        if self.change_behavior_countdown == 0:
            self.change_behavior_countdown = random.randint(20, 40)
            self.speed = random.randint(-4, 4)

        self.change_behavior_countdown -= 1

        self.update_position(time_delta)


class Bobber(FishingElement):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)
        self.sprite = pygame.image.load("graphics/menus/bobber/bobber.png").convert_alpha()
        self.reeling = False
        self.reel_acceleration: float = 1
        self.reel_window: float = 40  # percentual of the catch bar
        self.container_radius = 2

    def movement(self, time_delta: float) -> None:
        if self.reeling:
            self.reel(+1)

        self.speed += self.buoyancy

        self.speed *= 0.95

        if abs(self.speed) > 0.1:
            self.update_position(time_delta)

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)

        if event.type == pygame.MOUSEWHEEL:
            self.reel(event.precise_y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reeling = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.reeling = False

    def reel(self, direction: float) -> None:
        self.speed -= direction * self.reel_acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

    def get_container_left(self) -> float:
        return self.pos[0] - self.container_radius

    def get_container_top(self) -> float:
        return self.min_position - self.reel_window / 2 - self.container_radius

    def get_container_width(self) -> float:
        return self.sprite.get_width() + 2 * self.container_radius

    def get_container_height(self) -> float:
        return (self.max_position - self.min_position) + self.reel_window + 2 * self.container_radius

    def run(self, time_delta: float) -> None:
        surface = virtual_screen
        if self.show:
            bobber_container = pygame.Rect(
                self.get_container_left(),
                self.get_container_top(),
                self.get_container_width(),
                self.get_container_height(),
            )

            bobber_hitbox = pygame.Rect(
                self.pos[0],
                self.pos[1] - self.reel_window / 2,
                self.sprite.get_width(),
                self.reel_window,
            )

            pygame.draw.rect(surface, (0, 0, 0), bobber_container, self.container_radius)
            pygame.draw.rect(surface, (200, 200, 200), bobber_hitbox)
        super().run(time_delta)
