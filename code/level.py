import sys
import random

import pygame.mixer

from settings import *
from support import *
from inputs import *
from tileset import Tileset
from tile import Tile
from obstacle import Obstacle
from player import Player
from enemies import RedOctorock
from particles import Heart, Rupee, CBomb, Fairy, HeartReceptacle, Ladder, RedCandle, Boomerang, WoodenSword
from selector import Selector
from warp import Warp
from purchasable import Purchasable
from npc import Npc
from textblock import TextBlock


class Level:
    def __init__(self):
        # Set up variables
        self.player = None
        self.death_played = False
        self.death_floors = GAME_OVER_DEATH_FLOORS
        self.number_of_death_floors = len(self.death_floors)
        self.death_floor_index = 0
        self.in_menu = False
        self.kill_count = 0

        # Set up display surface
        self.display_surface = pygame.display.get_surface()
        self.floor_surface = None
        self.floor_rect = None
        self.transition_surface = None
        self.menu_surface = None
        self.menu_rect = None

        # Set up group sprites
        self.warp_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.particle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.money_amount_sprites = pygame.sprite.Group()
        self.keys_amount_sprites = pygame.sprite.Group()
        self.bombs_amount_sprites = pygame.sprite.Group()
        self.health_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        self.lootable_items_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.purchasable_sprites = pygame.sprite.Group()
        self.text_sprites = pygame.sprite.Group()

        self.equipped_item_a_sprite = None
        self.equipped_item_b_sprite = None
        self.current_selected_item = 'None'
        self.menu_item_coord_and_frame_id = {
            BOOMERANG_LABEL: (MENU_BOOMERANG_TOPLEFT, BOOMERANG_FRAME_ID),
            BOMB_LABEL: (MENU_BOMBS_TOPLEFT, BOMB_FRAME_ID),
            CANDLE_LABEL: (MENU_CANDLE_TOPLEFT, RED_CANDLE_FRAME_ID)
        }
        self.item_selector = None
        self.item_selected_sprite = None
        self.item_picked_up = None

        # Set up tile sets
        self.enemies_tile_set = Tileset('enemies')
        self.font_tile_set = Tileset('font')
        self.hud_tile_set = Tileset('hud')
        self.items_tile_set = Tileset('items')
        self.npcs_tile_set = Tileset('npcs')
        self.player_tile_set = Tileset('player')
        self.levels_tile_set = Tileset('levels')
        self.particle_tile_set = Tileset('particles')
        self.consumables_tile_set = Tileset('consumables')

        # Set up sounds
        self.overworld_background_theme = pygame.mixer.Sound(THEME_OVERWORLD)
        self.overworld_background_theme.set_volume(0.2)
        self.dungeon_background_theme = pygame.mixer.Sound(THEME_DUNGEON)
        self.dungeon_background_theme.set_volume(0.2)
        self.game_over_sound = pygame.mixer.Sound(SOUND_GAME_OVER)
        self.game_over_sound.set_volume(0.4)

        # Sprite setup
        # Player spawns at the center of the game surface
        player_x = SCREEN_WIDTH // 2 - TILE_SIZE
        player_y = SCREEN_HEIGHT // 2 + HUD_TILE_HEIGHT * TILE_SIZE // 2 - TILE_SIZE
        self.load_player((player_x, player_y))
        self.overworld_background_theme.play(loops=-1)

        self.current_map = 'level'
        self.current_map_screen = '10'
        self.create_map(self.current_map + self.current_map_screen)
        self.in_map_transition = None
        self.map_scroll_animation_counter = 0
        self.next_map = None
        self.next_map_screen = None
        self.player_new_position = None

        self.key_pressed_start_timer = 0
        self.key_pressed_cooldown = LEVEL_KEY_PRESSED_COOLDOWN

        # Set Stairs animation timer
        self.stairs_animation_starting_time = 0
        self.stairs_animation_duration = PLAYER_STAIRS_DURATION
        # Set Game Over animation variables & timers
        self.death_motion_index = 0
        self.death_spin_starting_time = 0
        self.death_spin_cooldown = PLAYER_DEATH_SPIN_AMOUNT * PLAYER_DEATH_SPIN_DURATION
        self.death_floor_switch_cooldown = MAP_DEATH_FADE_COOLDOWN
        self.death_floor_switch_starting_time = 0
        self.death_gray_cooldown = PLAYER_GRAY_COOLDOWN
        self.death_gray_starting_time = 0
        self.death_despawn_cooldown = PLAYER_DEATH_ANIMATION_COOLDOWN * PLAYER_DEATH_FRAMES
        self.death_despawn_starting_time = 0
        self.death_hurt_cooldown = PLAYER_DEATH_HURT_COOLDOWN
        self.death_hurt_starting_time = 0

    def draw_selector(self):
        # creates the item selector for the menu screen
        selector_pos = MENU_BOOMERANG_TOPLEFT
        if self.current_selected_item != 'None':
            selector_pos = self.menu_item_coord_and_frame_id[self.current_selected_item][0]
        self.item_selector = Selector([self.menu_sprites], selector_pos, self.hud_tile_set)

    def draw_menu(self):
        # Draw background
        self.floor_surface = pygame.image.load('../graphics/hud/pause_menu.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, 0))

        # Draw owned & selected items
        self.draw_items()

        self.draw_triforce()

    def draw_items(self):
        # Draw (if any) the currently selected item in the frame left of the items owned
        if self.current_selected_item != 'None':
            if self.item_selected_sprite is not None:
                self.item_selected_sprite.kill()
            self.item_selected_sprite = Tile(MENU_SELECTED_ITEM_TOPLEFT,
                                             [self.menu_sprites],
                                             self.items_tile_set.get_sprite_image(
                                                 self.menu_item_coord_and_frame_id[self.current_selected_item][1]))

        # Passive Items
        if self.player.has_item(LADDER_LABEL):
            Tile(MENU_LADDER_TOPLEFT, [self.menu_sprites], self.items_tile_set.get_sprite_image(LADDER_FRAME_ID))

        # Selectable items
        if self.player.has_item(BOOMERANG_LABEL):
            # Didn't implement red/blue boomerang system
            Tile(MENU_BOOMERANG_TOPLEFT, [self.menu_sprites], self.items_tile_set.get_sprite_image(BOOMERANG_FRAME_ID))
        if self.player.has_item(BOMB_LABEL):
            Tile(MENU_BOMBS_TOPLEFT, [self.menu_sprites], self.items_tile_set.get_sprite_image(BOMB_FRAME_ID))
        if self.player.has_item(CANDLE_LABEL):
            # Didn't implement red/blue candle system
            Tile(MENU_CANDLE_TOPLEFT, [self.menu_sprites], self.items_tile_set.get_sprite_image(RED_CANDLE_FRAME_ID))

    def draw_triforce(self):
        # TriForce fragment system is not implemented yet
        # Empty Triforce is part of the menu background, fragments will be drawn on top of it
        pass

    def draw_hud(self):
        # Draw HUD space either at the top (level) or the bottom (pause menu) of the screen
        self.menu_surface = pygame.image.load('../graphics/hud/hud_perma.png').convert()
        if self.in_menu:
            top_left = (0, SCREEN_HEIGHT - HUD_TILE_HEIGHT*TILE_SIZE)
        else:
            top_left = (0, 0)
        self.menu_rect = self.menu_surface.get_rect(topleft=top_left)
        self.display_surface.blit(self.menu_surface, top_left)

        # Minimap is not implemented yet
        self.draw_money()
        self.draw_keys()
        self.draw_bombs()
        self.draw_item_b()
        self.draw_item_a()
        self.draw_hearts()

    def draw_money(self):
        # Draw amount of rupees inside the HUD
        if self.in_menu:
            sprite_groups = [self.money_amount_sprites, self.menu_sprites]
        else:
            sprite_groups = [self.money_amount_sprites, self.visible_sprites]

        if self.money_amount_sprites:
            for sprite in self.money_amount_sprites:
                sprite.kill()
        hundreds = self.player.money // 100
        tens = (self.player.money // 10) % 10
        units = self.player.money % 10
        hundreds_pos = (self.menu_rect.x + HUD_MONEY_HUNDREDS_POSITION[0],
                        self.menu_rect.y + HUD_MONEY_HUNDREDS_POSITION[1])
        tens_pos = (self.menu_rect.x + HUD_MONEY_TENS_POSITION[0],
                    self.menu_rect.y + HUD_MONEY_TENS_POSITION[1])
        units_pos = (self.menu_rect.x + HUD_MONEY_UNITS_POSITION[0],
                     self.menu_rect.y + HUD_MONEY_UNITS_POSITION[1])

        Tile(hundreds_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(units))

    def draw_keys(self):
        # Draw amount of keys inside the HUD
        if self.in_menu:
            sprite_groups = [self.keys_amount_sprites, self.menu_sprites]
        else:
            sprite_groups = [self.keys_amount_sprites, self.visible_sprites]

        if self.keys_amount_sprites:
            for sprite in self.keys_amount_sprites:
                sprite.kill()
        hundreds = self.player.keys // 100
        tens = (self.player.keys // 10) % 10
        units = self.player.keys % 10
        hundreds_pos = (self.menu_rect.x + HUD_KEYS_HUNDREDS_POSITION[0],
                        self.menu_rect.y + HUD_KEYS_HUNDREDS_POSITION[1])
        tens_pos = (self.menu_rect.x + HUD_KEYS_TENS_POSITION[0],
                    self.menu_rect.y + HUD_KEYS_TENS_POSITION[1])
        units_pos = (self.menu_rect.x + HUD_KEYS_UNITS_POSITION[0],
                     self.menu_rect.y + HUD_KEYS_UNITS_POSITION[1])

        Tile(hundreds_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(units))

    def draw_bombs(self):
        # Draw amount of bombs inside the HUD
        if self.in_menu:
            sprite_groups = [self.bombs_amount_sprites, self.menu_sprites]
        else:
            sprite_groups = [self.bombs_amount_sprites, self.visible_sprites]

        if self.bombs_amount_sprites:
            for sprite in self.bombs_amount_sprites:
                sprite.kill()
        hundreds = self.player.bombs // 100
        tens = (self.player.bombs // 10) % 10
        units = self.player.bombs % 10
        hundreds_pos = (self.menu_rect.x + HUD_BOMBS_HUNDREDS_POSITION[0],
                        self.menu_rect.y + HUD_BOMBS_HUNDREDS_POSITION[1])
        tens_pos = (self.menu_rect.x + HUD_BOMBS_TENS_POSITION[0],
                    self.menu_rect.y + HUD_BOMBS_TENS_POSITION[1])
        units_pos = (self.menu_rect.x + HUD_BOMBS_UNITS_POSITION[0],
                     self.menu_rect.y + HUD_BOMBS_UNITS_POSITION[1])

        Tile(hundreds_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             self.font_tile_set.get_sprite_image(units))

    def draw_hearts(self):
        # Draw amount of health inside the HUD
        if self.in_menu:
            sprite_groups = [self.health_sprites, self.menu_sprites]
        else:
            sprite_groups = [self.health_sprites, self.visible_sprites]
        if self.health_sprites:
            for sprite in self.health_sprites:
                sprite.kill()
        nb_hearts = self.player.health // PLAYER_HEALTH_PER_HEART
        for heart_i in range(0, nb_hearts):
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (heart_i % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (heart_i // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 self.hud_tile_set.get_sprite_image(HUD_FULL_HEART_FRAME_ID))
        if self.player.health % PLAYER_HEALTH_PER_HEART > 0:
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (nb_hearts % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (nb_hearts // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 self.hud_tile_set.get_sprite_image(HUD_HALF_HEART_FRAME_ID))
            nb_hearts += 1
        for heart_i in range(nb_hearts, self.player.current_max_health // PLAYER_HEALTH_PER_HEART):
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (heart_i % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (heart_i // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 self.hud_tile_set.get_sprite_image(HUD_EMPTY_HEART_FRAME_ID))

    def draw_floor(self, death_color=''):
        # Draw the background of the level
        if death_color == 'black':
            self.floor_surface = pygame.image.load('../graphics/levels/black.png').convert()
        else:
            self.floor_surface = pygame.image.load(
                f'../graphics/levels/{self.current_map}{self.current_map_screen}{death_color}.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, HUD_TILE_HEIGHT*TILE_SIZE))

    def draw_item_a(self):
        # Draw the A item in the A Frame of the HUD
        if self.in_menu:
            sprite_groups = [self.menu_sprites]
        else:
            sprite_groups = [self.visible_sprites]

        item_a_pos = (self.menu_rect.x + 296,
                      self.menu_rect.y + 48)

        item_a_id = None
        # Define here all swords implemented
        if self.player.itemA == WOOD_SWORD_LABEL:
            item_a_id = WOOD_SWORD_FRAME_ID

        if self.equipped_item_a_sprite:
            self.equipped_item_a_sprite.kill()

        if item_a_id is not None:
            self.equipped_item_a_sprite = Tile(item_a_pos,
                                               sprite_groups,
                                               self.items_tile_set.get_sprite_image(item_a_id))

    def draw_item_b(self):
        # Draw the selected B item in the B Frame of the HUD
        if self.in_menu:
            sprite_groups = [self.menu_sprites]
        else:
            sprite_groups = [self.visible_sprites]

        item_b_pos = (self.menu_rect.x + 248,
                      self.menu_rect.y + 48)

        if self.equipped_item_b_sprite:
            self.equipped_item_b_sprite.kill()

        # Get selected item B id
        match self.player.itemB:
            case 'Boomerang':
                item_frame_id = BOOMERANG_FRAME_ID
            case 'Bomb':
                item_frame_id = BOMB_FRAME_ID
            case 'Candle':
                item_frame_id = RED_CANDLE_FRAME_ID
            case 'None':
                item_frame_id = None
            case _:
                # Item B not implemented, abort
                return

        if item_frame_id is not None:
            self.equipped_item_b_sprite = Tile(item_b_pos,
                                               sprite_groups,
                                               self.items_tile_set.get_sprite_image(item_frame_id))

    def load_warps(self, level_id):
        layout = import_csv_layout(f'../map/{level_id}_Warps.csv')
        # Warp tiles are invisible, and either induce a scrolling animation on the sides of the screen, or a
        # stairs animation anywhere else
        # No graphics, only collisions
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # Skipping the HUD tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    Warp((x, y), [self.warp_sprites], sprite_id, self.player, self)

    def load_limits(self, level_id):
        layout = import_csv_layout(f'../map/{level_id}_Limits.csv')
        # Draw lines of obstacles so no one gets into the menu or off the screen at the bottom
        for col in range(0, NB_TILE_WIDTH):
            y_top = (HUD_TILE_HEIGHT-1)*TILE_SIZE
            y_bottom = SCREEN_HEIGHT
            Obstacle((col*TILE_SIZE, y_top), [self.obstacle_sprites, self.border_sprites])
            Obstacle((col*TILE_SIZE, y_bottom), [self.obstacle_sprites, self.border_sprites])
        # Draw lines of obstacles so no one gets out of the sides of the screen
        for row in range(HUD_TILE_HEIGHT, NB_TILE_HEIGHT):
            x_left = - TILE_SIZE
            x_right = SCREEN_WIDTH
            Obstacle((x_left, row*TILE_SIZE), [self.obstacle_sprites, self.border_sprites])
            Obstacle((x_right, row*TILE_SIZE), [self.obstacle_sprites, self.border_sprites])

        # Draw obstacles inside the level layout
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    Obstacle((x, y), [self.obstacle_sprites], sprite_id)

    def load_items(self, level_id):
        layout = import_csv_layout(f'../map/{level_id}_Items.csv')
        # Ignore all items for levels that are not supposed to have any
        if level_id in MAP_ITEMS.keys():
            map_items = MAP_ITEMS[level_id].keys()
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # Skipping menu tiles at the top of screen
                    sprite_id = int(col)
                    # Ignore any item that has an id that is not supposed to be in this level
                    if (sprite_id == HEARTRECEPTACLE_FRAME_ID
                            and HEARTRECEPTACLE_LABEL in map_items
                            and MAP_ITEMS[level_id][HEARTRECEPTACLE_LABEL]):
                        HeartReceptacle((x, y),
                                        [self.visible_sprites, self.lootable_items_sprites],
                                        self.consumables_tile_set,
                                        level_id,
                                        self)
                    elif sprite_id == LADDER_FRAME_ID and MAP_ITEMS[level_id][LADDER_LABEL]:
                        Ladder((x, y),
                               [self.visible_sprites, self.lootable_items_sprites],
                               self.items_tile_set,
                               level_id,
                               self)
                    elif sprite_id == RED_CANDLE_FRAME_ID and MAP_ITEMS[level_id][CANDLE_LABEL]:
                        RedCandle((x, y),
                                  [self.visible_sprites, self.lootable_items_sprites],
                                  self.items_tile_set,
                                  level_id,
                                  self)
                    elif sprite_id == BOOMERANG_FRAME_ID and MAP_ITEMS[level_id][BOOMERANG_LABEL]:
                        Boomerang((x, y),
                                  [self.visible_sprites, self.lootable_items_sprites],
                                  self.items_tile_set,
                                  level_id,
                                  self)
                    elif sprite_id == WOOD_SWORD_FRAME_ID and MAP_ITEMS[level_id][WOOD_SWORD_LABEL]:
                        WoodenSword((x, y),
                                    [self.visible_sprites, self.lootable_items_sprites],
                                    self.items_tile_set,
                                    level_id,
                                    self)

    def load_enemies(self, level_id):
        layout = import_csv_layout(f'../map/{level_id}_Enemies.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # Skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id == 4:
                    RedOctorock((x, y),
                                [self.visible_sprites, self.enemy_sprites],
                                self.visible_sprites,
                                self.obstacle_sprites,
                                self.particle_sprites,
                                self.enemies_tile_set,
                                self.particle_tile_set)

    def load_shop(self, level_id):
        # Shops display from 1 to 3 items max
        if level_id in SHOPS.keys() and SHOPS[level_id]['items']:
            nb_items = len(SHOPS[level_id]['items'].keys())
            item_pos = []
            hud_offset = HUD_TILE_HEIGHT * TILE_SIZE
            text_offset = TEXT_MARGIN * FONT_SPRITE_SIZE
            item_y = hud_offset + text_offset + 9 * TILE_SIZE
            match nb_items:
                case 1:
                    item_pos.append((15 * TILE_SIZE, item_y))
                case 2:
                    item_pos.append((12 * TILE_SIZE, item_y))
                    item_pos.append((18 * TILE_SIZE, item_y))
                case _:
                    item_pos.append((10 * TILE_SIZE, item_y))
                    item_pos.append((15 * TILE_SIZE, item_y))
                    item_pos.append((20 * TILE_SIZE, item_y))
                    nb_items = 3

            # Caution : in python, 0 == False, so if npc_id is 0, this code is never executed
            if SHOPS[level_id]['npc_id']:
                npc_pos = (15 * TILE_SIZE, item_y - 4 * TILE_SIZE)
                npc_image = self.npcs_tile_set.get_sprite_image(SHOPS[level_id]['npc_id'])
                groups = [self.visible_sprites, self.npc_sprites]
                Npc(npc_pos, groups, npc_image)

            if SHOPS[level_id]['text']:
                text_pos_y = text_offset + hud_offset
                TextBlock([self.visible_sprites, self.text_sprites],
                          SHOPS[level_id]['text'],
                          self.font_tile_set,
                          text_pos_y)

            items = list(SHOPS[level_id]['items'].items())
            for i in range(nb_items):
                item_label, item_price = items[i]
                if item_label in SHOP_CONSUMABLES:
                    tile_set = self.consumables_tile_set
                    item_image = tile_set.get_sprite_image(SHOP_CONSUMABLES[item_label])
                elif item_label in SHOP_ITEMS:
                    tile_set = self.items_tile_set
                    item_image = tile_set.get_sprite_image(SHOP_ITEMS[item_label])
                else:
                    # Unidentified item, implement it in settings.py
                    # Abort
                    return

                Purchasable(item_pos[i],
                            [self.visible_sprites, self.purchasable_sprites],
                            item_label,
                            item_image,
                            item_price,
                            self)

                if item_label != RUPEE_LABEL and item_price > 0:
                    price_x = item_pos[i][0] + TILE_SIZE - FONT_SPRITE_SIZE // 2
                    if item_price // 100 != 0:
                        price_x -= FONT_SPRITE_SIZE
                    elif item_price // 10 != 0:
                        price_x -= FONT_SPRITE_SIZE // 2
                    price_y = item_pos[i][1] + 3 * TILE_SIZE
                    TextBlock([self.visible_sprites, self.text_sprites],
                              str(item_price),
                              self.font_tile_set,
                              price_y,
                              price_x)

    def load_player(self, pos):
        self.player = Player(pos,
                             [self.visible_sprites],
                             self.obstacle_sprites,
                             self.enemy_sprites,
                             self.visible_sprites,
                             self.particle_sprites,
                             self.lootable_items_sprites,
                             self.border_sprites,
                             self.purchasable_sprites,
                             self.npc_sprites,
                             self.player_tile_set,
                             self.particle_tile_set,
                             self.items_tile_set)

    def create_map(self, level_id):
        # This creates all Sprites of the new map
        # This is done AFTER any map change animation
        self.load_limits(level_id)
        self.load_warps(level_id)
        self.load_items(level_id)
        self.load_enemies(level_id)
        self.load_shop(level_id)

    def create_transition_surface(self):
        # Only Overworld and Dungeon maps will have warp tiles to border scroll
        # No loop from max right to max left as if the world was a sphere
        next_floor_x = 0
        next_floor_y = 0
        current_floor_x = 0
        current_floor_y = 0
        match self.in_map_transition:
            case 'Warp_U':
                if 'level' in self.current_map:
                    next_level_id = int(self.current_map_screen) - NB_MAPS_PER_ROW['Overworld']
                else:
                    next_level_id = int(self.current_map_screen) - NB_MAPS_PER_ROW['Dungeon']
                self.transition_surface = pygame.Surface(
                    (self.floor_rect.width, 2 * self.floor_rect.height))
                current_floor_y = self.floor_rect.height
            case 'Warp_R':
                next_level_id = int(self.current_map_screen) + 1
                self.transition_surface = pygame.Surface(
                    (2 * self.floor_rect.width, self.floor_rect.height))
                next_floor_x = self.floor_rect.width
            case 'Warp_D':
                if 'level' in self.current_map:
                    next_level_id = int(self.current_map_screen) + NB_MAPS_PER_ROW['Overworld']
                else:
                    next_level_id = int(self.current_map_screen) + NB_MAPS_PER_ROW['Dungeon']
                self.transition_surface = pygame.Surface(
                    (self.floor_rect.width, 2 * self.floor_rect.height))
                next_floor_y = self.floor_rect.height
            case 'Warp_L':
                next_level_id = int(self.current_map_screen) - 1
                self.transition_surface = pygame.Surface(
                    (2 * self.floor_rect.width, self.floor_rect.height))
                current_floor_x = self.floor_rect.width
            case _:
                # Undefined warp transition, abort
                return

        next_floor = pygame.image.load(f'../graphics/levels/{self.current_map}{next_level_id}.png').convert()
        self.transition_surface.blit(next_floor, (next_floor_x, next_floor_y))
        self.transition_surface.blit(self.floor_surface, (current_floor_x, current_floor_y))
        self.next_map_screen = next_level_id

    def change_map(self, change_id):
        if change_id >= 0:
            self.map_scroll_animation_counter = 0
            for warp in self.warp_sprites:
                warp.kill()
            for enemy in self.enemy_sprites:
                enemy.kill()
            for particle in self.particle_sprites:
                particle.kill()
            for obstacle in self.obstacle_sprites:
                obstacle.kill()
            for item in self.lootable_items_sprites:
                item.kill()
            for npc in self.npc_sprites:
                npc.kill()
            for purchasable in self.purchasable_sprites:
                purchasable.kill()
            for text in self.text_sprites:
                text.kill()

            # change_id 0 -> 3 is a side scrolling map change, respectively Up/Right/Down/Left
            # change_id > 3 is a stairs map change, with sound and a completely different map
            match change_id:
                case 0:
                    # Up
                    self.in_map_transition = 'Warp_U'
                    self.create_transition_surface()
                    self.player.set_state('warping')
                    # Animate slide - will be done in update
                case 1:
                    # Right
                    self.in_map_transition = 'Warp_R'
                    self.create_transition_surface()
                    self.player.set_state('warping')
                    # Animate slide - will be done in update
                case 2:
                    # Down
                    self.in_map_transition = 'Warp_D'
                    self.create_transition_surface()
                    self.player.set_state('warping')
                    # Animate slide - will be done in update
                case 3:
                    # Left
                    self.in_map_transition = 'Warp_L'
                    self.create_transition_surface()
                    self.player.set_state('warping')
                    # Animate slide - will be done in update
                case _:
                    if change_id - 4 < len(UNDERWORLD_STAIRS):
                        if UNDERWORLD_STAIRS[change_id - 4]['stairs']:
                            self.in_map_transition = 'Stairs'
                            self.player.set_state('stairs')
                            self.stairs_animation_starting_time = pygame.time.get_ticks()
                        else:
                            self.in_map_transition = 'Silent'

                        self.next_map = UNDERWORLD_STAIRS[change_id - 4]['map']
                        self.next_map_screen = UNDERWORLD_STAIRS[change_id - 4]['screen']
                        self.player_new_position = UNDERWORLD_STAIRS[change_id - 4]['player_pos']

    def animate_map_transition(self):
        self.map_scroll_animation_counter += 1
        x_fixed_offset = self.floor_rect.width / MAP_SCROLL_FRAMES_COUNT
        y_fixed_offset = self.floor_rect.height / MAP_SCROLL_FRAMES_COUNT
        x_offset = x_fixed_offset * self.map_scroll_animation_counter
        y_offset = y_fixed_offset * self.map_scroll_animation_counter
        hud_offset = HUD_TILE_HEIGHT*TILE_SIZE

        match self.in_map_transition:
            case 'Warp_U':
                self.display_surface.blit(self.transition_surface, (0, hud_offset - self.floor_rect.height + y_offset))
                self.draw_hud()
                self.player.offset_position(0, y_fixed_offset)
            case 'Warp_R':
                self.display_surface.blit(self.transition_surface, (-x_offset, hud_offset))
                self.player.offset_position(-x_fixed_offset, 0)
            case 'Warp_D':
                self.display_surface.blit(self.transition_surface, (0, hud_offset - y_offset))
                self.draw_hud()
                self.player.offset_position(0, -y_fixed_offset)
            case 'Warp_L':
                self.display_surface.blit(self.transition_surface, (x_offset - self.floor_rect.width, hud_offset))
                self.player.offset_position(x_fixed_offset, 0)

    def death(self):
        self.draw_hud()
        self.draw_floor()
        current_time = pygame.time.get_ticks()

        # Kill every enemy sprite and every particle sprite
        if self.death_motion_index == 1:
            for enemy in self.enemy_sprites:
                enemy.kill()
            for particle in self.particle_sprites:
                particle.kill()
            self.death_motion_index += 1

        # Player is in a hurt state for death_hurt_cooldown, by default 3 cycles of the hurt animation
        if self.death_motion_index == 2:
            if self.death_hurt_starting_time == 0:
                self.death_hurt_starting_time = current_time
                self.player.set_state('dying')
            elif current_time - self.death_hurt_starting_time >= self.death_hurt_cooldown:
                self.death_motion_index += 1
                self.game_over_sound.play()
                self.death_spin_starting_time = current_time

        # Set map img to red version
        if self.death_motion_index == 3:
            self.draw_floor(self.death_floors[self.death_floor_index])
            # Spin ! By default, 3 times (cf init of self.death_spin_cooldown)
            if current_time - self.death_spin_starting_time < self.death_spin_cooldown:
                self.player.set_state('spinning')
            else:
                self.death_motion_index += 1
                self.death_floor_index += 1
                self.player.set_state('idle_d')

        # Switch map img to 3 darker shades successively
        if self.death_motion_index == 4 and self.death_floor_index < self.number_of_death_floors:
            if self.death_floor_switch_starting_time == 0:
                self.death_floor_switch_starting_time = current_time
            self.draw_floor(self.death_floors[self.death_floor_index])
            if current_time - self.death_floor_switch_starting_time >= self.death_floor_switch_cooldown:
                self.death_floor_switch_starting_time = 0
                self.death_floor_index += 1
        elif self.death_motion_index == 4 and self.death_floor_index == self.number_of_death_floors:
            self.death_motion_index += 1

        # No more floor, just black
        if self.death_motion_index > 4:
            self.draw_floor('black')

        # Put player in gray state for animation
        if self.death_motion_index == 5:
            if self.death_gray_starting_time == 0:
                self.death_gray_starting_time = current_time
                self.player.set_state('gray')
            if current_time - self.death_gray_starting_time >= self.death_gray_cooldown:
                self.death_motion_index += 1

        # Put player in despawn state for animation
        if self.death_motion_index == 6:
            if self.death_despawn_starting_time == 0:
                self.death_despawn_starting_time = current_time
                self.player.set_state('despawn')
            if current_time - self.death_despawn_starting_time >= self.death_despawn_cooldown:
                self.death_motion_index += 1

        # Kill player sprite
        if self.death_motion_index == 7:
            self.player.kill()
            self.death_motion_index += 1

        # Print GAME OVER in middle of screen until key is pressed to exit game
        if self.death_motion_index == 8:
            game_over_message_pos_y = (SCREEN_HEIGHT // 2) + ((HUD_TILE_HEIGHT * TILE_SIZE) // 2) - (TILE_SIZE // 2)
            TextBlock([self.visible_sprites, self.text_sprites],
                      GAME_OVER_TEXT,
                      self.font_tile_set,
                      game_over_message_pos_y)
            self.death_motion_index += 1

        if self.death_motion_index == 9:
            keys = pygame.key.get_pressed()
            if is_action_a_key_pressed(keys):
                self.death_played = True

    def is_menu_key_pressed_out_of_menu(self, keys):
        if is_menu_key_pressed(keys) and not self.in_menu:
            return True
        return False

    def is_menu_key_pressed_in_menu(self, keys):
        if is_menu_key_pressed(keys) and self.in_menu:
            return True
        return False

    def is_right_key_pressed_in_menu_with_item(self, keys):
        if is_right_key_pressed(keys) and self.in_menu and self.current_selected_item != 'None':
            return True
        return False

    def is_left_key_pressed_in_menu_with_item(self, keys):
        if is_left_key_pressed(keys) and self.in_menu and self.current_selected_item != 'None':
            return True
        return False

    def get_selector_position_for_next_item(self, is_reversed=False):
        if is_reversed:
            item_list = list(reversed(list(self.menu_item_coord_and_frame_id.keys())))
        else:
            item_list = list(list(self.menu_item_coord_and_frame_id.keys()))

        current_item_index = item_list.index(self.current_selected_item) + 1
        for i in range(len(item_list) - current_item_index):
            if self.player.has_item(item_list[current_item_index + i]):
                self.current_selected_item = (item_list[current_item_index + i])
                break

        return self.menu_item_coord_and_frame_id[self.current_selected_item][0]

    def input(self):
        # Known issue : When key press is short, it is sometimes not registered and the menu doesn't open/close
        # How to fix that ?
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if current_time - self.key_pressed_start_timer >= self.key_pressed_cooldown:
            self.key_pressed_start_timer = current_time

            # Toggle pause menu on/off
            if self.is_menu_key_pressed_out_of_menu(keys) and not self.player.isDead:
                self.in_menu = True
                self.current_selected_item = self.player.itemB
                self.draw_selector()
            elif self.is_menu_key_pressed_in_menu(keys) and not self.player.isDead:
                self.in_menu = False
                self.player.change_item_b(self.current_selected_item)
                for sprite in self.menu_sprites:
                    sprite.kill()
            # Move item selector in menu
            elif self.is_right_key_pressed_in_menu_with_item(keys):
                item_pos = self.get_selector_position_for_next_item()
                self.item_selector.move(item_pos)
            elif self.is_left_key_pressed_in_menu_with_item(keys):
                item_pos = self.get_selector_position_for_next_item(True)
                self.item_selector.move(item_pos)

    def drop_loot(self, pos):
        # Loot system follows (loosely) the system used in the NES game
        # Monsters have a chance of dropping an item when they die
        # If Monster drops an item, which item spawns is decided by a loot table, that compares the kill count
        # of the current play session compared to the table of the group the monster is a part of
        # I chose to do only one table, and all monster will belong to this group :
        # From 0 to 9 : Rupee - Bombs - Rupee - Fairy - Rupee - Heart - Heart - Bombs - Rupee - Heart
        # 40% Rupee, 30% Heart, 20% Bombs, 10% Fairy
        self.kill_count += 1
        if random.randint(1, 100) <= LOOT_DROP_PERCENTAGE:
            loot = self.kill_count % 10
            match loot:
                case 0 | 2 | 4 | 8:
                    rupee_amount = 5 if random.randint(1, 100) <= LOOT_BIG_RUPEE_PERCENTAGE else 1
                    Rupee(pos,
                          [self.visible_sprites, self.particle_sprites],
                          self.consumables_tile_set,
                          self.obstacle_sprites,
                          rupee_amount,
                          self)
                case 1 | 7:
                    CBomb(pos,
                          [self.visible_sprites, self.particle_sprites],
                          self.consumables_tile_set,
                          self.obstacle_sprites,
                          self)
                case 3:
                    Fairy(pos,
                          [self.visible_sprites, self.particle_sprites],
                          self.consumables_tile_set,
                          self.border_sprites,
                          self)
                case 5 | 6 | 9:
                    Heart(pos,
                          [self.visible_sprites, self.particle_sprites],
                          self.consumables_tile_set,
                          self.obstacle_sprites,
                          self)

    def heal_player(self, amount):
        self.player.heal(amount)

    def player_pick_up(self, item_label):
        x_offset = 0
        y_offset = - TILE_SIZE * 2
        if item_label == HEARTRECEPTACLE_LABEL:
            item_image = self.consumables_tile_set.get_sprite_image(HEARTRECEPTACLE_FRAME_ID)
            x_offset -= 2
            y_offset += 4
        elif item_label == WOOD_SWORD_LABEL:
            item_image = self.items_tile_set.get_sprite_image(WOOD_SWORD_FRAME_ID)
            x_offset -= 12
        elif item_label == CANDLE_LABEL:
            item_image = self.items_tile_set.get_sprite_image(RED_CANDLE_FRAME_ID)
            x_offset -= 12
        elif item_label == BOOMERANG_LABEL:
            item_image = self.items_tile_set.get_sprite_image(BOOMERANG_FRAME_ID)
            x_offset -= 12
            y_offset += 9
        elif item_label == LADDER_LABEL:
            item_image = self.items_tile_set.get_sprite_image(LADDER_FRAME_ID)
            x_offset = 3
        else:
            # Item not implemented yet ? abort
            return

        self.player.add_item(item_label)
        item_pos = (self.player.rect.left + x_offset, self.player.rect.top + y_offset)
        self.item_picked_up = Tile(item_pos, [self.visible_sprites], item_image)

    def add_money(self, amount):
        self.player.add_money(amount)

    def add_bombs(self, amount):
        self.player.add_bombs(amount)

    def run(self):
        self.input()

        for monster in self.enemy_sprites:
            if monster.isDead and monster.deathPlayed:
                # Delete monsters that have played their death animation
                self.drop_loot(monster.rect.topleft)
                monster.kill()
            elif self.in_menu:
                # Reset attack cooldown timer until game is resumed
                monster.attack_starting_time = pygame.time.get_ticks()

        if self.item_picked_up is not None and 'pickup' not in self.player.state:
            self.item_picked_up.kill()
            self.item_picked_up = None

        if not self.player.isDead:
            self.draw_hud()
            # Update and draw the game
            if not self.in_menu:
                self.draw_floor()
            # Update and draw the pause menu
            else:
                self.draw_menu()

        elif not self.death_played:
            # Play death & game over animation
            if self.death_motion_index == 0:
                self.overworld_background_theme.stop()
                self.death_motion_index = 1
            self.death()

        elif self.death_played:
            # Close game
            pygame.quit()
            sys.exit()

        # Sprites are updated until map transitions
        if self.in_map_transition is None:
            if not self.in_menu:
                self.visible_sprites.update()
                self.warp_sprites.update()
            else:
                # While in menu, enemies sprites are not updated, thus "paused"
                self.menu_sprites.update()
        # During map transition, all existing sprite is paused, not being updated until the transition is over
        else:
            # Warp makes a scrolling transition of the screen level
            if 'Warp' in self.in_map_transition:
                if self.map_scroll_animation_counter <= MAP_SCROLL_FRAMES_COUNT:
                    self.animate_map_transition()
                else:
                    self.current_map_screen = self.next_map_screen
                    self.draw_floor()
                    self.create_map(self.current_map + str(self.current_map_screen))
                    self.player.set_state('idle')
                    self.map_scroll_animation_counter = 0
                    self.in_map_transition = None
            # Other transitions (caves with stairs animation, or secret stairs with no animation
            # Which, I know, is strange, but how the NES game operates from the player POV
            else:
                # Wait for the stairs animation (and sound) to be over with, if any
                if self.in_map_transition == 'Stairs':
                    current_time = pygame.time.get_ticks()
                    if current_time - self.stairs_animation_starting_time >= self.stairs_animation_duration:
                        self.in_map_transition = 'Done'
                # Generate new map's sprites (enemies, borders, ...), use appropriate music (if any), move the player
                else:
                    self.current_map = self.next_map
                    self.current_map_screen = self.next_map_screen
                    self.create_map(self.current_map + self.current_map_screen)
                    if 'level' in self.current_map:
                        self.overworld_background_theme.play(loops=-1)
                    else:
                        self.overworld_background_theme.stop()
                    # Play dungeon music if in dungeon
                    if 'dungeon' in self.current_map:
                        self.dungeon_background_theme.play(loops=-1)
                    else:
                        self.dungeon_background_theme.stop()
                    self.player.set_position(self.player_new_position)
                    self.next_map = None
                    self.next_map_screen = None
                    self.player_new_position = None
                    self.in_map_transition = None
            # Only visible sprites left at this point are the Player, and all the HUD sprites

            # Put the player on top of all other visible sprites
            self.visible_sprites.update()
