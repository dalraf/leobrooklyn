# Import the pygame module
import pygame
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame.time import Clock
from pygame.image import load
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
        self.counter = 0

    def update(self, pressed_keys):
        print(pressed_keys)
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.image = load(self.images[self.counter])
            self.counter = (self.counter + 1) % len(self.images)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -20)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 20)
        if pressed_keys[K_LEFT]:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.move_ip(-20, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(20, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = Clock()
grupo_player = GroupSingle()
player = Player()
grupo_player.add(player)

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

    grupo_player.draw(screen)
    pygame.display.update()