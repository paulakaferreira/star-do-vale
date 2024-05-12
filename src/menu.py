from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import pygame
from pygame.ftfont import Font
from pygame.surface import Surface

from . import colors
from .level import Level

if TYPE_CHECKING:
    pass


@dataclass
class Button:
    # content
    text: str

    # rectangle
    pos: tuple[int, int]
    width: int = 200
    height: int = 45

    # style
    font_color: tuple[int, int, int] = colors.WHITE
    selected_background_color: tuple[int, int, int] = colors.LIGHT_GRAY
    unselected_background_color: tuple[int, int, int] = colors.GRAY

    # behavior
    callback: Callable[[], None] = lambda: None

    def draw(self, screen: Surface, selected: bool) -> None:
        font = pygame.font.Font(None, 36)
        textobj = font.render(self.text, True, self.font_color)
        self.rect = pygame.rect.Rect(*self.pos, self.width, self.height)
        background_color = self.selected_background_color if selected else self.unselected_background_color
        pygame.draw.rect(screen, background_color, self.rect)
        screen.blit(textobj, self.rect)


def add_button(
    text: str,
    surface: pygame.surface.Surface,
    rect_coords: tuple[int, int, int, int],
    color: tuple[int, int, int],
    font: Font,
) -> pygame.Rect:
    textobj = font.render(text, 1, color)  # type: ignore
    textrect = textobj.get_rect()
    textrect.topleft = rect_coords[:2]
    surface.blit(textobj, textrect)
    return pygame.Rect(*rect_coords)


class Menu(Level):
    selected_button_idx: int

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.buttons = [
            Button(
                text="Resume",
                pos=(200, 100),
                callback=self.go_to_game,
            ),
            Button(
                text="Editor",
                pos=(200, 150),
                callback=self.go_to_editor,
            ),
            Button(
                text="Quit",
                pos=(200, 200),
                callback=self.quit,
            ),
        ]
        self.selected_button_idx = 0

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def open(self) -> None:
        self.game.cur_level = self
        pygame.display.set_caption("Menu")

    def go_to_game(self) -> None:
        self.game.cur_level = self.game.level
        pygame.display.set_caption("Star do Vale")

    def go_to_editor(self) -> None:
        self.game.cur_level = self.game.editor
        pygame.display.set_caption("Editor")

    @property
    def selected_button(self) -> Button:
        return self.buttons[self.selected_button_idx]

    def run(self, dt: float) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_button_idx += 1
                    self.selected_button_idx %= len(self.buttons)

                if event.key == pygame.K_UP:
                    self.selected_button_idx -= 1
                    self.selected_button_idx %= len(self.buttons)

                if event.key == pygame.K_RETURN:
                    self.selected_button.callback()

    def update_screen(self, screen: Surface) -> None:
        screen.fill(colors.BLACK)

        # Draw text on buttons
        for idx, button in enumerate(self.buttons):
            button.draw(screen, selected=idx == self.selected_button_idx)
