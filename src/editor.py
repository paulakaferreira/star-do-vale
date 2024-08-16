from __future__ import annotations

from src import colors

from .levels.level import Level


class Editor(Level):
    def setup(self) -> None:
        self.player = self.game.player
        self.player.enter_level(self)

    def run(self, dt: float) -> None:
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_interactables.update(dt)
