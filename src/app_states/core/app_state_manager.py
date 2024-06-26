from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from pygame import Surface

if TYPE_CHECKING:
    from .base_app_state import BaseAppState


class AppStateManager:
    def __init__(self) -> None:
        self.states: dict[str, BaseAppState] = {}
        self.active_state: BaseAppState | None = None

    def register_state(self, state: BaseAppState) -> None:
        if state.name not in self.states:
            self.states[state.name] = state

    def run(self, surface: Surface, time_delta: float) -> bool:
        if self.active_state is not None:
            self.active_state.run(surface, time_delta)

            if self.active_state.time_to_transition:
                self.active_state.time_to_transition = False
                new_state_name = self.active_state.target_state_name
                self.active_state.end()
                outgoing_data_copy = copy.deepcopy(self.active_state.outgoing_transition_data)
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
