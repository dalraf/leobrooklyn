from config import (
    screen,
    SCREEN_WIDTH,
    DIFICULT_AVANCE,
    DERIVACAO,
    calcule_vetor_distance,
)
import pygame
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
    MOUSEBUTTONUP,
)

from background import Background
from placar import Placar
from som import Som
from player import Player
from enemy import Wooden, Steam
from controle import Controle
from grupos import (grupo_player,
                    grupo_enemy,
                    grupo_objets_player,
                    grupo_objets_enemy,
                    All_sprites
                    )


tick_enemies = 0
clock = Clock()
background = Background()
som = Som()
placar = Placar()
controle = Controle()
enemylist = [Wooden, Steam]
paralaxe = 0
running = True
stopgame = True
# som.play()

while running:

    clock.tick(25)

    screen.fill((255, 255, 255))

    if not stopgame:
        if tick_enemies == 0:
            if background.distance % DIFICULT_AVANCE == 0:
                fator = 1 + int(background.distance / DIFICULT_AVANCE)
                grupo_enemy.add([random.choice(enemylist)(int(fator/2))
                                for i in range(random.randint(1, fator))])
                tick_enemies = 100
        tick_enemies -= 1
        if tick_enemies < 0:
            tick_enemies = 0

    for enemycol in grupo_enemy:
        for objectcol in grupo_objets_player:
            if calcule_vetor_distance(
                enemycol.rect.center,
                objectcol.rect.center,
                    ) < DERIVACAO:
                enemycol.move_hit(objectcol.damage)
                objectcol.kill()

    for playercol in grupo_player:
        for objectcol in grupo_objets_enemy:
            if calcule_vetor_distance(
                playercol.rect.center,
                objectcol.rect.center,
                    ) < DERIVACAO:
                playercol.move_hit(objectcol.damage)
                objectcol.kill()

    for playercol in grupo_player:
        if playercol.execute == playercol.action_attack:
            for enemycol in grupo_enemy:
                if not enemycol.execute == playercol.action_hit:
                    if calcule_vetor_distance(
                        playercol.rect.center,
                        enemycol.rect.center
                            ) < DERIVACAO:
                        if playercol.reverse:
                            if playercol.rect.left > enemycol.rect.left:
                                placar.add_enemy_kill(enemycol.speed)
                                enemycol.move_hit(playercol.calcule_hit())
                        else:
                            if playercol.rect.left < enemycol.rect.left:
                                placar.add_enemy_kill(enemycol.speed)
                                enemycol.move_hit(playercol.calcule_hit())
        else:
            for enemycol in grupo_enemy:
                if enemycol.execute == enemycol.action_attack:
                    if not playercol.execute == playercol.action_hit:
                        if calcule_vetor_distance(
                            playercol.rect.center,
                            enemycol.rect.center
                                ) < DERIVACAO:
                            if enemycol.reverse:
                                if enemycol.rect.left > playercol.rect.left:
                                    playercol.move_hit(enemycol.calcule_hit())
                            else:
                                if enemycol.rect.left < playercol.rect.left:
                                    playercol.move_hit(enemycol.calcule_hit())

    if len(grupo_player) == 0:
        stopgame = True

    for event in pygame.event.get():

        if event.type == MOUSEBUTTONUP:
            if stopgame:
                stopgame = False
                player = Player()
                grupo_player.add(player)
                for enemy in grupo_enemy:
                    enemy.kill()
                for objects in grupo_objets_enemy:
                    objects.kill()
                for objects in grupo_objets_player:
                    objects.kill()
                placar.zero()
                background.zero()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            if stopgame:
                if event.key == K_RETURN:
                    stopgame = False
                    player = Player()
                    grupo_player.add(player)
                    for enemy in grupo_enemy:
                        enemy.kill()
                    for objects in grupo_objets_enemy:
                        objects.kill()
                    for objects in grupo_objets_player:
                        objects.kill()
                    placar.zero()
                    background.zero()

        elif not event.type == MOUSEBUTTONUP and event.type == KEYUP:

            if event.key == K_SPACE:
                for player in grupo_player:
                    player.move_atirar()

            if event.key == K_LCTRL:
                for player in grupo_player:
                    player.move_attack()

        elif event.type == QUIT:
            running = False

    if not stopgame:

        pressed_keys = pygame.key.get_pressed()

        for player in grupo_player:

            if pressed_keys[K_RIGHT]:
                if player.rect.x > SCREEN_WIDTH * 0.5:
                    paralaxe = player.step
                    player.move_moonwalk()
                else:
                    paralaxe = 0
                    player.move_right()

            if pressed_keys[K_LEFT]:
                player.move_left()

            if pressed_keys[K_UP]:
                player.move_up()

            if pressed_keys[K_DOWN]:
                player.move_down()

            if (not pressed_keys[K_RIGHT] and
                    not pressed_keys[K_LEFT] and
                    not pressed_keys[K_UP] and
                    not pressed_keys[K_DOWN]):
                player.move_stopped()

        if paralaxe > 0:
            for enemy_active in grupo_enemy:
                enemy_active.paralaxe(paralaxe)
            for object_active in grupo_objets_player:
                object_active.paralaxe(paralaxe)
            for object_active in grupo_objets_enemy:
                object_active.paralaxe(paralaxe)
            background.paralaxe(paralaxe)
            paralaxe = 0

        grupo_player.update()
        grupo_enemy.update(grupo_player, grupo_enemy)
        grupo_objets_player.update()
        grupo_objets_enemy.update()

    else:
        controle.draw(screen)

    background.draw(screen)

    for player in grupo_player:
        placar.set_pedras(player.pedras)
        placar.set_life(player.life)

    placar.draw(screen)

    All_sprites.add(grupo_player)
    All_sprites.add(grupo_enemy)
    All_sprites.add(grupo_objets_player)
    All_sprites.add(grupo_objets_enemy)

    for sprite in sorted(All_sprites, key=lambda spr: spr.rect.bottom):
        screen.blit(sprite.image, sprite.rect)

    if stopgame:
        controle.draw(screen)

    pygame.display.update()
