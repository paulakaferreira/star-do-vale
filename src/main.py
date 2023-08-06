import pygame
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
            
            pygame.display.update()
            

if __name__ == "__main__":
    game = Game()
    game.run()
