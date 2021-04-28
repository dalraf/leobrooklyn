import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()

class Controle():
    def __init__(self):
        self.font = pygame.font.SysFont('Sans', 35)
        self.controle = self.font.render('Pressione ENTER para continuar', False, (255, 255, 255))
        self.rect = self.controle.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

    def draw(self, screen):
        screen.blit(self.controle,self.rect)