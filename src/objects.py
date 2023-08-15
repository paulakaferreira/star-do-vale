import pygame
from . import support


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.surfaces = {'stumps': [], 'trees': []}
        self.import_assets()
        # TODO: send this to a child class
        self.pos = pygame.math.Vector2((320, 100))
        # TODO: send this to a child class
        self.image = self.surfaces['stumps'][0]
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.get_hitbox()

    def import_assets(self):
        for key in self.surfaces.keys():
            full_path = 'graphics/objects/' + key
            self.surfaces[key] = support.import_folder(full_path)

    def get_hitbox(self):
        hitbox = self.rect.copy()
        hitbox.width /= 2
        hitbox.height /= 2
        hitbox.center = self.rect.center
        return hitbox