from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPRITE_LEVEL_Y_HIGH,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    STOPPED,
    MOONWALK,
    resource_path
)
import pygame
from pygame.image import load

from sprite_class import SpriteGame
from objetcs import Pedra
from sprite_groups import grupo_objets
class Player(SpriteGame):
    def __init__(self):
        super(Player, self).__init__()
        self.imagesattack = [resource_path('images/Player-Attack-' + str(i) + '.png') for i in range(1,6)]
        self.imageswalk = [resource_path('images/Player-Walk-' + str(i) + '.png') for i in range(1,6)]
        self.image = load(self.imageswalk[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT * (0.65)
        self.rect.x = SCREEN_WIDTH/2
        self.step = 10
        self.move_list = []
        self.sprint_walk_factor = 3
        self.counter = 0
        self.reverse = False
        self.armtime = 0
        self.in_attack = False
        self.attack_activated = False
        self.pedras = 5
        self.life = 10

    def update_image(self, images_list,reset):
        if not reset:
            self.counter = (self.counter + 1) % (len(images_list) * self.sprint_walk_factor)
            self.image = load(images_list[int(self.counter / self.sprint_walk_factor)])
        else:
            self.counter = 0
            self.image = load(images_list[0])
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def walk(self,direction):
        if not self.in_attack:
            if direction == STOPPED:
                self.update_image(self.imageswalk,True)
            else:
                self.update_image(self.imageswalk,False)
    
    def combine_moviment(self):
        if UP in self.move_list:
            self.walk(UP)
            self.move_list = []
        if DOWN in self.move_list:
            self.walk(DOWN)
            self.move_list = []
        if RIGHT in self.move_list:
            self.walk(RIGHT)
            self.move_list = []
        if LEFT in self.move_list:
            self.walk(LEFT)
            self.move_list = []
        if STOPPED in self.move_list:
            self.walk(STOPPED)
            self.move_list = []
        if MOONWALK in self.move_list:
            self.walk(MOONWALK)
            self.move_list = []

    def move(self, direction_vetor):
            self.rect.move_ip(direction_vetor)
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.bottom <= SPRITE_LEVEL_Y_HIGH:
                self.rect.bottom = SPRITE_LEVEL_Y_HIGH
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    def move_up(self):
        if not self.in_attack:
            self.move((0, -self.step))
            self.move_list.append(UP)
    
    def move_down(self):
        if not self.in_attack:
            self.move((0, self.step))
            self.move_list.append(DOWN)
    
    def move_left(self):
        if not self.in_attack:
            self.reverse = True
            self.move((-self.step, 0))    
            self.move_list.append(LEFT)

    def move_right(self):
        if not self.in_attack:
            self.reverse = False
            self.move((self.step, 0))
            self.move_list.append(RIGHT)

    def move_stopped(self):
        if not self.in_attack:
            self.move_list.append(MOONWALK)
    
    def stopped(self):
        self.move_list.append(STOPPED)

    def shoot(self):
        if self.pedras > 0:
            if self.armtime == 0:
                if self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, LEFT))
                if not self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, RIGHT))
                self.armtime = 10
                self.pedras -= 1

    
    def attack(self):
        if self.armtime == 0:
            self.in_attack = True
            self.armtime = len(self.imagesattack) * self.sprint_walk_factor

    def hit(self):
        self.life -= 1
        if self.life <=0:
            self.kill()
        
    def update(self):
    
        self.combine_moviment()

        self.armtime -= 1
        if self.armtime < 0:
            self.armtime = 0

        if self.armtime > 0 and self.in_attack:
            self.update_image(self.imagesattack,False)
            if int(self.counter / self.sprint_walk_factor) == (len(self.imagesattack) - 1):
                self.attack_activated = True
        
        elif self.armtime == 0 and self.in_attack:
            self.in_attack = False
            self.attack_activated = False
            self.update_image(self.imageswalk,True)


