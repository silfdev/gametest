import pygame
from config import CONFIG
from .entity import Entity, AttackHitbox

class Player(Entity):
    def __init__(self, x, y, anim_handler):
        super().__init__(x, y, anim_handler)
        self.anim_index = 0
        self.anim_state = "idle"
        self.img = self.anim_handler.get_initial_frame()

        self.rect = self.img.get_rect(topleft=(x,y))
        self.walking = False
        self.falling = False
        self.moving = False
        self.attacking = False
        self.onGround = False
        self.can_be_attacked = True
        self.direction = "right"
        self.can_walk = True
        self.can_attack = True
    def update(self, detector, dt, **args):
        self.can_walk = not self.attacking and self.onGround
        self.walking = self.can_walk and self.moving
        self.falling = self.onGround is False
        
        self.move(dt)
        self.fall(dt)
        detector.update(self)
        self.onGround = detector.onGround()

        self.anim_update(dt)
    def anim_update(self, dt):
        if self.attacking: self.change_anim_state("attack")
        elif self.walking: self.change_anim_state("walk")
        elif self.falling: self.change_anim_state("fall")
        else: self.change_anim_state("idle")
        
        self.anim_index, self.img = self.anim_handler.index_advancement(dt, self.anim_state, self.anim_index, self.direction, self.attacking)
        self.anim_handler.all_states[self.anim_state].update(self.anim_handler, self)
    def change_anim_state(self, new_state):
        if self.anim_state != new_state:
            self.anim_state = new_state
            self.anim_index = 0
    def draw(self, screen):
        screen.blit(self.img, self.rect)
    
    def attack(self, world_entities):
        if self.can_attack:
            self.attacking = True
            hitbox = AttackHitbox(self, 50, world_entities)
            attacked = hitbox.hit_check()
            if attacked:
                from .monster import Monster
                for obj in attacked:
                    if isinstance(obj, Monster):
                        obj.take_damage(50)
            self.can_attack = False
            pygame.time.set_timer(CONFIG.ATTACK_TIMER, CONFIG.DELAY_ATTACK)
    def reset_attack(self): self.can_attack = True
    def reset_invincible(self): self.can_be_attacked = True

    def handle_input(self, keys, world_entities):
        self.moving = keys[pygame.K_a] or keys[pygame.K_d]
        if keys[pygame.K_d] and not keys[pygame.K_a]: self.direction = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]: self.direction = "left"
        if keys[pygame.K_SPACE] and self.onGround and self.can_attack: 
            self.attack(world_entities)