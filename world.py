class World:
    def __init__(self):
        self.entities = {} # dict
        self.blocks = [] 
        self.collision_able = []
    def update(self,screen,detector, dt):
        died_entities = []
        for entity in self.entities: 
            if self.entities[entity].died:
                died_entities.append(entity)
                self.collision_able.remove(self.entities[entity])
                continue
            self.entities[entity].update(detector, dt, world_entities=self.entities)
            self.entities[entity].draw(screen)
        for entity in died_entities: del self.entities[entity]
        
        for block in self.blocks: block.draw(screen)
    def died_handle(self):
        pass
    def add_block(self, block):
        self.blocks.append(block)
        if block.collision_able(): self.collision_able.append(block)
    def add_entity(self, entity):
        self.entities[entity.id] = entity
        if entity.collision_able(): self.collision_able.append(entity)
    def get_entities(self): return self.entities
    def get_blocks(self): return self.blocks