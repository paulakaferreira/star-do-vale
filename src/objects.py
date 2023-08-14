import pygame
from . import support


class CollisionObject(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.surfaces = {'stumps': [], 'trees': []}
        self.import_assets()
        self.pos = pygame.math.Vector2((320, 100)) # TODO: send this to a child class
        self.image = self.surfaces['stumps'][0] # TODO: send this to a child class
        self.rect = self.image.get_rect(center = self.pos)

    def import_assets(self):
        for key in self.surfaces.keys():
            full_path = 'graphics/objects/' + key
            self.surfaces[key] = support.import_folder(full_path)
