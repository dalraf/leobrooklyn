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
        self.image = load('images/tiles-0.png')
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -20)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 20)
        if pressed_keys[K_LEFT]:
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

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
            
    pressed_keys = pygame.key.get_pressed()

    screen.fill((255, 255, 255))

    grupo_player.update(pressed_keys)

    grupo_player.draw(screen)

    pygame.display.update()