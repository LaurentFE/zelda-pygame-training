import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups: list, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.pos = pos
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.pos)
