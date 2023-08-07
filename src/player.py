import pygame
from .settings import *
from .colors import *

class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
