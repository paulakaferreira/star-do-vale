import pygame
import sys
from .level import Level
from .settings import *
from . import colors

from pygame.locals import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()

        pygame.display.set_caption('Estar do Vale')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.running = True

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

            self.fake_screen.fill(colors.PASTEL_GREEN)
            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            self.level.all_sprites.draw(self.fake_screen)
            self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0,0))
            pygame.display.update()
            

if __name__ == "__main__":
    game = Game()
    game.run()
