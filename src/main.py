import pygame
import sys
from .level import Level
from .settings import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()
            

if __name__ == "__main__":
    game = Game()
    game.run()
