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
    text: str
    pos: tuple[int, int]
    width: int
    height: int
    font_color: tuple[int, int, int]
    background_color: tuple[int, int, int]
    callback: Callable[[], None]

    def draw(self, screen: Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.hover(mouse_pos)

        font = pygame.font.Font(None, 36)
        textobj = font.render(self.text, 1, self.font_color)
        pygame.draw.rect(screen, self.background_color, self.rect)
        screen.blit(textobj, self.rect)

    def collidepoint(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def hover(self, mouse_pos: tuple[int, int]) -> None:
        if hasattr(self, "rect") is False:
            self.rect = pygame.rect.Rect(*self.pos, self.width, self.height)

        if self.rect.collidepoint(mouse_pos):
            self.background_color = colors.LIGHT_GRAY
        else:
            self.background_color = colors.GRAY


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
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.buttons = [
            Button(
                text="Resume",
                pos=(200, 100),
                width=200,
                height=45,
                font_color=colors.WHITE,
                background_color=colors.GRAY,
                callback=self.go_to_game,
            ),
            Button(
                text="Editor",
                pos=(200, 150),
                width=200,
                height=45,
                font_color=colors.WHITE,
                background_color=colors.GRAY,
                callback=self.go_to_editor,
            ),
            Button(
                text="Quit",
                pos=(200, 200),
                width=200,
                height=45,
                font_color=colors.WHITE,
                background_color=colors.GRAY,
                callback=self.quit,
            ),
        ]

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

    def run(self, dt: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(mouse_pos):
                        button.callback()

    def update_screen(self, screen: Surface) -> None:
        screen.fill(colors.BLACK)

        # Draw text on buttons
        for button in self.buttons:
            button.draw(screen)
