from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame.event import Event
from pygame_gui import UIManager
from pygame_gui.windows import UIConfirmationDialog

from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager


class ExitState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("exit", "main_menu", state_manager)
        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("graphics/app_states/main_menu/background.png").convert()
        self.previous_state_name = "main_menu"

    def start(self) -> None:
        self.exit_confirmation_dialog = UIConfirmationDialog(
            pygame.Rect((400, 350), (300, 200)),
            "Do you want to exit the game?",
            self.ui_manager,
            blocking=False,
        )

    def end(self) -> None:
        self.exit_confirmation_dialog.kill()

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)

        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_confirmation_dialog.confirm_button:
                self.time_to_quit_app = True
            if event.ui_element == self.exit_confirmation_dialog.cancel_button:
                self.set_target_state_name(self.previous_state_name)
                self.trigger_transition()
            if event.ui_element == self.exit_confirmation_dialog.close_window_button:
                self.set_target_state_name(self.previous_state_name)
                self.trigger_transition()

    def run(self, surface: pygame.Surface, time_delta: float) -> None:
        for event in pygame.event.get():
            self.handle_event(event)

        self.ui_manager.update(time_delta)

        self.ui_manager.draw_ui(surface)
