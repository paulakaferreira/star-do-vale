import pygame
from .player import Player
from . import colors


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()

    def run(self, dt):
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.animate()
        self.player.draw(self.display_surface)