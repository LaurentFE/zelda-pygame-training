import pygame
import sys
from settings import *
import tileset
from level import Level


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        tileset.CONSUMABLES_TILE_SET = tileset.TileSet(TILE_CONSUMABLES)
        tileset.DOORS_TILE_SET = tileset.TileSet(TILE_DOORS)
        tileset.ENEMIES_TILE_SET = tileset.TileSet(TILE_ENEMIES)
        tileset.FONT_TILE_SET = tileset.TileSet(TILE_FONTS)
        tileset.HUD_TILE_SET = tileset.TileSet(TILE_HUD)
        tileset.ITEMS_TILE_SET = tileset.TileSet(TILE_ITEMS)
        tileset.LEVELS_TILE_SET = tileset.TileSet(TILE_LEVELS)
        tileset.NPCS_TILE_SET = tileset.TileSet(TILE_NPCS)
        tileset.PARTICLES_TILE_SET = tileset.TileSet(TILE_PARTICLES)
        tileset.PLAYER_TILE_SET = tileset.TileSet(TILE_PLAYER)
        tileset.WARPS_TILE_SET = tileset.TileSet(TILE_WARPS)

    def run(self):
        keys_pressed = []
        while True:
            self.screen.fill(BLACK_LABEL)
            Level().run()
            pygame.display.update()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)
                if event.type == pygame.KEYUP:
                    keys_pressed.remove(event.key)
            Level().handle_input(keys_pressed)


if __name__ == '__main__':
    game = Game()
    game.run()
