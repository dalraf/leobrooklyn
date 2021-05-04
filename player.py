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
    STATE_ATTACK,
    STATE_INATTACK,
    STATE_WALK,
    STATE_STOP,
    STATE_MOONWALK,
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
        self.imagesattack = [resource_path('images/Player-1-Attack-' + str(i) + '.png') for i in range(1,5)]
        self.imageswalk = [resource_path('images/Player-1-Walk-' + str(i) + '.png') for i in range(1,6)]
        self.imagesstop = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,4)]
        self.images_list = self.imagesstop
        self.image = load(self.images_list[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT * (0.65)
        self.rect.x = SCREEN_WIDTH/2
        self.step = 10
        self.move_list = []
        self.sprint_walk_factor = 3
        self.counter = 0
        self.reverse = False
        self.armtime = 0
        self.pedras = 10
        self.life = 20
        self.hittime = 0
        self.execute = self.parado

    def update_image(self, images_list):
        if  self.images_list == images_list:
            self.counter = (self.counter + 1) % (len(images_list) * self.sprint_walk_factor)
            self.image = load(self.images_list[int(self.counter / self.sprint_walk_factor)])
        else:
            self.counter = 0
            self.images_list = images_list
            self.image = load(self.images_list[0])
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)

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

    def parado(self):
        self.update_image(self.imagesstop)
    
    def andando(self):
        self.update_image(self.imageswalk)

    def atirar(self):
        if self.pedras > 0:
            if self.reverse:
                grupo_objets.add(Pedra(self.rect.x , self.rect.y, LEFT))
            if not self.reverse:
                grupo_objets.add(Pedra(self.rect.x , self.rect.y, RIGHT))
            self.armtime = 10
            self.pedras -= 1
        self.execute = self.parado

    def in_attack(self):
        if self.armtime <= 0:
            self.armtime = len(self.imagesattack) * self.sprint_walk_factor
            self.update_image(self.imagesattack)
        if self.armtime > 0:
            self.update_image(self.imagesattack)
            self.armtime -= 1            
            if int(self.counter / self.sprint_walk_factor) == (len(self.imagesattack) - 1):
                self.execute = self.attack
    
    def attack(self):
        self.update_image(self.imagesattack)
        self.execute = self.parado

    def hit(self):
        if self.hittime <= 0:
            self.life -= 1
            if self.life <=0:
                self.kill()
            self.hittime = self.sprint_walk_factor * 7
            self.update_image(self.imagesstop)
        if self.hittime > 0 and self.hittime > self.sprint_walk_factor:
            self.hittime -= self.sprint_walk_factor
            self.update_image(self.imagesstop)
        if self.hittime > 0 and self.hittime < self.sprint_walk_factor:
            self.hittime =0
            self.execute = self.parado

    def combine_moviment(self):
        if UP in self.move_list:
            self.move((0, -self.step))
            self.execute = self.andando
            self.move_list = []
        if DOWN in self.move_list:
            self.move((0, self.step))
            self.execute = self.andando
            self.move_list = []
        if RIGHT in self.move_list:
            self.reverse = False
            self.move((self.step, 0))
            self.execute = self.andando
            self.move_list = []
        if LEFT in self.move_list:
            self.reverse = True
            self.move((-self.step, 0))   
            self.execute = self.andando
            self.move_list = []
        if STOPPED in self.move_list:
            self.execute = self.parado
            self.move_list = []
        if MOONWALK in self.move_list:
            self.execute = self.andando
            self.move_list = []

    def move_up(self):
        self.move_list.append(UP)
    
    def move_down(self):
        self.move_list.append(DOWN)
    
    def move_left(self):
        self.move_list.append(LEFT)

    def move_right(self):
        self.move_list.append(RIGHT)

    def moonwalk(self):
        self.move_list.append(MOONWALK)
            
    def update(self):
        self.combine_moviment()
        print(self.execute)
        self.execute()





