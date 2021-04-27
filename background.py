from config import resource_path
import pygame

class Background():

    def __init__(self):
        self.background = pygame.image.load("images/bg.png")
        self.rect = self.background.get_rect()
    
    def draw(self,screen):
        screen.blit(self.background, self.rect)

