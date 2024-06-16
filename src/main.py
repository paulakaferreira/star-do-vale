import os

import pygame

from .screen import get_transformation, real_screen, update_display, virtual_screen


class Game:
    def __init__(self) -> None:
        from .app_states.core.app_state_manager import AppStateManager
        from .editor import Editor

        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.key.set_repeat()

        pygame.display.set_caption("Star do Vale")
        self.clock = pygame.time.Clock()
        self.running = True
        self.editor = Editor(self)

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

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.running = self.app_state_manager.run(dt)
            self.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
