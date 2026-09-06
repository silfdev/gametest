import pygame
from config import CONFIG
from animation_handler import AnimationController
from physic import CollisionDetector
from world import World
from entity import Player, Monster
from ui import UIManager, HealthBar

class Block:
    def __init__(self, block_type, x, y, width, height):
        self.block_type = block_type
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self, screen):
        pygame.draw.rect(screen, "#000000", self.rect)
    def collision_able(self):
        if self.block_type == "Ground": return True
        return False

class Dirt(Block):
    def __init__(self, x, y, width, height):
        super().__init__("Ground", x, y, width, height)


pygame.init()
screen = pygame.display.set_mode((1280,720), vsync=1)
clock = pygame.time.Clock()

world = World()
detector = CollisionDetector(world)

#Block registry
ground = Dirt(0, 500, 300, 200)
world.add_block(ground)

#Entity registry
monster = Monster(200, 100, 50, 200, None)
character = Player(0,0, AnimationController(["idle", "walk", "fall", "attack"], "amia"))
world.add_entity(character)
world.add_entity(monster)

#UI registry
health_bar = HealthBar(10, 10, 300, 30, character)
ui_manager = UIManager(screen, [health_bar])

gameRunning = True
while gameRunning:
    dt = clock.tick(CONFIG.FPS) / 1000 * CONFIG.FPS # normalized
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

        # event check
        if event.type == CONFIG.ATTACK_TIMER:
            character.reset_attack()
            pygame.time.set_timer(CONFIG.ATTACK_TIMER, 0)
        if event.type == CONFIG.CAN_BE_ATTACKED_TIMER:
            character.reset_invincible()
            pygame.time.set_timer(CONFIG.CAN_BE_ATTACKED_TIMER, 0)

    screen.fill('white')
    all_keys = pygame.key.get_pressed()

    if not character.died: character.handle_input(all_keys, world.get_entities())
    world.update(screen, detector, dt) 
    ui_manager.update(dt)

    pygame.display.flip()

pygame.quit()
