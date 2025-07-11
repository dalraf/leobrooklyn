from config import screen, SCREEN_WIDTH, DIFICULT_AVANCE, DERIVACAO, calcule_vetor_distance, ENEMY_SPAWN_TICK_RESET, PARALLAX_START_THRESHOLD, WHITE_COLOR, GAME_FPS
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
from ui_elements import UIManager
import asyncio


class GameState:
    """Encapsula o estado do jogo"""
    def __init__(self):
        self.enemy_spawn_timer = 0
        self.parallax_offset = 0
        self.running = True
        self.stopgame = True
        self.enemylist = [Wooden, Steam]
        self.clock = Clock()
        
        # Inicializa componentes do jogo
        self.background = Background()
        self.som = Som()
        self.placar = Placar()
        self.mensagem_inicio = Mensagem_Inicio()
        self.ui_manager = UIManager() # Inicializa o UIManager
        self.player = Player() # Inicializa o player no início do jogo
        grupo_player.add(self.player) # Adiciona o player ao grupo de sprites

class Game:
    """Classe principal que controla o loop do jogo"""
    def __init__(self):
        self.state = GameState()
        self.key_actions = {
            K_ESCAPE: self.quit_game,
            K_RETURN: self.restart_game,
            K_SPACE: lambda: self.execute_player_action('move_atirar'),
            K_LCTRL: lambda: self.execute_player_action('move_attack'),
            # Adiciona suporte para clique do mouse para iniciar o jogo
            # Isso será tratado no handle_input para MOUSEBUTTONDOWN
        }

    def quit_game(self):
        self.state.running = False

    def restart_game(self):
        if self.state.stopgame:
            self.state.stopgame = False
            self.state.som.play()
            for player in grupo_player:
                player.kill()
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
        """
        Gera inimigos e objetos de acordo com a dificuldade do jogo.
        A geração ocorre quando o timer de spawn de inimigos chega a zero
        e a distância percorrida pelo background é um múltiplo de DIFICULT_AVANCE.
        """
        state = self.state
        if not state.stopgame:
            if state.enemy_spawn_timer == 0:
                if state.background.distance % DIFICULT_AVANCE == 0:
                    # Calcula o fator de dificuldade baseado na distância percorrida
                    fator = 1 + int(state.background.distance / DIFICULT_AVANCE)
                    self.spawn_enemies(fator)
                    self.spawn_objects()
                    state.enemy_spawn_timer = ENEMY_SPAWN_TICK_RESET
            # Decrementa o timer de spawn de inimigos, garantindo que não seja negativo
            state.enemy_spawn_timer = max(0, state.enemy_spawn_timer - 1)

    def spawn_enemies(self, fator):
        grupo_enemy.add([
            random.choice(self.state.enemylist)(int(fator / 2))
            for _ in range(random.randint(1, fator))
        ])

    def spawn_objects(self):
        grupo_objets_static.add([PedraParada() for _ in range(random.randint(0, 1))])
        grupo_objets_static.add([BandAid() for _ in range(random.randint(0, 1))])

    def object_sprite_colide(self, sprite_group, object_group):
        """
        Verifica colisões entre um grupo de sprites e um grupo de objetos.
        Se houver colisão (distância menor que DERIVACAO), o sprite sofre dano
        e o objeto é removido.
        """
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
        """
        Verifica se um sprite "pega" um objeto.
        Se houver proximidade (distância menor que DERIVACAO), o sprite adquire o objeto
        e o objeto é removido.
        """
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
        """
        Verifica e processa os ataques entre o jogador e os inimigos.
        Utiliza os métodos check_attack_hit refatorados nas classes Player e Enemy.
        """
        for player_single in grupo_player:
            for enemy_single in grupo_enemy:
                if player_single.check_attack_hit(enemy_single):
                    self.state.placar.add_enemy_kill(enemy_single.speed)
                    enemy_single.move_hit(player_single.calcule_hit())

                if enemy_single.check_attack_hit(player_single):
                    player_single.move_hit(enemy_single.calcule_hit())

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                action = self.key_actions.get(event.key)
                if action:
                    action()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1: # Botão esquerdo do mouse
                    if self.state.stopgame: # Se o jogo estiver parado, um clique inicia
                        self.restart_game()
                    else:
                        action = self.state.ui_manager.handle_click(event.pos)
                        if action:
                            if action in ["up", "down", "left", "right"]:
                                # Mapeia as direções do dpad para as funções de movimento do player
                                player_move_map = {
                                    "up": "move_up",
                                    "down": "move_down",
                                    "left": "move_left",
                                    "right": "move_right",
                                }
                                self.execute_player_action(player_move_map[action])
                            elif action in ["move_atirar", "move_attack"]:
                                self.execute_player_action(action)
            elif event.type == QUIT:
                self.state.running = False

    def update_game_state(self):
        state = self.state
        if not state.stopgame:
            pressed_keys = pygame.key.get_pressed()

            for player in grupo_player:
                # Verifica todas as teclas pressionadas simultaneamente
                if pressed_keys[K_RIGHT]:
                    if player.rect.x > SCREEN_WIDTH * PARALLAX_START_THRESHOLD:
                        state.parallax_offset = player.step
                        player.move_moonwalk()
                    else:
                        state.parallax_offset = 0
                        player.move_right()
                        
                if pressed_keys[K_LEFT]:
                    player.move_left()
                    
                if pressed_keys[K_UP]:
                    player.move_up()
                    
                if pressed_keys[K_DOWN]:
                    player.move_down()
                    
                # Só para se nenhuma tecla de movimento estiver pressionada
                if not any([pressed_keys[K_UP], pressed_keys[K_DOWN], pressed_keys[K_LEFT], pressed_keys[K_RIGHT]]):
                    player.move_stopped()

            if state.parallax_offset > 0:
                for grupo in [
                    grupo_enemy,
                    grupo_objets_player,
                    grupo_objets_enemy,
                    grupo_objets_static,
                ]:
                    for obj in grupo:
                        obj.paralaxe(state.parallax_offset)
                state.background.paralaxe(state.parallax_offset)
                state.parallax_offset = 0

            grupo_player.update()
            grupo_enemy.update(grupo_player, grupo_enemy)
            grupo_objets_player.update()
            grupo_objets_enemy.update()
            grupo_objets_static.update()

    def draw_elements(self):
        state = self.state
        screen.fill(WHITE_COLOR)
        state.background.draw(screen)

        for player in grupo_player:
            state.placar.set_pedras(player.pedras)
            state.placar.set_life(player.life)
        state.placar.draw(screen)

        if state.stopgame:
            state.mensagem_inicio.draw(screen)
        
        # Desenha os elementos da UI (dpad e botões)
        self.state.ui_manager.draw(screen)

        all_active_sprites = []
        all_active_sprites.extend(grupo_player)
        all_active_sprites.extend(grupo_enemy)
        all_active_sprites.extend(grupo_objets_player)
        all_active_sprites.extend(grupo_objets_enemy)
        all_active_sprites.extend(grupo_objets_static)

        for sprite in sorted(all_active_sprites, key=lambda spr: spr.rect.bottom):
            screen.blit(sprite.image, sprite.rect)
        
        pygame.display.update()

    async def run(self):
        while self.state.running:
            self.state.clock.tick(GAME_FPS)
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
            await asyncio.sleep(0)

if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
