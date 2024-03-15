import pygame
from settings import *


class Npc(pygame.sprite.Sprite):
    def __init__(self, pos, groups: list, image):
        super().__init__(groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.pos)

