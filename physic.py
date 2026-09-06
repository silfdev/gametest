import pygame
from config import CONFIG

class CollisionDetector:
    def __init__(self, world):
        self.entity = None
        self.world = world
        self.ground_list = self.world.collision_able
        self._on_ground = False
    def update(self, entity):
        self.entity = entity
        self._on_ground = False
        self.check_ground_below()
        self.collision_handle()
    def collision_handle(self): 
        for obj in self.ground_list:
            if not self.entity.rect.colliderect(obj.rect) or obj == self.entity: continue
            dx = min(self.entity.rect.right - obj.rect.left, obj.rect.right - self.entity.rect.left)
            dy = min(self.entity.rect.bottom - obj.rect.top, obj.rect.bottom - self.entity.rect.top)
            if dy < dx:
                if self.entity.rect.bottom - obj.rect.top < obj.rect.bottom - self.entity.rect.top:
                    self.entity.rect.bottom = obj.rect.top
                    self._on_ground = True
                else:
                    self.entity.rect.top = obj.rect.bottom
            else:
                if self.entity.rect.right - obj.rect.left < obj.rect.right - self.entity.rect.left:
                    self.entity.rect.right = obj.rect.left
                else:
                    self.entity.rect.left = obj.rect.right
    def check_ground_below(self):
        probe = self.entity.rect.move(0, 1)
        feet = self.entity.rect.bottom
        for obj in self.ground_list:
            if probe.colliderect(obj.rect) and feet - obj.rect.top <= CONFIG.GRAVITY and self.entity != obj:
                self._on_ground = True
    def onGround(self): return self._on_ground
