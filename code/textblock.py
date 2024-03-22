import pygame
import tileset
from settings import *


class TextBlock(pygame.sprite.Sprite):
    def __init__(self, groups, text, pos_y, pos_x=None):
        super().__init__()
        for group in groups:
            self.add(group)

        self.text = text.lower()

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = None
        self.draw_message()

    def draw_message(self):
        nb_row = 1
        char_count = 0
        formatted_text = ['']
        longest_row = 0
        for word in self.text.split():
            if char_count + len(word) > MAX_CHAR_PER_ROW:
                formatted_text[nb_row - 1] = formatted_text[nb_row - 1][:-1]
                if len(formatted_text[nb_row - 1]) > longest_row:
                    longest_row = len(formatted_text[nb_row - 1])
                nb_row += 1
                char_count = len(word) + 1
                formatted_text.append(word + ' ')
            else:
                char_count += len(word) + 1
                formatted_text[nb_row - 1] += word + ' '
        formatted_text[nb_row - 1] = formatted_text[nb_row - 1][:-1]
        if longest_row == 0:
            longest_row = len(formatted_text[nb_row - 1])

        self.image = pygame.surface.Surface((longest_row * FONT_SPRITE_SIZE, nb_row * FONT_SPRITE_SIZE))
        for i in range(nb_row):
            for j in range(len(formatted_text[i])):
                char_id = FONT_CHARS.index(formatted_text[i][j])
                char_image = tileset.FONT_TILE_SET.get_sprite_image(char_id)
                self.image.blit(char_image, (j * FONT_SPRITE_SIZE, i * FONT_SPRITE_SIZE))

        if self.pos_x is None:
            self.pos_x = SCREEN_WIDTH // 2 - self.image.get_rect().centerx

    def update(self):
        pygame.display.get_surface().blit(self.image, (self.pos_x, self.pos_y))
