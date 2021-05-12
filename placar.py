from config import FONT_SIZE
import pygame

pygame.font.init()


class Placar:
    def __init__(self):
        self.font = pygame.font.SysFont("Sans", FONT_SIZE)
        self.placar = 0
        self.pedras = 0
        self.life = 0

    def zero(self):
        self.placar = 0

    def add_enemy_kill(self, addnumber):
        self.placar += addnumber

    def set_pedras(self, pedras):
        self.pedras = pedras

    def set_life(self, life):
        self.life = life

    def draw(self, screen):
        self.placarshow = self.font.render(
            "Placar: "
            + str(self.placar)
            + "  Vida: "
            + str(self.life)
            + "  Pedras: "
            + str(self.pedras),
            False,
            (255, 255, 255),
        )
        screen.blit(self.placarshow, (0, 0))
