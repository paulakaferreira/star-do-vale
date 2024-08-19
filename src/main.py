import os

import pygame

from .debug import grid_surface
from .player import Player
from .screen import get_transformation, real_screen, update_display, virtual_screen
from .settings import DEFAULT_FPS


class Game:
    def __init__(self) -> None:
        from .app_states.core.app_state_manager import AppStateManager

        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.key.set_repeat()

        pygame.display.set_caption("Star do Vale")
        self.clock = pygame.time.Clock()
        self.running = True
        # self.editor = Editor(self)

        self.player = Player("capybaba")
        self.app_state_manager = AppStateManager(self)
        self.level = self.app_state_manager.states["game"].level  # type: ignore

    def update(self) -> None:
        x_trans, y_trans = get_transformation(virtual_screen, real_screen)
        update_display(x_trans, y_trans)

        def calculate_scaled_mouse_position(position: tuple[int, int]) -> tuple[int, int]:
            if y_trans[0] and x_trans[0]:
                unscaled_position = (
                    (position[0] - x_trans[1]) / x_trans[0],
                    (position[1] - y_trans[1]) / y_trans[0],
                )
                return unscaled_position  # type: ignore
            return (0, 0)

        self.app_state_manager.ui_manager.calculate_scaled_mouse_position = calculate_scaled_mouse_position

    def run_debug(self) -> None:
        font = pygame.font.SysFont("Comic Sans", 18)
        black = (0, 0, 0)
        current_state_name = self.app_state_manager.active_state.name if self.app_state_manager.active_state else "?"
        previous_state_name = (
            self.app_state_manager.previous_state.name if self.app_state_manager.previous_state else "?"
        )
        state_display = font.render(
            f"Game State: {current_state_name}\n" f"Previous State: {previous_state_name}",
            antialias=True,
            color=black,
        )

        virtual_screen.blit(state_display, (10, 10))

        fps = int(self.clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, black)
        virtual_screen.blit(fps_text, (450, 10))

        if self.app_state_manager.active_state_name == "game":
            virtual_screen.blit(grid_surface, (0, 0))

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(DEFAULT_FPS) / 1000
            self.running = self.app_state_manager.run(dt)

            # debug
            self.run_debug()

            self.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
