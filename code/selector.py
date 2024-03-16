import pygame
from settings import *
from tileset import TileSet


class Selector(pygame.sprite.Sprite):
    def __init__(self, groups, pos, hud_tile_set: TileSet):
        super().__init__(groups)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.animation_frames = []
        self.animation_start_timer = 0
        self.animation_frame_index = 0
        self.animation_cooldown = MENU_ITEM_SELECTOR_COOLDOWN
        self.load_animation_frames(hud_tile_set)

        self.image = self.animation_frames[0]

    def load_animation_frames(self, hud_tile_set):
        for i in range(MENU_ITEM_SELECTOR_FRAMES):
            tiles_offset = SPRITE_SIZE//TILE_SIZE * i
            self.animation_frames.append(hud_tile_set.get_sprite_image(MENU_ITEM_SELECTOR_FRAME_ID + tiles_offset))

    def animate(self):
        current_time = pygame.time.get_ticks()

        self.image = self.animation_frames[self.animation_frame_index]
        if current_time - self.animation_start_timer >= self.animation_cooldown:
            self.animation_start_timer = pygame.time.get_ticks()
            if self.animation_frame_index < MENU_ITEM_SELECTOR_FRAMES - 1:
                self.animation_frame_index += 1
            else:
                self.animation_frame_index = 0

    def move(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, (self.pos_x, self.pos_y))
