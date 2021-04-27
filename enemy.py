import pygame
from pygame.image import load
from config import SCREEN_HEIGHT, SCREEN_WIDTH, resource_path
from sprite_class import SpriteGame
import random

class Enemy(SpriteGame):
    def __init__(self):
        super(Enemy, self).__init__()
        self.images = [resource_path('images/tiles-0.png'),resource_path('images/tiles-1.png'),resource_path('images/tiles-2.png'),resource_path('images/tiles-3.png'),resource_path('images/tiles-4.png'),resource_path('images/tiles-5.png'),]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT
        self.rect.x = random.randint(0, SCREEN_WIDTH) + random.randint(1,10)
        self.counter = 0
        self.speed = 3
        self.dx = 0
        self.dy = 0

 
    def update(self,grupo_player,grupo_enemy):
        
        self.dx = 0
        self.dy = 0

        dx, dy = self.calculate_path(grupo_player, 0)
        
        self.dx += dx 
        self.dy += dy

        dx, dy = self.calculate_path(grupo_enemy, 100)

        self.dx -= dx
        self.dy -= dy

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.image = load(self.images[self.counter])
        
        if self.dx < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.dx * 10000 != 0 and self.dy * 10000 != 0:
            self.counter = (self.counter + 1) % len(self.images)

