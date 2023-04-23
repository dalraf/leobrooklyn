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
from grupos import (
    grupo_player,
    grupo_enemy,
    grupo_objets_player,
    grupo_objets_enemy,
    All_sprites,
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
som.play()

while running:

    clock.tick(25)

    screen.fill((255, 255, 255))


    def generate_enemies(tick_enemies):
        if not stopgame:
            if tick_enemies == 0:
                if background.distance % DIFICULT_AVANCE == 0:
                    fator = 1 + int(background.distance / DIFICULT_AVANCE)
                    grupo_enemy.add(
                        [
                            random.choice(enemylist)(int(fator / 2))
                            for i in range(random.randint(1, fator))
                        ]
                    )
                    tick_enemies = 100
            tick_enemies -= 1
            if tick_enemies < 0:
                tick_enemies = 0
        return tick_enemies

    tick_enemies = generate_enemies(tick_enemies)

    def object_sprite_colide(sprite_group, object_group):
        for sprite_single in sprite_group:
            for object_single in object_group:
                if (
                    calcule_vetor_distance(
                        sprite_single.rect.center,
                        object_single.rect.center,
                    )
                    < DERIVACAO
                ):
                    sprite_single.move_hit(object_single.damage)
                    object_single.kill()


    object_sprite_colide(grupo_enemy, grupo_objets_player)
    object_sprite_colide(grupo_player, grupo_objets_enemy)

    for player_single in grupo_player:
        for enemy_single in grupo_enemy:
            
            if player_single.execute == player_single.action_attack:
                if (
                    calcule_vetor_distance(
                        player_single.rect.center, enemy_single.rect.center
                    )
                    < DERIVACAO
                ):
                    if player_single.reverse:
                        if player_single.rect.left > enemy_single.rect.left:
                            placar.add_enemy_kill(enemy_single.speed)
                            enemy_single.move_hit(player_single.calcule_hit())
                    else:
                        if player_single.rect.left < enemy_single.rect.left:
                            placar.add_enemy_kill(enemy_single.speed)
                            enemy_single.move_hit(player_single.calcule_hit())
                                

            if enemy_single.execute == enemy_single.action_attack:
                if (
                    calcule_vetor_distance(
                        player_single.rect.center, enemy_single.rect.center
                    )
                    < DERIVACAO
                ):
                    if enemy_single.reverse:
                        if enemy_single.rect.left > player_single.rect.left:
                            player_single.move_hit(enemy_single.calcule_hit())
                    else:
                        if enemy_single.rect.left < player_single.rect.left:
                            player_single.move_hit(enemy_single.calcule_hit())


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

            if (
                not pressed_keys[K_RIGHT]
                and not pressed_keys[K_LEFT]
                and not pressed_keys[K_UP]
                and not pressed_keys[K_DOWN]
            ):
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
