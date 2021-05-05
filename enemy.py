from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPRITE_LEVEL_Y_HIGH,
    LEFT, RIGHT,
    ATTACK_RATIO,
    DERIVACAO,
    STATE_ATTACK,
    STATE_INATTACK,
    STATE_WALK,
    STATE_STOP,
    STATE_MOONWALK,
    resource_path,
)
import pygame
from pygame.image import load
from persons import SpritePerson
from objetcs import PedraEnemy
from grupos import grupo_objets_enemy, grupo_player
import random

class Enemy(SpritePerson):
    def __init__(self, speed):
        super(Enemy, self).__init__()
        self.tipo = random.choice([1,2])
        self.imageswalk = [resource_path('images/Enemy-' + str(self.tipo) + '-Walk-' + str(i) + '.png') for i in range(1,7)]
        self.imagesattack = [resource_path('images/Enemy-' + str(self.tipo) + '-Attack-' + str(i) + '.png') for i in range(1,7)]
        self.imagesstop = [resource_path('images/Enemy-' + str(self.tipo) + '-Walk-' + str(i) + '.png') for i in [1,]]
        self.imageshit = [resource_path('images/Enemy-' + str(self.tipo) + '-Walk-' + str(i) + '.png') for i in range(1,7)]
        self.imagesatirar = [resource_path('images/Enemy-' + str(self.tipo) + '-Attack-' + str(i) + '.png') for i in range(1,7)]
        self.image = load(self.imageswalk[0])
        self.images_list = self.imagesstop
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0,500)
        self.rect.x = SCREEN_WIDTH
        self.counter = 0
        self.speed = random.randint(3, 3 + speed)
        self.sprint_walk_factor = 2
        self.pedras = random.randint(0,2)
        self.reverse = False
        self.life = 3
        self.execute = self.action_parado
    
    def action_atirar(self):
        if self.pedras > 0:
            if not self.images_list == self.imagesatirar:
                if self.reverse:
                    grupo_objets_enemy.add(PedraEnemy(self.rect.x , self.rect.y, LEFT))
                if not self.reverse:
                    grupo_objets_enemy.add(PedraEnemy(self.rect.x , self.rect.y, RIGHT))
                self.pedras -= 1
                self.update_image(self.imagesatirar)
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
        else:
            self.execute = self.action_parado

    def move_hit(self):
        self.execute = self.action_hit

    def paralaxe(self,step):
        self.rect.x -= step
   
    def attack_trigger(self):
        if random.randint(1,3000) < self.speed * 30:
            return True
        else:
            return False
    
    def update(self,grupo_player,grupo_enemy):

        if not self.execute in [self.action_in_attack, self.action_attack, self.action_hit, self.action_atirar]:

            if not pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO)):
                for player_active in grupo_player:
                    if self.rect.y in range(player_active.rect.y - DERIVACAO, player_active.rect.y + DERIVACAO):
                        if self.attack_trigger():
                            self.execute = self.action_atirar
            
            if pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO)):
                for player_active in grupo_player:
                    if self.rect.y in range(player_active.rect.y - DERIVACAO, player_active.rect.y + DERIVACAO):
                        if self.attack_trigger():
                            self.execute = self.action_in_attack

        self.dx = 0
        self.dy = 0

        if not pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO)):

            dx, dy = self.calculate_path(grupo_player, 0)
            
            self.dx += dx 
            self.dy += dy

            dx, dy = self.calculate_path(grupo_enemy, 100)

            self.dx -= dx
            self.dy -= dy

        self.passo_x = int(self.dx * self.speed)
        self.passo_y = int(self.dy * self.speed)

        self.move((self.passo_x,self.passo_y))

        if self.dx < 0:
            self.reverse = True
        elif self.dx > 0:
            self.reverse = False

        if not self.execute in [self.action_in_attack, self.action_attack, self.action_hit, self.action_atirar]:
            if self.dx == 0 and self.dy == 0:
                self.execute = self.action_parado
            else:
                self.execute = self.action_andando

        self.execute()


