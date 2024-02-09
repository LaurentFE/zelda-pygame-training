import sys
import pygame
import random
from settings import *
from support import *
from tileset import Tileset
from tileset import Tile
from player import Player
from enemies import RedOctorock
from particles import Heart, Rupee, CBomb, Fairy


class Level:
    def __init__(self):
        # set up variables
        self.player = None
        self.current_level = 'level0'
        self.death_played = False
        self.in_menu = False
        self.kill_count = 0

        # set up display surface
        self.display_surface = pygame.display.get_surface()
        self.floor_surface = None
        self.floor_rect = None
        self.menu_surface = None
        self.menu_rect = None
        self.game_over_message = None

        # set up group sprites
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

        self.equipped_item_a_sprite = None
        self.equipped_item_b_sprite = None

        # set up tile sets
        self.enemies_tile_set = Tileset('enemies')
        self.font_tile_set = Tileset('font')
        self.hud_tile_set = Tileset('hud')
        self.items_tile_set = Tileset('items')
        # self.npcs_tile_set = Tileset('npcs')
        self.player_tile_set = Tileset('player')
        self.levels_tile_set = Tileset('levels')
        self.particle_tile_set = Tileset('particles')
        self.consumables_tile_set = Tileset('consumables')

        # sprite setup
        self.create_map()
        self.game_over_text = 'game over'
        self.game_over_message = self.draw_message(self.game_over_text, len(self.game_over_text), 1)
        self.game_over_message_pos = (
                (SCREEN_WIDTH // 2) - ((len(self.game_over_text) * TILE_SIZE) // 2),
                (SCREEN_HEIGHT // 2) + ((HUD_TILE_HEIGHT * TILE_SIZE) // 2) - (TILE_SIZE // 2)
        )

        # set up spin player timers
        self.key_pressed_start_timer = 0
        self.key_pressed_cooldown = LEVEL_KEY_PRESSED_COOLDOWN
        self.spin_start_timer = 0
        self.full_spin_duration = PLAYER_DEATH_SPIN_DURATION
        self.spin_status = 'todo'
        self.total_spin_amount = PLAYER_DEATH_SPIN_AMOUNT
        self.current_spin_amount = 0
        self.death_motion_index = 0
        self.death_floor_switch_cooldown = MAP_DEATH_FADE_COOLDOWN
        self.death_floor_switch_starting_time = 0
        self.death_gray_cooldown = PLAYER_GRAY_COOLDOWN
        self.death_gray_starting_time = 0
        self.death_despawn_cooldown = PLAYER_DEATH_ANIMATION_COOLDOWN * PLAYER_DEATH_FRAMES
        self.death_despawn_starting_time = 0
        self.death_hurt_cooldown = PLAYER_DEATH_HURT_COOLDOWN
        self.death_hurt_starting_time = 0

    def draw_menu(self):
        # Draw background
        self.floor_surface = pygame.image.load('../graphics/hud/pause_menu.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, 0))

        # Draw owned items
        self.draw_items()
        # Do I create item selector here, based on player action B ?
        # Item selector defines item B. It can't go on nonexistent items, jumps to the next available
        # Selected item should be drawn by selector hovered item (128, 96)

        self.draw_triforce()

    def draw_items(self):
        # Passive Items
        if self.player.has_raft:
            Tile((256, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(RAFT_FRAME_ID))
        # Magic Tome - not implemented
        # if self.player.has_magic_tome:
        #     Tile((296, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(MAGIC_TOME_FRAME_ID))
        # Blue / Red ring - Not implemented
        # if self.player.has_ring:
        #     Tile((320, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(RED_RING_FRAME_ID))
        if self.player.has_ladder:
            Tile((352, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(LADDER_FRAME_ID))
        # Magical Key - Not implemented
        # if self.player.has_magical_key:
        #     Tile((386, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(MAGIC_KEY_FRAME_ID))
        # Power Bracelet - Not implemented
        # if self.player.has_raft:
        #     Tile((408, 48), [self.menu_sprites], self.items_tile_set.get_sprite_image(POWER_BRACELET_FRAME_ID))

        # Selectable items
        if self.player.has_boomerang:
            # Didn't implement red/blue boomerang system
            Tile((256, 96), [self.menu_sprites], self.items_tile_set.get_sprite_image(BOOMERANG_FRAME_ID))
        if self.player.bombs:
            Tile((304, 96), [self.menu_sprites], self.items_tile_set.get_sprite_image(BOMB_FRAME_ID))
        # Bow & red/blue Arrow - Not Implemented
        # if self.player.has_bow:
        #     Tile((352, 96), [self.menu_sprites], self.items_tile_set.get_sprite_image(BOW_ARROW_FRAME_ID))
        if self.player.has_candle:
            # Didn't implement red/blue candle system
            Tile((400, 96), [self.menu_sprites], self.items_tile_set.get_sprite_image(RED_CANDLE_FRAME_ID))
        # Recorder - Not Implemented
        # if self.player.has_recorder:
        #     Tile((256, 128), [self.menu_sprites], self.items_tile_set.get_sprite_image(RECORDER_FRAME_ID))
        # Meat - Not Implemented
        # if self.player.has_meat:
        #     Tile((304, 128), [self.menu_sprites], self.items_tile_set.get_sprite_image(MEAT_FRAME_ID))
        # Medicine - Not Implemented
        # if self.player.has_medicine:
        #     Tile((352, 128), [self.menu_sprites], self.items_tile_set.get_sprite_image(MEDICINE_FRAME_ID))
        # Magical Rod - Not Implemented
        # if self.player.has_magical_rod:
        #     Tile((400, 128), [self.menu_sprites], self.items_tile_set.get_sprite_image(MAGICAL_ROD_FRAME_ID))

    def draw_triforce(self):
        # If I ever implement a dungeon level with a TriForce fragment as a reward, I should have a flag for every
        # fragment, and use them to both draw in the menu, and use them to keep track of cleared dungeons
        # Until I do this, the empty triforce will be drawn on the background of the menu directly
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

        # Draw ... minimap ? for this, best would be level number represent position on map, 0 being top left
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
        if death_color == 'black':
            self.floor_surface = pygame.image.load('../graphics/levels/black.png').convert()
        else:
            self.floor_surface = pygame.image.load(
                f'../graphics/levels/{self.current_level}{death_color}.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, HUD_TILE_HEIGHT*TILE_SIZE))

    def draw_message(self, text: str, width, height):
        pixel_text = []
        text = text.lower()

        for i in range(len(text)):
            char = text[i]
            char_id = FONT_CHARS.index(char)
            pixel_text.append(self.font_tile_set.get_sprite_image(char_id))

        # Arrange array in the amount of rows & columns desired
        message_surface = pygame.surface.Surface((width * TILE_SIZE, height * TILE_SIZE))
        for i in range(height):
            for j in range(width):
                message_surface.blit(pixel_text[i+j], (j * TILE_SIZE, i * TILE_SIZE))
        return message_surface

    def draw_item_a(self):
        if self.in_menu:
            sprite_groups = [self.menu_sprites]
        else:
            sprite_groups = [self.visible_sprites]

        item_a_pos = (self.menu_rect.x + 296,
                      self.menu_rect.y + 48)

        item_a_id = None
        if self.player.has_sword_wood:
            item_a_id = WOOD_SWORD_ID

        if self.equipped_item_a_sprite:
            self.equipped_item_a_sprite.kill()

        if item_a_id is not None:
            self.equipped_item_a_sprite = Tile(item_a_pos,
                                               sprite_groups,
                                               self.items_tile_set.get_sprite_image(item_a_id))

    def draw_item_b(self):
        if self.in_menu:
            sprite_groups = [self.menu_sprites]
        else:
            sprite_groups = [self.visible_sprites]

        item_b_pos = (self.menu_rect.x + 248,
                      self.menu_rect.y + 48)

        item_frame_id = None
        # Get selected item B id

        if self.equipped_item_b_sprite:
            self.equipped_item_b_sprite.kill()

        if item_frame_id is not None:
            self.equipped_item_b_sprite = Tile(item_b_pos,
                                               sprite_groups,
                                               self.items_tile_set.get_sprite_image(item_frame_id))

    def load_limits(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Limits.csv')
        # Draw lines of obstacles so no one gets into the menu or off the screen at the bottom
        nb_tiles_width = SCREEN_WIDTH//TILE_SIZE
        nb_tiles_height = SCREEN_HEIGHT//TILE_SIZE
        for col in range(0, nb_tiles_width):
            y_top = (HUD_TILE_HEIGHT-1)*TILE_SIZE
            y_bottom = SCREEN_HEIGHT
            Tile((col*TILE_SIZE, y_top), [self.obstacle_sprites, self.border_sprites])
            Tile((col*TILE_SIZE, y_bottom), [self.obstacle_sprites, self.border_sprites])
        # Draw lines of obstacles so no one gets out of the sides of the screen
        for row in range(HUD_TILE_HEIGHT, nb_tiles_height):
            x_left = - TILE_SIZE
            x_right = SCREEN_WIDTH
            Tile((x_left, row*TILE_SIZE), [self.obstacle_sprites])
            Tile((x_right, row*TILE_SIZE), [self.obstacle_sprites])
        # Draw obstacles inside the level layout
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    Tile((x, y), [self.obstacle_sprites])

    def load_enemies(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Enemies.csv')
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

    def load_player(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Player.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + HUD_TILE_HEIGHT * TILE_SIZE  # Skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    self.player = Player((x, y),
                                         self.visible_sprites,
                                         self.obstacle_sprites,
                                         self.enemy_sprites,
                                         self.visible_sprites,
                                         self.particle_sprites,
                                         self.player_tile_set,
                                         self.particle_tile_set)

    def create_map(self):
        # Lacks a proper level management, with screen changes for the over-world, and access to underworld sections
        self.load_limits()
        self.load_enemies()
        self.load_player()

    def spin_player(self):
        self.player.direction_vector = (0, 0)
        self.player.state = 'walking'
        self.player.direction_label = 'down'
        elapsed_spin_time = pygame.time.get_ticks() - self.spin_start_timer
        if elapsed_spin_time < self.full_spin_duration * 0.25:
            self.player.direction_label = 'right'
        elif elapsed_spin_time < self.full_spin_duration * 0.5:
            self.player.direction_label = 'up'
        elif elapsed_spin_time < self.full_spin_duration * 0.75:
            self.player.direction_label = 'left'
        elif elapsed_spin_time >= self.full_spin_duration:
            self.spin_status = 'done'

    def death(self):
        self.draw_hud()
        self.draw_floor()
        # Kill every enemy sprite and every particle sprite
        if self.death_motion_index == 1:
            for enemy in self.enemy_sprites:
                enemy.kill()
            for particle in self.particle_sprites:
                particle.kill()
            self.death_motion_index += 1

        # Call player.hurt_animation(3 seconds)
        if 1 <= self.death_motion_index <= 3:
            if self.death_hurt_starting_time == 0:
                self.death_hurt_starting_time = pygame.time.get_ticks()
                self.player.set_player_death_state('hurt')
            if pygame.time.get_ticks() - self.death_hurt_starting_time >= self.death_hurt_cooldown:
                self.death_motion_index += 1

        # Set map img to red version
        if self.death_motion_index == 4:
            self.draw_floor('red0')
            # Spin three times
            if self.current_spin_amount < self.total_spin_amount:
                if self.spin_status == 'todo':
                    self.spin_start_timer = pygame.time.get_ticks()
                    self.spin_status = 'doing'
                if self.spin_status == 'doing':
                    self.spin_player()
                if self.spin_status == 'done':
                    self.current_spin_amount += 1
                    self.spin_status = 'todo'
            if self.current_spin_amount >= self.total_spin_amount:
                self.death_motion_index += 1

        # Switch map img to 3 darker shades successively
        # Can be refactored (copied - pasted code with only index & map name changing)
        if self.death_motion_index == 5:
            if self.death_floor_switch_starting_time == 0:
                self.death_floor_switch_starting_time = pygame.time.get_ticks()
            self.draw_floor('red1')
            if pygame.time.get_ticks() - self.death_floor_switch_starting_time >= self.death_floor_switch_cooldown:
                self.death_floor_switch_starting_time = 0
                self.death_motion_index += 1
        if self.death_motion_index == 6:
            if self.death_floor_switch_starting_time == 0:
                self.death_floor_switch_starting_time = pygame.time.get_ticks()
            self.draw_floor('red2')
            if pygame.time.get_ticks() - self.death_floor_switch_starting_time >= self.death_floor_switch_cooldown:
                self.death_floor_switch_starting_time = 0
                self.death_motion_index += 1
        if self.death_motion_index == 7:
            if self.death_floor_switch_starting_time == 0:
                self.death_floor_switch_starting_time = pygame.time.get_ticks()
            self.draw_floor('red3')
            if pygame.time.get_ticks() - self.death_floor_switch_starting_time >= self.death_floor_switch_cooldown:
                self.death_floor_switch_starting_time = 0
                self.death_motion_index += 1

        # No more floor, just black
        if self.death_motion_index > 7:
            self.draw_floor('black')

        # Put player in gray state for animation
        if self.death_motion_index == 8:
            if self.death_gray_starting_time == 0:
                self.death_gray_starting_time = pygame.time.get_ticks()
                self.player.set_player_death_state('gray')
            if pygame.time.get_ticks() - self.death_gray_starting_time >= self.death_gray_cooldown:
                self.death_motion_index += 1

        # Put player in despawn state for animation
        if self.death_motion_index == 9:
            if self.death_despawn_starting_time == 0:
                self.death_despawn_starting_time = pygame.time.get_ticks()
                self.player.set_player_death_state('despawn')
            if pygame.time.get_ticks() - self.death_despawn_starting_time >= self.death_despawn_cooldown:
                self.death_motion_index += 1

        # Kill player sprite
        if self.death_motion_index == 10:
            self.player.kill()
            self.death_motion_index += 1

        # Print GAME OVER in middle of screen until key is pressed to exit game
        if self.death_motion_index == 11:
            self.display_surface.blit(self.game_over_message, self.game_over_message_pos)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.death_played = True

    def input(self):
        # Known issue : When key press is short, it is sometimes not registered and the menu doesn't open/close
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if current_time - self.key_pressed_start_timer >= self.key_pressed_cooldown:
            self.key_pressed_start_timer = current_time

            # Toggle pause menu on/off
            if keys[pygame.K_ESCAPE] and not self.in_menu:
                self.in_menu = True
            elif keys[pygame.K_ESCAPE] and self.in_menu:
                self.in_menu = False
                for sprite in self.menu_sprites:
                    sprite.kill()

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
                    Rupee(pos,
                          [self.visible_sprites, self.particle_sprites],
                          self.consumables_tile_set,
                          self.obstacle_sprites,
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
        if not self.player.isDead:
            # Update and draw the game
            if not self.in_menu:
                self.draw_hud()
                self.draw_floor()
            # Update and draw the pause menu
            else:
                self.draw_menu()
                self.draw_hud()
        elif not self.death_played:
            # Play death & game over animation
            if self.death_motion_index == 0:
                self.death_motion_index = 1
            self.death()
        elif self.death_played:
            # Close game
            pygame.quit()
            sys.exit()

        if not self.in_menu:
            self.visible_sprites.update()
        else:
            # While in menu, enemies sprites are not updated, thus "paused"
            self.menu_sprites.update()
