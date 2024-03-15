import pygame
from settings import *


class Purchasable(pygame.sprite.Sprite):
    def __init__(self, pos, groups: list, label, image, price, price_sprite_ref, level_ref):
        super().__init__(groups)
        self.pos = pos

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

        self.label = label
        self.price = price
        self.price_sprite_ref = price_sprite_ref
        self.level_ref = level_ref

        if self.label == RUPEE_LABEL and self.price >= 0:
            self.ignore_player_money_amount = True
        else:
            self.ignore_player_money_amount = False

    def effect(self):
        # Items that don't have a pickup animation
        if self.label == BOMB_LABEL:
            self.level_ref.add_bombs(PLAYER_BOMB_LOOT_AMOUNT)
        elif self.label == HEART_LABEL:
            self.level_ref.add_health(1)
        # Items that have a pickup animation
        elif self.label == HEARTRECEPTACLE_LABEL or self.label in SHOP_ITEMS.keys():
            self.level_ref.player_pick_up(self.label)

        self.level_ref.add_money(-self.price)
        level_id = self.level_ref.current_map + self.level_ref.current_map_screen
        SHOPS[level_id]['items'].pop(self.label, None)
        if self.price_sprite_ref is not None:
            self.price_sprite_ref.kill()

    def update(self):
        pygame.display.get_surface().blit(self.image, self.pos)
