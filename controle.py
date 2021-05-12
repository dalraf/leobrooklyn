import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, FONT_SIZE

pygame.font.init()


class Controle:
    def __init__(self):
        self.font = pygame.font.SysFont("Sans", FONT_SIZE)
        self.controle1 = self.font.render(
            "Pressione ENTER para continuar", False, (255, 255, 255)
        )
        self.controle2 = self.font.render(
            "Setas Movimentam, Espaço Atira, CTRL Bate", False, (255, 255, 255)
        )
        self.rect1 = self.controle1.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.rect2 = self.controle2.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )

    def draw(self, screen):
        screen.blit(self.controle1, self.rect1)
        screen.blit(self.controle2, self.rect2)
