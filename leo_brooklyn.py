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
    K_LCTRL,
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
            if background.distance % 600 == 0:
                fator = 1 + int(background.distance / 600)
                grupo_enemy.add([Enemy(int(fator/2)) for i in range(random.randint(1,fator))])
                tick_enemies = 100
        tick_enemies -= 1
        if tick_enemies < 0:
            tick_enemies = 0

    colisao_player_inimigo = groupcollide(grupo_player, grupo_enemy, True, False, pygame.sprite.collide_circle_ratio(0.2))

    colisao_object_inimigo = groupcollide(grupo_objets, grupo_enemy, True, True)

    colisao_attack_player_inimigo = groupcollide(grupo_player, grupo_enemy, False, False, pygame.sprite.collide_circle_ratio(1))

    if len(colisao_attack_player_inimigo) > 0:
        for playercol, enemylistcol in colisao_attack_player_inimigo.items():
            if playercol.attack_activated:
                for enemycol in enemylistcol:
                    if playercol.reverse:
                        if playercol.rect.left > enemycol.rect.left:
                            enemycol.kill()
                    else:
                        if playercol.rect.left < enemycol.rect.left:
                            enemycol.kill()


    if len(grupo_player) == 0:
        stopgame = True

    for event in pygame.event.get():
            
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_RETURN:
                stopgame = False
                grupo_player.add(player)
                grupo_enemy.empty()
                placar.zero()
                background.zero()
        
        elif event.type == KEYUP:
            
            if event.key == K_SPACE:
                player.shoot()
            
            if event.key == K_LCTRL:
                player.attack()

        elif event.type == QUIT:
            running = False

    if not stopgame:
        
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_RIGHT]:
            if player.rect.x > SCREEN_WIDTH * 0.5:
                for enemy_active in grupo_enemy:
                    enemy_active.walk(player.step)
                background.walk(player.step)
            else:
                 player.move_right()
        
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