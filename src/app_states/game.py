from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.event import Event
from pygame_gui import UIManager

from ..level import Level
from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager


class GameState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("game", "main_menu", ui_manager, state_manager)
        self.level = Level(self.state_manager.game)

    def set_level(self, level: Level) -> None:
        self.level = level

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_target_state_name("main_menu")
                self.trigger_transition()

    def run(self, time_delta: float) -> None:
        # If I don't do this, keys are not available for the Player logic.
        for event in pygame.event.get():
            self.handle_event(event)

        super().run(time_delta)
        self.level.update_screen()
        self.level.run(time_delta)
        self.level.update_screen()
