from src import colors, settings

from .level import Level


class Editor(Level):
    obstacles = []

    def setup(self) -> None:
        from .player import Player

        global surfaces
        self.player = Player((settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2), self.all_sprites)
        self.player.enter_level(self)

    def run(self, dt: float) -> None:
        self.display_surface.fill(colors.PASTEL_GREEN)
        self.all_sprites.update(dt)
