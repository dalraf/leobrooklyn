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
    def __init__(self, speed):
        super(Enemy, self).__init__()
        self.tipo = 1
        self.imageswalk = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in range(1, 6)
        ]
        self.imagesattack = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]
        self.imagesstop = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in [
                1,
            ]
        ]
        self.imageshit = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Hit-" + str(i) + ".png")
            for i in range(1, 4)
        ]
        self.imagesatirar = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]
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


class Wooden(Enemy):
    def __init__(self, speed):
        super(Wooden, self).__init__(speed)
        self.tipo = 1
        self.imageswalk = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in range(1, 6)
        ]
        self.imagesattack = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]
        self.imagesstop = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in [
                1,
            ]
        ]
        self.imageshit = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Hit-" + str(i) + ".png")
            for i in range(1, 4)
        ]
        self.imagesatirar = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]


class Steam(Enemy):
    def __init__(self, speed):
        super(Steam, self).__init__(speed)
        self.tipo = 2
        self.imageswalk = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in range(1, 7)
        ]
        self.imagesattack = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]
        self.imagesstop = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Walk-" + str(i) + ".png")
            for i in [
                1,
            ]
        ]
        self.imageshit = [
            resource_path("images/Enemy-" + str(self.tipo) + "-Hit-" + str(i) + ".png")
            for i in range(1, 4)
        ]
        self.imagesatirar = [
            resource_path(
                "images/Enemy-" + str(self.tipo) + "-Attack-" + str(i) + ".png"
            )
            for i in range(1, 7)
        ]
