from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPRITE_LEVEL_Y_HIGH,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    STOPPED,
    MOONWALK,
    STATE_ATTACK,
    STATE_INATTACK,
    STATE_WALK,
    STATE_STOP,
    STATE_MOONWALK,
    resource_path
)
import pygame
from pygame.image import load
from persons import SpritePerson
from objetcs import PedraPlayer
from grupos import grupo_objets_player
class Player(SpritePerson):
    def __init__(self):
        super(Player, self).__init__()
        self.imagesattack = [resource_path('images/Player-1-Attack-' + str(i) + '.png') for i in range(1,6)]
        self.imageswalk = [resource_path('images/Player-1-Walk-' + str(i) + '.png') for i in range(1,5)]
        self.imagesstop = [resource_path('images/Player-1-Stop-' + str(i) + '.png') for i in range(1,5)]
        self.imageshit = [resource_path('images/Player-1-Hit-' + str(i) + '.png') for i in range(1,5)]
        self.imagesatirar = [resource_path('images/Player-1-Atirar-' + str(i) + '.png') for i in range(1,6)]
        self.images_list = self.imagesstop
        self.image = load(self.images_list[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT * (0.65)
        self.rect.x = SCREEN_WIDTH/2
        self.step = 10
        self.move_list = []
        self.sprint_walk_factor = 2
        self.counter = 0
        self.reverse = False
        self.pedras = 10
        self.life = 20
        self.execute = self.action_parado

    def action_atirar(self):
        if self.pedras > 0:
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
            else:
                if self.counter == ((len(self.imagesatirar) - 1) * self.sprint_walk_factor):
                    if self.reverse:
                        grupo_objets_player.add(PedraPlayer(self.rect.left , self.rect.y, LEFT))
                    if not self.reverse:
                        grupo_objets_player.add(PedraPlayer(self.rect.right , self.rect.y, RIGHT))                
        else:
            self.execute = self.action_parado

    def combine_moviment(self):
        if UP in self.move_list:
            self.move((0, -self.step))
            self.execute = self.action_andando
            self.move_list = []
        if DOWN in self.move_list:
            self.move((0, self.step))
            self.execute = self.action_andando
            self.move_list = []
        if RIGHT in self.move_list:
            self.reverse = False
            self.move((self.step, 0))
            self.execute = self.action_andando
            self.move_list = []
        if LEFT in self.move_list:
            self.reverse = True
            self.move((-self.step, 0))   
            self.execute = self.action_andando
            self.move_list = []
        if STOPPED in self.move_list:
            self.execute = self.action_parado
            self.move_list = []
        if MOONWALK in self.move_list:
            self.execute = self.action_andando
            self.move_list = []

    def move_up(self):
        self.move_list.append(UP)
    
    def move_down(self):
        self.move_list.append(DOWN)
    
    def move_left(self):
        self.move_list.append(LEFT)

    def move_right(self):
        self.move_list.append(RIGHT)

    def move_stopped(self):
        if not self.execute in [self.action_in_attack, self.action_attack, self.action_hit, self.action_atirar]:
            self.move_list.append(STOPPED)

    def move_moonwalk(self):
        self.move_list.append(MOONWALK)
    
    def move_hit(self):
        self.execute = self.action_hit

    def move_atirar(self):
        self.execute = self.action_atirar
    
    def move_attack(self):
        self.execute = self.action_in_attack
            
    def update(self):
        self.combine_moviment()
        self.execute()





