import pygame
from code.settings import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_type=0):
        super().__init__()
        for group in groups:
            self.add(group)

        self.pos = pos
        self.type = obstacle_type
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def update(self):
        pass
