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
        self.rect.x = 0
        self.counter = 0
        self.step_choice = [0, 20, -20]
        self.speed = 3

    def update(self,player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.image = load(self.images[self.counter])
        if dx * self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.counter = (self.counter + 1) % len(self.images)




pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = Clock()
grupo_player = GroupSingle()
grupo_enemy = Group()
player = Player()
enemy = Enemy()
grupo_player.add(player)
grupo_enemy.add(enemy)

running = True

while running:

    clock.tick(20)

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    
    grupo_player.update(pressed_keys)
    grupo_enemy.update(player)

    grupo_player.draw(screen)
    grupo_enemy.draw(screen)

    pygame.display.update()