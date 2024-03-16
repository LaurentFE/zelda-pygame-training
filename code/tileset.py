import pygame
from settings import *


# Will need someday to SINGLETON-ify this
class TileSet(pygame.sprite.Sprite):
    def __init__(self, tile_type):
        super().__init__()

        self.file = f'../graphics/{tile_type}/{tile_type}.png'
        self.image = pygame.image.load(self.file)
        self.image.set_colorkey(COLOR_KEY)
        self.rec = self.image.get_rect()

        pygame.display.get_surface().blit(self.image, (0, 0))

        self.img_width = SPRITE_SIZE // TILE_SIZE
        self.img_height = SPRITE_SIZE // TILE_SIZE
        if tile_type == 'font':
            self.img_width = FONT_SPRITE_SIZE // TILE_SIZE
            self.img_height = FONT_SPRITE_SIZE // TILE_SIZE

        self.items_per_row = self.rec.width // TILE_SIZE

    def get_sprite_image(self, sprite_id):
        sprite_width = TILE_SIZE * self.img_width
        sprite_height = TILE_SIZE * self.img_height
        x = (int(sprite_id) % self.items_per_row) * TILE_SIZE
        y = (int(sprite_id) // self.items_per_row) * TILE_SIZE
        sprite_image = self.image.subsurface((x, y, sprite_width, sprite_height)).convert_alpha()
        return sprite_image
