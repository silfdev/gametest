import pygame

class Config:
    def __init__(self):
        # BASIC ATTRIBUTE
        self.FPS = 60
        self.VELOCITY = 2
        self.GRAVITY = 5
        self.SPRITE_SCALE = 0.8
        self.ANIMATION_SPEED = 0.2
        self.ATTACK_SPEED = 0.05
        self.DELAYED_ATTACKED = 1000 # ms
        self.DELAY_ATTACK = 1000 # ms

        # EVENT ID
        self.ATTACK_TIMER = pygame.USEREVENT + 1
        self.CAN_BE_ATTACKED_TIMER = pygame.USEREVENT + 2

        self.PATH_LOOKUP={
            "AMIA": "assets/amia"
        }
    def path_for(self, entity_name):
        return self.PATH_LOOKUP[entity_name.upper()]
CONFIG = Config()