import pygame
import os
from .settings import *

def import_folder(path):
    sprite_list = []
    for folder_name, sub_folder, contents in os.walk(path):
        # TODO: this assumes sprites are ordered alphabetically, which is not true for numbered sprites beyond 9
        for content in sorted(contents):
            full_path = path + '/' + content
            # imports the image as a surface
            content_surf = pygame.image.load(full_path).convert_alpha()
            sprite_list.append(content_surf)
    return sprite_list

def handle_resize_event(event):
    # Imports from .settings: WIDTH_RATIO, HEIGHT_RATIO

    new_width = event.size[0]
    new_height = event.size[1]

    if (new_width / WIDTH_RATIO) != (new_height / HEIGHT_RATIO):
        # Uses height to set new screen width:
        new_width = new_height * (WIDTH_RATIO / HEIGHT_RATIO)

    new_size = (new_width, new_height)

    return new_size


def handle_sprite_position(self):
    sorted_sprites = pygame.sprite.Group()
    for sprite in sorted(
        self.level.all_sprites.sprites(), key=lambda sprite: sprite.pos.y
    ):
        sorted_sprites.add(sprite)
    return sorted_sprites