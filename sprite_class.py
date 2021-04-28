import pygame
import random
import math

class SpriteGame(pygame.sprite.Sprite):
    def __init__(self):
        super(SpriteGame, self).__init__()
        self.images = []
        self.image = None
        self.counter = 0
        self.speed = 0
        self.dx = 0
        self.dy = 0

    def calculate_path(self, group, diametro):
        
        final_dx = 0
        final_dy = 0

        for sprite in group:
            
            if sprite != self:

                dx, dy = sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y
            
                dist = math.hypot(dx, dy)
            
                if diametro > 0 and dist < diametro and dist > 0:
                    dx, dy = dx / dist, dy / dist
            
                elif diametro > 0 and dist > diametro:
                    dx , dy = 0 , 0
            
                elif diametro == 0 and dist > 0:
                    dx, dy = dx / dist, dy / dist
            
                else:
                    dx , dy = 0 , 0

                final_dx += dx
                final_dy += dy

        return final_dx, final_dy

    def update(self,grupo_player,grupo_enemy):
        pass