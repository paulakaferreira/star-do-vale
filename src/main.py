import os

import pygame
<<<<<<< HEAD
=======
from pygame.locals import SCALED
from pygame_gui import UIManager
>>>>>>> 7d0aa93 (udpate: remove intermediate display and use pygame global)

from .screen import get_transformation, real_screen, update_display, virtual_screen


class Game:
    def __init__(self) -> None:
        from .app_states.core.app_state_manager import AppStateManager
        from .editor import Editor

        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.key.set_repeat()
<<<<<<< HEAD

=======
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCALED)
>>>>>>> 7d0aa93 (udpate: remove intermediate display and use pygame global)
        pygame.display.set_caption("Star do Vale")
        self.clock = pygame.time.Clock()
        self.running = True
        self.editor = Editor(self)

<<<<<<< HEAD
        self.app_state_manager = AppStateManager(self)
        self.level = self.app_state_manager.states["game"].level  # type: ignore

    def update(self) -> None:
        x_trans, y_trans = get_transformation(virtual_screen, real_screen)
        update_display(x_trans, y_trans)

        def calculate_scaled_mouse_position(position: tuple[int, int]) -> tuple[int, int]:
            unscaled_position = ((position[0] - x_trans[1]) / x_trans[0], (position[1] - y_trans[1]) / y_trans[0])
            # breakpoint()
            return unscaled_position  # type: ignore

        self.app_state_manager.ui_manager.calculate_scaled_mouse_position = calculate_scaled_mouse_position
=======
        ui_manager = UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.app_state_manager = AppStateManager(self)
        MainMenuState(ui_manager, self.app_state_manager)
        GameState(ui_manager, self.cur_level, self.app_state_manager)
        ExitState(ui_manager, self.app_state_manager)
        self.app_state_manager.set_initial_state("main_menu")
>>>>>>> 7d0aa93 (udpate: remove intermediate display and use pygame global)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.running = self.app_state_manager.run(dt)
<<<<<<< HEAD
            self.update()
=======

            pygame.display.flip()
>>>>>>> 7d0aa93 (udpate: remove intermediate display and use pygame global)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
