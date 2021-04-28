from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_LEVEL_Y_HIGH, resource_path
import pygame
from pygame.image import load
import random
from sprite_class import SpriteGame
class Enemy(SpriteGame):
    def __init__(self):
        super(Enemy, self).__init__()
        self.images = [resource_path('images/tiles-0.png'),resource_path('images/tiles-1.png'),resource_path('images/tiles-2.png'),resource_path('images/tiles-3.png'),resource_path('images/tiles-4.png'),resource_path('images/tiles-5.png'),]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0,500)
        self.rect.x = random.choice([0, SCREEN_WIDTH])
        self.counter = 0
        self.speed = random.randint(3,12)
 
    def update(self,grupo_player,grupo_enemy):
        
        self.dx = 0
        self.dy = 0

        dx, dy = self.calculate_path(grupo_player, 0)
        
        self.dx += dx 
        self.dy += dy

        dx, dy = self.calculate_path(grupo_enemy, 100)

        self.dx -= dx
        self.dy -= dy

        passo_x = int(self.dx * self.speed)
        passo_y = int(self.dy * self.speed)

        self.rect.x += passo_x
        self.rect.y += passo_y
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= SPRITE_LEVEL_Y_HIGH:
            self.rect.top = SPRITE_LEVEL_Y_HIGH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.image = load(self.images[self.counter])
        
        if self.dx < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        if passo_x != 0 or passo_y != 0:
            self.counter = (self.counter + 1) % len(self.images)


