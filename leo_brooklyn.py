from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    ATTACK_RATIO,
    OBJET_KILL_RATIO,
)
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
from sprite_groups import grupo_player, grupo_enemy, grupo_objets, All_sprites

pygame.init()

pygame.display.set_caption('Leo Brooklin Stories')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

tick_enemies = 0
clock = Clock()
background = Background()
som = Som()
placar = Placar()
controle = Controle()
grupo_player.add(Player())

paralaxe = 0
running = True
stopgame = True
#som.play()

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

    colisao_object_inimigo = groupcollide(grupo_enemy, grupo_objets, False, True, pygame.sprite.collide_circle_ratio(OBJET_KILL_RATIO))
    
    if len(colisao_object_inimigo) > 0:
        for enemycol, objectlistcol in colisao_object_inimigo.items():
            enemycol.hit()

    colisao_object_player = groupcollide(grupo_player, grupo_objets, False, True, pygame.sprite.collide_circle_ratio(OBJET_KILL_RATIO))

    if len(colisao_object_player) > 0:
        for playercol, objectlistcol in colisao_object_player.items():
            playercol.hit()

    colisao_attack_player_inimigo = groupcollide(grupo_player, grupo_enemy, False, False, pygame.sprite.collide_circle_ratio(ATTACK_RATIO))

    if len(colisao_attack_player_inimigo) > 0:
        for playercol, enemylistcol in colisao_attack_player_inimigo.items():
            if playercol.attack_activated:
                for enemycol in enemylistcol:
                    if playercol.reverse:
                        if playercol.rect.left > enemycol.rect.left:
                            placar.add_enemy_kill(enemycol.speed)
                            enemycol.hit()
                    else:
                        if playercol.rect.left < enemycol.rect.left:
                            placar.add_enemy_kill(enemycol.speed)
                            enemycol.hit()
            else:
                for enemycol in enemylistcol:
                    if enemycol.attack_activated:
                        if enemycol.reverse:
                            if enemycol.rect.left > playercol.rect.left:
                                playercol.hit()
                        else:
                            if enemycol.rect.left < playercol.rect.left:
                                playercol.hit()

    if len(grupo_player) == 0:
        stopgame = True

    for event in pygame.event.get():
            
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False
            
            if stopgame:
                if event.key == K_RETURN:
                    stopgame = False
                    player = Player()
                    grupo_player.add(player)
                    grupo_enemy.empty()
                    grupo_objets.empty()
                    placar.zero()
                    background.zero()
        
        elif event.type == KEYUP:
            
            if event.key == K_SPACE:
                for player in grupo_player:
                    player.shoot()
            
            if event.key == K_LCTRL:
                for player in grupo_player:
                    player.attack()

        elif event.type == QUIT:
            running = False

    if not stopgame:
        
        pressed_keys = pygame.key.get_pressed()

        for player in grupo_player:

            if pressed_keys[K_RIGHT]:
                if player.rect.x > SCREEN_WIDTH * 0.5:
                    paralaxe = player.step
                    player.move_stopped()
                else:
                    paralaxe = 0
                    player.move_right()
            
            if pressed_keys[K_LEFT]:
                player.move_left()
            
            if pressed_keys[K_UP]:
                player.move_up()

            if pressed_keys[K_DOWN]:
                player.move_down()

            if not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT] and not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
                player.stopped()
        
        if paralaxe > 0:
            for enemy_active in grupo_enemy:
                enemy_active.paralaxe(paralaxe)
            for object_active in grupo_objets:
                object_active.paralaxe(paralaxe)
            background.paralaxe(paralaxe)
            paralaxe = 0


        grupo_player.update()
        grupo_enemy.update(grupo_player, grupo_enemy)
        grupo_objets.update()
    
    else:
        controle.draw(screen)

    background.draw(screen)


    for player in grupo_player:
        placar.set_pedras(player.pedras)
        placar.set_life(player.life)
    
    placar.draw(screen)


    All_sprites.add(grupo_player)
    All_sprites.add(grupo_enemy)
    All_sprites.add(grupo_objets)
    
    for sprite in sorted(All_sprites, key=lambda spr: spr.rect.bottom):
        screen.blit(sprite.image, sprite.rect)

    if stopgame:
        controle.draw(screen)

    pygame.display.update()