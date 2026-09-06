import pygame
from abc import abstractmethod
import uuid
from config import CONFIG

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, anim_handler=None):
        super().__init__()
        if anim_handler is not None: self.anim_handler = anim_handler
        self.rect = pygame.Rect(x, y, 0, 0)
        self.onGround = False
        self.direction = "right"
        self.id = uuid.uuid4()

        self.health = 100
        self.max_health = 100
        self.died = False

        self.moving = False
        self.walking = False
        self.falling = False
        self.attacking = False
    @abstractmethod
    def update(self, detector, dt): pass
    @abstractmethod
    def draw(self, screen): pass
    def fall(self,dt):
        if self.falling: self.rect.y += CONFIG.GRAVITY*dt
    def move(self, dt):
        if self.moving:
            if self.direction == "left": self.rect.x -= CONFIG.VELOCITY * dt
            else: self.rect.x += CONFIG.VELOCITY * dt
    def collision_able(self): return True
    def get_health(self): return self.health, self.max_health
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0: 
            self.health = 0
            self.died = True

class AttackHitbox:
    def __init__(self, entity, attack_range, world_entites):
        self.entity = entity
        self.entity_rect = entity.rect
        self.attack_range = attack_range
        self.world_entites = world_entites
        self.rect = self.entity_rect.copy()
        self.rect.x = self.entity_rect.x + (self.attack_range if self.entity.direction == "right" else -self.attack_range)
        if attack_range == 0:
            default_range = 5
            self.rect.x -= default_range
            self.rect.width += default_range * 2
    def hit_check(self):
        objs = []
        for obj in self.world_entites.values():
            if obj == self.entity: continue
            if self.rect.colliderect(obj.rect): 
                objs.append(obj)
        return objs