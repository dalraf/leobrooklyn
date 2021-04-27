import pygame
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from player import Player
from enemy import Enemy
from pygame.time import Clock
from config import SCREEN_HEIGHT, SCREEN_WIDTH
import random
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

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