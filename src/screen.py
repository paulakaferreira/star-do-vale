import pygame
from pygame.locals import RESIZABLE

from .settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

real_screen = pygame.display.get_surface()
virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


def update_display(virtual_screen: pygame.Surface, real_screen: pygame.Surface) -> None:
    window_width, window_height = real_screen.get_size()
    game_width, game_height = virtual_screen.get_size()
    aspect_ratio = game_width / game_height

    if window_width / window_height > aspect_ratio:
        new_height = window_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = window_width
        new_height = int(new_width / aspect_ratio)

    x_offset = (window_width - new_width) // 2
    y_offset = (window_height - new_height) // 2

    rescaled_screen = pygame.transform.smoothscale(virtual_screen, (new_width, new_height))

    real_screen.fill((0, 0, 0))

    real_screen.blit(rescaled_screen, (x_offset, y_offset))

    pygame.display.update()


def get_scaled_rect(original_rect: pygame.Rect, scale_factor: float) -> pygame.Rect:
    return pygame.Rect(
        original_rect.x * scale_factor,
        original_rect.y * scale_factor,
        original_rect.width * scale_factor,
        original_rect.height * scale_factor,
    )
