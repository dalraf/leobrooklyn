from config import SCREEN_HEIGHT, SCREEN_WIDTH, SPRITE_LEVEL_Y_HIGH, LEFT, RIGHT, resource_path
import pygame
from pygame.image import load

from sprite_class import SpriteGame
from objetcs import Pedra
from sprite_groups import grupo_objets
class Player(SpriteGame):
    def __init__(self):
        super(Player, self).__init__()
        self.images = [resource_path('images/Player-Walk-' + str(i) + '.png') for i in range(1,6)]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT/2
        self.rect.x = SCREEN_WIDTH/2
        self.step = 10
        self.counter = 0
        self.reverse = False
        self.armtime = 0

    def move_up(self):
        self.rect.move_ip(0, -self.step)
    
    def move_down(self):
        self.rect.move_ip(0, self.step)
    
    def move_left(self):
        self.reverse = True
        self.rect.move_ip(-self.step, 0)     

    def move_right(self):
        self.reverse = False
        self.rect.move_ip(self.step, 0)

    def shoot(self):
        if self.armtime == 0:
            if self.reverse:
                grupo_objets.add(Pedra(self.rect.x , self.rect.y, LEFT))
            if not self.reverse:
                grupo_objets.add(Pedra(self.rect.x , self.rect.y, RIGHT))
            self.armtime = 10
    
    def walk(self):
        self.image = load(self.images[self.counter])
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
        self.counter = (self.counter + 1) % len(self.images)
        
    def update(self):
    
        self.armtime -= 1
        if self.armtime < 0:
            self.armtime = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= SPRITE_LEVEL_Y_HIGH:
            self.rect.top = SPRITE_LEVEL_Y_HIGH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

