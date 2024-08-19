import pygame
from pygame.locals import RESIZABLE

from .settings import ANTI_ALIASING, SCREEN_HEIGHT, SCREEN_WIDTH

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

real_screen = pygame.display.get_surface()
virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


def get_transformation(
    virtual_screen: pygame.Surface,
    real_screen: pygame.Surface,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    Update the display and return the ratio.
    """
    window_width, window_height = real_screen.get_size()
    SCREEN_WIDTH, SCREEN_HEIGHT = virtual_screen.get_size()
    aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT

    if window_width / window_height > aspect_ratio:
        new_height = window_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = window_width
        new_height = int(new_width / aspect_ratio)

    x_offset = (window_width - new_width) // 2
    y_offset = (window_height - new_height) // 2

    return (new_width / SCREEN_WIDTH, x_offset), ((new_height / SCREEN_HEIGHT), y_offset)


def update_display(x_trans: tuple[float, float], y_trans: tuple[float, float]) -> None:
    (x_ratio, x_offset), (y_ratio, y_offset) = x_trans, y_trans

    if ANTI_ALIASING:
        rescaled_screen = pygame.transform.smoothscale_by(virtual_screen, (x_ratio, y_ratio))
    else:
        rescaled_screen = pygame.transform.scale_by(virtual_screen, (x_ratio, y_ratio))

    real_screen.fill((0, 0, 0))

    real_screen.blit(rescaled_screen, (x_offset, y_offset))
    # real_screen.blit(virtual_screen, (x_offset, y_offset))

    pygame.display.update()


def get_scaled_rect(original_rect: pygame.Rect, scale_factor: float) -> pygame.Rect:
    return pygame.Rect(
        original_rect.x * scale_factor,
        original_rect.y * scale_factor,
        original_rect.width * scale_factor,
        original_rect.height * scale_factor,
    )
