from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_LEVEL_Y_HIGH, resource_path
import pygame
from pygame.image import load
import random
from sprite_class import SpriteGame
class Enemy(SpriteGame):
    def __init__(self, speed):
        super(Enemy, self).__init__()
        self.imageswalk = [resource_path('images/tiles-0.png'),resource_path('images/tiles-1.png'),resource_path('images/tiles-2.png'),resource_path('images/tiles-3.png'),resource_path('images/tiles-4.png'),resource_path('images/tiles-5.png'),]
        self.image = load(self.imageswalk[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0,500)
        self.rect.x = SCREEN_WIDTH
        self.counter = 0
        self.speed = random.randint(3, 3 + speed)
        self.sprint_walk_factor = 2

    def update_image(self, images_list):
        self.image = load(images_list[int(self.counter / self.sprint_walk_factor)])
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
   
        if self.passo_x != 0 or self.passo_y != 0:
            self.counter = (self.counter + 1) % (len(images_list) * self.sprint_walk_factor)

    def paralaxe(self,step):
        self.rect.x -= step
    
    def update(self,grupo_player,grupo_enemy):
        
        self.dx = 0
        self.dy = 0

        dx, dy = self.calculate_path(grupo_player, 0)
        
        self.dx += dx 
        self.dy += dy

        dx, dy = self.calculate_path(grupo_enemy, 100)

        self.dx -= dx
        self.dy -= dy

        self.passo_x = int(self.dx * self.speed)
        self.passo_y = int(self.dy * self.speed)

        self.rect.x += self.passo_x
        self.rect.y += self.passo_y
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= SPRITE_LEVEL_Y_HIGH:
            self.rect.top = SPRITE_LEVEL_Y_HIGH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.dx < 0:
            self.reverse = True
        else:
            self.reverse = False
        
        self.update_image(self.imageswalk)



