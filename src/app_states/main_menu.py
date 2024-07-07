from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame_gui
from pygame.event import Event
from pygame_gui import UIManager
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from src.screen import virtual_screen
from src.support import blit_centered, ratio_to_lefttop

from .core.base_app_state import BaseAppState

if TYPE_CHECKING:
    from .core.app_state_manager import AppStateManager


class MainMenuState(BaseAppState):
    def __init__(self, ui_manager: UIManager, state_manager: AppStateManager):
        super().__init__("main_menu", "game", ui_manager, state_manager)
        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("graphics/app_states/main_menu/background.png").convert()
        self.title_label: UILabel | None = None
        self.play_game_button: UIButton | None = None
        self.exit_game_button: UIButton | None = None
        self.ui_elements: list[UIButton] = []

    def start(self) -> None:
        self.create_ui_elements()

    def end(self) -> None:
        super().end()
        for element in self.ui_elements:
            element.kill()

    def create_ui_elements(self) -> None:
        width_height = (150, 35)
        left_top = ratio_to_lefttop((1 / 2, 3 / 4), width_height)
        self.start_game_button = UIButton(
            pygame.Rect(left_top, width_height),
            "Start Game",
            self.ui_manager,
            tool_tip_text="<b>This is a tooltip.</b>",
        )
        left_top = (left_top[0], left_top[1] + width_height[1])
        self.exit_game_button = UIButton(
            pygame.Rect(left_top, width_height),
            "Exit Game",
            self.ui_manager,
            tool_tip_text="<b>This is a tooltip.</b>",
        )
        self.ui_elements = [self.start_game_button, self.exit_game_button]

    def handle_event(self, event: Event) -> None:
        super().handle_event(event)
        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_game_button:
                self.set_target_state_name("game")
                self.trigger_transition()
            elif event.ui_element == self.exit_game_button:
                self.set_target_state_name("exit")
                self.trigger_transition()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_target_state_name("exit")
            self.trigger_transition()

    def run(self, time_delta: float) -> None:
        surface = virtual_screen
        for event in pygame.event.get():
            self.handle_event(event)

        surface = virtual_screen
        self.ui_manager.update(time_delta)
        blit_centered(self.background_image)
        self.ui_manager.draw_ui(surface)
