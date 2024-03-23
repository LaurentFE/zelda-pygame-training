import random

import pygame.mixer

from settings import *
from support import *
from inputs import *
import tileset
from tile import Tile
from obstacle import Obstacle
from player import Player
from enemies import RedOctorock, BlueOctorock, RedMoblin, BlackMoblin, Stalfos, Goriya, Zora, Leever
from particles import (Heart, Rupee, CBomb, Fairy, Key, HeartReceptacle,
                       Ladder, RedCandle, Boomerang, WoodenSword, Triforce)
from selector import Selector
from warp import Warp, SecretPassage
from purchasable import Purchasable
from npc import Npc
from textblock import TextBlock
from door import Door


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Level(metaclass=Singleton):
    def __init__(self):
        # Set up variables
        self.player = None
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
        self.secret_bomb_sprites = pygame.sprite.Group()
        self.secret_flame_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()

        self.equipped_item_a_sprite = None
        self.equipped_item_b_sprite = None
        self.current_selected_item = NONE_LABEL
        self.menu_item_coord_and_frame_id = {
            BOOMERANG_LABEL: (MENU_BOOMERANG_TOPLEFT, BOOMERANG_FRAME_ID),
            BOMB_LABEL: (MENU_BOMBS_TOPLEFT, BOMB_FRAME_ID),
            CANDLE_LABEL: (MENU_CANDLE_TOPLEFT, RED_CANDLE_FRAME_ID)
        }
        self.item_selector = None
        self.item_selected_sprite = None
        self.item_picked_up = None

        # Set up sounds
        self.overworld_background_theme = pygame.mixer.Sound(THEME_OVERWORLD)
        self.overworld_background_theme.set_volume(0.2)
        self.dungeon_background_theme = pygame.mixer.Sound(THEME_DUNGEON)
        self.dungeon_background_theme.set_volume(0.2)
        self.game_over_sound = pygame.mixer.Sound(SOUND_GAME_OVER)
        self.game_over_sound.set_volume(0.4)
        self.event_cleared_sound = pygame.mixer.Sound(SOUND_EVENT_CLEARED)
        self.event_cleared_sound.set_volume(0.4)
        self.triforce_sound = pygame.mixer.Sound(SOUND_TRIFORCE_OBTAINED)
        self.triforce_sound.set_volume(0.4)

        self.current_map = STARTING_MAP
        self.current_map_screen = STARTING_SCREEN
        if self.current_map == OVERWORLD_STARTING_MAP:
            self.load_player(OVERWORLD_PLAYER_START_POS)
            self.overworld_background_theme.play(loops=-1)
        else:
            self.load_player(DUNGEON_PLAYER_START_POS)
            self.dungeon_background_theme.play(loops=-1)
        self.create_map(self.current_map + self.current_map_screen)
        self.in_map_transition = None
        self.map_scroll_animation_counter = 0
        self.next_map = None
        self.next_map_screen = None
        self.player_new_position = None
        self.enemies_spawned_in_the_room = 0
        self.monsters_killed_in_the_room = 0
        self.dead_monsters_event_played = False

        self.key_pressed_start_timer = 0
        self.key_pressed_cooldown = LEVEL_KEY_PRESSED_COOLDOWN

        # Set Stairs animation timer
        self.stairs_animation_starting_time = 0
        self.stairs_animation_duration = PLAYER_STAIRS_DURATION
        # Set Victory animation variables & timers
        self.victory_played = False
        self.victory_floor_index = 0
        self.victory_motion_index = 0
        self.victory_floor_switch_starting_time = 0
        self.victory_floor_switch_cooldown = MAP_VICTORY_FADE_COOLDOWN
        # Set Game Over animation variables & timers
        self.death_played = False
        self.death_floor_index = 0
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
        if self.current_selected_item != NONE_LABEL:
            selector_pos = self.menu_item_coord_and_frame_id[self.current_selected_item][0]
        self.item_selector = Selector((self.menu_sprites,), selector_pos)

    def draw_menu(self):
        # Draw background
        self.floor_surface = pygame.image.load(PAUSE_MENU_PATH).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, 0))

        # Draw owned & selected items
        self.draw_items()

        self.draw_triforce()

    def draw_items(self):
        # Draw (if any) the currently selected item in the frame left of the items owned
        if self.current_selected_item != NONE_LABEL:
            if self.item_selected_sprite is not None:
                self.item_selected_sprite.kill()
            self.item_selected_sprite = Tile(MENU_SELECTED_ITEM_TOPLEFT,
                                             (self.menu_sprites,),
                                             tileset.ITEMS_TILE_SET.get_sprite_image(
                                                 self.menu_item_coord_and_frame_id[self.current_selected_item][1]))

        # Passive Items
        if self.player.has_item(LADDER_LABEL):
            Tile(MENU_LADDER_TOPLEFT,
                 (self.menu_sprites,),
                 tileset.ITEMS_TILE_SET.get_sprite_image(LADDER_FRAME_ID))

        # Selectable items
        if self.player.has_item(BOOMERANG_LABEL):
            # Didn't implement red/blue boomerang system
            Tile(MENU_BOOMERANG_TOPLEFT,
                 (self.menu_sprites,),
                 tileset.ITEMS_TILE_SET.get_sprite_image(BOOMERANG_FRAME_ID))
        if self.player.has_item(BOMB_LABEL):
            Tile(MENU_BOMBS_TOPLEFT,
                 (self.menu_sprites,),
                 tileset.ITEMS_TILE_SET.get_sprite_image(BOMB_FRAME_ID))
        if self.player.has_item(CANDLE_LABEL):
            # Didn't implement red/blue candle system
            Tile(MENU_CANDLE_TOPLEFT,
                 (self.menu_sprites,),
                 tileset.ITEMS_TILE_SET.get_sprite_image(RED_CANDLE_FRAME_ID))

    def draw_triforce(self):
        # TriForce fragment system is not implemented yet
        # Empty Triforce is part of the menu background, fragments will be drawn on top of it
        pass

    def draw_hud(self):
        # Draw HUD space either at the top (level) or the bottom (pause menu) of the screen
        self.menu_surface = pygame.image.load(HUD_PERMA_PATH).convert()
        if self.in_menu:
            top_left = (0, SCREEN_HEIGHT - HUD_OFFSET)
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
            sprite_groups = (self.money_amount_sprites, self.menu_sprites)
        else:
            sprite_groups = (self.money_amount_sprites, self.visible_sprites)

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
             tileset.FONT_TILE_SET.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(units))

    def draw_keys(self):
        # Draw amount of keys inside the HUD
        if self.in_menu:
            sprite_groups = (self.keys_amount_sprites, self.menu_sprites)
        else:
            sprite_groups = (self.keys_amount_sprites, self.visible_sprites)

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
             tileset.FONT_TILE_SET.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(units))

    def draw_bombs(self):
        # Draw amount of bombs inside the HUD
        if self.in_menu:
            sprite_groups = (self.bombs_amount_sprites, self.menu_sprites)
        else:
            sprite_groups = (self.bombs_amount_sprites, self.visible_sprites)

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
             tileset.FONT_TILE_SET.get_sprite_image(hundreds))
        Tile(tens_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(tens))
        Tile(units_pos,
             sprite_groups,
             tileset.FONT_TILE_SET.get_sprite_image(units))

    def draw_hearts(self):
        # Draw amount of health inside the HUD
        if self.in_menu:
            sprite_groups = (self.health_sprites, self.menu_sprites)
        else:
            sprite_groups = (self.health_sprites, self.visible_sprites)
        if self.health_sprites:
            for sprite in self.health_sprites:
                sprite.kill()
        nb_hearts = self.player.health // PLAYER_HEALTH_PER_HEART
        for heart_i in range(0, nb_hearts):
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (heart_i % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (heart_i // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 tileset.HUD_TILE_SET.get_sprite_image(HUD_FULL_HEART_FRAME_ID))
        if self.player.health % PLAYER_HEALTH_PER_HEART > 0:
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (nb_hearts % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (nb_hearts // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 tileset.HUD_TILE_SET.get_sprite_image(HUD_HALF_HEART_FRAME_ID))
            nb_hearts += 1
        for heart_i in range(nb_hearts, self.player.current_max_health // PLAYER_HEALTH_PER_HEART):
            heart_x = self.menu_rect.x + HUD_FIRST_HEART_POSITION_X + (heart_i % 8) * TILE_SIZE
            heart_y = self.menu_rect.y + HUD_FIRST_HEART_POSITION_Y - (heart_i // HUD_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 sprite_groups,
                 tileset.HUD_TILE_SET.get_sprite_image(HUD_EMPTY_HEART_FRAME_ID))

    def draw_floor(self, death_color=''):
        # Draw the background of the level
        if death_color == BLACK_LABEL:
            self.floor_surface = pygame.image.load(BLACK_PATH).convert()
        else:
            self.floor_surface = pygame.image.load(
                f'{LEVELS_PATH}{self.current_map}{self.current_map_screen}{death_color}{GRAPHICS_EXTENSION}').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, HUD_OFFSET))

    def draw_item_a(self):
        # Draw the A item in the A Frame of the HUD
        if self.in_menu:
            sprite_groups = (self.menu_sprites,)
        else:
            sprite_groups = (self.visible_sprites,)

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
                                               tileset.ITEMS_TILE_SET.get_sprite_image(item_a_id))

    def draw_item_b(self):
        # Draw the selected B item in the B Frame of the HUD
        if self.in_menu:
            sprite_groups = (self.menu_sprites,)
        else:
            sprite_groups = (self.visible_sprites,)

        item_b_pos = (self.menu_rect.x + 248,
                      self.menu_rect.y + 48)

        if self.equipped_item_b_sprite:
            self.equipped_item_b_sprite.kill()

        # Get selected item B id
        if self.player.itemB == BOOMERANG_LABEL:
            item_frame_id = BOOMERANG_FRAME_ID
        elif self.player.itemB == BOMB_LABEL:
            item_frame_id = BOMB_FRAME_ID
        elif self.player.itemB == CANDLE_LABEL:
            item_frame_id = RED_CANDLE_FRAME_ID
        elif self.player.itemB == NONE_LABEL:
            item_frame_id = None
        else:
            # Item B not implemented, abort
            return

        if item_frame_id is not None:
            self.equipped_item_b_sprite = Tile(item_b_pos,
                                               sprite_groups,
                                               tileset.ITEMS_TILE_SET.get_sprite_image(item_frame_id))

    def load_warps(self, level_id, warp_type):
        image = None
        revealed = False
        warp_file_path = MAPS_PATH + str(level_id)
        ignore_non_existing_file = False
        if warp_type == WARP_WARPS:
            warp_file_path += MAPS_WARP
            groups = (self.warp_sprites,)
        elif warp_type == WARP_BOMB:
            ignore_non_existing_file = True
            warp_file_path += MAPS_BOMB
            groups = (self.visible_sprites, self.secret_bomb_sprites)
            if DUNGEON_PREFIX_LABEL in level_id:
                image = tileset.WARPS_TILE_SET.get_sprite_image(SECRET_WALL_FRAME_ID)
            else:
                image = tileset.WARPS_TILE_SET.get_sprite_image(SECRET_CAVE_FRAME_ID)
            if level_id in MAP_SECRETS_REVEALED.keys():
                revealed = MAP_SECRETS_REVEALED[level_id]
            else:
                revealed = False
        elif warp_type == WARP_FLAME:
            ignore_non_existing_file = True
            warp_file_path += MAPS_FLAME
            groups = (self.visible_sprites, self.secret_flame_sprites)
            image = tileset.WARPS_TILE_SET.get_sprite_image(SECRET_STAIRS_FRAME_ID)
            if level_id in MAP_SECRETS_REVEALED.keys():
                revealed = MAP_SECRETS_REVEALED[level_id]
            else:
                revealed = False
        else:
            # warp type not implemented, abort
            return
        layout = import_csv_layout(f'{warp_file_path}{MAPS_EXTENSION}', ignore_non_existing_file)

        if layout is not None:
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * TILE_SIZE
                    # Skipping the HUD tiles at the top of screen
                    y = row_index * TILE_SIZE + HUD_OFFSET
                    sprite_id = int(col)
                    if sprite_id != -1:
                        if warp_type == WARP_WARPS:
                            Warp((x, y), groups, sprite_id, self.player)
                        elif warp_type == WARP_BOMB:
                            SecretPassage((x, y),
                                          groups,
                                          self.obstacle_sprites,
                                          sprite_id,
                                          level_id,
                                          self.player,
                                          image,
                                          revealed)
                        elif warp_type == WARP_FLAME:
                            SecretPassage((x, y),
                                          groups,
                                          self.obstacle_sprites,
                                          sprite_id,
                                          level_id,
                                          self.player,
                                          image,
                                          revealed)

    def load_limits(self, level_id):
        layout = import_csv_layout(f'{MAPS_PATH}{level_id}{MAPS_LIMITS}{MAPS_EXTENSION}')
        # Draw lines of obstacles so no one gets into the menu or off the screen at the bottom
        for col in range(0, NB_TILE_WIDTH):
            y_top = HUD_OFFSET - TILE_SIZE
            y_bottom = SCREEN_HEIGHT
            Obstacle((col*TILE_SIZE, y_top), (self.obstacle_sprites, self.border_sprites))
            Obstacle((col*TILE_SIZE, y_bottom), (self.obstacle_sprites, self.border_sprites))
        # Draw lines of obstacles so no one gets out of the sides of the screen
        for row in range(HUD_TILE_HEIGHT, NB_TILE_HEIGHT):
            x_left = - TILE_SIZE
            x_right = SCREEN_WIDTH
            Obstacle((x_left, row*TILE_SIZE), (self.obstacle_sprites, self.border_sprites))
            Obstacle((x_right, row*TILE_SIZE), (self.obstacle_sprites, self.border_sprites))

        # Draw obstacles inside the level layout
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_OFFSET  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    Obstacle((x, y), (self.obstacle_sprites,), sprite_id)

    def load_items(self, level_id):
        layout = import_csv_layout(f'{MAPS_PATH}{level_id}{MAPS_ITEMS}{MAPS_EXTENSION}', True)
        # Ignore all items for levels that are not supposed to have any
        if layout is not None and level_id in MAP_ITEMS.keys():
            map_items = MAP_ITEMS[level_id].keys()
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE + HUD_OFFSET  # Skipping menu tiles at the top of screen
                    sprite_id = int(col)
                    # Ignore any item that has an id that is not supposed to be in this level
                    if (sprite_id == HEARTRECEPTACLE_FRAME_ID
                            and HEARTRECEPTACLE_LABEL in map_items
                            and MAP_ITEMS[level_id][HEARTRECEPTACLE_LABEL]):
                        HeartReceptacle((x, y),
                                        (self.visible_sprites, self.lootable_items_sprites),
                                        level_id)
                    elif sprite_id == LADDER_FRAME_ID and MAP_ITEMS[level_id][LADDER_LABEL]:
                        Ladder((x, y),
                               (self.visible_sprites, self.lootable_items_sprites),
                               level_id)
                    elif sprite_id == RED_CANDLE_FRAME_ID and MAP_ITEMS[level_id][CANDLE_LABEL]:
                        RedCandle((x, y),
                                  (self.visible_sprites, self.lootable_items_sprites),
                                  level_id)
                    elif sprite_id == BOOMERANG_FRAME_ID and MAP_ITEMS[level_id][BOOMERANG_LABEL]:
                        Boomerang((x, y),
                                  (self.visible_sprites, self.lootable_items_sprites),
                                  level_id)
                    elif sprite_id == WOOD_SWORD_FRAME_ID and MAP_ITEMS[level_id][WOOD_SWORD_LABEL]:
                        WoodenSword((x, y),
                                    (self.visible_sprites, self.lootable_items_sprites),
                                    level_id)
                    elif sprite_id == KEY_FRAME_ID and MAP_ITEMS[level_id][KEY_LABEL]:
                        Key((x, y),
                            (self.visible_sprites, self.lootable_items_sprites, self.particle_sprites),
                            level_id)
                    elif sprite_id == TRIFORCE_FRAME_ID and MAP_ITEMS[level_id][TRIFORCE_LABEL]:
                        Triforce((x, y),
                                 (self.visible_sprites, self.lootable_items_sprites),
                                 level_id)

    def load_enemies(self, level_id):
        layout = import_csv_layout(f'{MAPS_PATH}{level_id}{MAPS_ENEMIES}{MAPS_EXTENSION}', True)
        self.enemies_spawned_in_the_room = 0
        self.monsters_killed_in_the_room = 0
        if (layout is not None
                and ((DUNGEON_PREFIX_LABEL in level_id and not DUNGEON_DECIMATION[level_id])
                     or LEVEL_PREFIX_LABEL in level_id)):
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE + HUD_OFFSET  # Skipping menu tiles at the top of screen
                    sprite_id = int(col)
                    self.enemies_spawned_in_the_room += 1
                    if sprite_id == RED_OCTOROCK_WALKING_DOWN_FRAME_ID:
                        RedOctorock((x, y),
                                    (self.visible_sprites, self.enemy_sprites),
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.particle_sprites)
                    elif sprite_id == BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID:
                        BlueOctorock((x, y),
                                     (self.visible_sprites, self.enemy_sprites),
                                     self.visible_sprites,
                                     self.obstacle_sprites,
                                     self.particle_sprites)
                    elif sprite_id == RED_MOBLIN_WALKING_DOWN_FRAME_ID:
                        RedMoblin((x, y),
                                  (self.visible_sprites, self.enemy_sprites),
                                  self.visible_sprites,
                                  self.obstacle_sprites,
                                  self.particle_sprites)
                    elif sprite_id == BLACK_MOBLIN_WALKING_DOWN_FRAME_ID:
                        BlackMoblin((x, y),
                                    (self.visible_sprites, self.enemy_sprites),
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.particle_sprites)
                    elif sprite_id == STALFOS_WALKING_FRAME_ID:
                        Stalfos((x, y),
                                (self.visible_sprites, self.enemy_sprites),
                                self.visible_sprites,
                                self.obstacle_sprites,
                                self.particle_sprites)
                    elif sprite_id == GORIYA_WALKING_DOWN_FRAME_ID:
                        Goriya((x, y),
                               (self.visible_sprites, self.enemy_sprites),
                               self.visible_sprites,
                               self.obstacle_sprites,
                               self.particle_sprites,
                               self.border_sprites)
                    elif sprite_id == ZORA_WALKING_DOWN_FRAME_ID:
                        Zora((x, y),
                             (self.visible_sprites, self.enemy_sprites),
                             self.visible_sprites,
                             self.obstacle_sprites,
                             self.particle_sprites)
                    elif sprite_id == LEEVER_WALKING_FRAME_ID:
                        Leever((x, y),
                               (self.visible_sprites, self.enemy_sprites),
                               self.visible_sprites,
                               self.obstacle_sprites,
                               self.particle_sprites)
                    else:
                        # If the sprite_id is undefined/-1, it didn't generate an Enemy
                        self.enemies_spawned_in_the_room -= 1

    def load_shop(self, level_id):
        # Shops display from 0 to 3 items max
        if level_id in SHOPS.keys() and ITEMS_LABEL in SHOPS[level_id].keys():
            nb_items = len(SHOPS[level_id][ITEMS_LABEL].keys())
            item_pos = []

            match nb_items:
                case 0:
                    pass
                case 1:
                    item_pos.append((15 * TILE_SIZE, ITEM_Y))
                case 2:
                    item_pos.append((12 * TILE_SIZE, ITEM_Y))
                    item_pos.append((18 * TILE_SIZE, ITEM_Y))
                case _:
                    item_pos.append((10 * TILE_SIZE, ITEM_Y))
                    item_pos.append((15 * TILE_SIZE, ITEM_Y))
                    item_pos.append((20 * TILE_SIZE, ITEM_Y))
                    nb_items = 3

            flame_images = [tileset.NPCS_TILE_SET.get_sprite_image(NPC_FLAME_ID),
                            pygame.transform.flip(tileset.NPCS_TILE_SET.get_sprite_image(NPC_FLAME_ID),
                                                  True,
                                                  False)]
            Npc(FLAME_1_POS, (self.visible_sprites, self.npc_sprites), flame_images)
            Npc(FLAME_2_POS, (self.visible_sprites, self.npc_sprites), flame_images)

            # Caution : in python, 0 == False, so if npc_id is 0, this code is never executed
            npc_id = SHOPS[level_id][NPC_ID_LABEL]
            if npc_id:
                npc_images = [tileset.NPCS_TILE_SET.get_sprite_image(npc_id)]
                if SHOPS[level_id][NPC_ID_LABEL] in ANIMATED_FLIPPED_NPCS:
                    npc_images.append(pygame.transform.flip(npc_images[0],
                                                            True,
                                                            False))
                Npc((NPC_X, NPC_Y), (self.visible_sprites, self.npc_sprites), npc_images)

            if SHOPS[level_id][TEXT_LABEL] and nb_items > 0:
                text_pos_y = TEXT_OFFSET + HUD_OFFSET
                TextBlock((self.visible_sprites, self.text_sprites),
                          SHOPS[level_id][TEXT_LABEL],
                          text_pos_y)

            items = list(SHOPS[level_id][ITEMS_LABEL].items())
            for i in range(nb_items):
                item_label, item_price = items[i]
                if item_label in SHOP_CONSUMABLES:
                    tile_set = tileset.CONSUMABLES_TILE_SET
                    item_image = tile_set.get_sprite_image(SHOP_CONSUMABLES[item_label])
                elif item_label in SHOP_ITEMS:
                    tile_set = tileset.ITEMS_TILE_SET
                    item_image = tile_set.get_sprite_image(SHOP_ITEMS[item_label])
                else:
                    # Unidentified item, implement it in settings.py
                    # Abort
                    return

                price_sprite = None
                if item_label != RUPEE_LABEL and item_price > 0:
                    price_x = item_pos[i][0] + TILE_SIZE - FONT_SPRITE_SIZE // 2
                    if item_price // 100 != 0:
                        price_x -= FONT_SPRITE_SIZE
                    elif item_price // 10 != 0:
                        price_x -= FONT_SPRITE_SIZE // 2
                    price_y = item_pos[i][1] + 3 * TILE_SIZE
                    price_sprite = TextBlock((self.visible_sprites, self.text_sprites),
                                             str(item_price),
                                             price_y,
                                             price_x)

                Purchasable(item_pos[i],
                            (self.visible_sprites, self.purchasable_sprites),
                            item_label,
                            item_image,
                            item_price,
                            price_sprite)

    def load_doors(self, level_id):
        if DUNGEON_PREFIX_LABEL in level_id and level_id in DUNGEON_DOORS.keys():
            for door_pos, door_type in DUNGEON_DOORS[level_id].items():
                Door((self.visible_sprites, self.door_sprites),
                     door_pos,
                     door_type)

    def load_player(self, pos):
        self.player = Player(pos,
                             (self.visible_sprites,),
                             self.obstacle_sprites,
                             self.enemy_sprites,
                             self.visible_sprites,
                             self.particle_sprites,
                             self.lootable_items_sprites,
                             self.border_sprites,
                             self.purchasable_sprites,
                             self.npc_sprites,
                             self.secret_flame_sprites,
                             self.secret_bomb_sprites,
                             self.door_sprites)

    def create_map(self, level_id):
        # This creates all Sprites of the new map
        # This is done AFTER any map change animation
        self.load_limits(level_id)
        self.load_warps(level_id, WARP_WARPS)
        self.load_warps(level_id, WARP_BOMB)
        self.load_warps(level_id, WARP_FLAME)
        self.load_doors(level_id)
        self.load_items(level_id)
        self.load_enemies(level_id)
        self.load_shop(level_id)
        self.dead_monsters_event_played = False

    def create_transition_surface(self):
        # Only Overworld and Dungeon maps will have warp tiles to border scroll
        # No loop from max right to max left as if the world was a sphere
        next_floor_x = 0
        next_floor_y = 0
        current_floor_x = 0
        current_floor_y = 0
        if self.in_map_transition == MAP_TRANSITION_UP:
            if LEVEL_PREFIX_LABEL in self.current_map:
                next_level_id = int(self.current_map_screen) - NB_MAPS_PER_ROW[OVERWORLD_LABEL]
            else:
                next_level_id = int(self.current_map_screen) - NB_MAPS_PER_ROW[DUNGEON_LABEL]
            self.transition_surface = pygame.Surface(
                (self.floor_rect.width, 2 * self.floor_rect.height))
            current_floor_y = self.floor_rect.height
        elif self.in_map_transition == MAP_TRANSITION_RIGHT:
            next_level_id = int(self.current_map_screen) + 1
            self.transition_surface = pygame.Surface(
                (2 * self.floor_rect.width, self.floor_rect.height))
            next_floor_x = self.floor_rect.width
        elif self.in_map_transition == MAP_TRANSITION_DOWN:
            if LEVEL_PREFIX_LABEL in self.current_map:
                next_level_id = int(self.current_map_screen) + NB_MAPS_PER_ROW[OVERWORLD_LABEL]
            else:
                next_level_id = int(self.current_map_screen) + NB_MAPS_PER_ROW[DUNGEON_LABEL]
            self.transition_surface = pygame.Surface(
                (self.floor_rect.width, 2 * self.floor_rect.height))
            next_floor_y = self.floor_rect.height
        elif self.in_map_transition == MAP_TRANSITION_LEFT:
            next_level_id = int(self.current_map_screen) - 1
            self.transition_surface = pygame.Surface(
                (2 * self.floor_rect.width, self.floor_rect.height))
            current_floor_x = self.floor_rect.width
        else:
            # Undefined warp transition, abort
            return

        next_floor = pygame.image.load(f'{LEVELS_PATH}{self.current_map}{next_level_id}{GRAPHICS_EXTENSION}').convert()
        self.transition_surface.blit(next_floor, (next_floor_x, next_floor_y))
        self.transition_surface.blit(self.floor_surface, (current_floor_x, current_floor_y))
        self.next_map_screen = next_level_id

    def change_map(self, change_id):
        if change_id >= 0:
            self.map_scroll_animation_counter = 0
            for warp in self.warp_sprites:
                warp.kill()
            for secret_flame in self.secret_flame_sprites:
                secret_flame.kill()
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
            for door in self.door_sprites:
                door.kill()
            if self.player.ladder_in_use:
                self.player.ladder_in_use = False
                self.player.ladder.kill()
                self.player.ladder = None

            # change_id 0 -> 3 is a side scrolling map change, respectively Up/Right/Down/Left
            # change_id > 3 is a stairs map change, with sound and a completely different map
            if DUNGEON_PREFIX_LABEL in self.current_map:
                new_state = STATE_WARPING_DUNGEON
            else:
                new_state = STATE_WARPING
            match change_id:
                case 0:
                    # Up
                    self.in_map_transition = MAP_TRANSITION_UP
                    self.create_transition_surface()
                    self.player.set_state(new_state)
                    # Animate slide - will be done in update
                case 1:
                    # Right
                    self.in_map_transition = MAP_TRANSITION_RIGHT
                    self.create_transition_surface()
                    self.player.set_state(new_state)
                    # Animate slide - will be done in update
                case 2:
                    # Down
                    self.in_map_transition = MAP_TRANSITION_DOWN
                    self.create_transition_surface()
                    self.player.set_state(new_state)
                    # Animate slide - will be done in update
                case 3:
                    # Left
                    self.in_map_transition = MAP_TRANSITION_LEFT
                    self.create_transition_surface()
                    self.player.set_state(new_state)
                    # Animate slide - will be done in update
                case _:
                    if change_id - 4 < len(UNDERWORLD_STAIRS):
                        if UNDERWORLD_STAIRS[change_id - 4][STAIRS_LABEL]:
                            self.in_map_transition = MAP_TRANSITION_STAIRS
                            self.player.set_state(STATE_STAIRS)
                            self.stairs_animation_starting_time = pygame.time.get_ticks()
                        else:
                            self.in_map_transition = MAP_TRANSITION_SILENT

                        self.next_map = UNDERWORLD_STAIRS[change_id - 4][MAP_LABEL]
                        self.next_map_screen = UNDERWORLD_STAIRS[change_id - 4][SCREEN_LABEL]
                        self.player_new_position = UNDERWORLD_STAIRS[change_id - 4][PLAYER_POS_LABEL]

    def animate_map_transition(self):
        self.map_scroll_animation_counter += 1
        x_fixed_offset = self.floor_rect.width / MAP_SCROLL_FRAMES_COUNT
        y_fixed_offset = self.floor_rect.height / MAP_SCROLL_FRAMES_COUNT
        x_offset = x_fixed_offset * self.map_scroll_animation_counter
        y_offset = y_fixed_offset * self.map_scroll_animation_counter

        if self.in_map_transition == MAP_TRANSITION_UP:
            self.display_surface.blit(self.transition_surface, (0, HUD_OFFSET - self.floor_rect.height + y_offset))
            self.draw_hud()
            self.player.define_warping_position(0, y_offset, self.current_map)
        elif self.in_map_transition == MAP_TRANSITION_RIGHT:
            self.display_surface.blit(self.transition_surface, (-x_offset, HUD_OFFSET))
            self.player.define_warping_position(-x_offset, 0, self.current_map)
        elif self.in_map_transition == MAP_TRANSITION_DOWN:
            self.display_surface.blit(self.transition_surface, (0, HUD_OFFSET - y_offset))
            self.draw_hud()
            self.player.define_warping_position(0, -y_offset, self.current_map)
        elif self.in_map_transition == MAP_TRANSITION_LEFT:
            self.display_surface.blit(self.transition_surface, (x_offset - self.floor_rect.width, HUD_OFFSET))
            self.player.define_warping_position(x_offset, 0, self.current_map)

    def palette_shift_floor(self, palette_in, palette_out, color_level):
        if len(palette_in) != len(palette_out[color_level]):
            raise ValueError(INCOMPATIBLE_PALETTES)
        for i in range(len(palette_in)):
            img_copy = self.floor_surface.copy()
            img_copy.fill(palette_out[color_level][i])
            self.floor_surface.set_colorkey(palette_in[i])
            img_copy.blit(self.floor_surface, (0, 0))
            self.floor_surface = img_copy

    def victory(self):
        self.draw_hud()
        self.draw_floor()
        current_time = pygame.time.get_ticks()
        # Kill every sprite
        for enemy in self.enemy_sprites:
            enemy.kill()
        for particle in self.particle_sprites:
            particle.kill()
        for npc in self.npc_sprites:
            npc.kill()
        for text in self.text_sprites:
            text.kill()
        for loot in self.lootable_items_sprites:
            loot.kill()
        for merch in self.purchasable_sprites:
            merch.kill()

        if self.victory_motion_index == 1 and self.victory_floor_index < len(WHITE_LIST):
            if self.victory_floor_switch_starting_time == 0:
                self.victory_floor_switch_starting_time = current_time
            palette_in = PALETTE_NATURAL_DUNGEON
            palette_out = PALETTE_TRIFORCE
            self.palette_shift_floor(palette_in, palette_out, WHITE_LIST[self.victory_floor_index])
            self.display_surface.blit(self.floor_surface, (0, HUD_OFFSET))
            if current_time - self.victory_floor_switch_starting_time >= self.victory_floor_switch_cooldown:
                self.victory_floor_switch_starting_time = 0
                self.victory_floor_index += 1
        elif self.victory_motion_index == 1 and self.victory_floor_index == len(WHITE_LIST):
            self.victory_motion_index += 1

        if self.victory_motion_index > 1:
            self.draw_floor(BLACK_LABEL)

        if self.victory_motion_index == 2:
            victory_message_pos_y = HUD_OFFSET + TILE_SIZE * 4
            TextBlock((self.visible_sprites,),
                      VICTORY_TEXT,
                      victory_message_pos_y)
            self.victory_motion_index += 1

    def death(self):
        self.draw_hud()
        self.draw_floor()
        current_time = pygame.time.get_ticks()

        # Kill every sprite
        for warp in self.warp_sprites:
            warp.kill()
        for obstacle in self.obstacle_sprites:
            obstacle.kill()
        for border in self.border_sprites:
            border.kill()
        for enemy in self.enemy_sprites:
            enemy.kill()
        for particle in self.particle_sprites:
            particle.kill()
        for npc in self.npc_sprites:
            npc.kill()
        for loot in self.lootable_items_sprites:
            loot.kill()
        for merch in self.purchasable_sprites:
            merch.kill()
        for npc in self.npc_sprites:
            npc.kill()
        for bomb_tile in self.secret_bomb_sprites:
            bomb_tile.kill()
        for flame_tile in self.secret_flame_sprites:
            flame_tile.kill()
        for door in self.door_sprites:
            door.kill()

        # Player is in a hurt state for death_hurt_cooldown, by default 3 cycles of the hurt animation
        if self.death_motion_index == 1:
            for text in self.text_sprites:
                text.kill()
            if self.death_hurt_starting_time == 0:
                self.death_hurt_starting_time = current_time
                self.player.set_state(STATE_DYING)
            elif current_time - self.death_hurt_starting_time >= self.death_hurt_cooldown:
                self.death_motion_index += 1
                self.game_over_sound.play()
                self.death_spin_starting_time = current_time

        # Set map img to red version
        if self.death_motion_index == 2:
            if LEVEL_PREFIX_LABEL in self.current_map:
                palette_in = PALETTE_NATURAL_LEVEL
            elif DUNGEON_PREFIX_LABEL in self.current_map:
                palette_in = PALETTE_NATURAL_DUNGEON
            else:
                palette_in = PALETTE_NATURAL_CAVE
            self.palette_shift_floor(palette_in, PALETTE_DEATH, RED_LIST[self.death_floor_index])
            self.display_surface.blit(self.floor_surface, (0, HUD_OFFSET))
            # Spin ! By default, 3 times (cf init of self.death_spin_cooldown)
            if current_time - self.death_spin_starting_time < self.death_spin_cooldown:
                self.player.set_state(STATE_SPINNING)
            else:
                self.death_motion_index += 1
                self.death_floor_index += 1
                self.player.set_state(STATE_IDLE_DOWN)

        # Switch map img to 3 darker shades successively
        if self.death_motion_index == 3 and self.death_floor_index < len(RED_LIST):
            if self.death_floor_switch_starting_time == 0:
                self.death_floor_switch_starting_time = current_time
            if LEVEL_PREFIX_LABEL in self.current_map:
                palette_in = PALETTE_NATURAL_LEVEL
            elif DUNGEON_PREFIX_LABEL in self.current_map:
                palette_in = PALETTE_NATURAL_DUNGEON
            else:
                palette_in = PALETTE_NATURAL_CAVE
            self.palette_shift_floor(palette_in, PALETTE_DEATH, RED_LIST[self.death_floor_index])
            self.display_surface.blit(self.floor_surface, (0, HUD_OFFSET))
            if current_time - self.death_floor_switch_starting_time >= self.death_floor_switch_cooldown:
                self.death_floor_switch_starting_time = 0
                self.death_floor_index += 1
        elif self.death_motion_index == 3 and self.death_floor_index == len(RED_LIST):
            self.death_motion_index += 1

        # No more floor, just black
        if self.death_motion_index > 3:
            self.draw_floor(BLACK_LABEL)

        # Put player in gray state for animation
        if self.death_motion_index == 4:
            if self.death_gray_starting_time == 0:
                self.death_gray_starting_time = current_time
                self.player.set_state(STATE_GRAY)
            if current_time - self.death_gray_starting_time >= self.death_gray_cooldown:
                self.death_motion_index += 1

        # Put player in despawn state for animation
        if self.death_motion_index == 5:
            if self.death_despawn_starting_time == 0:
                self.death_despawn_starting_time = current_time
                self.player.set_state(STATE_DESPAWN)
            if current_time - self.death_despawn_starting_time >= self.death_despawn_cooldown:
                self.death_motion_index += 1

        # Kill player sprite
        if self.death_motion_index == 6:
            self.player.kill()
            self.death_motion_index += 1

        # Print GAME OVER in middle of screen until key is pressed to exit game
        if self.death_motion_index == 7:
            game_over_message_pos_y = (SCREEN_HEIGHT // 2) + (HUD_OFFSET // 2) - (TILE_SIZE // 2)
            TextBlock((self.visible_sprites, self.text_sprites),
                      GAME_OVER_TEXT,
                      game_over_message_pos_y)
            self.death_motion_index += 1

    def is_menu_key_pressed_out_of_menu(self, keys):
        if is_menu_key_pressed(keys) and not self.in_menu:
            return True
        return False

    def is_menu_key_pressed_in_menu(self, keys):
        if is_menu_key_pressed(keys) and self.in_menu:
            return True
        return False

    def is_right_key_pressed_in_menu_with_item(self, keys):
        if is_right_key_pressed(keys) and self.in_menu and self.current_selected_item != NONE_LABEL:
            return True
        return False

    def is_left_key_pressed_in_menu_with_item(self, keys):
        if is_left_key_pressed(keys) and self.in_menu and self.current_selected_item != NONE_LABEL:
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

    def handle_input(self, keys):
        if (not self.player.isDead
                and not self.in_menu
                and not self.in_map_transition):
            self.player.handle_input(keys)
        current_time = pygame.time.get_ticks()
        if current_time - self.key_pressed_start_timer >= self.key_pressed_cooldown:
            self.key_pressed_start_timer = current_time

            # Toggle pause menu on/off
            if (self.is_menu_key_pressed_out_of_menu(keys)
                    and not self.player.isDead
                    and not self.player.is_winning):
                self.in_menu = True
                self.current_selected_item = self.player.itemB
                self.draw_selector()
            elif (self.is_menu_key_pressed_in_menu(keys)
                  and not self.player.isDead
                    and not self.player.is_winning):
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
            elif (is_suicide_key_pressed(keys)
                  and not self.in_menu
                  and not self.player.isDead):
                self.player.health = 0
            elif self.death_motion_index == 8 and is_continue_key_pressed(keys):
                self.continue_init()
            elif self.death_motion_index == 8 and is_exit_key_pressed(keys) != 0:
                self.death_played = True
            elif self.victory_motion_index == 3 and len(keys) != 0:
                self.victory_played = True

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
                    Rupee(pos, (self.visible_sprites, self.particle_sprites), rupee_amount)
                case 1 | 7:
                    CBomb(pos, (self.visible_sprites, self.particle_sprites))
                case 3:
                    Fairy(pos, (self.visible_sprites, self.particle_sprites), self.border_sprites)
                case 5 | 6 | 9:
                    Heart(pos, (self.visible_sprites, self.particle_sprites))

    def player_pick_up(self, item_label, amount=0):
        if item_label in ITEM_PICKUP_ANIMATION.keys():
            x_offset = 0 + self.player.direction_vector[0] * self.player.speed
            y_offset = - TILE_SIZE * 2 + self.player.direction_vector[1] * self.player.speed
            if item_label == HEARTRECEPTACLE_LABEL:
                item_image = tileset.CONSUMABLES_TILE_SET.get_sprite_image(HEARTRECEPTACLE_FRAME_ID)
                x_offset += 1
                y_offset += 4
            elif item_label == WOOD_SWORD_LABEL:
                item_image = tileset.ITEMS_TILE_SET.get_sprite_image(WOOD_SWORD_FRAME_ID)
                x_offset -= 12
            elif item_label == CANDLE_LABEL:
                item_image = tileset.ITEMS_TILE_SET.get_sprite_image(RED_CANDLE_FRAME_ID)
                x_offset -= 12
            elif item_label == BOOMERANG_LABEL:
                item_image = tileset.ITEMS_TILE_SET.get_sprite_image(BOOMERANG_FRAME_ID)
                x_offset -= 12
                y_offset += 10
            elif item_label == LADDER_LABEL:
                item_image = tileset.ITEMS_TILE_SET.get_sprite_image(LADDER_FRAME_ID)
                x_offset += 0
            else:
                # Item not implemented yet ? abort
                return

            self.player.add_item(item_label)
            item_pos = (self.player.rect.left + x_offset, self.player.rect.top + y_offset)
            self.item_picked_up = Tile(item_pos, (self.visible_sprites,), item_image)
        else:
            if (item_label == HEART_LABEL
                    or item_label == FAIRY_LABEL):
                self.player.heal(amount)
            elif item_label == RUPEE_LABEL:
                self.player.add_money(amount)
            elif item_label == BOMB_LABEL:
                self.player.add_bombs(amount)
            elif item_label == KEY_LABEL:
                self.player.add_keys(amount)
            else:
                # Item not implemented yet ? abort
                return

    def map_kill_event_done(self):
        self.event_cleared_sound.play()
        level_id = str(self.current_map) + str(self.current_map_screen)
        event_label = MONSTER_KILL_EVENT[level_id]
        item_pos = (SCREEN_WIDTH // 2 - TILE_SIZE, (SCREEN_HEIGHT + HUD_OFFSET) // 2 - TILE_SIZE)
        if event_label == BOMB_LABEL:
            CBomb(item_pos,
                  (self.visible_sprites, self.particle_sprites),
                  True)
        elif event_label == RUPEE_LABEL:
            Rupee(item_pos,
                  (self.visible_sprites, self.particle_sprites),
                  DUNGEON_RUPEE_AMOUNT,
                  True)
        elif event_label == HEART_LABEL:
            Heart(item_pos,
                  (self.visible_sprites, self.particle_sprites),
                  True)
        elif event_label == KEY_LABEL:
            Key(item_pos,
                (self.visible_sprites, self.particle_sprites),
                level_id,
                True)
        elif event_label == HEARTRECEPTACLE_LABEL:
            HeartReceptacle(item_pos,
                            (self.visible_sprites, self.particle_sprites),
                            level_id,
                            True)
        elif event_label == BOOMERANG_LABEL:
            Boomerang(item_pos,
                      (self.visible_sprites, self.lootable_items_sprites),
                      level_id,
                      True)
        elif event_label == OPEN_DOORS_LABEL:
            for door in self.door_sprites:
                if door.type == DOOR_EVENT_LABEL:
                    door.open()
        self.dead_monsters_event_played = True

    def pick_up_triforce(self):
        # Put the Triforce in the hands of the Player
        self.player.set_position((SCREEN_WIDTH // 2 - TILE_SIZE, SCREEN_HEIGHT // 2 + HUD_OFFSET // 2 - TILE_SIZE))
        y_offset = - TILE_SIZE * 2 + self.player.direction_vector[1] * self.player.speed
        item_image = tileset.ITEMS_TILE_SET.get_sprite_image(TRIFORCE_FRAME_ID)
        y_offset += 2
        item_pos = (self.player.rect.left, self.player.rect.top + y_offset)
        self.item_picked_up = Tile(item_pos, (self.visible_sprites,), item_image)
        self.player.set_state(STATE_TRIFORCE)
        self.triforce_sound.play()

    def continue_init(self):
        for text in self.text_sprites:
            text.kill()
        if self.current_map == OVERWORLD_STARTING_MAP:
            self.current_map = OVERWORLD_STARTING_MAP
            self.current_map_screen = OVERWORLD_STARTING_SCREEN
            self.create_map(OVERWORLD_STARTING_MAP + OVERWORLD_STARTING_SCREEN)
            self.overworld_background_theme.play(loops=-1)
        else:
            self.current_map = DUNGEON_STARTING_MAP
            self.current_map_screen = DUNGEON_STARTING_SCREEN
            self.create_map(DUNGEON_STARTING_MAP + DUNGEON_STARTING_SCREEN)
            self.dungeon_background_theme.play(loops=-1)
        self.player.revive(self.current_map)
        self.death_motion_index = 0
        self.death_floor_index = 0
        self.death_hurt_starting_time = 0
        self.death_floor_switch_starting_time = 0
        self.death_despawn_starting_time = 0

    def run(self):
        for monster in self.enemy_sprites:
            if monster.isDead and monster.deathPlayed:
                # Delete monsters that have played their death animation
                self.drop_loot(monster.rect.topleft)
                monster.kill()
                self.monsters_killed_in_the_room += 1
            elif self.in_menu:
                # Reset attack cooldown timer until game is resumed
                monster.attack_starting_time = pygame.time.get_ticks()

        if self.item_picked_up is not None and PICKUP_PREFIX not in self.player.state:
            self.item_picked_up.kill()
            self.item_picked_up = None

        if not self.player.isDead:
            self.draw_hud()
            # Put the player on top of all other visible sprites
            self.visible_sprites.remove(self.player)
            self.visible_sprites.add(self.player)
            # Update and draw the game
            if self.player.is_winning:
                if self.victory_motion_index == 0:
                    self.victory_motion_index = 1
                    self.dungeon_background_theme.stop()
                self.victory()
                if self.victory_played:
                    # Close game
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif not self.in_menu:
                self.draw_floor()
            # Update and draw the pause menu
            else:
                self.draw_menu()

        elif not self.death_played:
            # Play death & game over animation
            if self.death_motion_index == 0:
                self.overworld_background_theme.stop()
                self.dungeon_background_theme.stop()
                self.death_motion_index = 1
            self.death()

        elif self.death_played:
            # Close game
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Sprites are updated until map transitions
        if self.in_map_transition is None:
            if not self.in_menu:
                if self.monsters_killed_in_the_room == self.enemies_spawned_in_the_room:
                    level_id = str(self.current_map) + str(self.current_map_screen)
                    DUNGEON_DECIMATION[level_id] = True
                    if(level_id in MONSTER_KILL_EVENT.keys()
                            and not self.dead_monsters_event_played):
                        self.map_kill_event_done()
                self.visible_sprites.update()
                self.warp_sprites.update()
            else:
                # While in menu, enemies sprites are not updated, thus "paused"
                self.menu_sprites.update()
        # During map transition, all existing sprite is paused, not being updated until the transition is over
        else:
            # Warp makes a scrolling transition of the screen level
            if MAP_TRANSITION_WARP in self.in_map_transition:
                # Delete the cave stairs sprite when transitioning screen
                for secret_bomb in self.secret_bomb_sprites:
                    secret_bomb.kill()
                if self.map_scroll_animation_counter <= MAP_SCROLL_FRAMES_COUNT:
                    self.animate_map_transition()
                else:
                    self.current_map_screen = self.next_map_screen
                    self.draw_floor()
                    self.create_map(self.current_map + str(self.current_map_screen))
                    self.player.set_state(STATE_IDLE)
                    self.player.set_position((self.player.warping_x, self.player.warping_y))
                    self.map_scroll_animation_counter = 0
                    self.in_map_transition = None
            # Other transitions (caves with stairs animation, or secret stairs with no animation)
            # Which, I know, is strange, but how the NES game operates from the player POV
            else:
                # Wait for the stairs animation (and sound) to be over with, if any
                if self.in_map_transition == MAP_TRANSITION_STAIRS:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.stairs_animation_starting_time >= self.stairs_animation_duration:
                        self.in_map_transition = MAP_TRANSITION_DONE

                # Generate new map's sprites (enemies, borders, ...), use appropriate music (if any), move the player
                else:
                    # Delete the cave stairs sprite when transitioning screen is done
                    for secret_bomb in self.secret_bomb_sprites:
                        secret_bomb.kill()

                    self.current_map = self.next_map
                    self.current_map_screen = self.next_map_screen
                    self.create_map(self.current_map + self.current_map_screen)
                    if LEVEL_PREFIX_LABEL in self.current_map:
                        self.overworld_background_theme.play(loops=-1)
                    else:
                        self.overworld_background_theme.stop()
                    # Play dungeon music if in dungeon
                    if DUNGEON_PREFIX_LABEL in self.current_map:
                        self.dungeon_background_theme.play(loops=-1)
                    else:
                        self.dungeon_background_theme.stop()
                    self.player.set_position(self.player_new_position)
                    self.next_map = None
                    self.next_map_screen = None
                    self.player_new_position = None
                    self.in_map_transition = None
            # Only visible sprites left at this point are the Player, and all the HUD sprites

            self.visible_sprites.update()
