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
from enemy import Wooden, Steam
from controle import Controle
from objetcs import PedraParada
from grupos import (
    grupo_player,
    grupo_enemy,
    grupo_objets_player,
    grupo_objets_enemy,
    grupo_objets_static,
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


def generate_enemies_objects(tick_enemies):
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
                grupo_objets_static.add(
                    [PedraParada() for i in range(random.randint(1, 2))]
                )
                tick_enemies = 100
        tick_enemies -= 1
        if tick_enemies < 0:
            tick_enemies = 0
    return tick_enemies


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

def object_sprite_get(sprite_group, object_group):
    for sprite_single in sprite_group:
        for object_single in object_group:
            if (
                calcule_vetor_distance(
                    sprite_single.rect.center,
                    object_single.rect.center,
                )
                < DERIVACAO
            ):
                sprite_single.get_object(object_single.damage)
                object_single.kill()


def player_enemy_attack_hit(grupo_player, grupo_enemy, placar):
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


while running:
    clock.tick(25)

    screen.fill((255, 255, 255))

    tick_enemies = generate_enemies_objects(tick_enemies)
    object_sprite_get(grupo_player, grupo_objets_static)
    object_sprite_colide(grupo_enemy, grupo_objets_player)
    object_sprite_colide(grupo_player, grupo_objets_enemy)
    player_enemy_attack_hit(grupo_player, grupo_enemy, placar)

    # Termina jogo se jogadores morreram
    if len(grupo_player) == 0:
        stopgame = True
        som.stop()

    # loop de eventos do teclado
    for event in pygame.event.get():
        # Verifica tecla apertada
        if event.type == KEYDOWN:
            # Para o jogo em caso de scape
            if event.key == K_ESCAPE:
                running = False

            # Renicia o jogo em caso de jogo parado e apertar Enter
            if stopgame:
                if event.key == K_RETURN:
                    stopgame = False
                    som.play()
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

            # Faz player atirar
            if event.key == K_SPACE:
                for player in grupo_player:
                    player.move_atirar()

            # Faz player socar
            if event.key == K_LCTRL:
                for player in grupo_player:
                    player.move_attack()

        elif event.type == QUIT:
            running = False

    # Verificar se jogo continua
    if not stopgame:
        # Verifica teclas pressionadas
        pressed_keys = pygame.key.get_pressed()

        # Define movimento do player
        for player in grupo_player:
            if pressed_keys[K_RIGHT]:
                if player.rect.x > SCREEN_WIDTH * 0.8:
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

        # Calcula paralaxe
        if paralaxe > 0:
            for grupo in [
                grupo_enemy,
                grupo_objets_player,
                grupo_objets_enemy,
                grupo_objets_static,
            ]:
                for object in grupo:
                    object.paralaxe(paralaxe)
            background.paralaxe(paralaxe)
            paralaxe = 0

        # Update de objetos
        grupo_player.update()
        grupo_enemy.update(grupo_player, grupo_enemy)
        grupo_objets_player.update()
        grupo_objets_enemy.update()
        grupo_objets_static.update()

    # Printa Background
    background.draw(screen)

    # Define Placar
    for player in grupo_player:
        placar.set_pedras(player.pedras)
        placar.set_life(player.life)
    placar.draw(screen)

    # Imprime mensagem de jogo finalizado
    if stopgame:
        controle.draw(screen)

    # Printa todos os sriptes
    All_sprites.add(grupo_player)
    All_sprites.add(grupo_enemy)
    All_sprites.add(grupo_objets_player)
    All_sprites.add(grupo_objets_enemy)
    All_sprites.add(grupo_objets_static)

    # Faz impressao dos sprites de acordo com a posicao vertical
    for sprite in sorted(All_sprites, key=lambda spr: spr.rect.bottom):
        screen.blit(sprite.image, sprite.rect)

    pygame.display.update()
