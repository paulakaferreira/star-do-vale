from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.event import Event
from pygame_gui import UIManager

from ..levels.level import Level
from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager

from src.menus.fishing import Fishing


class GameState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("game", "main_menu", ui_manager, state_manager)
        self.setup_levels()
        self.overlays = []
        self.overlays.append(Fishing())

    def setup_levels(self) -> None:
        self.levels = {}
        home = Level("home", self.state_manager.game)
        lake = Level("lake", self.state_manager.game)
        self.levels["home"] = home
        self.levels["lake"] = lake
        self.level = lake

    def set_level(self, level: Level) -> None:
        self.level = level
        self.level.player.enter_level(self.level)
        self.state_manager.game.level = level

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_target_state_name("exit")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                self.set_level(self.levels["lake"])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.set_level(self.levels["home"])

        for overlay in self.overlays:
            overlay.handle_event(event)

    def run(self, time_delta: float) -> None:
        super().run(time_delta)

        self.level.update_screen()
        self.level.run(time_delta)
        self.level.update_screen()

        for overlay in self.overlays:
            overlay.run(time_delta)
