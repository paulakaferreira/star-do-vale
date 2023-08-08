import pygame
import os
from .settings import *
from .colors import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # dimentions
        self.width = 50
        self.height = 50

        # position
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

        self.speed = 2

        # Initialize animations
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'down_idle': []}
        self.import_assets()
        self.current_animation = self.animations['down_idle']
        self.animation_index = 0

    # TODO: send this to another file
    def import_folder(self, path):
        sprite_list = []
        print(os.walk(path))
        for folder_name, sub_folder, contents in os.walk(path):
            print(folder_name)
            for content in contents:
                full_path = path + '/' + content
                content_surf = pygame.image.load(full_path).convert_alpha()
                sprite_list.append(content_surf)
        return sprite_list
    
    def import_assets(self):
        for key in self.animations.keys():
            full_path = 'graphics/character/' + key
            print(full_path)
            self.animations[key] = self.import_folder(full_path)

    def animate(self):
        self.image = self.current_animation[self.animation_index // (180//len(self.current_animation)) % len(self.current_animation)]
        self.animation_index += 1

    def draw(self, surface):
        rect = self.image.get_rect()
        width = rect.width
        height = rect.height
        surface.blit(self.image, (self.x - width/2, self.y - height/2))

    def move(self, keys):
        self.current_animation = self.animations['down_idle']

        if keys[pygame.K_LEFT]:
            self.current_animation = self.animations['left']
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.current_animation = self.animations['right']
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.current_animation = self.animations['up']
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.current_animation = self.animations['down']
            self.y += self.speed

        
        # Boundary checking
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
