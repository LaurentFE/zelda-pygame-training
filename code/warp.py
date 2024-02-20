import pygame
from settings import *


class Warp(pygame.sprite.Sprite):
    def __init__(self, pos, groups, warp_id, player, level):
        super().__init__(groups)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.warp_id = warp_id
        self.player_ref = player
        self.level_ref = level

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def collisions(self):
        if self.player_ref.hitbox.colliderect(self.hitbox):
            self.level_ref.change_map(self.warp_id)
            self.kill()

    def update(self):
        self.collisions()
