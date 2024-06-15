import os

import pygame
from pygame.locals import SCALED
from pygame_gui import UIManager

from .app_states.core.app_state_manager import AppStateManager
from .app_states.exit import ExitState
from .app_states.game import GameState
from .app_states.main_menu import MainMenuState
from .editor import Editor
from .level import Level
from .settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
    def __init__(self) -> None:
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.key.set_repeat()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED)
        pygame.display.set_caption("Star do Vale")
        self.clock = pygame.time.Clock()
        self.level = Level(self)
        self.running = True
        self.editor = Editor(self)
        self.cur_level = self.level

        ui_manager = UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.app_state_manager = AppStateManager(self)
        MainMenuState(ui_manager, self.app_state_manager)
        GameState(ui_manager, self.cur_level, self.app_state_manager)
        ExitState(ui_manager, self.app_state_manager)
        self.app_state_manager.set_initial_state("main_menu")

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.running = self.app_state_manager.run(dt)

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
