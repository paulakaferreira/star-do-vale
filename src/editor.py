from __future__ import annotations

from src import colors, settings

from .level import Level
from .player import Player


class Editor(Level):
    def setup(self) -> None:
        self.player = Player(
            (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_interactables, "capybaba"
        )
        self.player.enter_level(self)

    def run(self, dt: float) -> None:
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_interactables.update(dt)
