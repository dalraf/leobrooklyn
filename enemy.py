from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    LEFT,
    RIGHT,
    DERIVACAO,
    resource_path,
    calcule_vetor_distance,
    verify_align,
)
from pygame.image import load
from persons import SpritePerson
from objetcs import PedraEnemy
from grupos import grupo_objets_enemy
import random


class Enemy(SpritePerson):
    def _load_images(self, action, start, end):
        """Carrega imagens de forma centralizada"""
        return [
            resource_path(f"images/Enemy-{self.tipo}-{action}-{i}.png")
            for i in range(start, end)
        ]

    def __init__(self, speed):
        super().__init__()
        self.tipo = 1  # Valor padrão será sobrescrito pelas subclasses
        self.imageswalk = self._load_images("Walk", 1, 6)
        self.imagesattack = self._load_images("Attack", 1, 7)
        self.imagesstop = [self._load_images("Walk", 1, 2)[0]]  # Primeiro frame do walk
        self.imageshit = self._load_images("Hit", 1, 4)
        self.imagesatirar = self._load_images("Attack", 1, 7)
        self.image = load(self.imageswalk[0])
        self.images_list = self.imagesstop
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - random.randint(0, 500)
        self.rect.x = SCREEN_WIDTH
        self.counter = 0
        self.speed = random.randint(3, 3 + speed)
        self.sprint = 3
        self.pedras = random.randint(0, 2)
        self.reverse = False
        self.life = 6
        self.execute = self.action_parado

    def action_atirar(self):
        if self.pedras > 0:
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
            else:
                if self.counter == ((len(self.imagesatirar) - 1) * self.sprint):
                    if self.reverse:
                        grupo_objets_enemy.add(
                            PedraEnemy(self.rect.left, self.rect.y, LEFT)
                        )
                    if not self.reverse:
                        grupo_objets_enemy.add(
                            PedraEnemy(self.rect.right, self.rect.y, RIGHT)
                        )
                    self.pedras -= 1
        else:
            self.execute = self.action_parado

    def paralaxe(self, step):
        self.rect.x -= step

    def attack_trigger(self):
        if random.randint(1, 3000) < self.speed * 30:
            return True
        else:
            return False

    def update(self, grupo_player, grupo_enemy):

        if self.execute not in [
            self.action_in_attack,
            self.action_attack,
            self.action_hit,
            self.action_atirar,
        ]:

            for player_active in grupo_player:
                if verify_align(self.rect.y, player_active.rect.y):
                    if (
                        calcule_vetor_distance(
                            self.rect.center, player_active.rect.center
                        )
                        > DERIVACAO
                    ):
                        if self.attack_trigger():
                            self.execute = self.action_atirar

                    if (
                        calcule_vetor_distance(
                            self.rect.center, player_active.rect.center
                        )
                        < DERIVACAO
                    ):
                        if self.attack_trigger():
                            self.execute = self.action_in_attack

        self.dx = 0
        self.dy = 0

        for player_active in grupo_player:
            if (
                calcule_vetor_distance(self.rect.center, player_active.rect.center)
                > DERIVACAO
            ):

                dx, dy = self.calculate_path(grupo_player, 0)

                self.dx += dx
                self.dy += dy

                dx, dy = self.calculate_path(grupo_enemy, 40)

                self.dx -= dx
                self.dy -= dy

        self.passo_x = int(self.dx * self.speed)
        self.passo_y = int(self.dy * self.speed)

        self.move((self.passo_x, self.passo_y))

        if self.dx < 0:
            self.reverse = True
        elif self.dx > 0:
            self.reverse = False

        if self.execute not in [
            self.action_in_attack,
            self.action_attack,
            self.action_hit,
            self.action_atirar,
        ]:
            if self.dx == 0 and self.dy == 0:
                self.execute = self.action_parado
            else:
                self.execute = self.action_andando

        self.execute()

    def check_attack_hit(self, target_sprite):
        """Verifica se o ataque do inimigo atinge o sprite alvo."""
        from config import calcule_vetor_distance, DERIVACAO # Importação local para evitar circular
        if self.execute == self.action_attack:
            if calcule_vetor_distance(self.rect.center, target_sprite.rect.center) < DERIVACAO:
                if self.reverse:
                    return self.rect.left > target_sprite.rect.left
                else:
                    return self.rect.left < target_sprite.rect.left
        return False


class Wooden(Enemy):
    def __init__(self, speed):
        super().__init__(speed)
        self.tipo = 1


class Steam(Enemy):
    def __init__(self, speed):
        super().__init__(speed)
        self.tipo = 2
