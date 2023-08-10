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

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
            
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()
            

if __name__ == "__main__":
    game = Game()
    game.run()
