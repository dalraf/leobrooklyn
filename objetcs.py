from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_LEVEL_Y_HIGH, resource_path
import pygame
from pygame.image import load
import random
from sprite_class import SpriteGame


class Pedra(SpriteGame):
    def __init__(self,x,y):
        super(Pedra, self).__init__()
        self.images = [resource_path('images/pedra.png'),]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.speed = 3
 
    def update(self,grupo_player,grupo_enemy):
        pass

