import pygame
from config import CONFIG
from abc import ABC, abstractmethod

class AnimationLoader:
    def __init__(self, path): 
        self.path = path
    def load(self, animation_name):
        frames = {"left": [], "right": []}
        loadable = True
        i = 1
        while loadable:
            try:
                frame = pygame.image.load(f"{self.path}/{animation_name}_{i}.png")
                frame = pygame.transform.scale_by(frame, CONFIG.SPRITE_SCALE)
                frame_flip = pygame.transform.flip(frame, True, False)
                frames["right"].append(frame)
                frames["left"].append(frame_flip)
                i+=1
            except FileNotFoundError:
                loadable = False
        return frames

class AnimationController:
    def __init__(self, state_available=None, entity_name="amia"):
        if state_available is None: state_available=["idle"]
        self.animation_path = CONFIG.path_for(entity_name)
        self.animations = {}
        self.all_states = {}
        self.state_available = state_available
        self.load()
    def load(self):
        loader = AnimationLoader(self.animation_path)
        for subclass in State.__subclasses__():
            obj = subclass()
            if obj.animation_name in self.state_available:
                self.all_states[obj.animation_name] = obj
        for anim_name in self.all_states:
            frame_loaded = loader.load(anim_name)
            self.animations[anim_name] = frame_loaded
    def get_frame(self, anim_state, entity_direction, anim_index): return self.animations[anim_state][entity_direction][int(anim_index)]
    def index_advancement(self, dt, anim_state, anim_index, direction, attacking):
        if attacking:
            anim_index += CONFIG.ATTACK_SPEED * dt
        else:
            anim_index += CONFIG.ANIMATION_SPEED * dt
        if int(anim_index) >= len(self.animations[anim_state][direction]) - 1:
            if self.all_states[anim_state].loop:
                anim_index = 0
            else: anim_index = len(self.animations[anim_state][direction])-1
        img = self.get_frame(anim_state, direction, anim_index)
        return anim_index, img
    def get_initial_frame(self):
        return self.get_frame("idle", "right", 0)
class State(ABC):
    def __init__(self):
        self.animation_name = ""
        self.loop = False
    @abstractmethod
    def update(self, anim_handler, entity): pass

class IdleState(State):
    def __init__(self):
        self.animation_name = "idle"
        self.loop = True
    def update(self, anim_handler, entity): pass

class WalkState(State):
    def __init__(self):
        self.animation_name = "walk"
        self.loop = True
    def update(self, anim_handler, entity): pass

class FallState(State):
    def __init__(self):
        self.animation_name = "fall"
        self.loop = False
    def update(self, anim_handler, entity): pass

class AttackState(State):
    def __init__(self):
        self.animation_name = "attack"
        self.loop = False
    def update(self, anim_handler, entity):
        if entity.anim_index >= len(anim_handler.animations[self.animation_name]["right"]) - 1:
            entity.attacking = False
