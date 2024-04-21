import pygame
from pygame.locals import DOUBLEBUF, HWSURFACE, RESIZABLE

from .editor import Editor
from .level import Level
from .menu import Menu
from .settings import SCREEN_HEIGHT, SCREEN_WIDTH
from .support import handle_resize_event


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.fake_screen = self.screen.copy()
        pygame.display.set_caption("Star do Vale")
        self.clock = pygame.time.Clock()
        self.level = Level(self)
        self.running = True
        self.menu = Menu(self)
        self.editor = Editor(self)
        self.cur_level = self.level

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.open()
                if event.type == pygame.VIDEORESIZE:
                    window_size = handle_resize_event(event)
                    self.screen = pygame.display.set_mode(window_size, HWSURFACE | DOUBLEBUF | RESIZABLE)

            self.cur_level.update_screen(self.fake_screen)
            dt = self.clock.tick(60) / 1000
            self.cur_level.run(dt)

            self.screen.blit(
                pygame.transform.scale(self.fake_screen, self.screen.get_rect().size),
                (0, 0),
            )
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
