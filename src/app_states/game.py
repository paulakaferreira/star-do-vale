from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame_gui import UIManager

from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager
    from .level import Level


class GameState(BaseAppState):
    def __init__(self, ui_manager: UIManager, level: Level, screen: Surface, state_manger: AppStateManager):
        super().__init__("game", "main_menu", state_manger)

        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("graphics/app_states/game/background.png").convert()

        self.cur_level = level
        self.screen = screen
        self.fake_screen = screen.copy()

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    def run(self, surface: Surface, time_delta: float) -> None:
        # If I don't do this, keys are not available for the Player logic.
        for event in pygame.event.get():
            self.handle_event(event)

        self.cur_level.update_screen(self.fake_screen)
        self.cur_level.run(time_delta)
        self.cur_level.update_screen(surface)
