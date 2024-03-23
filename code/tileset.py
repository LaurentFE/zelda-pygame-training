import pygame
import settings as cfg


class TileSet(pygame.sprite.Sprite):
    def __init__(self, tile_type):
        super().__init__()

        if tile_type in cfg.TILE_TYPES:
            self.file = f'{cfg.GRAPHICS_PATH}{tile_type}/{tile_type}{cfg.GRAPHICS_EXTENSION}'
            self.image = pygame.image.load(self.file)
            self.image.set_colorkey(cfg.COLOR_KEY)
            self.rec = self.image.get_rect()

            pygame.display.get_surface().blit(self.image, (0, 0))

            self.img_width = cfg.SPRITE_SIZE // cfg.TILE_SIZE
            self.img_height = cfg.SPRITE_SIZE // cfg.TILE_SIZE
            if tile_type == cfg.TILE_FONTS:
                self.img_width = cfg.FONT_SPRITE_SIZE // cfg.TILE_SIZE
                self.img_height = cfg.FONT_SPRITE_SIZE // cfg.TILE_SIZE
            elif tile_type == cfg.TILE_DOORS:
                self.img_width = cfg.DOOR_TILE_SIZE
                self.img_height = cfg.DOOR_TILE_SIZE

            self.items_per_row = self.rec.width // cfg.TILE_SIZE
        else:
            raise ValueError(cfg.UNKNOWN_TILE_TYPE)

    def get_sprite_image(self, sprite_id):
        sprite_width = cfg.TILE_SIZE * self.img_width
        sprite_height = cfg.TILE_SIZE * self.img_height
        x = (int(sprite_id) % self.items_per_row) * cfg.TILE_SIZE
        y = (int(sprite_id) // self.items_per_row) * cfg.TILE_SIZE
        sprite_image = self.image.subsurface((x, y, sprite_width, sprite_height)).convert_alpha()
        return sprite_image


# Global TileSet instances, they MUST be instantiated in Game __init__
CONSUMABLES_TILE_SET = None
DOORS_TILE_SET = None
ENEMIES_TILE_SET = None
FONT_TILE_SET = None
HUD_TILE_SET = None
ITEMS_TILE_SET = None
LEVELS_TILE_SET = None
NPCS_TILE_SET = None
PARTICLES_TILE_SET = None
PLAYER_TILE_SET = None
WARPS_TILE_SET = None
