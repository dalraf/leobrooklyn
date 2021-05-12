from config import resource_path, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame


class Background:
    def __init__(self):
        self.backgroundwidth = SCREEN_WIDTH * 3
        self.background = pygame.image.load(resource_path("images/bg.png"))
        self.background = pygame.transform.scale(
            self.background, (self.backgroundwidth, SCREEN_HEIGHT)
        )
        self.rect = self.background.get_rect()
        self.step = 0
        self.distance = 0
        self.walk1 = 0
        self.walk2 = self.backgroundwidth

    def zero(self):
        self.distance = 0

    def paralaxe(self, step):
        self.distance += step
        self.step += step

    def draw(self, screen):
        self.walk1 = 0 - self.step
        self.walk2 = self.backgroundwidth - self.step
        if self.walk1 < -self.backgroundwidth and self.walk2 < 0:
            self.walk1 = 0
            self.walk2 = self.backgroundwidth
            self.step = 0
        screen.blit(self.background, (self.walk1, self.rect.y))
        screen.blit(self.background, (self.walk2, self.rect.y))
