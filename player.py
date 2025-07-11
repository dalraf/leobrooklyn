from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    STOPPED,
    MOONWALK,
    resource_path,
)
from pygame.image import load
from persons import SpritePerson
from objetcs import PedraPlayer, PedraParada, BandAid
from grupos import grupo_objets_player


class Player(SpritePerson):
    def __init__(self):
        super(Player, self).__init__()
        self.imagesattack = self._load_images("Attack", 1, 6)
        self.imageswalk = self._load_images("Walk", 1, 5)
        self.imagesstop = self._load_images("Stop", 1, 5)
        self.imageshit = self._load_images("Hit", 1, 5)
        self.imagesatirar = self._load_images("Atirar", 1, 6)
        self.images_list = self.imagesstop
        self.image = load(self.images_list[0])
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT * (0.65)
        self.rect.x = SCREEN_WIDTH / 2
        self.step = 10
        self.move_list = []
        self.sprint = 2
        self.counter = 0
        self.reverse = False
        self.pedras = 10
        self.life = 20
        self.execute = self.action_parado
        self.moonwalk = False


    def action_atirar(self):
        if self.pedras > 0:
            if self.update_image(self.imagesatirar):
                self.execute = self.action_parado
            else:
                if self.counter == ((len(self.imagesatirar) - 1) * self.sprint):
                    if self.reverse:
                        grupo_objets_player.add(
                            PedraPlayer(self.rect.left, self.rect.y, LEFT)
                        )
                    if not self.reverse:
                        grupo_objets_player.add(
                            PedraPlayer(self.rect.right, self.rect.y, RIGHT)
                        )
                    self.pedras -= 1
        else:
            self.execute = self.action_parado

    def combine_moviment(self):
        dx, dy = 0, 0
        reverse = self.reverse
        
        # Mantém ação atual se estiver em ataque/tiro
        current_action = self.execute
        
        # Só processa movimento se não estiver em ação prioritária
        if current_action not in [self.action_attack, self.action_atirar, self.action_in_attack]:
            # Calcula movimento combinado
            if UP in self.move_list:
                dy -= self.step
            if DOWN in self.move_list:
                dy += self.step
            if LEFT in self.move_list:
                dx -= self.step
                reverse = True
            if RIGHT in self.move_list:
                dx += self.step
                reverse = False
            if MOONWALK in self.move_list:
                self.execute = self.action_andando
                reverse = False
                
            # Aplica movimento combinado
            if dx != 0 or dy != 0:
                self.move((dx, dy))
                self.execute = self.action_andando
                self.reverse = reverse
            else:
                if MOONWALK in self.move_list:
                    self.execute = self.action_andando
                else:
                    self.execute = self.action_parado
                
        self.move_list = []

    def move_up(self):
        self.move_list.append(UP)
        self.moonwalk = False


    def move_down(self):
        self.move_list.append(DOWN)
        self.moonwalk = False


    def move_left(self):
        self.move_list.append(LEFT)
        self.moonwalk = False
        
    def move_right(self):
        if not self.moonwalk:
            self.move_list.append(RIGHT)

    def move_stopped(self):
        if self.execute not in [
            self.action_in_attack,
            self.action_attack,
            self.action_hit,
            self.action_atirar,
        ]:
            self.move_list.append(STOPPED)

    def move_moonwalk(self):
        self.move_list.append(MOONWALK)
        self.moonwalk = True

    def move_atirar(self):
        self.execute = self.action_atirar

    def move_attack(self):
        self.execute = self.action_in_attack
    
    def _load_images(self, action, start, end):
        """Carrega imagens de forma centralizada"""
        return [
            resource_path(f"images/Player-1-{action}-{i}.png")
            for i in range(start, end)
        ]

    def get_object(self, object):
        if isinstance(object ,PedraParada):
            self.pedras += object.damage
        if isinstance(object, BandAid):
            self.life += object.damage

    def check_attack_hit(self, target_sprite):
        """Verifica se o ataque do jogador atinge o sprite alvo."""
        from config import calcule_vetor_distance, DERIVACAO # Importação local para evitar circular
        if self.execute == self.action_attack:
            if calcule_vetor_distance(self.rect.center, target_sprite.rect.center) < DERIVACAO:
                if self.reverse:
                    return self.rect.left > target_sprite.rect.left
                else:
                    return self.rect.left < target_sprite.rect.left
        return False

    def update(self):
        self.combine_moviment()
        self.execute()
