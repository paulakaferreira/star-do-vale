from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame.event import Event
from pygame_gui import UIManager

from src.screen import virtual_screen

if TYPE_CHECKING:
    from .app_state_manager import AppStateManager


class BaseAppState:
    def __init__(self, name: str, target_state_name: str, ui_manager: UIManager, state_manager: AppStateManager):
        self.name = name
        self.target_state_name = target_state_name
        self.previous_state_name = name
        self.outgoing_transition_data: dict[str, Any] = {}
        self.incoming_transition_data: dict[str, Any] = {}
        self.state_manager = state_manager
        self.time_to_transition = False
        self.time_to_quit_app = False
        self.ui_manager = ui_manager
        self.state_manager.register_state(self)

    def set_target_state_name(self, target_name: str) -> None:
        self.state_manager.states[target_name].previous_state_name = self.name
        self.target_state_name = target_name

    def trigger_transition(self) -> None:
        self.time_to_transition = True

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    def run(self, time_delta: float) -> None:
        surface = virtual_screen
        for event in pygame.event.get():
            self.handle_event(event)

        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(surface)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self.set_target_state_name("exit")
            self.trigger_transition()
