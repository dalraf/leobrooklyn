import pygame

pygame.font.init()

class Placar():
    def __init__(self):
        self.font = pygame.font.SysFont('Sans', 35)
        self.placar = 0
        self.placarshow = self.font.render('Placar: ' + str(self.placar), False, (255, 255, 255))

    def update(self, addnumber):
        self.placar += addnumber
        self.placarshow = self.font.render('Placar: ' + str(self.placar), False, (255, 255, 255))

    def zero(self):
        self.placar = 0
        self.placarshow = self.font.render('Placar: ' + str(self.placar), False, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.placarshow,(0,0))