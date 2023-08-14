import pygame
from pygame.math import Vector2
from .support import *
from . import settings
from .colors import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Initialize animations
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'down_idle': []}
        self.import_assets()
        self.status = 'down_idle'
        self.animation_index = 0
        self.animation_speed = 4  # cycle through 4 sprites each second

        # general setup
        self.image = self.animations[self.status][self.animation_index]
        self.rect = self.image.get_rect(center = pos)

        # movement setup
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
    
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

    @staticmethod
    def manhattan(pos, collision_objects):
        for obj in collision_objects:
            if abs(pos.y - obj.pos.y) < 32 and abs(pos.x - obj.pos.x) < 32:
                return True
        return False
            
    def check_horizontal_move(self, pos, collision_objects):
        return not(self.manhattan(pos, collision_objects)) and pos.x <= settings.SCREEN_WIDTH and pos.x >= 0

    def check_vertical_move(self, pos, collision_objects):
        return not(self.manhattan(pos, collision_objects)) and pos.y <= settings.SCREEN_HEIGHT and pos.y >= 0

    def move(self, dt, collision_objects = []):
        # normalize vector
        if self.direction.magnitude() > 0: # checks if vector is not zero
            self.direction = self.direction.normalize()
        
        new_pos = self.pos + self.direction * self.speed * dt

        if self.check_horizontal_move(new_pos, collision_objects):
            self.pos.x = new_pos.x
            
        if self.check_vertical_move(new_pos, collision_objects):
            self.pos.y = new_pos.y
    
        self.rect.center = self.pos

    def animate(self, dt):
        self.animation_index += self.animation_speed * dt # can return float
        if self.animation_index >= len(self.animations[self.status]):
            self.animation_index = 0
        self.image = self.animations[self.status][int(self.animation_index)]

    def update(self, dt):
        self.input()
        self.move(dt, self.collision_objects)
        self.animate(dt)
