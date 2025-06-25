from config import screen, SCREEN_WIDTH, DIFICULT_AVANCE, DERIVACAO, calcule_vetor_distance
import pygame
from pygame.time import Clock
import random
from pygame.locals import *
from grupos import grupo_player, grupo_enemy, All_sprites, grupo_objets_player, grupo_objets_enemy, grupo_objets_static
from background import Background
from som import Som
from placar import Placar
from enemy import Wooden, Steam
from player import Player
from objetcs import PedraParada, BandAid
from controle import Mensagem_Inicio


class GameState:
    """Encapsula o estado do jogo"""
    def __init__(self):
        self.tick_enemies = 0
        self.paralaxe = 0
        self.running = True
        self.stopgame = True
        self.enemylist = [Wooden, Steam]
        self.clock = Clock()
        
        # Inicializa componentes do jogo
        self.background = Background()
        self.som = Som()
        self.placar = Placar()
        self.mensagem_inicio = Mensagem_Inicio()
        self.player = None

class Game:
    """Classe principal que controla o loop do jogo"""
    def __init__(self):
        self.state = GameState()
        self.key_actions = {
            K_ESCAPE: self.quit_game,
            K_RETURN: self.restart_game,
            K_SPACE: lambda: self.execute_player_action('move_atirar'),
            K_LCTRL: lambda: self.execute_player_action('move_attack')
        }

    def quit_game(self):
        self.state.running = False

    def restart_game(self):
        if self.state.stopgame:
            self.state.stopgame = False
            self.state.som.play()
            self.state.player = Player()
            grupo_player.add(self.state.player)
            for enemy in grupo_enemy:
                enemy.kill()
            for objects in grupo_objets_enemy:
                objects.kill()
            for objects in grupo_objets_player:
                objects.kill()
            self.state.placar.zero()
            self.state.background.zero()

    def execute_player_action(self, action_name):
        for player in grupo_player:
            getattr(player, action_name)()

    def generate_enemies(self):
        """Gera inimigos e objetos de acordo com a dificuldade"""
        state = self.state
        if not state.stopgame:
            if state.tick_enemies == 0:
                if state.background.distance % DIFICULT_AVANCE == 0:
                    fator = 1 + int(state.background.distance / DIFICULT_AVANCE)
                    self.spawn_enemies(fator)
                    self.spawn_objects()
                    state.tick_enemies = 100
            state.tick_enemies = max(0, state.tick_enemies - 1)

    def spawn_enemies(self, fator):
        grupo_enemy.add([
            random.choice(self.state.enemylist)(int(fator / 2))
            for _ in range(random.randint(1, fator))
        ])

    def spawn_objects(self):
        grupo_objets_static.add([PedraParada() for _ in range(random.randint(0, 1))])
        grupo_objets_static.add([BandAid() for _ in range(random.randint(0, 1))])

    def object_sprite_colide(self, sprite_group, object_group):
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

    def object_sprite_get(self, sprite_group, object_group):
        for sprite_single in sprite_group:
            for object_single in object_group:
                if (
                    calcule_vetor_distance(
                        sprite_single.rect.center,
                        object_single.rect.center,
                    )
                    < DERIVACAO
                ):
                    sprite_single.get_object(object_single)
                    object_single.kill()

    def player_enemy_attack_hit(self):
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
                                self.state.placar.add_enemy_kill(enemy_single.speed)
                                enemy_single.move_hit(player_single.calcule_hit())
                        else:
                            if player_single.rect.left < enemy_single.rect.left:
                                self.state.placar.add_enemy_kill(enemy_single.speed)
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

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                action = self.key_actions.get(event.key)
                if action:
                    action()
            elif event.type == QUIT:
                self.state.running = False

    def update_game_state(self):
        state = self.state
        if not state.stopgame:
            pressed_keys = pygame.key.get_pressed()

            for player in grupo_player:
                if pressed_keys[K_RIGHT]:
                    if player.rect.x > SCREEN_WIDTH * 0.8:
                        state.paralaxe = player.step
                        player.move_moonwalk()
                    else:
                        state.paralaxe = 0
                        player.move_right()
                elif pressed_keys[K_LEFT]:
                    player.move_left()
                elif pressed_keys[K_UP]:
                    player.move_up()
                elif pressed_keys[K_DOWN]:
                    player.move_down()
                else:
                    player.move_stopped()

            if state.paralaxe > 0:
                for grupo in [
                    grupo_enemy,
                    grupo_objets_player,
                    grupo_objets_enemy,
                    grupo_objets_static,
                ]:
                    for obj in grupo:
                        obj.paralaxe(state.paralaxe)
                state.background.paralaxe(state.paralaxe)
                state.paralaxe = 0

            grupo_player.update()
            grupo_enemy.update(grupo_player, grupo_enemy)
            grupo_objets_player.update()
            grupo_objets_enemy.update()
            grupo_objets_static.update()

    def draw_elements(self):
        state = self.state
        screen.fill((255, 255, 255))
        state.background.draw(screen)

        for player in grupo_player:
            state.placar.set_pedras(player.pedras)
            state.placar.set_life(player.life)
        state.placar.draw(screen)

        if state.stopgame:
            state.mensagem_inicio.draw(screen)

        All_sprites.add(grupo_player)
        All_sprites.add(grupo_enemy)
        All_sprites.add(grupo_objets_player)
        All_sprites.add(grupo_objets_enemy)
        All_sprites.add(grupo_objets_static)

        for sprite in sorted(All_sprites, key=lambda spr: spr.rect.bottom):
            screen.blit(sprite.image, sprite.rect)
        
        pygame.display.update()

    def run(self):
        while self.state.running:
            self.state.clock.tick(25)
            self.handle_input()
            
            if len(grupo_player) == 0:
                self.state.stopgame = True
                self.state.som.stop()

            self.generate_enemies()
            self.object_sprite_get(grupo_player, grupo_objets_static)
            self.object_sprite_colide(grupo_enemy, grupo_objets_player)
            self.object_sprite_colide(grupo_player, grupo_objets_enemy)
            self.player_enemy_attack_hit()
            
            self.update_game_state()
            self.draw_elements()

if __name__ == '__main__':
    game = Game()
    game.run()
