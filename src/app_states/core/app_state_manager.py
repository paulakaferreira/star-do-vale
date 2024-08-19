from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from pygame_gui import UIManager

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    from ...main import Game
    from .base_app_state import BaseAppState


class AppStateManager:
    def __init__(self, game: Game) -> None:
        from ..exit import ExitState
        from ..game import GameState
        from ..main_menu import MainMenuState

        self.states: dict[str, BaseAppState] = {}
        self.previous_state: BaseAppState | None = None
        self.active_state: BaseAppState | None = None
        self.game = game

        self.ui_manager = UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        MainMenuState(self.ui_manager, self)
        GameState(self.ui_manager, self)
        ExitState(self.ui_manager, self)

        self.set_initial_state("main_menu")

    @property
    def active_state_name(self) -> str | None:
        if self.active_state:
            return self.active_state.name
        return None

    @property
    def previous_state_name(self) -> str | None:
        if self.previous_state:
            return self.previous_state.name
        return None

    def register_state(self, state: BaseAppState) -> None:
        if state.name not in self.states:
            self.states[state.name] = state

    def run(self, time_delta: float) -> bool:
        if self.active_state is not None:
            self.active_state.run(time_delta)

            if self.active_state.time_to_transition:
                self.active_state.time_to_transition = False
                self.active_state.end()
                new_state_name = self.active_state.target_state_name
                outgoing_data_copy = copy.deepcopy(self.active_state.outgoing_transition_data)
                self.previous_state = self.active_state
                self.active_state = self.states[new_state_name]
                self.active_state.incoming_transition_data = outgoing_data_copy
                self.active_state.start()

            if self.active_state.time_to_quit_app:
                return False
        return True

    def set_initial_state(self, name: str) -> None:
        if name in self.states:
            self.active_state = self.states[name]
            self.active_state.start()
