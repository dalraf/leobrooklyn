from config import resource_path, SCREEN_WIDTH
import pygame
class Background():

    def __init__(self):
        self.background = pygame.image.load(resource_path("images/bg.png"))
        self.rect = self.background.get_rect()
        self.step = 0
        self.walk1 = 0
        self.walk2 = SCREEN_WIDTH
    
    def walk(self,step):
        self.step += step

    def draw(self,screen):
        self.walk1 = 0 - self.step
        self.walk2 = SCREEN_WIDTH - self.step
        if self.walk1 < -SCREEN_WIDTH and self.walk2 < 0:
            self.walk1 = 0
            self.walk2 = SCREEN_WIDTH
            self.step = 0
        screen.blit(self.background, ( self.walk1, self.rect.y))
        screen.blit(self.background, ( self.walk2, self.rect.y))
