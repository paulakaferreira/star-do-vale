from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame import Surface
from pygame.event import Event
from pygame_gui import UIManager
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager


class MainMenuState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("main_menu", "game", state_manager)

        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("graphics/app_states/main_menu/background.png").convert()

        self.title_label: UILabel | None = None
        self.play_game_button: UIButton | None = None

    def start(self) -> None:
        self.start_game_button = UIButton(
            pygame.Rect((437, 515), (150, 35)), "Start Game", self.ui_manager, tool_tip_text="<b>This is a tooltip.</b>"
        )
        self.exit_game_button = UIButton(
            pygame.Rect((437, 550), (150, 35)), "Exit Game", self.ui_manager, tool_tip_text="<b>This is a tooltip.</b>"
        )

    def end(self) -> None:
        self.start_game_button.kill()
        self.exit_game_button.kill()

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)
        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_game_button:
                self.set_target_state_name("game")
                self.trigger_transition()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_game_button:
                self.set_target_state_name("exit")
                self.trigger_transition()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_target_state_name("exit")
            self.trigger_transition()

    def run(self, surface: Surface, time_delta: float) -> None:
        for event in pygame.event.get():
            self.handle_event(event)

        self.ui_manager.update(time_delta)

        surface.blit(self.background_image, (0, 0))  # draw the background

        self.ui_manager.draw_ui(surface)
