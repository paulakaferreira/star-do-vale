import pygame
import os

def import_folder(path):
    sprite_list = []
    for folder_name, sub_folder, contents in os.walk(path):
        for content in contents:
            full_path = path + '/' + content
            # imports the image as a surface
            content_surf = pygame.image.load(full_path).convert_alpha()
            sprite_list.append(content_surf)
    return sprite_list