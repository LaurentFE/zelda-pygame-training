import pygame
from settings import *
from debug import debug
from entities import Entity
from particles import WoodenSword


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
#       Original allows player to change direction of attack during animation (framerate is lower though,
#         so "on cooldown" I guess)
#       My version : probably won't allow it, because player won't really 'attack' or 'cast', but most likely
#         'cast' every item, sword included, and I don't want to change directions in middle of candle for instance,
#         or of flute.

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, enemy_sprites, visible_sprites, particle_sprites,
                 player_tile_set, particle_tileset):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, particle_tileset)

        self.enemy_sprites = enemy_sprites
        self.visible_sprites = visible_sprites
        self.particle_sprites = particle_sprites

        self.action_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.pickup_minor_animation = []
        self.pickup_major_animation = []
        self.gray_animation = {
            'down': []
        }
        self.load_animation_frames(player_tile_set)

        self.direction_label = 'down'
        self.state = 'idle'
        self.speed = 3

        self.pos = pos
        self.image = self.walking_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = PLAYER_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_minor_animation_cooldown = PLAYER_PICKUP_MINOR_ANIMATION_COOLDOWN
        self.pickup_major_animation_cooldown = PLAYER_PICKUP_MAJOR_ANIMATION_COOLDOWN
        self.hurt_animation_cooldown = PLAYER_HURT_ANIMATION_COOLDOWN
        self.despawn_animation_cooldown = PLAYER_DEATH_ANIMATION_COOLDOWN
        # Time at which animation frame started
        self.walking_animation_starting_time = 0
        self.action_animation_starting_time = 0
        self.pickup_minor_animation_starting_time = 0
        self.pickup_major_animation_starting_time = 0
        self.hurt_animation_starting_time = 0
        self.despawn_animation_starting_time = 0
        # Index of animation being played
        self.walking_animation_frame_count = 0
        self.action_animation_frame_count = 0
        self.pickup_minor_animation_frame_count = 0
        self.pickup_major_animation_frame_count = 0
        self.hurt_animation_frame_count = 0
        self.despawn_animation_frame_count = 0
        # Animation reset
        self.idle_time = 0

        # Player actions cooldowns
        self.action_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN
        self.pickup_minor_cooldown = 1500
        self.pickup_major_cooldown = 2500
        self.hurt_cooldown = PLAYER_HURT_FRAMES * self.hurt_animation_cooldown
        self.invulnerability_cooldown = 1.5 * self.hurt_cooldown
        self.action_starting_time = 0
        self.pickup_minor_starting_time = 0
        self.pickup_major_starting_time = 0
        self.hurt_starting_time = 0

        self.action_particle = None

        # Player stats and items
        # 1 Heart = 256 health
        self.current_max_health = PLAYER_INITIAL_HEALTH
        self.health = int(self.current_max_health)
        self.invulnerable = False
        self.money = 0
        self.keys = 123
        self.bombs = 456
        self.isDead = False
        self.current_speed = self.speed

        # Items flags
        self.has_boomerang = True
        self.has_candle = True
        self.has_ladder = True
        self.has_raft = True
        self.has_sword_wood = True

    def load_animation_frames(self, player_tile_set):
        for i in range(PLAYER_WALKING_FRAMES):
            self.walking_animations['up'].append(
                player_tile_set.get_sprite_image(PLAYER_WALKING_UP_FRAME_ID + (2 * i)))
            self.walking_animations['right'].append(
                player_tile_set.get_sprite_image(PLAYER_WALKING_RIGHT_FRAME_ID + (2 * i)))
            self.walking_animations['down'].append(
                player_tile_set.get_sprite_image(PLAYER_WALKING_DOWN_FRAME_ID + (2 * i)))
            self.walking_animations['left'].append(
                pygame.transform.flip(
                    player_tile_set.get_sprite_image(PLAYER_WALKING_RIGHT_FRAME_ID + (2 * i)),
                    True,
                    False))
            self.gray_animation['down'].append(
                player_tile_set.get_sprite_image(PLAYER_GRAY_WALKING_DOWN_FRAME_ID + (2 * i)))

        for i in range(PLAYER_ACTION_FRAMES):
            self.action_animations['up'].append(
                player_tile_set.get_sprite_image(PLAYER_ACTION_UP_FRAME_ID + (2 * i)))
            self.action_animations['right'].append(
                player_tile_set.get_sprite_image(PLAYER_ACTION_RIGHT_FRAME_ID + (2 * i)))
            self.action_animations['down'].append(
                player_tile_set.get_sprite_image(PLAYER_ACTION_DOWN_FRAME_ID + (2 * i)))
            self.action_animations['left'].append(
                pygame.transform.flip(
                    player_tile_set.get_sprite_image(PLAYER_ACTION_RIGHT_FRAME_ID + (2 * i)),
                    True,
                    False))

        for i in range(PLAYER_PICKUP_MINOR_FRAMES):
            self.pickup_minor_animation.append(
                player_tile_set.get_sprite_image(PLAYER_PICKUP_MINOR_FRAME_ID + (2 * i)))

        for i in range(PLAYER_PICKUP_MAJOR_FRAMES):
            self.pickup_major_animation.append(
                player_tile_set.get_sprite_image(PLAYER_PICKUP_MAJOR_FRAME_ID + (2 * i)))

        for i in range(PLAYER_HURT_FRAMES):
            self.hurt_animations['up'].append(
                player_tile_set.get_sprite_image(PLAYER_HURT_UP_FRAME_ID + (2 * i)))
            self.hurt_animations['right'].append(
                player_tile_set.get_sprite_image(PLAYER_HURT_RIGHT_FRAME_ID + (2 * i)))
            self.hurt_animations['down'].append(
                player_tile_set.get_sprite_image(PLAYER_HURT_DOWN_FRAME_ID + (2 * i)))
            self.hurt_animations['left'].append(
                pygame.transform.flip(
                    player_tile_set.get_sprite_image(PLAYER_HURT_RIGHT_FRAME_ID + (2 * i)),
                    True,
                    False))

        for i in range(PLAYER_DEATH_FRAMES):
            self.despawn_animation.append(player_tile_set.get_sprite_image(PLAYER_DEATH_FRAME_ID + (2 * i)))

    # input() detects which key is pressed, and modifies player direction_label & direction_vector,
    # and/or player_state, and starts cooldown on actions if used.
    def input(self):
        keys = pygame.key.get_pressed()
        moving_key_pressed = False

        if (keys[pygame.K_UP] or keys[pygame.K_z]) and (self.state == 'walking' or self.state == 'idle'):
            self.direction_vector.y = -1
            self.direction_label = 'up'
            moving_key_pressed = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (self.state == 'walking' or self.state == 'idle'):
            self.direction_vector.y = 1
            self.direction_label = 'down'
            moving_key_pressed = True
        else:
            self.direction_vector.y = 0

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and (self.state == 'walking' or self.state == 'idle'):
            self.direction_vector.x = -1
            self.direction_label = 'left'
            moving_key_pressed = True
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (self.state == 'walking' or self.state == 'idle'):
            self.direction_vector.x = 1
            self.direction_label = 'right'
            moving_key_pressed = True
        else:
            self.direction_vector.x = 0

        if moving_key_pressed and self.state != 'walking':
            self.state = 'walking'
            self.walking_animation_starting_time = pygame.time.get_ticks()
            self.idle_time = pygame.time.get_ticks()

        # Attack input has prio over Move input
        # Can't move during attack
        if keys[pygame.K_SPACE] and self.state != 'attacking' and self.state != 'casting':
            self.state = 'attacking'
            self.action_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0
            self.action_particle = WoodenSword(self.rect.topleft, self.direction_vector, self.direction_label,
                                               [self.visible_sprites, self.particle_sprites],
                                               self.particle_tileset)

        # Cast input has prio over Attack input
        # Can't move during cast
        if keys[pygame.K_LSHIFT] and self.state != 'casting' and self.state != 'attacking':
            self.state = 'casting'
            self.action_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0

        # REMOVE ALL THE FOLLOWING KEY DETECTIONS AFTER TESTING
        # THESE KEYS ARE FOR TESTING SPECIFIC ANIMATIONS
        if keys[pygame.K_a] and self.state != 'casting' and self.state != 'attacking':
            self.state = 'pickup_minor'
            # Don't forget, there is also a timer on the action to stop movement !
            self.pickup_minor_animation_starting_time = pygame.time.get_ticks()
            self.pickup_minor_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0
        if keys[pygame.K_z] and self.state != 'casting' and self.state != 'attacking':
            self.state = 'pickup_major'
            # Don't forget, there is also a timer on the action to stop movement !
            self.pickup_major_animation_starting_time = pygame.time.get_ticks()
            self.pickup_major_starting_time = pygame.time.get_ticks()
            self.direction_vector.x = 0
            self.direction_vector.y = 0
        if keys[pygame.K_e] and self.state != 'casting' and self.state != 'attacking':
            self.state = 'hurt_h'
            self.hurt_animation_starting_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.state == 'attacking' or self.state == 'casting':
            if current_time - self.action_starting_time >= self.action_cooldown:
                # Casting doesn't have a particle created yet because no items are implemented
                # Attacking is fixed on Wooden Sword. When items are implemented, should be actionA and actionB
                if self.state == 'attacking':
                    self.action_particle.kill()
                    self.action_particle = None
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
        elif 'hurt' in self.state:
            if self.action_particle is not None:
                self.action_particle.kill()
                self.action_particle = None
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = 'idle'

        if 'hurt' not in self.state:
            if current_time - self.hurt_starting_time >= self.invulnerability_cooldown:
                self.invulnerable = False

    # collision (direction) detects collision with both enemies and obstacle sprites
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.enemy_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if 'hurt' not in self.state and not self.invulnerable:
                        self.state = 'hurt_h'
                        self.hurt_starting_time = pygame.time.get_ticks()
                        self.invulnerable = True
                        self.direction_vector.y = 0
                        if self.hitbox.centerx - sprite.hitbox.centerx <= 0:
                            self.direction_vector.x = -1
                            self.hitbox.x -= self.current_speed
                        else:
                            self.direction_vector.x = 1
                            self.hitbox.x += self.current_speed
                        self.health -= sprite.collision_damage

            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.enemy_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if 'hurt' not in self.state and not self.invulnerable:
                        self.state = 'hurt_v'
                        self.hurt_starting_time = pygame.time.get_ticks()
                        self.invulnerable = True
                        self.direction_vector.x = 0
                        if self.hitbox.centerx - sprite.hitbox.centerx <= 0:
                            self.direction_vector.y = -1
                            self.hitbox.y -= self.current_speed
                        else:
                            self.direction_vector.y = 1
                            self.hitbox.y += self.current_speed
                        self.health -= sprite.collision_damage

            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

        for particle in self.particle_sprites:
            if particle.hitbox.colliderect(self.hitbox):
                if 'hurt' not in self.state and not self.invulnerable and particle.affects_player:
                    # Shield test
                    if ((self.direction_label == 'up' and particle.direction_vector.y > 0)
                            or (self.direction_label == 'down' and particle.direction_vector.y < 0)
                            or (self.direction_label == 'left' and particle.direction_vector.x > 0)
                            or (self.direction_label == 'right' and particle.direction_vector.x < 0)):
                        # Successful block ! Should add a sound
                        particle.kill()
                    else:
                        self.state = 'hurt_p'
                        self.hurt_starting_time = pygame.time.get_ticks()
                        self.hurt_animation_starting_time = self.hurt_starting_time
                        self.invulnerable = True
                        self.direction_vector = particle.direction_vector
                        self.hitbox.x += self.current_speed*self.direction_vector.x
                        self.hitbox.y += self.current_speed*self.direction_vector.y
                        self.health -= particle.collision_damage
                        particle.kill()

    def move(self):
        if self.direction_vector.magnitude() != 0:
            self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision('vertical')

        if not self.isDead:
            self.rect.center = self.hitbox.center

    def set_player_death_state(self, state):
        if state == 'hurt':
            self.state = state
            self.hurt_starting_time = pygame.time.get_ticks()
        elif state == 'gray':
            self.state = state
        elif state == 'despawn':
            self.state = state
            self.despawn_animation_starting_time = pygame.time.get_ticks()
        else:
            debug(f'trying to change player state in death to : {state}. Does not exist')

    def animate(self):
        current_time = pygame.time.get_ticks()
        if self.state == 'idle':
            # Stops all animation, resetting to 1st walking frame of the current direction
            self.image = self.walking_animations[self.direction_label][0]
        elif self.state == 'walking':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
            if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
                self.walking_animation_starting_time = pygame.time.get_ticks()
                if self.walking_animation_frame_count < PLAYER_WALKING_FRAMES-1:
                    self.walking_animation_frame_count += 1
                else:
                    self.walking_animation_frame_count = 0
        elif self.state == 'attacking' or self.state == 'casting':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.action_animations[self.direction_label][self.action_animation_frame_count]
            if current_time - self.action_animation_starting_time >= self.action_animation_cooldown:
                self.action_animation_starting_time = pygame.time.get_ticks()
                if self.action_animation_frame_count < PLAYER_ACTION_FRAMES-1:
                    self.action_animation_frame_count += 1
                else:
                    self.action_animation_frame_count = 0
        elif self.state == 'pickup_minor':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.pickup_minor_animation[self.pickup_minor_animation_frame_count]
            if current_time - self.pickup_minor_animation_starting_time >= self.pickup_minor_animation_cooldown:
                self.pickup_minor_animation_starting_time = pygame.time.get_ticks()
                if self.pickup_minor_animation_frame_count < PLAYER_PICKUP_MINOR_FRAMES-1:
                    self.pickup_minor_animation_frame_count += 1
                else:
                    self.pickup_minor_animation_frame_count = 0
        elif self.state == 'pickup_major':
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.pickup_major_animation[self.pickup_major_animation_frame_count]
            if current_time - self.pickup_major_animation_starting_time >= self.pickup_major_animation_cooldown:
                self.pickup_major_animation_starting_time = pygame.time.get_ticks()
                if self.pickup_major_animation_frame_count < PLAYER_PICKUP_MAJOR_FRAMES-1:
                    self.pickup_major_animation_frame_count += 1
                else:
                    self.pickup_major_animation_frame_count = 0
        elif 'hurt' in self.state:
            # Going through the motions of multiple frames, with a timer per frame
            self.image = self.hurt_animations[self.direction_label][self.hurt_animation_frame_count]
            if current_time - self.hurt_animation_starting_time >= self.hurt_animation_cooldown:
                self.hurt_animation_starting_time = pygame.time.get_ticks()
                if self.hurt_animation_frame_count < PLAYER_HURT_FRAMES-1:
                    self.hurt_animation_frame_count += 1
                else:
                    self.hurt_animation_frame_count = 0
        elif self.state == 'gray':
            # be gray
            self.image = self.gray_animation['down'][0]
        elif self.state == 'despawn':
            self.image = self.despawn_animation[self.despawn_animation_frame_count]
            if current_time - self.despawn_animation_starting_time >= self.despawn_animation_cooldown:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                if self.despawn_animation_frame_count < PLAYER_DEATH_FRAMES-1:
                    self.despawn_animation_frame_count += 1
                else:
                    self.despawn_animation_frame_count = 0
        else:
            debug(f'Error : animate({self.state}) does not exist')

    def update(self):
        if not self.isDead:
            if 'hurt' not in self.state:
                self.input()
                self.current_speed = self.speed
            else:
                self.current_speed = (PLAYER_HURT_FRAMES - self.hurt_animation_frame_count)
            self.move()
            self.animate()
            self.cooldowns()
            if self.health <= 0:
                self.isDead = True
        else:
            self.animate()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)
