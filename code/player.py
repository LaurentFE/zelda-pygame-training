import pygame.mixer

from settings import *
from inputs import *
from debug import debug
from tile import Tile
from entities import Entity
from particles import PWoodenSword, Bomb


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

# Will need someday to SINGLETON-ify this

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, enemy_sprites, visible_sprites, particle_sprites,
                 lootable_items_sprites, player_tile_set, particle_tileset, item_tileset):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, particle_tileset)

        self.enemy_sprites = enemy_sprites
        self.visible_sprites = visible_sprites
        self.particle_sprites = particle_sprites
        self.lootable_items_sprites = lootable_items_sprites

        self.item_tileset = item_tileset

        # Initialisation of the values used to load the different animations
        self.is_right_flipped = True
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
        self.pickup_minor_frames = PLAYER_PICKUP_MINOR_FRAMES
        self.pickup_minor_frame_id = PLAYER_PICKUP_MINOR_FRAME_ID
        self.pickup_major_frames = PLAYER_PICKUP_MAJOR_FRAMES
        self.pickup_major_frame_id = PLAYER_PICKUP_MAJOR_FRAME_ID
        self.hurt_frames = PLAYER_HURT_FRAMES
        self.hurt_up_frame_id = PLAYER_HURT_UP_FRAME_ID
        self.hurt_down_frame_id = PLAYER_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = PLAYER_HURT_RIGHT_FRAME_ID
        self.hurt_right_frame_id = PLAYER_HURT_RIGHT_FRAME_ID
        self.despawn_frames = PLAYER_DEATH_FRAMES
        self.despawn_frame_id = PLAYER_DEATH_FRAME_ID
        self.stairs_frames = PLAYER_STAIRS_FRAMES
        self.stairs_frame_id = PLAYER_STAIRS_FRAME_ID
        self.load_animation_frames(player_tile_set)

        # Sounds
        self.shield_block_sound = pygame.mixer.Sound(SOUND_SHIELD_BLOCK)
        self.shield_block_sound.set_volume(0.5)
        self.player_hurt_sound = pygame.mixer.Sound(SOUND_PLAYER_HURT)
        self.player_hurt_sound.set_volume(0.1)
        self.rupee_acquired_sound = pygame.mixer.Sound(SOUND_RUPEE_ACQUIRED)
        self.rupee_acquired_sound.set_volume(0.3)
        self.is_low_health = False
        self.low_health_sound = pygame.mixer.Sound(SOUND_LOW_HEALTH)
        self.low_health_sound.set_volume(0.3)
        self.despawn_sound = pygame.mixer.Sound(SOUND_PLAYER_DESPAWN)
        self.despawn_sound.set_volume(0.4)
        self.stairs_sound = pygame.mixer.Sound(SOUND_STAIRS)
        self.stairs_sound.set_volume(0.4)
        self.pick_up_sound = pygame.mixer.Sound(SOUND_PICKUP)
        self.pick_up_sound.set_volume(0.3)

        self.direction_label = 'down'
        self.state = 'idle'
        self.speed = 3

        self.pos = pos
        self.image = self.walking_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-8, -16)
        self.hitbox.top = self.rect.top + 14
        self.hitbox.left = self.rect.left + 4

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = PLAYER_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_minor_animation_cooldown = PLAYER_PICKUP_MINOR_ANIMATION_COOLDOWN
        self.pickup_major_animation_cooldown = PLAYER_PICKUP_MAJOR_ANIMATION_COOLDOWN
        self.hurt_animation_cooldown = PLAYER_HURT_ANIMATION_COOLDOWN
        self.despawn_animation_cooldown = PLAYER_DEATH_ANIMATION_COOLDOWN
        self.stairs_animation_cooldown = PLAYER_STAIRS_ANIMATION_COOLDOWN
        # Time at which animation frame started
        self.walking_animation_starting_time = 0
        self.action_animation_starting_time = 0
        self.pickup_minor_animation_starting_time = 0
        self.pickup_major_animation_starting_time = 0
        self.hurt_animation_starting_time = 0
        self.spin_animation_starting_time = 0
        self.despawn_animation_starting_time = 0
        self.stairs_animation_starting_time = 0
        # Index of animation being played
        self.walking_animation_frame_count = 0
        self.action_animation_frame_count = 0
        self.pickup_minor_animation_frame_count = 0
        self.pickup_major_animation_frame_count = 0
        self.hurt_animation_frame_count = 0
        self.despawn_animation_frame_count = 0
        self.stairs_animation_frame_count = 0
        # Animation reset
        self.idle_time = 0

        # Player actions cooldowns
        self.action_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_minor_cooldown = 1500
        self.pickup_major_cooldown = PLAYER_PICKUP_MAJOR_COOLDOWN
        self.hurt_cooldown = PLAYER_HURT_FRAMES * self.hurt_animation_cooldown
        self.invulnerability_cooldown = 1.5 * self.hurt_cooldown
        self.action_starting_time = 0
        self.pickup_minor_starting_time = 0
        self.pickup_major_starting_time = 0
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

    def load_animation_frames(self, player_tile_set):
        super().load_animation_frames(player_tile_set)

    def can_move(self):
        if self.state == 'walking' or self.state == 'idle':
            return True
        return False

    def can_action(self):
        if 'action' not in self.state:
            return True
        return False

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction_vector.x = 0
        self.direction_vector.y = 0
        if is_move_key_pressed(keys) and self.can_move():
            if is_up_key_pressed(keys):
                self.direction_vector.y = -1
                self.direction_label = 'up'
            elif is_down_key_pressed(keys):
                self.direction_vector.y = 1
                self.direction_label = 'down'
            if is_left_key_pressed(keys):
                self.direction_vector.x = -1
                self.direction_label = 'left'
            elif is_right_key_pressed(keys):
                self.direction_vector.x = 1
                self.direction_label = 'right'
            if self.state != 'walking':
                self.state = 'walking'
                self.walking_animation_starting_time = pygame.time.get_ticks()
                self.idle_time = pygame.time.get_ticks()

        # ActionA input has prio over Move input
        # Can't move during sword use
        if is_action_a_key_pressed(keys) and self.can_action() and self.itemA != "None":
            self.state = 'actionA'
            self.action_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0
            # Define here all different item A weapons implemented
            if self.itemA == WOOD_SWORD_LABEL:
                self.action_a_particle = PWoodenSword(self.rect.topleft, self.direction_vector, self.direction_label,
                                                      [self.visible_sprites, self.particle_sprites],
                                                      self.particle_tileset)

        # Can't move during item use
        if is_action_b_key_pressed(keys) and self.can_action():
            self.state = 'actionB'
            self.action_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0
            if self.itemB == BOOMERANG_LABEL:
                # Create Boomerang particle
                pass
            elif self.itemB == BOMB_LABEL:
                if self.bombs > 0:
                    # Bombs are dropped and forgotten, won't get deleted upon timer but when they die by themselves
                    Bomb(self.rect.topleft, self.direction_vector, self.direction_label,
                         [self.visible_sprites, self.particle_sprites],
                         self.particle_tileset)
                    self.bombs -= 1
                else:
                    self.state = 'idle'
            elif self.itemB == CANDLE_LABEL:
                # Create Flame particle
                pass
            elif self.itemB == 'None':
                self.state = 'idle'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if 'action' in self.state:
            if current_time - self.action_starting_time >= self.action_cooldown:
                if self.state == 'actionA':
                    self.action_a_particle.kill()
                    self.action_a_particle = None
                elif self.state == 'actionB' and self.action_b_particle is not None:
                    self.action_b_particle.kill()
                    self.action_b_particle = None
                self.state = 'idle'
        elif self.state == 'walking':
            if current_time - self.idle_time >= self.walking_animation_cooldown:
                self.state = 'idle'
        elif self.state == 'pickup_minor':
            if current_time - self.pickup_minor_starting_time >= self.pickup_minor_cooldown:
                self.state = 'idle'
        elif self.state == 'pickup_major':
            if current_time - self.pickup_major_starting_time >= self.pickup_major_cooldown:
                self.state = 'idle'
                self.invulnerable = False
        elif 'hurt' in self.state:
            if self.action_a_particle is not None:
                self.action_a_particle.kill()
                self.action_a_particle = None
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = 'idle'

        if 'hurt' not in self.state:
            if current_time - self.hurt_starting_time >= self.invulnerability_cooldown:
                self.invulnerable = False
                self.hurt_animation_frame_count = 0

    def collision(self, direction):
        # Collision with Enemies
        for sprite in self.enemy_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if 'hurt' not in self.state and not self.invulnerable and not sprite.invulnerable:
                    self.hurt_starting_time = pygame.time.get_ticks()
                    self.invulnerable = True
                    self.player_hurt_sound.play()
                    if direction == 'horizontal':
                        self.state = 'hurt_h'
                        self.direction_vector.y = 0
                        if self.hitbox.centerx - sprite.hitbox.centerx <= 0:
                            self.direction_vector.x = -1
                            self.hitbox.x -= self.current_speed
                        else:
                            self.direction_vector.x = 1
                            self.hitbox.x += self.current_speed
                    else:
                        self.state = 'hurt_v'
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
                    ladder_image = self.item_tileset.get_sprite_image(LADDER_FRAME_ID)
                    ladder_pos_x = sprite.pos[0]
                    ladder_pos_y = sprite.pos[1]
                    if direction == 'horizontal':
                        if self.direction_vector.x < 0:
                            ladder_pos_x -= 16
                    else:
                        if self.direction_vector.y < 0:
                            ladder_pos_y -= 16
                    self.ladder = Tile((ladder_pos_x, ladder_pos_y), self.visible_sprites, ladder_image)
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

            elif sprite.type != LIMIT_LADDER_INDEX:
                # If it's anything but a walkable water, block Player's path
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
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
                else:
                    sprite.type = LIMIT_WATER_INDEX

        # Collision with Particles
        for particle in self.particle_sprites:
            if particle.hitbox.colliderect(self.hitbox):
                if 'hurt' not in self.state and not self.invulnerable and particle.affects_player:
                    # Shield test
                    if (not particle.bypasses_shield
                            and 'action' not in self.state
                            and ((self.direction_label == 'up' and particle.direction_vector.y > 0)
                                 or (self.direction_label == 'down' and particle.direction_vector.y < 0)
                                 or (self.direction_label == 'left' and particle.direction_vector.x > 0)
                                 or (self.direction_label == 'right' and particle.direction_vector.x < 0))):
                        # Successful block !
                        self.shield_block_sound.play()
                        particle.kill()
                    else:
                        if particle.collision_damage != 0:
                            self.state = 'hurt_p'
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
                if 'hurt' not in self.state:
                    item.effect()
                    item.kill()

    def move(self):
        if self.direction_vector.magnitude() != 0:
            self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision('vertical')

        if not self.isDead:
            self.rect.top = self.hitbox.top - 12
            self.rect.left = self.hitbox.left - 4

    def set_state(self, state):
        current_time = pygame.time.get_ticks()
        if state == 'dying':
            self.state = state
            self.hurt_starting_time = current_time
        elif state == 'spinning':
            if not self.is_spinning:
                self.state = state
                self.spin_animation_starting_time = current_time
            self.is_spinning = True
        elif state == 'idle_d':
            self.state = 'idle'
            self.direction_label = 'down'
        elif state == 'gray':
            self.state = state
        elif state == 'despawn':
            self.state = state
            self.despawn_sound.play()
            self.despawn_animation_starting_time = current_time
        elif state == 'warping':
            self.state = state
        elif state == 'stairs':
            self.state = state
            self.stairs_sound.play()
            self.stairs_animation_starting_time = current_time
        elif state == 'idle':
            self.state = state
        elif state == 'pickup_major':
            self.state = 'pickup_major'
            self.invulnerable = True
            self.pickup_major_starting_time = current_time
            self.pick_up_sound.play()
        else:
            debug(f'trying to change player state in death to : {state}. Does not exist')

    def animate(self):
        current_time = pygame.time.get_ticks()
        if self.state == 'idle':
            # Stops all animation, resetting to 1st walking frame of the current direction
            self.image = self.walking_animations[self.direction_label][0]
        elif self.state == 'walking' or self.state == 'warping':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
            if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
                self.walking_animation_starting_time = current_time
                if self.walking_animation_frame_count < PLAYER_WALKING_FRAMES-1:
                    self.walking_animation_frame_count += 1
                else:
                    self.walking_animation_frame_count = 0
        elif 'action' in self.state:
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.action_animations[self.direction_label][self.action_animation_frame_count]
            if current_time - self.action_animation_starting_time >= self.action_animation_cooldown:
                self.action_animation_starting_time = current_time
                if self.action_animation_frame_count < PLAYER_ACTION_FRAMES-1:
                    self.action_animation_frame_count += 1
                else:
                    self.action_animation_frame_count = 0
        elif self.state == 'pickup_minor':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.pickup_minor_animation[self.pickup_minor_animation_frame_count]
            if current_time - self.pickup_minor_animation_starting_time >= self.pickup_minor_animation_cooldown:
                self.pickup_minor_animation_starting_time = current_time
                if self.pickup_minor_animation_frame_count < PLAYER_PICKUP_MINOR_FRAMES-1:
                    self.pickup_minor_animation_frame_count += 1
                else:
                    self.pickup_minor_animation_frame_count = 0
        elif self.state == 'pickup_major':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.pickup_major_animation[self.pickup_major_animation_frame_count]
            if current_time - self.pickup_major_animation_starting_time >= self.pickup_major_animation_cooldown:
                self.pickup_major_animation_starting_time = current_time
                if self.pickup_major_animation_frame_count < PLAYER_PICKUP_MAJOR_FRAMES-1:
                    self.pickup_major_animation_frame_count += 1
                else:
                    self.pickup_major_animation_frame_count = 0
        elif 'hurt' in self.state:
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.hurt_animations[self.direction_label][self.hurt_animation_frame_count]
            if current_time - self.hurt_animation_starting_time >= self.hurt_animation_cooldown:
                self.hurt_animation_starting_time = current_time
                if self.hurt_animation_frame_count < PLAYER_HURT_FRAMES-1:
                    self.hurt_animation_frame_count += 1
        elif self.state == 'stairs':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.stairs_animation[self.stairs_animation_frame_count]
            if current_time - self.stairs_animation_starting_time >= self.stairs_animation_cooldown:
                self.stairs_animation_starting_time = current_time
                if self.stairs_animation_frame_count < PLAYER_STAIRS_FRAMES-1:
                    self.stairs_animation_frame_count += 1
                else:
                    self.stairs_animation_frame_count = 0
                    self.state = 'idle'
        elif self.state == 'dying':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.hurt_animations[self.direction_label][self.hurt_animation_frame_count]
            if current_time - self.hurt_animation_starting_time >= self.hurt_animation_cooldown:
                self.hurt_animation_starting_time = current_time
                if self.hurt_animation_frame_count < PLAYER_HURT_FRAMES-1:
                    self.hurt_animation_frame_count += 1
                else:
                    self.hurt_animation_frame_count = 0
        elif self.state == 'spinning':
            # Spin spin spin !
            self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
            if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
                self.walking_animation_starting_time = current_time
                if self.walking_animation_frame_count < PLAYER_WALKING_FRAMES - 1:
                    self.walking_animation_frame_count += 1
                else:
                    self.walking_animation_frame_count = 0
            elapsed_spin_time = current_time - self.spin_animation_starting_time
            if elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.25:
                self.direction_label = 'right'
            elif elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.5:
                self.direction_label = 'up'
            elif elapsed_spin_time < PLAYER_DEATH_SPIN_DURATION * 0.75:
                self.direction_label = 'left'
            else:
                self.spin_animation_starting_time = current_time
                self.direction_label = 'down'
        elif self.state == 'gray':
            # be gray
            self.image = self.gray_animation['down'][0]
        elif self.state == 'despawn':
            self.image = self.despawn_animation[self.despawn_animation_frame_count]
            if current_time - self.despawn_animation_starting_time >= self.despawn_animation_cooldown:
                self.despawn_animation_starting_time = current_time
                if self.despawn_animation_frame_count < PLAYER_DEATH_FRAMES-1:
                    self.despawn_animation_frame_count += 1
                else:
                    self.despawn_animation_frame_count = 0
        else:
            debug(f'Error : animate({self.state}) does not exist')

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
            self.heal(PLAYER_HEALTH_PER_HEART)
        else:
            self.current_max_health = PLAYER_HEALTH_MAX

    def add_money(self, amount):
        if amount >= 0:
            self.rupee_acquired_sound.play()
            self.money += amount
            if self.money > 999:
                self.money = 999

    def add_bombs(self, amount):
        if amount >= 0:
            if not self.has_bombs:
                self.has_bombs = True
                if self.itemB == 'None':
                    self.itemB = BOMB_LABEL
            self.bombs += amount
            if self.bombs > PLAYER_BOMBS_MAX:
                self.bombs = PLAYER_BOMBS_MAX

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
            self.itemA = 'None'

    def change_item_b(self, label):
        if self.has_item(label):
            self.itemB = label

    def offset_position(self, offset_x, offset_y):
        new_x = self.hitbox.x + offset_x
        new_y = self.hitbox.y + offset_y

        if TILE_SIZE >= new_x:
            new_x = TILE_SIZE + 1
        elif new_x >= SCREEN_WIDTH - TILE_SIZE * 3:
            new_x = SCREEN_WIDTH - TILE_SIZE * 3 - 1

        if TILE_SIZE + TILE_SIZE * HUD_TILE_HEIGHT >= new_y:
            new_y = TILE_SIZE + TILE_SIZE * HUD_TILE_HEIGHT + 1
        elif new_y >= SCREEN_HEIGHT - TILE_SIZE * 3:
            new_y = SCREEN_HEIGHT - TILE_SIZE * 3 - 1

        self.hitbox.x = new_x
        self.hitbox.y = new_y
        self.rect.top = self.hitbox.top - 12
        self.rect.left = self.hitbox.left - 4

    def set_position(self, pos):
        self.hitbox.x = pos[0]
        self.hitbox.y = pos[1]
        self.rect.top = self.hitbox.top - 12
        self.rect.left = self.hitbox.left - 4

    def update(self):
        if not self.isDead:
            if 'hurt' not in self.state:
                self.input()
                self.current_speed = self.speed
            else:
                self.current_speed = (PLAYER_HURT_FRAMES - self.hurt_animation_frame_count)

            if self.state != 'warping':
                self.move()
            self.animate()
            self.cooldowns()
            if self.health <= 0:
                self.isDead = True
                self.low_health_sound.stop()
        else:
            self.animate()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)
