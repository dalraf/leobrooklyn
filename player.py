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
        self.imageswalk = [resource_path('images/Player-1-Walk-' + str(i) + '.png') for i in range(1,4)]
        self.imagesstop = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,4)]
        self.imageshit = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,3)]
        self.imagesatirar = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,2)]
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
        self.pedras = 10
        self.life = 20
        self.execute = self.action_parado

    def update_image(self, images_list):
        
        if  self.images_list == images_list:
            self.counter = (self.counter + 1) % (len(images_list) * self.sprint_walk_factor)
            self.image = load(self.images_list[int(self.counter / self.sprint_walk_factor)])
            if self.reverse:
                self.image = pygame.transform.flip(self.image, True, False)
            if self.counter == 0:
                return True
            else:
                return False
        else:
            self.counter = 0
            self.images_list = images_list
            self.image = load(self.images_list[0])
            if self.reverse:
                self.image = pygame.transform.flip(self.image, True, False)
            return False

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

    def action_parado(self):
        self.update_image(self.imagesstop)
    
    def action_andando(self):
        self.update_image(self.imageswalk)

    def action_atirar(self):
        if self.pedras > 0:
            if not self.images_list == self.imagesatirar:
                if self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, LEFT))
                if not self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, RIGHT))
                self.pedras -= 1
                self.update_image(self.imagesatirar)
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
        else:
            self.execute = self.action_parado

    def action_in_attack(self):
        if not self.images_list == self.imagesattack:
            self.update_image(self.imagesattack)
        if self.images_list == self.imagesattack:
            self.update_image(self.imagesattack)         
            if self.counter == ((len(self.imagesattack) - 1) * self.sprint_walk_factor):
                self.execute = self.action_attack
    
    def action_attack(self):
        if self.update_image(self.imagesattack):
            self.execute = self.action_parado

    def action_hit(self):
        if not self.images_list == self.imageshit:
            self.life -= 1
            if self.life <=0:
                self.kill()
            self.update_image(self.imageshit)
        if self.update_image(self.imageshit):
            self.execute = self.action_parado

    def combine_moviment(self):
        if UP in self.move_list:
            self.move((0, -self.step))
            self.execute = self.action_andando
            self.move_list = []
        if DOWN in self.move_list:
            self.move((0, self.step))
            self.execute = self.action_andando
            self.move_list = []
        if RIGHT in self.move_list:
            self.reverse = False
            self.move((self.step, 0))
            self.execute = self.action_andando
            self.move_list = []
        if LEFT in self.move_list:
            self.reverse = True
            self.move((-self.step, 0))   
            self.execute = self.action_andando
            self.move_list = []
        if STOPPED in self.move_list:
            self.execute = self.action_parado
            self.move_list = []
        if MOONWALK in self.move_list:
            self.execute = self.action_andando
            self.move_list = []

    def move_up(self):
        self.move_list.append(UP)
    
    def move_down(self):
        self.move_list.append(DOWN)
    
    def move_left(self):
        self.move_list.append(LEFT)

    def move_right(self):
        self.move_list.append(RIGHT)

    def move_stopped(self):
        if not self.execute in [self.action_in_attack, self.action_attack, self.action_hit, self.action_atirar]:
            self.move_list.append(STOPPED)

    def move_moonwalk(self):
        self.move_list.append(MOONWALK)
    
    def move_hit(self):
        self.execute = self.action_hit

    def move_atirar(self):
        self.execute = self.action_atirar
    
    def move_attack(self):
        self.execute = self.action_in_attack
            
    def update(self):
        self.combine_moviment()
        print(self.execute)
        self.execute()





