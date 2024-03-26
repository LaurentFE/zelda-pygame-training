import pygame
import code.tileset as tileset
import sys
from code.settings import *


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

    def draw_message(self, align_center=True):
        nb_row = 1
        char_count = 0
        formatted_text = ['']
        longest_row = 0

        for line in self.text.splitlines():
            for word in line.split(' '):
                if len(word) > MAX_CHAR_PER_ROW:
                    raise ValueError(WORD_TOO_LONG_FOR_TEXTBLOCK + word)
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

            if len(formatted_text[nb_row - 1]) > longest_row:
                longest_row = len(formatted_text[nb_row - 1])
            nb_row += 1
            formatted_text.append('')
            char_count = 0

        formatted_text[nb_row - 1] = formatted_text[nb_row - 1][:-1]
        if longest_row == 0:
            longest_row = len(formatted_text[nb_row - 1])

        self.image = pygame.surface.Surface((longest_row * FONT_SPRITE_SIZE, nb_row * FONT_SPRITE_SIZE))
        for i in range(nb_row):
            if align_center:
                row_width = len(formatted_text[i]) * FONT_SPRITE_SIZE
                x_offset_of_row = (self.image.get_width() - row_width) // 2
            else:
                x_offset_of_row = 0
            for j in range(len(formatted_text[i])):
                if formatted_text[i][j] in FONT_CHARS:
                    char_id = FONT_CHARS.index(formatted_text[i][j])
                    char_image = tileset.FONT_TILE_SET.get_sprite_image(char_id)
                    self.image.blit(char_image, (j * FONT_SPRITE_SIZE + x_offset_of_row, i * FONT_SPRITE_SIZE))
                else:
                    print(TEXTBLOCK_CHAR_SPRITE_NOT_DEFINED + formatted_text[i][j], file=sys.stderr)

        if self.pos_x is None:
            self.pos_x = SCREEN_WIDTH // 2 - self.image.get_rect().centerx

    def update(self):
        pygame.display.get_surface().blit(self.image, (self.pos_x, self.pos_y))
