import pygame
import sys
import code.settings as cfg
import code.tileset as tileset
import code.inputs as inputs
from code.level import Level


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pygame.display.set_caption(cfg.GAME_NAME)
        self.clock = pygame.time.Clock()
        tileset.CONSUMABLES_TILE_SET = tileset.TileSet(cfg.TILE_CONSUMABLES)
        tileset.DOORS_TILE_SET = tileset.TileSet(cfg.TILE_DOORS)
        tileset.ENEMIES_TILE_SET = tileset.TileSet(cfg.TILE_ENEMIES)
        tileset.FONT_TILE_SET = tileset.TileSet(cfg.TILE_FONTS)
        tileset.HUD_TILE_SET = tileset.TileSet(cfg.TILE_HUD)
        tileset.ITEMS_TILE_SET = tileset.TileSet(cfg.TILE_ITEMS)
        tileset.LEVELS_TILE_SET = tileset.TileSet(cfg.TILE_LEVELS)
        tileset.NPCS_TILE_SET = tileset.TileSet(cfg.TILE_NPCS)
        tileset.PARTICLES_TILE_SET = tileset.TileSet(cfg.TILE_PARTICLES)
        tileset.PLAYER_TILE_SET = tileset.TileSet(cfg.TILE_PLAYER)
        tileset.WARPS_TILE_SET = tileset.TileSet(cfg.TILE_WARPS)

    def run(self):
        keys_pressed = []
        while True:
            self.screen.fill(cfg.BLACK_LABEL)
            Level().run()
            pygame.display.update()
            self.clock.tick(cfg.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)
                if event.type == pygame.KEYUP:
                    if event.key == inputs.SAVE_KEY:
                        Level().save()
                    if event.key == inputs.LOAD_KEY:
                        Level().load()
                    keys_pressed.remove(event.key)
            Level().handle_input(keys_pressed)


if __name__ == '__main__':
    game = Game()
    game.run()
