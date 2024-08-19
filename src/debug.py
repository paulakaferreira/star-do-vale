import pygame

from .settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE

grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
grid_surface.set_alpha(128)
for x in range(0, SCREEN_WIDTH, TILE_SIZE):
    pygame.draw.line(grid_surface, (255, 255, 255, 128), (x, 0), (x, SCREEN_HEIGHT))

for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
    pygame.draw.line(grid_surface, (255, 255, 255, 128), (0, y), (SCREEN_WIDTH, y))
