from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_LEVEL_Y_HIGH, LEFT, RIGHT, resource_path
import pygame
from pygame.image import load
import random
from sprite_class import SpriteGame


class Pedra(SpriteGame):
    def __init__(self,x,y,direction):
        super(Pedra, self).__init__()
        self.images = [resource_path('images/pedra.png'),]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = y + 35
        self.counter = 0
        self.speed = 3
        self.direction = direction
        if direction == RIGHT: 
            self.rect.x = x + 35
        if direction == LEFT:
            self.rect.x = x - 35 
 
    def update(self):
        
        if self.direction == RIGHT:
            self.rect.x += 15
        
        if self.direction == LEFT:
            self.rect.x -= 15
