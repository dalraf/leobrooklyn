from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPRITE_LEVEL_Y_HIGH,
    LEFT, RIGHT,
    ATTACK_RATIO,
    Y_DEVIRACAO,
    resource_path
)
import pygame
from pygame.image import load
import random
from sprite_class import SpriteGame
from objetcs import Pedra
from sprite_groups import grupo_objets, grupo_player

class Enemy(SpriteGame):
    def __init__(self, speed):
        super(Enemy, self).__init__()
        self.imageswalk = [resource_path('images/Enemy-1-Walk-' + str(i) + '.png') for i in range(1,6)]
        self.imagesattack = [resource_path('images/Enemy-1-Attack-' + str(i) + '.png') for i in range(1,6)]
        self.image = load(self.imageswalk[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0,500)
        self.rect.x = SCREEN_WIDTH
        self._layer = self.rect.y
        self.counter = 0
        self.speed = random.randint(3, 3 + speed)
        self.sprint_walk_factor = 3
        self.armtime = 0
        self.in_attack = False
        self.attack_activated = False
        self.pedras = random.randint(0,2)
        self.reverse = False
        self.life = 3
        self.hittime = 0

    def update_image(self, images_list,reset):
        if not reset:
            self.counter = (self.counter + 1) % (len(images_list) * self.sprint_walk_factor)
            self.image = load(images_list[int(self.counter / self.sprint_walk_factor)])
        else:
            self.counter = 0
            self.image = load(images_list[0])
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False) 


    def paralaxe(self,step):
        self.rect.x -= step

    
    def attack_trigger(self):
        if random.randint(1,3000) < self.speed * 30:
            return True
        else:
            return False

    def shoot(self):
        if self.pedras > 0:
            if self.armtime == 0:
                if self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, LEFT))
                if not self.reverse:
                    grupo_objets.add(Pedra(self.rect.x , self.rect.y, RIGHT))
                self.armtime = 20
                self.pedras -= 1

    def attack(self):
        if self.armtime == 0:
            self.in_attack = True
            self.counter = 0
            self.armtime = len(self.imagesattack) * self.sprint_walk_factor

    def hit(self):
        if self.hittime <= 0:
            self.life -= 1
            if self.life <=0:
                self.kill()
            self.hittime = self.sprint_walk_factor * 6
    
    def update(self,grupo_player,grupo_enemy):

        self.hittime -= self.sprint_walk_factor

        self.armtime -= 1
        if self.armtime < 0:
            self.armtime = 0

        if not self.in_attack and self.armtime == 0 and self.hittime <= 0:

            if not pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO)):
                for player_active in grupo_player:
                    if self.rect.y in range(player_active.rect.y - Y_DEVIRACAO, player_active.rect.y + Y_DEVIRACAO):
                        if self.attack_trigger():
                            self.shoot()
            
            if pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO)):
                for player_active in grupo_player:
                    if self.rect.y in range(player_active.rect.y - Y_DEVIRACAO, player_active.rect.y + Y_DEVIRACAO):
                        if self.attack_trigger():
                            self.attack()

        self.dx = 0
        self.dy = 0

        if not pygame.sprite.spritecollide(self, grupo_player, False, pygame.sprite.collide_circle_ratio(1.5)):

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
        self._layer = self.rect.y
        
        if self.rect.bottom <= SPRITE_LEVEL_Y_HIGH:
            self.rect.bottom = SPRITE_LEVEL_Y_HIGH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.dx < 0:
            self.reverse = True
        elif self.dx > 0:
            self.reverse = False
        
        if self.dx == 0:
            self.stopped = True
        else: 
            self.stopped = False

        if self.armtime > 0 and self.in_attack:
            self.update_image(self.imagesattack,False)
            if int(self.counter / self.sprint_walk_factor) == (len(self.imagesattack) - 1):
                self.attack_activated = True
        
        elif self.armtime == 0 and self.in_attack:
            self.in_attack = False
            self.attack_activated = False
            self.update_image(self.imageswalk,True)

        elif self.stopped:
            self.update_image(self.imageswalk,True)

        else:
            self.update_image(self.imageswalk,False)



