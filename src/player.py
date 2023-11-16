import pygame
from pygame.math import Vector2
from .support import *
from . import settings
from .colors import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Initialize animations
        self.animations = {'up': [], 'down': [],
                           'left': [], 'right': [], 'down_idle': []}
        self.import_assets()
        self.status = 'down_idle'
        self.animation_index = 0
        self.animation_speed = 4  # cycle through 4 sprites each second

        # general setup
        self.image = self.animations[self.status][self.animation_index]
        self.rect = self.image.get_rect(center=pos)

        # movement setup
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.hitbox_vertical_offset = 20
        self.level = None
        

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

    def get_hitbox(self):
        hitbox = self.rect.copy()
        hitbox.width /= 5
        hitbox.height /= 10
        hitbox.center = self.rect.center
        return hitbox

    def enter_level(self, level):
        self.level = level

    def import_assets(self):
        for key in self.animations.keys():
            full_path = 'graphics/character/' + key
            self.animations[key] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        self.status = 'down_idle'
        self.direction.y = 0
        self.direction.x = 0

        if keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x = 1
        if keys[pygame.K_UP]:
            self.status = 'up'
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.status = 'down'
            self.direction.y = 1

    def predict_position(self, dt):
        """Predict the next position without actually moving the player."""
        # normalize vector
        if self.direction.magnitude() > 0:  # checks if vector is not zero
            self.direction = self.direction.normalize()

        return self.pos + self.direction * self.speed * dt

    def predict_horizontal_hitbox(self, new_pos):
        """Predict horizontal movement."""
        hitbox = self.get_hitbox()
        hitbox.center = (new_pos.x, self.pos.y + self.hitbox_vertical_offset)
        return hitbox

    def predict_vertical_hitbox(self, new_pos):
        """Predict vertical movement."""
        hitbox = self.get_hitbox()
        hitbox.center = (self.pos.x, new_pos.y + self.hitbox_vertical_offset)
        return hitbox

    def check_horizontal_move(self, pos):
        return pos.x <= (settings.SCREEN_WIDTH - 30) and (pos.x >= 30)

    def check_vertical_move(self, pos):
        return pos.y <= (settings.SCREEN_HEIGHT - 40) and (pos.y >= 30)

    def move(self, dt):
        new_pos = self.predict_position(dt)

        future_horizontal_position = self.predict_horizontal_hitbox(new_pos)
        future_vertical_position = self.predict_vertical_hitbox(new_pos)

        horizontal_collisions = [
            obstacle for obstacle in self.level.obstacles if future_horizontal_position.colliderect(obstacle.hitbox)]

        vertical_collisions = [
            obstacle for obstacle in self.level.obstacles if future_vertical_position.colliderect(obstacle.hitbox)]

        if self.check_horizontal_move(new_pos) and len(horizontal_collisions) == 0:
            self.pos.x = new_pos.x

        if self.check_vertical_move(new_pos) and len(vertical_collisions) == 0:
            self.pos.y = new_pos.y

        self.rect.center = self.pos

    def animate(self, dt):
        self.animation_index += self.animation_speed * dt  # can return float
        if self.animation_index >= len(self.animations[self.status]):
            self.animation_index = 0
        self.image = self.animations[self.status][int(self.animation_index)]
