from config import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
from pygame.sprite import groupcollide
from pygame.time import Clock
import random

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from background import Background
from player import Player
from enemy import Enemy
from sprite_groups import grupo_player, grupo_enemy, grupo_objets

pygame.init()

pygame.display.set_caption('Leo Brooklin Stories')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

tick_enemies = 0
clock = Clock()
background = Background()
player = Player()
grupo_player.add(player)

running = True

while running:

    clock.tick(20)

    screen.fill((255, 255, 255))

    if tick_enemies == 0:
        grupo_enemy.add([Enemy() for i in range(random.randint(1,2))])
        tick_enemies = 100
    tick_enemies -= 1
    if tick_enemies < 0:
        tick_enemies = 0

    colisao_inimigo_inimigo = groupcollide(grupo_enemy, grupo_enemy, False, False)

    colisao_player_inimigo = groupcollide(grupo_player, grupo_enemy, False, False)

    colisao_object_inimigo = groupcollide(grupo_objets, grupo_enemy, True, True)

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

    grupo_objets.update()

    background.draw(screen)

    grupo_player.draw(screen)
    
    grupo_enemy.draw(screen)

    grupo_objets.draw(screen)

    pygame.display.update()