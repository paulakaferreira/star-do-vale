from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame
from pygame import Surface

from src.support import handle_resize_event

if TYPE_CHECKING:
    from .app_state_manager import AppStateManager


class BaseAppState:
    def __init__(self, name: str, target_state_name: str, state_manager: AppStateManager):
        self.name = name
        self.target_state_name = target_state_name
        self.outgoing_transition_data: dict[str, Any] = {}
        self.incoming_transition_data: dict[str, Any] = {}
        self.state_manager = state_manager
        self.time_to_transition = False
        self.time_to_quit_app = False

        self.state_manager.register_state(self)

    def set_target_state_name(self, target_name: str) -> None:
        self.target_state_name = target_name

    def trigger_transition(self) -> None:
        self.time_to_transition = True

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    def run(self, surface: Surface, time_delta: float) -> None:
        pass

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == pygame.QUIT:
            self.set_target_state_name("quit")
            self.trigger_transition()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_target_state_name("quit")
                self.trigger_transition()

        if event.type == pygame.VIDEORESIZE:
            window_size = handle_resize_event(event)
            self.screen = pygame.display.set_mode(window_size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
