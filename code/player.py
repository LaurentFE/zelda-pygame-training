import pygame.mixer
import tileset

from settings import *
from inputs import *
from tile import Tile
from entities import Entity
from particles import PWoodenSword, Bomb, PBoomerang, Flame


# NOTE : Behaviour difference between original NES version, and mine :
#   HURT :
#       Original does 3 cycles of blinking. Blinks even while walking, can't walk during first cycle (I guess ?)
#       My version has 1 cycle of blinking, then invulnerability for 1.5 animation cycle
#           COULD add hurt animation for duration while walking and idling, lack sprites for now
#       Original pushback linked to Link's cumulative speed from walking in the same direction it seems
#       My version pushes back at the same speed Link moves normally
#       Original has no pushback if Link isn't moving when a monster runs into him
#       My version pushes Link back regardless of who initiates the collision
#       Original pushback has no fading effect
#       My version fades the pushback speed down, to stop at the same time as the animation
#
# NOTE : Behavior observed on NES videos :
#    ATTACK :
#       Original allows player to change direction of attack during animation (frame rate is lower though,
#         so "on cooldown" I guess)
#       My version : probably won't allow it, because player won't really 'attack' or 'cast', but most likely
#         'cast' every item, sword included, and I don't want to change directions in middle of candle for instance,
#         or of flute.
class Player(Entity):

    def __init__(self, pos,
                 groups,
                 obstacle_sprites,
                 enemy_sprites,
                 visible_sprites,
                 particle_sprites,
                 lootable_items_sprites,
                 border_sprites,
                 purchasable_sprites,
                 npc_sprites,
                 secret_flame_sprites,
                 secret_bomb_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites)

        self.enemy_sprites = enemy_sprites
        self.visible_sprites = visible_sprites
        self.particle_sprites = particle_sprites
        self.lootable_items_sprites = lootable_items_sprites
        self.border_sprites = border_sprites
        self.purchasable_sprites = purchasable_sprites
        self.npc_sprites = npc_sprites
        self.secret_flame_sprites = secret_flame_sprites
        self.secret_bomb_sprites = secret_bomb_sprites

        self.pickup_one_handed_animation = []
        self.pickup_two_handed_animation = []
        self.stairs_animation = []

        # Initialisation of the values used to load the different animations
        self.is_right_x_flipped = True
        self.walking_frames = PLAYER_WALKING_FRAMES
        self.walking_up_frame_id = PLAYER_WALKING_UP_FRAME_ID
        self.walking_down_frame_id = PLAYER_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = PLAYER_WALKING_RIGHT_FRAME_ID
        self.walking_right_frame_id = PLAYER_WALKING_RIGHT_FRAME_ID
        self.can_be_gray = True
        self.walking_down_gray_frame_id = PLAYER_GRAY_WALKING_DOWN_FRAME_ID
        self.action_frames = PLAYER_ACTION_FRAMES
        self.action_up_frame_id = PLAYER_ACTION_UP_FRAME_ID
        self.action_down_frame_id = PLAYER_ACTION_DOWN_FRAME_ID
        self.action_left_frame_id = PLAYER_ACTION_RIGHT_FRAME_ID
        self.action_right_frame_id = PLAYER_ACTION_RIGHT_FRAME_ID
        self.pickup_one_handed_frames = PLAYER_PICKUP_ONE_HANDED_FRAMES
        self.pickup_one_handed_frame_id = PLAYER_PICKUP_ONE_HANDED_FRAME_ID
        self.pickup_two_handed_frames = PLAYER_PICKUP_TWO_HANDED_FRAMES
        self.pickup_two_handed_frame_id = PLAYER_PICKUP_TWO_HANDED_FRAME_ID
        self.hurt_frames = PLAYER_HURT_FRAMES
        self.hurt_up_frame_id = PLAYER_HURT_UP_FRAME_ID
        self.hurt_down_frame_id = PLAYER_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = PLAYER_HURT_RIGHT_FRAME_ID
        self.hurt_right_frame_id = PLAYER_HURT_RIGHT_FRAME_ID
        self.despawn_frames = PLAYER_DEATH_FRAMES
        self.despawn_frame_id = PLAYER_DEATH_FRAME_ID
        self.stairs_frames = PLAYER_STAIRS_FRAMES
        self.stairs_frame_id = PLAYER_STAIRS_FRAME_ID
        self.load_animation_frames(tileset.PLAYER_TILE_SET)

        # Sounds
        self.shield_block_sound = pygame.mixer.Sound(SOUND_SHIELD_BLOCK)
        self.shield_block_sound.set_volume(0.5)
        self.player_hurt_sound = pygame.mixer.Sound(SOUND_PLAYER_HURT)
        self.player_hurt_sound.set_volume(0.1)
        self.rupee_acquired_sound = pygame.mixer.Sound(SOUND_RUPEE_ACQUIRED)
        self.rupee_acquired_sound.set_volume(0.3)
        self.rupees_acquired_sound = pygame.mixer.Sound(SOUND_RUPEES_ACQUIRED)
        self.rupees_acquired_sound.set_volume(0.3)
        self.key_acquired_sound = pygame.mixer.Sound(SOUND_SMALL_PICKUP)
        self.key_acquired_sound.set_volume(0.3)
        self.is_low_health = False
        self.low_health_sound = pygame.mixer.Sound(SOUND_LOW_HEALTH)
        self.low_health_sound.set_volume(0.3)
        self.despawn_sound = pygame.mixer.Sound(SOUND_PLAYER_DESPAWN)
        self.despawn_sound.set_volume(0.4)
        self.stairs_sound = pygame.mixer.Sound(SOUND_STAIRS)
        self.stairs_sound.set_volume(0.4)
        self.pick_up_sound = pygame.mixer.Sound(SOUND_PICKUP)
        self.pick_up_sound.set_volume(0.3)

        self.direction_label = DOWN_LABEL
        self.state = STATE_IDLE
        self.speed = 3

        self.pos = pos
        self.warping_x = 0
        self.warping_y = 0
        self.image = self.walking_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-PLAYER_HITBOX_X_DEFLATE, -PLAYER_HITBOX_Y_DEFLATE)
        self.hitbox.top = self.rect.top + PLAYER_HITBOX_Y_OFFSET
        self.hitbox.left = self.rect.left + PLAYER_HITBOX_X_OFFSET
        shield_x = SHIELD_DOWN_X + self.rect.left
        shield_y = SHIELD_DOWN_Y + self.rect.top
        self.shield_hitbox = pygame.Rect((shield_x, shield_y), (SHIELD_HORIZONTAL_WIDTH, SHIELD_HORIZONTAL_HEIGHT))

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = PLAYER_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_one_handed_animation_cooldown = PLAYER_PICKUP_ONE_HANDED_ANIMATION_COOLDOWN
        self.pickup_two_handed_animation_cooldown = PLAYER_PICKUP_TWO_HANDED_ANIMATION_COOLDOWN
        self.hurt_animation_cooldown = PLAYER_HURT_ANIMATION_COOLDOWN
        self.despawn_animation_cooldown = PLAYER_DEATH_ANIMATION_COOLDOWN
        self.stairs_animation_cooldown = PLAYER_STAIRS_ANIMATION_COOLDOWN
        # Time at which animation frame started
        self.walking_animation_starting_time = 0
        self.action_animation_starting_time = 0
        self.pickup_one_handed_animation_starting_time = 0
        self.pickup_two_handed_animation_starting_time = 0
        self.hurt_animation_starting_time = 0
        self.spin_animation_starting_time = 0
        self.despawn_animation_starting_time = 0
        self.stairs_animation_starting_time = 0
        # Index of animation being played
        self.walking_animation_frame_count = 0
        self.action_animation_frame_count = 0
        self.pickup_one_handed_animation_frame_count = 0
        self.pickup_two_handed_animation_frame_count = 0
        self.hurt_animation_frame_count = 0
        self.despawn_animation_frame_count = 0
        self.stairs_animation_frame_count = 0
        # Animation reset
        self.idle_time = 0

        # Current animation pointers
        self.current_animation_cooldown = 0
        self.current_animation_starting_time = 0
        self.current_animation_frame_count = 0
        self.current_animation_frames_nb = 0
        self.current_animation_list = []

        # Player actions cooldowns
        self.action_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_one_handed_cooldown = PLAYER_PICKUP_ONE_HANDED_COOLDOWN
        self.pickup_two_handed_cooldown = PLAYER_PICKUP_TWO_HANDED_COOLDOWN
        self.hurt_cooldown = PLAYER_HURT_FRAMES * self.hurt_animation_cooldown
        self.invulnerability_cooldown = 1.5 * self.hurt_cooldown
        self.action_starting_time = 0
        self.pickup_one_handed_starting_time = 0
        self.pickup_two_handed_starting_time = 0
        self.hurt_starting_time = 0

        self.action_a_particle = None
        self.action_b_particle = None

        # Player stats and items
        self.current_max_health = PLAYER_INITIAL_HEALTH
        self.health = int(self.current_max_health)
        self.invulnerable = False
        self.money = PLAYER_INITIAL_MONEY
        self.keys = PLAYER_INITIAL_KEY
        self.bombs = PLAYER_INITIAL_BOMB
        self.is_spinning = False
        self.isDead = False
        self.is_winning = False
        self.current_speed = self.speed

        # Items flags
        self.has_boomerang = PLAYER_INITIAL_HAS_BOOMERANG
        self.has_candle = PLAYER_INITIAL_HAS_RED_CANDLE
        self.has_bombs = PLAYER_INITIAL_HAS_BOMB
        self.has_ladder = PLAYER_INITIAL_HAS_LADDER
        self.has_wood_sword = PLAYER_INITIAL_HAS_WOOD_SWORD
        self.itemA = PLAYER_INITIAL_ITEM_A
        self.itemB = PLAYER_INITIAL_ITEM_B
        self.ladder_in_use = False
        self.ladder = None
        self.is_boomerang_thrown = False
        self.is_candle_lit = False

    def realign_shield(self):
        if self.direction_label == UP_LABEL:
            self.shield_hitbox.top = self.rect.top + SHIELD_UP_Y
            self.shield_hitbox.left = self.rect.left + SHIELD_UP_X
            self.shield_hitbox.height = SHIELD_HORIZONTAL_HEIGHT
            self.shield_hitbox.width = SHIELD_HORIZONTAL_WIDTH
        elif self.direction_label == DOWN_LABEL:
            self.shield_hitbox.top = self.rect.top + SHIELD_DOWN_Y
            self.shield_hitbox.left = self.rect.left + SHIELD_DOWN_X
            self.shield_hitbox.height = SHIELD_HORIZONTAL_HEIGHT
            self.shield_hitbox.width = SHIELD_HORIZONTAL_WIDTH
        elif self.direction_label == LEFT_LABEL:
            self.shield_hitbox.top = self.rect.top + SHIELD_LEFT_Y
            self.shield_hitbox.left = self.rect.left + SHIELD_LEFT_X
            self.shield_hitbox.height = SHIELD_VERTICAL_HEIGHT
            self.shield_hitbox.width = SHIELD_VERTICAL_WIDTH
        else:
            self.shield_hitbox.top = self.rect.top + SHIELD_RIGHT_Y
            self.shield_hitbox.left = self.rect.left + SHIELD_RIGHT_X
            self.shield_hitbox.height = SHIELD_VERTICAL_HEIGHT
            self.shield_hitbox.width = SHIELD_VERTICAL_WIDTH

    def load_pickup_one_handed_frames(self, player_tile_set):
        for i in range(self.pickup_one_handed_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.pickup_one_handed_animation.append(
                player_tile_set.get_sprite_image(self.pickup_one_handed_frame_id + tiles_offset))

    def load_pickup_two_handed_frames(self, player_tile_set):
        for i in range(self.pickup_two_handed_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.pickup_two_handed_animation.append(
                player_tile_set.get_sprite_image(self.pickup_two_handed_frame_id + tiles_offset))

    def load_stairs_frames(self, player_tile_set):
        for i in range(self.stairs_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.stairs_animation.append(player_tile_set.get_sprite_image(self.stairs_frame_id + tiles_offset))

    def load_animation_frames(self, player_tile_set):
        super().load_animation_frames(player_tile_set)
        self.load_pickup_one_handed_frames(player_tile_set)
        self.load_pickup_two_handed_frames(player_tile_set)
        self.load_stairs_frames(player_tile_set)

    def can_move(self):
        if self.state == STATE_WALKING or self.state == STATE_IDLE:
            return True
        return False

    def can_action(self):
        if (STATE_ACTION not in self.state
                and STATE_WARPING not in self.state
                and self.state != STATE_STAIRS
                and self.state != STATE_TRIFORCE):
            return True
        return False

    def handle_input(self, keys):
        if STATE_HURT not in self.state:
            self.direction_vector.x = 0
            self.direction_vector.y = 0
            if is_move_key_pressed(keys) and self.can_move():
                if is_up_key_pressed(keys):
                    self.direction_vector.y = -1
                    self.direction_label = UP_LABEL
                elif is_down_key_pressed(keys):
                    self.direction_vector.y = 1
                    self.direction_label = DOWN_LABEL
                if is_left_key_pressed(keys):
                    self.direction_vector.x = -1
                    self.direction_label = LEFT_LABEL
                elif is_right_key_pressed(keys):
                    self.direction_vector.x = 1
                    self.direction_label = RIGHT_LABEL
                if self.state != STATE_WALKING:
                    self.state = STATE_WALKING
                    self.walking_animation_starting_time = pygame.time.get_ticks()
                    self.idle_time = pygame.time.get_ticks()

            # ActionA input has prio over Move input
            # Can't move during sword use
            if is_action_a_key_pressed(keys) and self.can_action() and self.itemA != NONE_LABEL:
                # Define here all different item A weapons implemented
                if self.itemA == WOOD_SWORD_LABEL:
                    self.action_a_particle = PWoodenSword(self.rect.topleft,
                                                          self.direction_vector,
                                                          self.direction_label,
                                                          (self.visible_sprites, self.particle_sprites),
                                                          self.enemy_sprites,
                                                          self.particle_sprites)
                else:
                    # ItemA used not implemented, abort
                    return
                self.state = STATE_ACTION_A
                self.action_starting_time = pygame.time.get_ticks()
                self.direction_vector.x = 0
                self.direction_vector.y = 0

            # Can't move during item use
            if is_action_b_key_pressed(keys) and self.can_action() and self.itemB != NONE_LABEL:
                if self.itemB == BOOMERANG_LABEL and not self.is_boomerang_thrown:
                    PBoomerang(self.rect.topleft,
                               self.direction_vector,
                               self.direction_label,
                               (self.visible_sprites, self.particle_sprites),
                               self.enemy_sprites,
                               self.particle_sprites,
                               self.border_sprites,
                               self)
                    self.is_boomerang_thrown = True
                elif self.itemB == BOMB_LABEL:
                    if self.bombs > 0:
                        # Bombs are dropped and forgotten, won't get deleted upon timer but when they die by themselves
                        Bomb(self.rect.topleft,
                             self.direction_vector,
                             self.direction_label,
                             (self.visible_sprites, self.particle_sprites),
                             self.secret_bomb_sprites,)
                        self.bombs -= 1
                    else:
                        # Not enough bombs to operate, abort
                        return
                elif self.itemB == CANDLE_LABEL and not self.is_candle_lit:
                    Flame(self.rect.topleft,
                          self.direction_vector,
                          self.direction_label,
                          (self.visible_sprites, self.particle_sprites),
                          self.enemy_sprites,
                          self.secret_flame_sprites,
                          self)
                    self.is_candle_lit = True
                else:
                    # ItemB used not implemented, abort
                    return

                self.state = STATE_ACTION_B
                self.action_starting_time = pygame.time.get_ticks()
                self.direction_vector.x = 0
                self.direction_vector.y = 0

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if STATE_ACTION in self.state:
            if current_time - self.action_starting_time >= self.action_cooldown:
                if self.state == STATE_ACTION_A:
                    self.action_a_particle.kill()
                    self.action_a_particle = None
                elif self.state == STATE_ACTION_B and self.action_b_particle is not None:
                    self.action_b_particle.kill()
                    self.action_b_particle = None
                self.state = STATE_IDLE
        elif self.state == STATE_WALKING:
            if current_time - self.idle_time >= self.walking_animation_cooldown:
                self.state = STATE_IDLE
        elif self.state == ONE_HANDED:
            if current_time - self.pickup_one_handed_starting_time >= self.pickup_one_handed_cooldown:
                self.state = STATE_IDLE
                self.invulnerable = False
        elif self.state == TWO_HANDED:
            if current_time - self.pickup_two_handed_starting_time >= self.pickup_two_handed_cooldown:
                self.state = STATE_IDLE
                self.invulnerable = False
        elif STATE_HURT in self.state:
            if self.action_a_particle is not None:
                self.action_a_particle.kill()
                self.action_a_particle = None
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = STATE_IDLE

        if STATE_HURT not in self.state:
            if current_time - self.hurt_starting_time >= self.invulnerability_cooldown:
                self.invulnerable = False
                self.hurt_animation_frame_count = 0

    def collision(self, direction):
        # Collision with Enemies
        for sprite in self.enemy_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if STATE_HURT not in self.state and not self.invulnerable and not sprite.invulnerable:
                    self.hurt_starting_time = pygame.time.get_ticks()
                    self.invulnerable = True
                    self.player_hurt_sound.play()
                    if direction == HORIZONTAL_LABEL:
                        self.state = STATE_HURT_HORIZONTAL
                        self.direction_vector.y = 0
                        if self.hitbox.centerx - sprite.hitbox.centerx <= 0:
                            self.direction_vector.x = -1
                            self.hitbox.x -= self.current_speed
                        else:
                            self.direction_vector.x = 1
                            self.hitbox.x += self.current_speed
                    else:
                        self.state = STATE_HURT_VERTICAL
                        self.direction_vector.x = 0
                        if self.hitbox.centerx - sprite.hitbox.centerx <= 0:
                            self.direction_vector.y = -1
                            self.hitbox.y -= self.current_speed
                        else:
                            self.direction_vector.y = 1
                            self.hitbox.y += self.current_speed
                    self.health -= sprite.collision_damage
                    if self.health <= PLAYER_HEALTH_PER_HEART and not self.is_low_health:
                        self.low_health_sound.play(loops=-1)
                        self.is_low_health = True

        # Collision with Obstacles
        for sprite in self.obstacle_sprites:
            if sprite.type == LIMIT_WATER_INDEX and self.has_ladder and not self.ladder_in_use:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.ladder_in_use = True
                    ladder_image = tileset.ITEMS_TILE_SET.get_sprite_image(LADDER_FRAME_ID)
                    ladder_pos_x = sprite.pos[0]
                    ladder_pos_y = sprite.pos[1]
                    if direction == HORIZONTAL_LABEL:
                        if self.direction_vector.x < 0:
                            ladder_pos_x -= 16
                    else:
                        if self.direction_vector.y < 0:
                            ladder_pos_y -= 16
                    self.ladder = Tile((ladder_pos_x, ladder_pos_y), (self.visible_sprites,), ladder_image)
                    sprite.type = LIMIT_LADDER_INDEX

                    # Put player above the ladder by being the last visible sprite added
                    self.visible_sprites.remove(self)
                    self.visible_sprites.add(self)

            elif (sprite.type == LIMIT_WATER_INDEX and
                  self.has_ladder and
                  self.ladder_in_use and
                  sprite.hitbox.colliderect(self.ladder.hitbox)):
                # If it's water under the ladder, make it walkable
                sprite.type = LIMIT_LADDER_INDEX

            elif sprite.type != LIMIT_LADDER_INDEX and sprite.type != LIMIT_LAKE_BORDER_INDEX:
                # If it's anything but a walkable water, block Player's path
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == HORIZONTAL_LABEL:
                        if self.direction_vector.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction_vector.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                    else:
                        if self.direction_vector.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction_vector.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

            else:
                # If it's a walkable water tile, delete it (and the ladder also) if the ladder is not being used.
                if self.ladder_in_use:
                    # Delete ladder if the Player is not on top of it anymore
                    if not self.ladder.rect.colliderect(self.hitbox):
                        sprite.type = LIMIT_WATER_INDEX
                        self.ladder.kill()
                        self.ladder = None
                        self.ladder_in_use = False
                elif sprite.type != LIMIT_LAKE_BORDER_INDEX:
                    sprite.type = LIMIT_WATER_INDEX

        # Collision with Particles
        for particle in self.particle_sprites:
            if particle.hitbox.colliderect(self.hitbox):
                if STATE_HURT not in self.state and not self.invulnerable and particle.affects_player:
                    # Shield test
                    if (not particle.bypasses_shield
                            and STATE_ACTION not in self.state
                            and particle.hitbox.colliderect(self.shield_hitbox)):
                        # Successful block !
                        self.shield_block_sound.play()
                        if not isinstance(particle, PBoomerang):
                            particle.kill()
                        else:
                            particle.go_back = True
                            particle.collision_damage = 0
                    else:
                        if particle.collision_damage != 0:
                            self.state = STATE_HURT_PARTICLE
                            self.hurt_starting_time = pygame.time.get_ticks()
                            self.hurt_animation_starting_time = self.hurt_starting_time
                            self.invulnerable = True
                            self.player_hurt_sound.play()
                            self.direction_vector = particle.direction_vector
                            self.hitbox.x += self.current_speed*self.direction_vector.x
                            self.hitbox.y += self.current_speed*self.direction_vector.y
                            self.health -= particle.collision_damage
                            if self.health <= PLAYER_HEALTH_PER_HEART and not self.is_low_health:
                                self.low_health_sound.play(loops=-1)
                                self.is_low_health = True
                        else:
                            particle.effect()
                        particle.kill()

        # Collision with a lootable item
        for item in self.lootable_items_sprites:
            if item.hitbox.colliderect(self.rect):
                if STATE_HURT not in self.state:
                    item.effect()
                    item.kill()

        # Collision with a purchasable item
        for purchasable in self.purchasable_sprites:
            if (purchasable.hitbox.colliderect(self.hitbox)
                    and (purchasable.price < 0
                         or (self.money >= purchasable.price or purchasable.ignore_player_money_amount))):
                purchasable.effect()
                purchasable.kill()

        # Collision with a Npc
        for npc in self.npc_sprites:
            if npc.hitbox.colliderect(self.hitbox):
                if direction == HORIZONTAL_LABEL:
                    if self.direction_vector.x > 0:
                        self.hitbox.right = npc.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = npc.hitbox.right
                else:
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = npc.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = npc.hitbox.bottom

    def move(self):
        if self.direction_vector.magnitude() != 0:
            self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision(VERTICAL_LABEL)

        if not self.isDead:
            self.rect.top = self.hitbox.top - PLAYER_HITBOX_Y_OFFSET
            self.rect.left = self.hitbox.left - PLAYER_HITBOX_X_OFFSET
            self.realign_shield()

    def set_state(self, state):
        current_time = pygame.time.get_ticks()
        if state == STATE_DYING:
            self.state = state
            self.hurt_starting_time = current_time
        elif state == STATE_SPINNING:
            if not self.is_spinning:
                self.state = state
                self.spin_animation_starting_time = current_time
            self.is_spinning = True
        elif state == STATE_IDLE_DOWN:
            self.state = STATE_IDLE
            self.direction_label = DOWN_LABEL
        elif state == STATE_GRAY:
            self.state = state
        elif state == STATE_DESPAWN:
            self.state = state
            self.despawn_sound.play()
            self.despawn_animation_starting_time = current_time
        elif state == STATE_WARPING:
            self.state = state
        elif state == STATE_WARPING_DUNGEON:
            self.state = state
        elif state == STATE_STAIRS:
            self.state = state
            self.stairs_sound.play()
            self.stairs_animation_starting_time = current_time
        elif state == STATE_IDLE:
            self.state = state
        elif state == TWO_HANDED:
            self.state = TWO_HANDED
            self.invulnerable = True
            self.pickup_two_handed_starting_time = current_time
            self.pick_up_sound.play()
        elif state == ONE_HANDED:
            self.state = ONE_HANDED
            self.invulnerable = True
            self.pickup_one_handed_starting_time = current_time
            self.pick_up_sound.play()
        elif state == STATE_TRIFORCE:
            self.state = STATE_TRIFORCE
            self.invulnerable = True
            self.is_winning = True

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = animation_list[animation_frame_count]
        if current_time - animation_starting_time >= animation_cooldown:
            animation_starting_time = current_time
            if animation_frame_count < animation_frames_nb - 1:
                animation_frame_count += 1
            elif reset_for_loop:
                animation_frame_count = 0
                if idle_after:
                    self.state = STATE_IDLE

        return animation_starting_time, animation_frame_count

    def animate(self):
        current_time = pygame.time.get_ticks()
        if self.state == STATE_IDLE:
            # Stops all animation, resetting to 1st walking frame of the current direction
            self.image = self.walking_animations[self.direction_label][0]
        elif self.state == STATE_WARPING_DUNGEON:
            self.image = tileset.PLAYER_TILE_SET.get_sprite_image(PLAYER_TRANSPARENT_FRAME_ID)
        elif self.state == STATE_WALKING or self.state == STATE_WARPING:
            self.walking_animation_starting_time, self.walking_animation_frame_count = (
                self.change_animation_frame(self.walking_animations[self.direction_label],
                                            self.walking_animation_frame_count,
                                            self.walking_animation_starting_time,
                                            self.walking_animation_cooldown,
                                            self.walking_frames))
        elif STATE_ACTION in self.state:
            self.action_animation_starting_time, self.action_animation_frame_count = (
                self.change_animation_frame(self.action_animations[self.direction_label],
                                            self.action_animation_frame_count,
                                            self.action_animation_starting_time,
                                            self.action_animation_cooldown,
                                            self.action_frames))
        elif self.state == ONE_HANDED:
            self.pickup_one_handed_animation_starting_time, self.pickup_one_handed_animation_frame_count = (
                self.change_animation_frame(self.pickup_one_handed_animation,
                                            self.pickup_one_handed_animation_frame_count,
                                            self.pickup_one_handed_animation_starting_time,
                                            self.pickup_one_handed_animation_cooldown,
                                            self.pickup_one_handed_frames))

        elif self.state == TWO_HANDED or self.state == STATE_TRIFORCE:
            self.pickup_two_handed_animation_starting_time, self.pickup_two_handed_animation_frame_count = (
                self.change_animation_frame(self.pickup_two_handed_animation,
                                            self.pickup_two_handed_animation_frame_count,
                                            self.pickup_two_handed_animation_starting_time,
                                            self.pickup_two_handed_animation_cooldown,
                                            self.pickup_two_handed_frames))
        elif STATE_HURT in self.state or self.state == STATE_DYING:
            reset_for_loop = False if STATE_HURT in self.state else True
            self.hurt_animation_starting_time, self.hurt_animation_frame_count = (
                self.change_animation_frame(self.hurt_animations[self.direction_label],
                                            self.hurt_animation_frame_count,
                                            self.hurt_animation_starting_time,
                                            self.hurt_animation_cooldown,
                                            self.hurt_frames,
                                            reset_for_loop))
        elif self.state == STATE_STAIRS:
            self.stairs_animation_starting_time, self.stairs_animation_frame_count = (
                self.change_animation_frame(self.stairs_animation,
                                            self.stairs_animation_frame_count,
                                            self.stairs_animation_starting_time,
                                            self.stairs_animation_cooldown,
                                            self.stairs_frames,
                                            True,
                                            True))
        elif self.state == STATE_SPINNING:
            # Spin spin spin !
            self.walking_animation_starting_time, self.walking_animation_frame_count = (
                self.change_animation_frame(self.walking_animations[self.direction_label],
                                            self.walking_animation_frame_count,
                                            self.walking_animation_starting_time,
                                            self.walking_animation_cooldown,
                                            self.walking_frames))
            elapsed_spin_time = current_time - self.spin_animation_starting_time
            if elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.25:
                self.direction_label = RIGHT_LABEL
            elif elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.5:
                self.direction_label = UP_LABEL
            elif elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.75:
                self.direction_label = LEFT_LABEL
            else:
                self.spin_animation_starting_time = current_time
                self.direction_label = DOWN_LABEL
        elif self.state == STATE_GRAY:
            # be gray
            self.image = self.gray_animation[DOWN_LABEL][0]
        elif self.state == STATE_DESPAWN:
            self.despawn_animation_starting_time, self.despawn_animation_frame_count = (
                self.change_animation_frame(self.despawn_animation,
                                            self.despawn_animation_frame_count,
                                            self.despawn_animation_starting_time,
                                            self.despawn_animation_cooldown,
                                            self.despawn_frames))

    def heal(self, amount):
        if amount >= 0:
            self.health += amount * PLAYER_HEALTH_PER_HEART
            if self.health > PLAYER_HEALTH_PER_HEART and self.is_low_health:
                self.low_health_sound.stop()
                self.is_low_health = False
            if self.health > self.current_max_health:
                self.health = self.current_max_health

    def add_max_health(self):
        if self.current_max_health < PLAYER_HEALTH_MAX:
            self.current_max_health += PLAYER_HEALTH_PER_HEART
            self.heal(1)
        else:
            self.current_max_health = PLAYER_HEALTH_MAX

    def add_money(self, amount):
        if amount != 0:
            if amount == 1:
                self.rupee_acquired_sound.play()
            else:
                self.rupees_acquired_sound.play()
            self.money += amount
            if self.money > 999:
                self.money = 999
            elif self.money < 0:
                self.money = 0

    def add_bombs(self, amount):
        if amount >= 0:
            if not self.has_bombs:
                self.has_bombs = True
                if self.itemB == NONE_LABEL:
                    self.itemB = BOMB_LABEL
            self.bombs += amount
            if self.bombs > PLAYER_BOMBS_MAX:
                self.bombs = PLAYER_BOMBS_MAX

    def add_keys(self, amount):
        if amount >= 0:
            self.key_acquired_sound.play()
            self.keys += amount

    def add_item(self, label):
        if label == HEARTRECEPTACLE_LABEL:
            self.add_max_health()
        elif label == WOOD_SWORD_LABEL:
            self.has_wood_sword = True
            self.equip_best_sword()
        elif label == BOOMERANG_LABEL:
            self.has_boomerang = True
            self.change_item_b(label)
        elif label == CANDLE_LABEL:
            self.has_candle = True
            self.change_item_b(label)
        elif label == LADDER_LABEL:
            self.has_ladder = True
        self.set_state(ITEM_PICKUP_ANIMATION[label])

    def has_item(self, label):
        if label == BOOMERANG_LABEL:
            return self.has_boomerang
        elif label == BOMB_LABEL:
            return self.has_bombs
        elif label == CANDLE_LABEL:
            return self.has_candle
        elif label == LADDER_LABEL:
            return self.has_ladder
        else:
            return False

    def equip_best_sword(self):
        # If new sword types are implemented, define here new cases, from best to worst option
        if self.has_wood_sword:
            self.itemA = WOOD_SWORD_LABEL
        else:
            self.itemA = NONE_LABEL

    def change_item_b(self, label):
        if self.has_item(label):
            self.itemB = label

    def define_warping_position(self, offset_x, offset_y, map_name):
        new_x = self.rect.x + offset_x
        new_y = self.rect.y + offset_y

        left_border = TILE_SIZE
        right_border = SCREEN_WIDTH - TILE_SIZE * 3
        top_border = TILE_SIZE + HUD_OFFSET
        bottom_border = SCREEN_HEIGHT - TILE_SIZE * 3
        if DUNGEON_PREFIX_LABEL in map_name:
            left_border += TILE_SIZE * 2 + 4
            right_border -= TILE_SIZE * 2 + 4
            top_border += TILE_SIZE * 2 + 4
            bottom_border -= TILE_SIZE * 2 + 4
        if left_border >= new_x:
            new_x = left_border + 4
        elif new_x >= right_border:
            new_x = right_border - 4

        if top_border >= new_y:
            new_y = top_border + 4
        elif new_y >= bottom_border:
            new_y = bottom_border - 4

        self.warping_x = new_x
        self.warping_y = new_y

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.hitbox.top = self.rect.top + PLAYER_HITBOX_Y_OFFSET
        self.hitbox.left = self.rect.left + PLAYER_HITBOX_X_OFFSET
        self.realign_shield()

    def update(self):
        if not self.isDead:
            if STATE_HURT not in self.state:
                self.current_speed = self.speed
            else:
                self.current_speed = (PLAYER_HURT_FRAMES - self.hurt_animation_frame_count)

            if STATE_WARPING not in self.state:
                self.move()
                player_draw_pos = self.rect.topleft
                if self.health < 0:
                    self.health = 0
            else:
                player_draw_pos = (self.warping_x, self.warping_y)
            self.animate()
            self.cooldowns()
            if self.health <= 0:
                self.isDead = True
                self.low_health_sound.stop()
        else:
            player_draw_pos = self.rect.topleft
            self.animate()

        pygame.display.get_surface().blit(self.image, player_draw_pos)
