import pygame
from pygame.image import load
from config import SCREEN_HEIGHT, SCREEN_WIDTH, resource_path
from sprite_class import SpriteGame
from pygame.locals import (
    K_DOWN,
    K_UP,
    K_LEFT,
    K_RIGHT,
)

class Player(SpriteGame):
    def __init__(self):
        super(Player, self).__init__()
        self.images = [resource_path('images/tiles-0.png'),resource_path('images/tiles-1.png'),resource_path('images/tiles-2.png'),resource_path('images/tiles-3.png'),resource_path('images/tiles-4.png'),resource_path('images/tiles-5.png'),]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT/2
        self.rect.x = SCREEN_WIDTH/2
        self.counter = 0
        self.reverse = False

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -20)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 20)
        if pressed_keys[K_LEFT]:
            self.reverse = True
            self.rect.move_ip(-20, 0)
        if pressed_keys[K_RIGHT]:
            self.reverse = False
            self.rect.move_ip(20, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.image = load(self.images[self.counter])
            if self.reverse:
                self.image = pygame.transform.flip(self.image, True, False)
            self.counter = (self.counter + 1) % len(self.images)