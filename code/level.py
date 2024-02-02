import sys
import pygame
from settings import *
from support import *
from tileset import Tileset
from tileset import Tile
from player import Player
from Enemies import RedOctorock


# SHOULD PLAYER BE CREATED IN LEVEL ? HE SHOULD BE PASSED TO LEVELS AS THEY CHANGE
# How to remember dead mobs on other maps ? Respawn timers ?
# Should there be juste one level = MAP and then a camera system ?
# so much to think so much to do


class Level:
    def __init__(self):
        # set up variables
        self.player = None
        self.current_level = 'level0'
        self.death_played = False

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
        self.enemy_sprites = pygame.sprite.Group()
        self.money_amount_sprites = pygame.sprite.Group()
        self.keys_amount_sprites = pygame.sprite.Group()
        self.bombs_amount_sprites = pygame.sprite.Group()
        self.health_sprites = pygame.sprite.Group()

        # set up tile sets
        self.enemies_tile_set = Tileset('enemies')
        self.font_tile_set = Tileset('font')
        self.hud_tile_set = Tileset('hud')
        # self.items_tile_set = Tileset('items')
        # self.npcs_tile_set = Tileset('npcs')
        self.player_tile_set = Tileset('player')
        self.levels_tile_set = Tileset('levels')

        # sprite setup
        self.create_map()
        self.game_over_text = 'game over'
        self.game_over_message = self.draw_message(self.game_over_text, len(self.game_over_text), 1)
        self.game_over_message_pos = (
                (SCREEN_WIDTH // 2) - ((len(self.game_over_text) * TILE_SIZE) // 2),
                (SCREEN_HEIGHT // 2) + ((MENU_TILE_HEIGHT * TILE_SIZE) // 2) - (TILE_SIZE // 2)
        )

        # set up spin player timers
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

    def draw_hud(self):
        # draw HUD space
        self.menu_surface = pygame.image.load('../graphics/hud/hud_perma.png').convert()
        self.menu_rect = self.menu_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.menu_surface, (0, 0))
        # draw ... minimap ? for this, best would be level number represent position on map, 0 being top left
        self.draw_money()
        self.draw_keys()
        self.draw_bombs()
        # draw items B & A
        # draw hearts
        self.draw_hearts()

    def draw_money(self):
        if self.money_amount_sprites:
            for sprite in self.money_amount_sprites:
                sprite.kill()
        hundreds = self.player.money // 100
        tens = (self.player.money // 10) % 10
        units = self.player.money % 10
        Tile(MENU_MONEY_HUNDREDS_POSITION,
             [self.money_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(MENU_MONEY_TENS_POSITION,
             [self.money_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(tens))
        Tile(MENU_MONEY_UNITS_POSITION,
             [self.money_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(units))

    def draw_keys(self):
        if self.keys_amount_sprites:
            for sprite in self.keys_amount_sprites:
                sprite.kill()
        hundreds = self.player.keys // 100
        tens = (self.player.keys // 10) % 10
        units = self.player.keys % 10
        Tile(MENU_KEYS_HUNDREDS_POSITION,
             [self.keys_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(MENU_KEYS_TENS_POSITION,
             [self.keys_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(tens))
        Tile(MENU_KEYS_UNITS_POSITION,
             [self.keys_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(units))

    def draw_bombs(self):
        if self.bombs_amount_sprites:
            for sprite in self.bombs_amount_sprites:
                sprite.kill()
        hundreds = self.player.bombs // 100
        tens = (self.player.bombs // 10) % 10
        units = self.player.bombs % 10
        Tile(MENU_BOMBS_HUNDREDS_POSITION,
             [self.bombs_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(hundreds))
        Tile(MENU_BOMBS_TENS_POSITION,
             [self.bombs_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(tens))
        Tile(MENU_BOMBS_UNITS_POSITION,
             [self.bombs_amount_sprites, self.visible_sprites],
             self.font_tile_set.get_sprite_image(units))

    def draw_hearts(self):
        if self.health_sprites:
            for sprite in self.health_sprites:
                sprite.kill()
        nb_hearts = self.player.health // PLAYER_HEALTH_PER_HEART
        for heart_index in range(0, nb_hearts):
            heart_x = MENU_FIRST_HEART_POSITION_X + (heart_index % 8) * TILE_SIZE
            heart_y = MENU_FIRST_HEART_POSITION_Y - (heart_index // MENU_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 [self.health_sprites, self.visible_sprites],
                 self.hud_tile_set.get_sprite_image(MENU_FULL_HEART_FRAME_ID))
        if self.player.health % PLAYER_HEALTH_PER_HEART > 0:
            heart_x = MENU_FIRST_HEART_POSITION_X + (nb_hearts % 8) * TILE_SIZE
            heart_y = MENU_FIRST_HEART_POSITION_Y - (nb_hearts // MENU_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 [self.health_sprites, self.visible_sprites],
                 self.hud_tile_set.get_sprite_image(MENU_HALF_HEART_FRAME_ID))
            nb_hearts += 1
        for heart_index in range(nb_hearts, self.player.current_max_health // PLAYER_HEALTH_PER_HEART):
            heart_x = MENU_FIRST_HEART_POSITION_X + (heart_index % 8) * TILE_SIZE
            heart_y = MENU_FIRST_HEART_POSITION_Y - (heart_index // MENU_NB_HEARTS_PER_LINE) * TILE_SIZE
            Tile((heart_x, heart_y),
                 [self.health_sprites, self.visible_sprites],
                 self.hud_tile_set.get_sprite_image(MENU_EMPTY_HEART_FRAME_ID))

    def draw_floor(self, death_color=''):
        if death_color == 'black':
            self.floor_surface = pygame.image.load('../graphics/levels/black.png').convert()
        else:
            self.floor_surface = pygame.image.load(
                f'../graphics/levels/{self.current_level}{death_color}.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        self.display_surface.blit(self.floor_surface, (0, MENU_TILE_HEIGHT*TILE_SIZE))

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

    def load_limits(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Limits.csv')
        # draw lines of obstacles so no one gets into the menu or off the screen at the bottom
        nb_tiles_width = SCREEN_WIDTH//TILE_SIZE
        nb_tiles_height = SCREEN_HEIGHT//TILE_SIZE
        for col in range(0, nb_tiles_width):
            y_top = (MENU_TILE_HEIGHT-1)*TILE_SIZE
            y_bottom = SCREEN_HEIGHT
            Tile((col*TILE_SIZE, y_top), self.obstacle_sprites)
            Tile((col*TILE_SIZE, y_bottom), self.obstacle_sprites)
        # draw lines of obstacles so no one gets out of the sides of the screen
        for row in range(MENU_TILE_HEIGHT, nb_tiles_height):
            x_left = - TILE_SIZE
            x_right = SCREEN_WIDTH
            Tile((x_left, row*TILE_SIZE), self.obstacle_sprites)
            Tile((x_right, row*TILE_SIZE), self.obstacle_sprites)
        # draw obstacles inside the level layout
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + MENU_TILE_HEIGHT * TILE_SIZE  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    Tile((x, y), self.obstacle_sprites)

    def load_enemies(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Enemies.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + MENU_TILE_HEIGHT * TILE_SIZE  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id == 4:
                    RedOctorock((x, y),
                                [self.visible_sprites, self.enemy_sprites],
                                self.obstacle_sprites,
                                self.enemies_tile_set)

    def load_player(self):
        layout = import_csv_layout(f'../map/{self.current_level}_Player.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE + MENU_TILE_HEIGHT * TILE_SIZE  # skipping menu tiles at the top of screen
                sprite_id = int(col)
                if sprite_id != -1:
                    self.player = Player((x, y),
                                         self.visible_sprites,
                                         self.obstacle_sprites,
                                         self.enemy_sprites,
                                         self.player_tile_set)

    def create_map(self):
        # later, will need to handle warps on their own tile set, with ID = level number & pos or something
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
        # kill every enemy sprite
        if self.death_motion_index == 1:
            for sprite in self.enemy_sprites:
                sprite.kill()
            self.death_motion_index += 1

        # call player.hurt_animation(3 seconds)
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

        # call player.beGray()
        if self.death_motion_index == 8:
            if self.death_gray_starting_time == 0:
                self.death_gray_starting_time = pygame.time.get_ticks()
                self.player.set_player_death_state('gray')
            if pygame.time.get_ticks() - self.death_gray_starting_time >= self.death_gray_cooldown:
                self.death_motion_index += 1

        # call player.animate_despawn()
        if self.death_motion_index == 9:
            if self.death_despawn_starting_time == 0:
                self.death_despawn_starting_time = pygame.time.get_ticks()
                self.player.set_player_death_state('despawn')
            if pygame.time.get_ticks() - self.death_despawn_starting_time >= self.death_despawn_cooldown:
                self.death_motion_index += 1

        # kill player sprite
        if self.death_motion_index == 10:
            self.player.kill()
            self.death_motion_index += 1

        # print GAME OVER in middle of screen until key is pressed to exit game
        if self.death_motion_index == 11:
            self.display_surface.blit(self.game_over_message, self.game_over_message_pos)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.death_played = True

    def run(self):
        if not self.player.isDead:
            # update and draw the game
            self.draw_hud()
            self.draw_floor()
        elif not self.death_played:
            # play death & game over animation
            if self.death_motion_index == 0:
                self.death_motion_index = 1
            self.death()
        elif self.death_played:
            # close game
            pygame.quit()
            sys.exit()

        self.visible_sprites.update()
