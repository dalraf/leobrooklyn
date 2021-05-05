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
from grupos import grupo_objets_player
from objetcs import PedraPlayer
import random
import math

class SpritePerson(pygame.sprite.Sprite):
    def __init__(self):
        super(SpritePerson, self).__init__()
        self.pedra = PedraPlayer
        self.imagesattack = [resource_path('images/Player-1-Attack-' + str(i) + '.png') for i in range(1,6)]
        self.imageswalk = [resource_path('images/Player-1-Walk-' + str(i) + '.png') for i in range(1,5)]
        self.imagesstop = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,5)]
        self.imageshit = [resource_path('images/Player-1-Hit-' + str(i) + '.png') for i in range(1,5)]
        self.imagesatirar = [resource_path('images/Player-1-Atirar-' + str(i) + '.png') for i in range(1,5)]
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
        self.damage_attack_1 = 2
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

    def calcule_hit(self):
        if self.execute == self.action_attack:
            return self.damage_attack_1

    def action_parado(self):
        self.update_image(self.imagesstop)
    
    def action_andando(self):
        self.update_image(self.imageswalk)

    def action_atirar(self):
        if self.pedras > 0:
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
            else:
                if self.counter >= (len(self.imagesatirar) * self.sprint_walk_factor):
                    if self.reverse:
                        grupo_objets_player.add(PedraPlayer(self.rect.x , self.rect.y, LEFT))
                    if not self.reverse:
                        grupo_objets_player.add(PedraPlayer(self.rect.x , self.rect.y, RIGHT))                
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
        if self.update_image(self.imageshit):
            self.execute = self.action_parado
    
    def move_hit(self,damage):
        self.execute = self.action_hit
        self.life -= damage
        if self.life <=0:
            self.kill()

    def calculate_path(self, group, diametro):
        
        final_dx = 0
        final_dy = 0

        for sprite in group:
            
            if sprite != self:

                dx, dy = sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y
            
                dist = math.hypot(dx, dy)
            
                if diametro > 0 and dist < diametro and dist > 0:
                    dx, dy = dx / dist, dy / dist
            
                elif diametro > 0 and dist > diametro:
                    dx , dy = 0 , 0
            
                elif diametro == 0 and dist > 0:
                    dx, dy = dx / dist, dy / dist
            
                else:
                    dx , dy = 0 , 0

                final_dx += dx
                final_dy += dy

        return final_dx, final_dy

    def update(self,grupo_player,grupo_enemy):
        pass