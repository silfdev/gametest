import pygame
from abc import ABC, abstractmethod
class UIManager:
    def __init__(self, screen, ui_instance):
        self.screen = screen
        self.ui_instance = ui_instance
    def update(self, dt):
        for ui_element in self.ui_instance:
            ui_element.update(self.screen, dt)
class UI(ABC):
    def __init__(self, x, y, width, height, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.custom_config = []
        for key, value in kwargs.items():
            setattr(self, key, value)
    @abstractmethod
    def update(self, screen, dt):
        pass

class HealthBar(UI):
    def __init__(self, x, y, width, height, player):
        super().__init__(x, y, width, height)
        self.player = player
        self.display = 1
    def update(self, screen, dt):
        if self.visible:
            current_health, max_health = self.player.get_health()
            border_width = 2
            pygame.draw.rect(screen, (0, 0, 0), self.rect, width=border_width) # health bar border

            health_percentage = current_health / max_health
            self.display += (health_percentage - self.display) * min(1, 0.1*dt)
            real_health_bar = pygame.Rect(self.rect.x+border_width, self.rect.y+border_width, (self.rect.width - border_width*2) * health_percentage, self.rect.height - border_width *2)
            ghost_health_bar = pygame.Rect(self.rect.x+border_width, self.rect.y+border_width, (self.rect.width - border_width*2) * self.display, self.rect.height - border_width *2)

            pygame.draw.rect(screen, (0, 0, 0), ghost_health_bar) # ghost health bar fill
            pygame.draw.rect(screen, (255, 0, 0), real_health_bar) # health bar fill
