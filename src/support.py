import os
from typing import Any

import pygame
from pygame.surface import Surface

from src.screen import virtual_screen


def import_folder(path) -> list[Surface]:  # type: ignore
    sprite_list = []
    for folder_name, sub_folder, contents in os.walk(path):
        # TODO: this assumes sprites are ordered alphabetically, which is not true for numbered sprites beyond 9
        for content in sorted(contents):
            full_path = path + "/" + content
            # imports the image as a surface
            content_surf = pygame.image.load(full_path).convert_alpha()
            sprite_list.append(content_surf)
    return sprite_list


def handle_sprite_position(self) -> Any:  # type: ignore
    sorted_sprites: Any = pygame.sprite.Group()
    for sprite in sorted(self.level.all_interactables.sprites(), key=lambda sprite: sprite.pos.y):
        sorted_sprites.add(sprite)
    return sorted_sprites


def blit_centered(image: Surface) -> None:
    surface = virtual_screen

    surface_width, surface_height = surface.get_size()
    image_width, image_height = image.get_size()

    x = (surface_width - image_width) // 2
    y = (surface_height - image_height) // 2

    surface.blit(image, (x, y))


def ratio_to_lefttop(ratio: tuple[float, float], width_height: tuple[float, float]) -> tuple[float, float]:
    surface = virtual_screen
    surface_width, surface_height = surface.get_size()
    image_width, image_height = width_height

    x = (surface_width - image_width) * ratio[0]
    y = (surface_height - image_height) * ratio[1]

    return (x, y)
