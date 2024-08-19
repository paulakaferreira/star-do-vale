from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame.event import Event
from pygame_gui import UIManager
from pygame_gui.windows import UIConfirmationDialog

from ..support import ratio_to_lefttop
from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager


class ExitState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("exit", "main_menu", ui_manager, state_manager)
        self.background_image = pygame.image.load("graphics/app_states/main_menu/background.png").convert()
        self.previous_state_name = "main_menu"

    def start(self) -> None:
        super().start()
        width_height = (300, 200)
        left_top = ratio_to_lefttop((1 / 2, 7 / 8), width_height)
        self.exit_confirmation_dialog = UIConfirmationDialog(
            pygame.Rect(left_top, width_height),
            "Do you want to exit the game?",
            self.ui_manager,
            blocking=False,
        )

    def end(self) -> None:
        super().end()
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_target_state_name(self.previous_state_name)
