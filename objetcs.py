from config import LEFT, RIGHT, resource_path, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
from pygame.image import load
import random


class PedraPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super(PedraPlayer, self).__init__()
        self.images = [
            resource_path("images/pedra.png"),
        ]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = y + 15
        self.counter = 0
        self.speed = random.randint(15, 20)
        self.direction = direction
        self.damage = 3
        if direction == RIGHT:
            self.rect.x = x
        if direction == LEFT:
            self.rect.x = x

    def paralaxe(self, step):
        self.rect.x -= step

    def update(self):
        if self.direction == RIGHT:
            self.rect.x += self.speed

        if self.direction == LEFT:
            self.rect.x -= self.speed


class PedraEnemy(PedraPlayer):
    def __init__(self, x, y, direction):
        super(PedraEnemy, self).__init__(x, y, direction)
        self.rect.y = y + 35


class PedraParada(pygame.sprite.Sprite):
    def __init__(self):
        super(PedraParada, self).__init__()
        self.images = [
            resource_path("images/pedra.png"),
        ]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0, 150)
        self.rect.x = SCREEN_WIDTH
        self.counter = 0
        self.damage = 3

    def paralaxe(self, step):
        self.rect.x -= step

    def update(self):
        pass


class BandAid(pygame.sprite.Sprite):
    def __init__(self):
        super(BandAid, self).__init__()
        self.images = [
            resource_path("images/band_aid.png"),
        ]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0, 150)
        self.rect.x = SCREEN_WIDTH
        self.counter = 0
        self.damage = 3

    def paralaxe(self, step):
        self.rect.x -= step

    def update(self):
        pass