from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.event import Event
from pygame_gui import UIManager

from ..levels.home import Level
from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager

from src.menus.fishing import Fishing


class GameState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("game", "main_menu", ui_manager, state_manager)
        self.level = Level(self.state_manager.game)

        self.submenus = []
        self.submenus.append(Fishing())

    def set_level(self, level: Level) -> None:
        self.level = level

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_target_state_name("main_menu")
                self.trigger_transition()

        for submenu in self.submenus:
            submenu.handle_event(event)

    def run(self, time_delta: float) -> None:
        super().run(time_delta)

        self.level.update_screen()
        self.level.run(time_delta)
        self.level.update_screen()

        for submenu in self.submenus:
            submenu.run(time_delta)
