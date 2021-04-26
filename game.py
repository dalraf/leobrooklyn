# Import the pygame module
import pygame
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame.time import Clock
from pygame.image import load
import random
import math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.images = ['images/tiles-0.png','images/tiles-2.png','images/tiles-3.png','images/tiles-4.png','images/tiles-5.png',]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT/2
        self.rect.x = SCREEN_WIDTH/2
        self.counter = 0
        self.reverse = False

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -20)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 20)
        if pressed_keys[K_LEFT]:
            self.reverse = True
            self.rect.move_ip(-20, 0)
        if pressed_keys[K_RIGHT]:
            self.reverse = False
            self.rect.move_ip(20, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.image = load(self.images[self.counter])
            if self.reverse:
                self.image = pygame.transform.flip(self.image, True, False)
            self.counter = (self.counter + 1) % len(self.images)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.images = ['images/tiles-0.png','images/tiles-2.png','images/tiles-3.png','images/tiles-4.png','images/tiles-5.png',]
        self.image = load(self.images[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.counter = 0
        self.speed = 3
        self.dx = 0
        self.dy = 0

    def calculate_path(self, group, diametro):
        
        final_dx = 0
        final_dy = 0

        for sprite in group:
            
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
        
        self.dx = 0
        self.dy = 0

        dx, dy = self.calculate_path(grupo_player, 0)
        
        self.dx += dx 
        self.dy += dy

        dx, dy = self.calculate_path(grupo_enemy, 100)

        self.dx -= dx
        self.dy -= dy

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.image = load(self.images[self.counter])
        if self.dx < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.dx != 0 and self.dy != 0:
            self.counter = (self.counter + 1) % len(self.images)




pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = Clock()
grupo_player = GroupSingle()
grupo_enemy = Group()
player = Player()
enemylist = [Enemy() for i in range(4)]
grupo_player.add(player)
grupo_enemy.add(enemylist)

running = True

while running:

    clock.tick(20)

    screen.fill((255, 255, 255))

    colisao_inimigo_inimigo = groupcollide(grupo_enemy, grupo_enemy, False, False)

    colisao_player_inimigo = groupcollide(grupo_player, grupo_enemy, False, False)

    if len(colisao_player_inimigo) > 0:
        for playercol, enemiescol in colisao_player_inimigo.items():
            playercol.kill()
            for enemycol in enemiescol:
                enemycol.kill()

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    
    grupo_player.update(pressed_keys)
    grupo_enemy.update(grupo_player, grupo_enemy)

    grupo_player.draw(screen)
    grupo_enemy.draw(screen)

    pygame.display.update()