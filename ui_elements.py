import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, DPAD_BUTTON_SIZE, DPAD_PADDING, ACTION_BUTTON_SIZE, ACTION_BUTTON_PADDING, UI_BOTTOM_MARGIN, WHITE_COLOR

class DPad:
    def __init__(self):
        self.button_size = DPAD_BUTTON_SIZE
        self.padding = DPAD_PADDING
        self.center_x = self.padding + self.button_size
        self.center_y = SCREEN_HEIGHT - UI_BOTTOM_MARGIN - self.button_size * 2

        self.buttons = {
            "up": pygame.Rect(self.center_x, self.center_y - self.button_size, self.button_size, self.button_size),
            "down": pygame.Rect(self.center_x, self.center_y + self.button_size, self.button_size, self.button_size),
            "left": pygame.Rect(self.center_x - self.button_size, self.center_y, self.button_size, self.button_size),
            "right": pygame.Rect(self.center_x + self.button_size, self.center_y, self.button_size, self.button_size),
        }

    def draw(self, screen):
        for button_name, rect in self.buttons.items():
            pygame.draw.rect(screen, WHITE_COLOR, rect, 2) # Desenha apenas a borda
            font = pygame.font.SysFont("Arial", 15)
            text = font.render(button_name.upper(), True, WHITE_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def handle_click(self, pos):
        for direction, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return direction
        return None

class ActionButton:
    def __init__(self, x, y, text, action):
        self.size = ACTION_BUTTON_SIZE
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE_COLOR, self.rect, 2)
        font = pygame.font.SysFont("Arial", 15)
        text_surface = font.render(self.text, True, WHITE_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.action
        return None

class UIManager:
    def __init__(self):
        self.dpad = DPad()
        
        # Posições dos botões de ação
        attack_button_x = SCREEN_WIDTH - ACTION_BUTTON_SIZE - ACTION_BUTTON_PADDING
        shoot_button_x = attack_button_x - ACTION_BUTTON_SIZE - ACTION_BUTTON_PADDING
        button_y = SCREEN_HEIGHT - UI_BOTTOM_MARGIN - ACTION_BUTTON_SIZE * 2

        self.attack_button = ActionButton(attack_button_x, button_y, "ATTACK", "move_attack")
        self.shoot_button = ActionButton(shoot_button_x, button_y, "SHOOT", "move_atirar")
        self.buttons = [self.attack_button, self.shoot_button]

    def draw(self, screen):
        self.dpad.draw(screen)
        for button in self.buttons:
            button.draw(screen)

    def handle_click(self, pos):
        dpad_action = self.dpad.handle_click(pos)
        if dpad_action:
            return dpad_action
        
        for button in self.buttons:
            button_action = button.handle_click(pos)
            if button_action:
                return button_action
        return None