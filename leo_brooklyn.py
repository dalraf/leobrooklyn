from config import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
from pygame.sprite import groupcollide
from pygame.time import Clock
import random

from pygame.locals import (
    KEYDOWN,
    KEYUP,
    QUIT,
    K_ESCAPE,
    K_RETURN,
    K_DOWN,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

from background import Background
from placar import Placar
from som import Som
from player import Player
from enemy import Enemy
from controle import Controle
from sprite_groups import grupo_player, grupo_enemy, grupo_objets

pygame.init()

pygame.display.set_caption('Leo Brooklin Stories')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

tick_enemies = 0
clock = Clock()
background = Background()
som = Som()
placar = Placar()
controle = Controle()
player = Player()
grupo_player.add(player)

running = True
stopgame = True
som.play()

while running:

    clock.tick(20)

    screen.fill((255, 255, 255))

    if not stopgame:
        if tick_enemies == 0:
            fator = 1 + int(background.distance / 100)
            grupo_enemy.add([Enemy(int(fator/2)) for i in range(random.randint(1,fator))])
            tick_enemies = 100
        tick_enemies -= 1
        if tick_enemies < 0:
            tick_enemies = 0

    colisao_inimigo_inimigo = groupcollide(grupo_enemy, grupo_enemy, False, False)

    colisao_player_inimigo = groupcollide(grupo_player, grupo_enemy, False, False)

    colisao_object_inimigo = groupcollide(grupo_objets, grupo_enemy, True, False)

    if len(colisao_object_inimigo) > 0:
        for objectcol, enemiescol in colisao_object_inimigo.items():
            for enemycol in  enemiescol:
                placar.update(enemycol.speed)
                enemycol.kill()

    if len(colisao_player_inimigo) > 0:
        for playercol, enemiescol in colisao_player_inimigo.items():
            playercol.kill()
            stopgame = True
            for enemycol in enemiescol:
                enemycol.kill()

    for event in pygame.event.get():
            
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_RETURN:
                stopgame = False
                grupo_player.add(player)
                grupo_enemy.empty()
                placar.zero()
        
        elif event.type == KEYUP:
            
            if event.key == K_SPACE:
                player.shoot()

        elif event.type == QUIT:
            running = False

    if not stopgame:
        
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_RIGHT]:
            player.move_right()
            if player.rect.x > SCREEN_WIDTH /2:
                for enemy_active in grupo_enemy:
                    enemy_active.walk(player.step)
                background.walk(player.step)
        
        if pressed_keys[K_LEFT]:
            player.move_left()
        
        if pressed_keys[K_UP]:
            player.move_up()

        if pressed_keys[K_DOWN]:
            player.move_down()

        if pressed_keys[K_DOWN] or pressed_keys[K_UP] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            player.walk()

        grupo_player.update()
        grupo_enemy.update(grupo_player, grupo_enemy)
        grupo_objets.update()
    else:
        controle.draw(screen)

    background.draw(screen)

    placar.draw(screen)

    grupo_player.draw(screen)
    
    grupo_enemy.draw(screen)

    grupo_objets.draw(screen)

    if stopgame:
        controle.draw(screen)

    pygame.display.update()