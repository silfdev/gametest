from .entity import Entity, AttackHitbox
import pygame
from config import CONFIG

class Monster(Entity):
    def __init__(self, x, y, width, height, anim_handler):
        super().__init__(x, y, anim_handler)
        self.rect = pygame.Rect(x, y, width, height)
    def update(self, detector, dt, world_entities=None):
        self.can_walk = not self.attacking and self.onGround
        self.walking = self.can_walk and self.moving
        self.falling = self.onGround is False
        
        hitbox = AttackHitbox(self, 0, world_entities)
        attacked = hitbox.hit_check()
        if attacked:
            for obj in attacked:
                from .amia import Player
                if isinstance(obj, Player):
                    if obj.can_be_attacked: 
                        obj.take_damage(10)
                        obj.can_be_attacked = False
                        pygame.time.set_timer(CONFIG.CAN_BE_ATTACKED_TIMER, CONFIG.DELAYED_ATTACKED)
                        break
        
        self.move(dt)
        self.fall(dt)
        detector.update(self)
        self.onGround = detector.onGround()
    def draw(self, screen):
        pygame.draw.rect(screen, "#FF0000", self.rect)
    def collision_able(self): return True

