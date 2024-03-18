import pygame
import level as game
from settings import *


class Warp(pygame.sprite.Sprite):
    def __init__(self, pos, groups, warp_id, player):
        super().__init__(groups)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.warp_id = warp_id
        self.player_ref = player
        self.in_transition = False

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def collisions(self):
        if not self.in_transition and self.player_ref.hitbox.colliderect(self.hitbox):
            self.in_transition = True
            game.Level().change_map(self.warp_id)

    def update(self):
        self.collisions()


class SecretPassage(Warp):
    def __init__(self, pos, groups, obstacle_sprites, warp_id, level_id, player, surface, is_revealed=False):
        super().__init__(pos, groups, warp_id, player)

        self.obstacle_sprites = obstacle_sprites
        self.warp_id = warp_id
        self.level_id = level_id
        self.is_revealed = is_revealed

        self.image = surface
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect

        # Ensure Obstacle destruction if secret is already revealed
        if self.is_revealed:
            self.reveal()

    def collisions(self):
        super().collisions()

    def reveal(self):
        self.is_revealed = True
        MAP_SECRETS_REVEALED[self.level_id] = True
        self.hitbox = self.rect.inflate(-16, -16)
        if UNDERWORLD_STAIRS[int(self.warp_id) - 4][STAIRS_LABEL]:
            self.hitbox.top = self.rect.top
        for obstacle in self.obstacle_sprites:
            if obstacle.rect.colliderect(self.rect):
                obstacle.kill()

    def update(self):
        if self.is_revealed:
            self.collisions()
            pygame.display.get_surface().blit(self.image, self.rect.topleft)
