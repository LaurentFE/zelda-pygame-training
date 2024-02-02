import pygame
from settings import *


# Need to remove particles from tile sets for later
class Tileset(pygame.sprite.Sprite):
    def __init__(self, tile_type):
        super().__init__()

        self.file = f'../graphics/{tile_type}/{tile_type}.png'
        self.image = pygame.image.load(self.file)
        self.image.set_colorkey(COLOR_KEY)
        self.rec = self.image.get_rect()

        pygame.display.get_surface().blit(self.image, (0, 0))

        self.img_width = None
        self.img_height = None
        if tile_type == 'enemies':
            self.img_width = 2
            self.img_height = 2
        elif tile_type == 'font':
            self.img_width = 1
            self.img_height = 1
        elif tile_type == 'hud':
            self.img_width = 1  # sometimes 2 though, how to handle ?
            self.img_height = 1  # sometimes 2 though, how to handle ?
        elif tile_type == 'items':
            self.img_width = 1  # sometimes 2 though, how to handle ?
            self.img_height = 1  # sometimes 2 though, how to handle ?
        elif tile_type == 'npcs':
            self.img_width = 2  # EXCEPT FAIRIES THOUGH LOL WTF
            self.img_height = 2
        elif tile_type == 'player':
            self.img_width = 2
            self.img_height = 2

        self.items_per_row = self.rec.width // TILE_SIZE

    def get_sprite_image(self, sprite_id):
        sprite_width = TILE_SIZE*self.img_width
        sprite_height = TILE_SIZE*self.img_height
        x = (int(sprite_id) % self.items_per_row) * TILE_SIZE
        y = (int(sprite_id) // self.items_per_row) * TILE_SIZE
        sprite_image = self.image.subsurface((x, y, sprite_width, sprite_height)).convert_alpha()
        return sprite_image


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups: list, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.pos = pos
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.pos)
