import abc
import pygame
import random
import tileset
import level as game
from settings import *
from entities import Entity
from particles import Rock, Arrow, MagicMissile


# Known issue : Monster waits for STATE_ACTION to end before getting hurt
class Enemy(Entity):
    def __init__(self, groups, visible_sprites, obstacle_sprites, particle_sprites, uses_projectiles=False):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites)

        self.direction_label = random.choice([UP_LABEL, DOWN_LABEL, LEFT_LABEL, RIGHT_LABEL])
        self.state = ''
        self.speed = 1
        self.can_dive = False
        self.is_above_ground = True

        # Initialisation of values common to all Enemy used to load the different animations
        self.dive_animations = []
        self.dive_frames = 0
        self.dive_frame_id = 0
        self.rise_animations = []
        self.rise_frames = 0
        self.rise_frame_id = 0
        self.hurt_frames = MONSTER_HURT_FRAMES
        self.spawn_frames = MONSTER_SPAWN_FRAMES
        self.spawn_frame_id = MONSTER_SPAWN_FRAME_ID
        self.despawn_frames = MONSTER_DEATH_FRAMES
        self.despawn_frame_id = MONSTER_DEATH_FRAME_ID

        # Monster actions cooldowns
        # Monsters always move, except if shooting, or special mechanic such as flying, jumping, diving(water/land)
        self.uses_projectiles = uses_projectiles
        self.can_attack = self.uses_projectiles
        self.has_attacked = True
        self.attack_range_start = MONSTER_ATTACK_RANGE_START
        self.attack_range_stop = MONSTER_ATTACK_RANGE_STOP
        self.attack_cooldown = random.randrange(self.attack_range_start, self.attack_range_stop, 100)
        self.attack_starting_time = pygame.time.get_ticks()
        self.can_move = True
        self.direction_cooldown = 200
        self.direction_starting_time = 0
        self.hurt_starting_time = 0
        self.hurt_animation_cooldown = MONSTER_HURT_ANIMATION_COOLDOWN
        self.hurt_cooldown = (MONSTER_HURT_FRAMES + 1) * self.hurt_animation_cooldown
        self.dive_cooldown = 0
        self.dive_starting_time = 0
        self.rise_cooldown = 0
        self.rise_starting_time = 0

        self.spawn_animation_frame_count = 0
        self.spawn_animation_starting_time = 0
        self.spawn_animation_cooldown = MONSTER_SPAWN_ANIMATION_COOLDOWN
        self.despawn_animation_frame_count = 0
        self.despawn_animation_starting_time = 0
        self.despawn_animation_cooldown = MONSTER_DEATH_ANIMATION_COOLDOWN

        self.above_ground_starting_time = pygame.time.get_ticks()
        self.under_ground_starting_time = 0
        self.above_ground_cooldown = MONSTER_ABOVE_GROUND_COOLDOWN
        self.under_ground_cooldown = MONSTER_UNDER_GROUND_COOLDOWN
        self.dive_animation_starting_time = 0
        self.dive_animation_frame_count = 0
        self.dive_animation_cooldown = 0
        self.rise_animation_starting_time = pygame.time.get_ticks()
        self.rise_animation_frame_count = 0
        self.rise_animation_cooldown = 0

        # Sounds
        self.monster_hurt_sound = pygame.mixer.Sound(SOUND_MONSTER_HURT)
        self.monster_hurt_sound.set_volume(0.3)
        self.monster_despawn_sound = pygame.mixer.Sound(SOUND_MONSTER_DESPAWN)
        self.monster_despawn_sound.set_volume(0.3)

        # Monster stats
        self.health = 0
        self.collision_damage = 0
        self.invulnerable = False
        self.current_speed = self.speed
        self.isSpawned = False
        self.isDead = False
        self.deathPlayed = False

    @abc.abstractmethod
    def load_dive_frames(self, enemies_tile_set):
        for i in range(self.dive_frames):
            tile_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.rise_animations.append(
                enemies_tile_set.get_sprite_image(self.rise_frame_id + tile_offset))
            self.dive_animations.insert(
                0,
                enemies_tile_set.get_sprite_image(self.dive_frame_id + tile_offset))

    @abc.abstractmethod
    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)
        if self.can_dive:
            self.load_dive_frames(enemies_tile_set)

    @abc.abstractmethod
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Monster can shoot if he isn't in the hurt animation. Attack cooldown is randomized
        if self.uses_projectiles and STATE_HURT not in self.state:
            if self.has_attacked:
                if current_time - self.attack_starting_time >= self.attack_cooldown:
                    self.has_attacked = False
                    self.attack_cooldown = random.randrange(self.attack_range_start, self.attack_range_stop, 100)
                if self.state == STATE_ACTION:
                    if current_time - self.attack_starting_time >= self.action_animation_cooldown * 2:
                        self.state = STATE_WALKING
        # Hurt monster is invulnerable during animation, this is reset here
        if STATE_HURT in self.state:
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = STATE_WALKING
                self.invulnerable = False
                self.hurt_animation_frame_count = 0

    @abc.abstractmethod
    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    @abc.abstractmethod
    def animate(self):
        if not self.isSpawned:
            self.spawn_animation_starting_time, self.spawn_animation_frame_count = (
                self.change_animation_frame(self.spawn_animation,
                                            self.spawn_animation_frame_count,
                                            self.spawn_animation_starting_time,
                                            self.spawn_animation_cooldown,
                                            MONSTER_SPAWN_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.isSpawned = True
                self.state = STATE_WALKING
        elif not self.isDead:
            super().animate()
        else:
            self.hitbox = self.rect.inflate(-TILE_SIZE * 2, -TILE_SIZE * 2)
            self.despawn_animation_starting_time, self.despawn_animation_frame_count = (
                self.change_animation_frame(self.despawn_animation,
                                            self.despawn_animation_frame_count,
                                            self.despawn_animation_starting_time,
                                            self.despawn_animation_cooldown,
                                            MONSTER_DEATH_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.deathPlayed = True

    @abc.abstractmethod
    # Monsters don't collide with other Monsters : NES compliant
    # Monsters don't collide with particles. Particles collide with enemies
    def collision(self, direction):
        if direction == HORIZONTAL_LABEL:
            for sprite in self.obstacle_sprites:
                if (sprite.hitbox.colliderect(self.hitbox)
                        and sprite.type != LIMIT_LADDER_INDEX
                        and sprite.type != LIMIT_LAKE_BORDER_INDEX):
                    if self.direction_vector.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == VERTICAL_LABEL:
            for sprite in self.obstacle_sprites:
                if (sprite.hitbox.colliderect(self.hitbox)
                        and sprite.type != LIMIT_LADDER_INDEX
                        and sprite.type != LIMIT_LAKE_BORDER_INDEX):
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    @abc.abstractmethod
    def move(self):
        if self.state == STATE_WALKING:
            if self.direction_label == UP_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            elif self.direction_label == DOWN_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            elif self.direction_label == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0
            elif self.direction_label == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            else:
                # Illegal move, ignore
                return

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision(VERTICAL_LABEL)

        self.rect.center = self.hitbox.center

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def take_damage(self, amount, direction):
        if self.isSpawned and STATE_HURT not in self.state and not self.invulnerable:
            self.state = STATE_HURT
            self.hurt_starting_time = pygame.time.get_ticks()
            self.hurt_animation_starting_time = self.hurt_starting_time
            self.invulnerable = True

            # If origin of damage is static, enemy is pushed back to where he came from
            if direction == '':
                if self.direction_label == UP_LABEL:
                    direction = DOWN_LABEL
                elif self.direction_label == RIGHT_LABEL:
                    direction = LEFT_LABEL
                elif self.direction_label == DOWN_LABEL:
                    direction = UP_LABEL
                else:
                    direction = RIGHT_LABEL

            if direction == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0
                self.hitbox.x -= self.current_speed
                self.direction_label = RIGHT_LABEL
            elif direction == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
                self.hitbox.x += self.current_speed
                self.direction_label = LEFT_LABEL
            elif direction == UP_LABEL:
                self.direction_vector.y = -1
                self.direction_vector.x = 0
                self.hitbox.y -= self.current_speed
                self.direction_label = DOWN_LABEL
            else:
                self.direction_vector.y = 1
                self.direction_vector.x = 0
                self.hitbox.y += self.current_speed
                self.direction_label = UP_LABEL

            self.health -= amount
            if self.health > 0:
                self.monster_hurt_sound.play()

    @abc.abstractmethod
    def update(self):
        current_time = pygame.time.get_ticks()

        # Attacks interrupt movements if available.
        if STATE_HURT not in self.state:
            self.current_speed = self.speed
            if (self.isSpawned
                    and self.state == STATE_WALKING
                    and current_time - self.direction_starting_time >= self.direction_cooldown):
                self.direction_label = random.choice([UP_LABEL, DOWN_LABEL, LEFT_LABEL, RIGHT_LABEL])
                self.direction_starting_time = current_time
                self.direction_cooldown = random.randrange(500, 2000, 100)
            if self.isSpawned and self.can_attack and not self.has_attacked:
                self.state = STATE_ACTION
                self.attack_starting_time = current_time
        else:
            # While hurt, Monster is repelled with a fading speed
            self.current_speed = (MONSTER_HURT_FRAMES - self.hurt_animation_frame_count)
        if self.isSpawned and not self.isDead:
            if self.state == STATE_ACTION and not self.has_attacked:
                self.attack()
                self.has_attacked = True
            elif self.state != STATE_ACTION:
                self.move()
            if self.health <= 0:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                self.isDead = True
                self.monster_despawn_sound.play()

        self.animate()
        self.cooldowns()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class RedOctorock(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.walking_frames = OCTOROCK_WALKING_FRAMES
        self.action_frames = OCTOROCK_WALKING_FRAMES
        self.is_up_y_flipped = True
        self.is_up_action_y_flipped = True
        self.is_right_x_flipped = True
        self.walking_up_frame_id = RED_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_down_frame_id = RED_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = RED_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.walking_right_frame_id = RED_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_up_frame_id = RED_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_down_frame_id = RED_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_left_frame_id = RED_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_right_frame_id = RED_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.hurt_up_frame_id = OCTOROCK_HURT_DOWN_FRAME_ID
        self.hurt_down_frame_id = OCTOROCK_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = OCTOROCK_HURT_LEFT_FRAME_ID
        self.hurt_right_frame_id = OCTOROCK_HURT_LEFT_FRAME_ID

        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Red Octorock Stats
        self.health = RED_OCTOROCK_HEALTH
        self.collision_damage = RED_OCTOROCK_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = OCTOROCK_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = OCTOROCK_ACTION_ANIMATION_COOLDOWN

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        super().cooldowns()

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        super().animate()

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def attack(self):
        Rock(self.rect.topleft,
             self.direction_vector,
             [self.visible_sprites, self.particle_sprites],
             self.direction_label,
             self.obstacle_sprites)

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        super().update()


class BlueOctorock(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.walking_frames = OCTOROCK_WALKING_FRAMES
        self.action_frames = OCTOROCK_WALKING_FRAMES
        self.is_up_y_flipped = True
        self.is_up_action_y_flipped = True
        self.is_right_x_flipped = True
        self.walking_up_frame_id = BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_down_frame_id = BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = BLUE_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.walking_right_frame_id = BLUE_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_up_frame_id = BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_down_frame_id = BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_left_frame_id = BLUE_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_right_frame_id = BLUE_OCTOROCK_WALKING_LEFT_FRAME_ID
        self.hurt_up_frame_id = OCTOROCK_HURT_DOWN_FRAME_ID
        self.hurt_down_frame_id = OCTOROCK_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = OCTOROCK_HURT_LEFT_FRAME_ID
        self.hurt_right_frame_id = OCTOROCK_HURT_LEFT_FRAME_ID

        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Red Octorock Stats
        self.health = BLUE_OCTOROCK_HEALTH
        self.collision_damage = BLUE_OCTOROCK_DMG
        self.speed = BLUE_OCTOROCK_SPEED

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = OCTOROCK_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = OCTOROCK_ACTION_ANIMATION_COOLDOWN
        self.attack_range_start = BLUE_OCTOROCK_ATTACK_RANGE_START
        self.attack_range_stop = BLUE_OCTOROCK_ATTACK_RANGE_STOP

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        super().cooldowns()

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        super().animate()

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def attack(self):
        # Rock is aimed "towards" the player, not randomly.
        # Still on a mutually exclusive x/y-axis, not like Zora shots
        x_displacement = self.rect.centerx - game.Level().player.rect.centerx
        y_displacement = self.rect.centery - game.Level().player.rect.centery
        direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
        if direction_vector.magnitude() != 0:
            direction_vector = direction_vector.normalize()
        if abs(direction_vector.x) >= abs(direction_vector.y):
            if direction_vector.x >= 0:
                self.direction_label = RIGHT_LABEL
            else:
                self.direction_label = LEFT_LABEL
        else:
            if direction_vector.y >= 0:
                self.direction_label = DOWN_LABEL
            else:
                self.direction_label = UP_LABEL
        self.animate()

        Rock(self.rect.topleft,
             self.direction_vector,
             [self.visible_sprites, self.particle_sprites],
             self.direction_label,
             self.obstacle_sprites)

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        super().update()


class RedMoblin(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.walking_frames = MOBLIN_WALKING_FRAMES
        self.action_frames = MOBLIN_WALKING_FRAMES
        self.is_right_x_flipped = True
        self.is_walking_animation_x_flipped = True
        self.is_action_animation_x_flipped = True
        self.walking_up_frame_id = RED_MOBLIN_WALKING_UP_FRAME_ID
        self.walking_down_frame_id = RED_MOBLIN_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = RED_MOBLIN_WALKING_LEFT_FRAME_ID
        self.walking_right_frame_id = RED_MOBLIN_WALKING_LEFT_FRAME_ID
        self.action_up_frame_id = RED_MOBLIN_WALKING_UP_FRAME_ID
        self.action_down_frame_id = RED_MOBLIN_WALKING_DOWN_FRAME_ID
        self.action_left_frame_id = RED_MOBLIN_WALKING_LEFT_FRAME_ID
        self.action_right_frame_id = RED_MOBLIN_WALKING_LEFT_FRAME_ID
        self.hurt_up_frame_id = MOBLIN_HURT_UP_FRAME_ID
        self.hurt_down_frame_id = MOBLIN_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = MOBLIN_HURT_LEFT_FRAME_ID
        self.hurt_right_frame_id = MOBLIN_HURT_LEFT_FRAME_ID

        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Red Octorock Stats
        self.health = RED_MOBLIN_HEALTH
        self.collision_damage = RED_MOBLIN_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = MOBLIN_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = MOBLIN_ACTION_ANIMATION_COOLDOWN

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        super().cooldowns()

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        super().animate()

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def attack(self):
        Arrow(self.rect.topleft,
              self.direction_vector,
              [self.visible_sprites, self.particle_sprites],
              self.direction_label,
              self.obstacle_sprites)

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        super().update()


class BlackMoblin(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.walking_frames = MOBLIN_WALKING_FRAMES
        self.action_frames = MOBLIN_WALKING_FRAMES
        self.is_right_x_flipped = True
        self.is_walking_animation_x_flipped = True
        self.is_action_animation_x_flipped = True
        self.walking_up_frame_id = BLACK_MOBLIN_WALKING_UP_FRAME_ID
        self.walking_down_frame_id = BLACK_MOBLIN_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = BLACK_MOBLIN_WALKING_LEFT_FRAME_ID
        self.walking_right_frame_id = BLACK_MOBLIN_WALKING_LEFT_FRAME_ID
        self.action_up_frame_id = BLACK_MOBLIN_WALKING_UP_FRAME_ID
        self.action_down_frame_id = BLACK_MOBLIN_WALKING_DOWN_FRAME_ID
        self.action_left_frame_id = BLACK_MOBLIN_WALKING_LEFT_FRAME_ID
        self.action_right_frame_id = BLACK_MOBLIN_WALKING_LEFT_FRAME_ID
        self.hurt_up_frame_id = MOBLIN_HURT_UP_FRAME_ID
        self.hurt_down_frame_id = MOBLIN_HURT_DOWN_FRAME_ID
        self.hurt_left_frame_id = MOBLIN_HURT_LEFT_FRAME_ID
        self.hurt_right_frame_id = MOBLIN_HURT_LEFT_FRAME_ID

        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Red Octorock Stats
        self.health = BLACK_MOBLIN_HEALTH
        self.collision_damage = BLACK_MOBLIN_DMG
        self.speed = BLACK_MOBLIN_SPEED

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = MOBLIN_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = MOBLIN_ACTION_ANIMATION_COOLDOWN
        self.attack_range_start = BLACK_MOBLIN_ATTACK_RANGE_START
        self.attack_range_stop = BLACK_MOBLIN_ATTACK_RANGE_STOP

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        super().cooldowns()

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        super().animate()

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def attack(self):
        # Arrow is aimed "towards" the player, not randomly.
        # Still on a mutually exclusive x/y-axis, not like Zora shots
        x_displacement = self.rect.centerx - game.Level().player.rect.centerx
        y_displacement = self.rect.centery - game.Level().player.rect.centery
        direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
        if direction_vector.magnitude() != 0:
            direction_vector = direction_vector.normalize()
        if abs(direction_vector.x) >= abs(direction_vector.y):
            if direction_vector.x >= 0:
                self.direction_label = RIGHT_LABEL
            else:
                self.direction_label = LEFT_LABEL
        else:
            if direction_vector.y >= 0:
                self.direction_label = DOWN_LABEL
            else:
                self.direction_label = UP_LABEL
        self.animate()

        Arrow(self.rect.topleft,
              direction_vector,
              [self.visible_sprites, self.particle_sprites],
              self.direction_label,
              self.obstacle_sprites)

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        super().update()


class Stalfos(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.walking_frames = STALFOS_WALKING_FRAMES
        self.action_frames = STALFOS_WALKING_FRAMES
        self.walking_frame_id = STALFOS_WALKING_FRAME_ID
        self.action_frame_id = STALFOS_WALKING_FRAME_ID
        self.hurt_frame_id = STALFOS_HURT_FRAME_ID

        self.walking_animations = []
        self.action_animations = []
        self.hurt_animations = []
        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

        # Stalfos Stats
        self.health = STALFOS_HEALTH
        self.collision_damage = STALFOS_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = STALFOS_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = STALFOS_ACTION_ANIMATION_COOLDOWN

        self.player_seeking_starting_time = pygame.time.get_ticks()
        self.random_starting_time = pygame.time.get_ticks()
        self.random_duration = STALFOS_RANDOM_DURATION
        self.player_seeking_duration = STALFOS_PLAYER_SEEKING_DURATION

    def load_walking_frames(self, entity_tile_set):
        self.walking_animations.append(
            entity_tile_set.get_sprite_image(self.walking_frame_id))
        self.walking_animations.append(
            pygame.transform.flip(entity_tile_set.get_sprite_image(self.walking_frame_id),
                                  True,
                                  False))

    def load_action_frames(self, entity_tile_set):
        self.action_animations.append(
            entity_tile_set.get_sprite_image(self.action_frame_id))
        self.action_animations.append(
            pygame.transform.flip(entity_tile_set.get_sprite_image(self.action_frame_id),
                                  True,
                                  False))

    def load_hurt_frames(self, entity_tile_set):
        for i in range(self.hurt_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.hurt_animations.append(
                entity_tile_set.get_sprite_image(self.hurt_frame_id + tiles_offset))

    def load_dive_frames(self, enemies_tile_set):
        pass

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Hurt monster is invulnerable during animation, this is reset here
        if STATE_HURT in self.state:
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = STATE_IDLE
                self.random_starting_time = current_time
                self.invulnerable = False
                self.hurt_animation_frame_count = 0
        elif self.state == STATE_WALKING:
            if current_time - self.player_seeking_starting_time >= self.player_seeking_duration:
                self.random_starting_time = current_time
                self.state = STATE_IDLE
        elif self.state == STATE_IDLE:
            if current_time - self.random_starting_time >= self.random_duration:
                self.player_seeking_starting_time = current_time
                self.state = STATE_WALKING

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        if not self.isSpawned:
            self.spawn_animation_starting_time, self.spawn_animation_frame_count = (
                self.change_animation_frame(self.spawn_animation,
                                            self.spawn_animation_frame_count,
                                            self.spawn_animation_starting_time,
                                            self.spawn_animation_cooldown,
                                            MONSTER_SPAWN_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.isSpawned = True
        elif not self.isDead:
            if self.state == STATE_WALKING or self.state == STATE_IDLE:
                self.walking_animation_starting_time, self.walking_animation_frame_count = (
                    self.change_animation_frame(self.walking_animations,
                                                self.walking_animation_frame_count,
                                                self.walking_animation_starting_time,
                                                self.walking_animation_cooldown,
                                                self.walking_frames))
            elif STATE_HURT in self.state:
                self.hurt_animation_starting_time, self.hurt_animation_frame_count = (
                    self.change_animation_frame(self.hurt_animations,
                                                self.hurt_animation_frame_count,
                                                self.hurt_animation_starting_time,
                                                self.hurt_animation_cooldown,
                                                self.hurt_frames,
                                                False))
        else:
            self.hitbox = self.rect.inflate(-TILE_SIZE * 2, -TILE_SIZE * 2)
            self.despawn_animation_starting_time, self.despawn_animation_frame_count = (
                self.change_animation_frame(self.despawn_animation,
                                            self.despawn_animation_frame_count,
                                            self.despawn_animation_starting_time,
                                            self.despawn_animation_cooldown,
                                            MONSTER_DEATH_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.deathPlayed = True

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        if self.state == STATE_IDLE:
            if self.direction_label == UP_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            elif self.direction_label == DOWN_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            elif self.direction_label == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0
            elif self.direction_label == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            else:
                # Illegal move, ignore
                return
        elif self.state == STATE_WALKING:
            x_displacement = self.rect.centerx - game.Level().player.rect.centerx
            y_displacement = self.rect.centery - game.Level().player.rect.centery
            self.direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
            if self.direction_vector.magnitude() != 0:
                self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision(VERTICAL_LABEL)

        self.rect.center = self.hitbox.center

    def attack(self):
        pass

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.isSpawned and not self.isDead:
            if (self.state == STATE_IDLE
                    and self.isSpawned
                    and current_time - self.direction_starting_time >= self.direction_cooldown):
                self.direction_label = random.choice([UP_LABEL, DOWN_LABEL, LEFT_LABEL, RIGHT_LABEL])
                self.direction_starting_time = current_time
                self.direction_cooldown = random.randrange(500, 2000, 100)

            self.move()

            if self.health <= 0:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                self.isDead = True
                self.monster_despawn_sound.play()

        self.animate()
        self.cooldowns()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Zora(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.can_dive = True
        self.direction_label = DOWN_LABEL

        self.dive_frames = ZORA_DIVE_FRAMES
        self.rise_frames = ZORA_DIVE_FRAMES
        self.walking_frames = ZORA_WALKING_FRAMES
        self.action_frames = ZORA_WALKING_FRAMES
        self.walking_up_frame_id = ZORA_WALKING_UP_FRAME_ID
        self.walking_down_frame_id = ZORA_WALKING_DOWN_FRAME_ID
        self.action_up_frame_id = ZORA_WALKING_UP_FRAME_ID
        self.action_down_frame_id = ZORA_WALKING_DOWN_FRAME_ID
        self.hurt_up_frame_id = ZORA_HURT_UP_FRAME_ID
        self.hurt_down_frame_id = ZORA_HURT_DOWN_FRAME_ID
        self.dive_frame_id = ZORA_DIVE_FRAME_ID
        self.rise_frame_id = ZORA_DIVE_FRAME_ID

        self.walking_animations = {
            UP_LABEL: [],
            DOWN_LABEL: []
        }
        self.action_animations = {
            UP_LABEL: [],
            DOWN_LABEL: []
        }
        self.hurt_animations = {
            UP_LABEL: [],
            DOWN_LABEL: []
        }
        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Zora Stats
        self.health = ZORA_HEALTH
        self.collision_damage = ZORA_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = ZORA_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = ZORA_ACTION_ANIMATION_COOLDOWN
        self.dive_animation_cooldown = ZORA_DIVE_ANIMATION_COOLDOWN
        self.rise_animation_cooldown = ZORA_DIVE_ANIMATION_COOLDOWN

        self.above_ground_starting_time = pygame.time.get_ticks()
        self.has_attacked = False
        self.attack_cooldown = MONSTER_ABOVE_GROUND_COOLDOWN // 2
        self.dive_cooldown = ZORA_DIVE_ANIMATION_COOLDOWN * ZORA_DIVE_FRAMES
        self.rise_cooldown = ZORA_DIVE_ANIMATION_COOLDOWN * ZORA_DIVE_FRAMES

    def load_walking_frames(self, entity_tile_set):
        for i in range(self.walking_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.walking_animations[UP_LABEL].append(
                entity_tile_set.get_sprite_image(self.walking_up_frame_id + tiles_offset))
            self.walking_animations[DOWN_LABEL].append(
                entity_tile_set.get_sprite_image(self.walking_down_frame_id + tiles_offset))

    def load_action_frames(self, entity_tile_set):
        for i in range(self.action_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.action_animations[UP_LABEL].append(
                entity_tile_set.get_sprite_image(self.action_up_frame_id + tiles_offset))
            self.action_animations[DOWN_LABEL].append(
                entity_tile_set.get_sprite_image(self.action_down_frame_id + tiles_offset))

    def load_hurt_frames(self, entity_tile_set):
        for i in range(self.hurt_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.hurt_animations[UP_LABEL].append(
                entity_tile_set.get_sprite_image(self.hurt_up_frame_id + tiles_offset))
            self.hurt_animations[DOWN_LABEL].append(
                entity_tile_set.get_sprite_image(self.hurt_down_frame_id + tiles_offset))

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.state == STATE_RISING:
            if current_time - self.rise_starting_time >= self.rise_cooldown:
                self.invulnerable = False
                self.state = STATE_WALKING
                if self.rect.y <= game.Level().player.hitbox.centery:
                    self.direction_label = DOWN_LABEL
                else:
                    self.direction_label = UP_LABEL
        elif self.state == STATE_DIVING:
            self.invulnerable = True
            if current_time - self.dive_starting_time >= self.dive_cooldown:
                self.state = STATE_IDLE
        elif self.is_above_ground:
            # Hurt monster is invulnerable during animation, this is reset here
            if STATE_HURT in self.state:
                if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                    self.state = STATE_WALKING
                    self.invulnerable = False
                    self.hurt_animation_frame_count = 0
            elif current_time - self.above_ground_starting_time >= self.above_ground_cooldown:
                self.state = STATE_DIVING
                self.is_above_ground = False
                self.has_attacked = False
                self.under_ground_starting_time = current_time
                self.dive_starting_time = current_time
        else:
            if current_time - self.under_ground_starting_time >= self.under_ground_cooldown:
                self.state = STATE_RISING
                self.is_above_ground = True
                self.above_ground_starting_time = current_time
                self.rise_starting_time = current_time

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        super().animate()
        if self.state == STATE_DIVING:
            self.dive_animation_starting_time, self.dive_animation_frame_count = (
                self.change_animation_frame(self.dive_animations,
                                            self.dive_animation_frame_count,
                                            self.dive_animation_starting_time,
                                            self.dive_animation_cooldown,
                                            self.dive_frames))
        elif self.state == STATE_RISING:
            self.rise_animation_starting_time, self.rise_animation_frame_count = (
                self.change_animation_frame(self.rise_animations,
                                            self.rise_animation_frame_count,
                                            self.rise_animation_starting_time,
                                            self.rise_animation_cooldown,
                                            self.rise_frames))

    def collision(self, direction):
        if direction == HORIZONTAL_LABEL:
            for obstacle in self.obstacle_sprites:
                if obstacle.hitbox.colliderect(self.hitbox) and obstacle.type != LIMIT_WATER_INDEX:
                    if self.direction_vector.x > 0:
                        self.hitbox.right = obstacle.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = obstacle.hitbox.right

        elif direction == VERTICAL_LABEL:
            for obstacle in self.obstacle_sprites:
                if obstacle.hitbox.colliderect(self.hitbox) and obstacle.type != LIMIT_WATER_INDEX:
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = obstacle.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = obstacle.hitbox.bottom

    def move(self):
        if self.state == STATE_IDLE:
            if self.direction_label == UP_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            elif self.direction_label == DOWN_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            elif self.direction_label == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0
            elif self.direction_label == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            else:
                # Illegal move, ignore
                return

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision(VERTICAL_LABEL)

        self.rect.center = self.hitbox.center

    def attack(self):
        MagicMissile(self.rect.topleft,
                     self.direction_vector,
                     [self.visible_sprites, self.particle_sprites],
                     self.obstacle_sprites)

    def take_damage(self, amount, direction):
        if self.isSpawned and STATE_HURT not in self.state and not self.invulnerable:
            self.state = STATE_HURT
            self.hurt_starting_time = pygame.time.get_ticks()
            self.hurt_animation_starting_time = self.hurt_starting_time
            self.invulnerable = True

            # Zora isn't fazed by your attack, he isn't pushed anywhere.
            # But, still, it hurts.
            self.health -= amount
            if self.health > 0:
                self.monster_hurt_sound.play()

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.isSpawned and not self.isDead:
            if self.is_above_ground:
                if self.state == STATE_WALKING:
                    if (not self.has_attacked
                            and current_time - self.above_ground_starting_time >= self.attack_cooldown):
                        self.has_attacked = True
                        self.attack()
            else:
                if (self.isSpawned
                        and current_time - self.direction_starting_time >= self.direction_cooldown):
                    self.direction_label = random.choice([UP_LABEL, DOWN_LABEL, LEFT_LABEL, RIGHT_LABEL])
                    self.direction_starting_time = current_time
                    self.direction_cooldown = random.randrange(500, 2000, 100)
                self.move()
            if self.health <= 0:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                self.isDead = True
                self.monster_despawn_sound.play()

        self.animate()
        self.cooldowns()

        if self.state != STATE_IDLE:
            pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Leever(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, True)

        self.can_dive = True

        self.dive_frames = LEEVER_DIVE_FRAMES
        self.rise_frames = LEEVER_DIVE_FRAMES
        self.walking_frames = LEEVER_WALKING_FRAMES
        self.action_frames = LEEVER_WALKING_FRAMES
        self.walking_frame_id = LEEVER_WALKING_FRAME_ID
        self.action_frame_id = LEEVER_WALKING_FRAME_ID
        self.hurt_frame_id = LEEVER_HURT_FRAME_ID
        self.dive_frame_id = LEEVER_DIVE_FRAME_ID
        self.rise_frame_id = LEEVER_DIVE_FRAME_ID

        self.walking_animations = []
        self.action_animations = []
        self.hurt_animations = []
        self.load_animation_frames(tileset.ENEMIES_TILE_SET)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Leever Stats
        self.health = LEEVER_HEALTH
        self.collision_damage = LEEVER_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = LEEVER_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = LEEVER_ACTION_ANIMATION_COOLDOWN
        self.dive_animation_cooldown = LEEVER_DIVE_ANIMATION_COOLDOWN
        self.rise_animation_cooldown = LEEVER_DIVE_ANIMATION_COOLDOWN

        self.above_ground_starting_time = pygame.time.get_ticks()
        self.dive_cooldown = LEEVER_DIVE_ANIMATION_COOLDOWN * LEEVER_DIVE_FRAMES
        self.rise_cooldown = LEEVER_DIVE_ANIMATION_COOLDOWN * LEEVER_DIVE_FRAMES

    def load_walking_frames(self, entity_tile_set):
        for i in range(self.walking_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.walking_animations.append(
                entity_tile_set.get_sprite_image(self.walking_frame_id + tiles_offset))

    def load_action_frames(self, entity_tile_set):
        for i in range(self.action_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.action_animations.append(
                entity_tile_set.get_sprite_image(self.action_frame_id + tiles_offset))

    def load_hurt_frames(self, entity_tile_set):
        for i in range(self.hurt_frames):
            tiles_offset = (SPRITE_SIZE // TILE_SIZE) * i
            self.hurt_animations.append(
                entity_tile_set.get_sprite_image(self.hurt_frame_id + tiles_offset))

    def load_dive_frames(self, enemies_tile_set):
        super().load_dive_frames(enemies_tile_set)

    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.state == STATE_RISING:
            if current_time - self.rise_starting_time >= self.rise_cooldown:
                self.invulnerable = False
                self.state = STATE_WALKING
        elif self.state == STATE_DIVING:
            self.invulnerable = True
            if current_time - self.dive_starting_time >= self.dive_cooldown:
                self.state = STATE_IDLE
        elif self.is_above_ground:
            # Hurt monster is invulnerable during animation, this is reset here
            if STATE_HURT in self.state:
                if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                    self.state = STATE_WALKING
                    self.invulnerable = False
                    self.hurt_animation_frame_count = 0
            elif current_time - self.above_ground_starting_time >= self.above_ground_cooldown:
                self.state = STATE_DIVING
                self.dive_animation_frame_count = 0
                self.is_above_ground = False
                self.under_ground_starting_time = current_time
                self.dive_starting_time = current_time
                self.dive_animation_starting_time = current_time
        else:
            if current_time - self.under_ground_starting_time >= self.under_ground_cooldown:
                self.state = STATE_RISING
                self.rise_animation_frame_count = 0
                self.is_above_ground = True
                self.above_ground_starting_time = current_time
                self.rise_starting_time = current_time
                self.rise_animation_starting_time = current_time

    def change_animation_frame(self,
                               animation_list,
                               animation_frame_count,
                               animation_starting_time,
                               animation_cooldown,
                               animation_frames_nb,
                               reset_for_loop=True,
                               idle_after=False):
        return super().change_animation_frame(animation_list,
                                              animation_frame_count,
                                              animation_starting_time,
                                              animation_cooldown,
                                              animation_frames_nb,
                                              reset_for_loop,
                                              idle_after)

    def animate(self):
        if not self.isSpawned:
            self.spawn_animation_starting_time, self.spawn_animation_frame_count = (
                self.change_animation_frame(self.spawn_animation,
                                            self.spawn_animation_frame_count,
                                            self.spawn_animation_starting_time,
                                            self.spawn_animation_cooldown,
                                            MONSTER_SPAWN_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.isSpawned = True
                self.state = STATE_WALKING
        elif not self.isDead:
            if self.state == STATE_WALKING:
                self.walking_animation_starting_time, self.walking_animation_frame_count = (
                    self.change_animation_frame(self.walking_animations,
                                                self.walking_animation_frame_count,
                                                self.walking_animation_starting_time,
                                                self.walking_animation_cooldown,
                                                self.walking_frames))
            elif STATE_HURT in self.state:
                self.hurt_animation_starting_time, self.hurt_animation_frame_count = (
                    self.change_animation_frame(self.hurt_animations,
                                                self.hurt_animation_frame_count,
                                                self.hurt_animation_starting_time,
                                                self.hurt_animation_cooldown,
                                                self.hurt_frames,
                                                False))
            elif STATE_ACTION in self.state:
                self.action_animation_starting_time, self.action_animation_frame_count = (
                    self.change_animation_frame(self.action_animations,
                                                self.action_animation_frame_count,
                                                self.action_animation_starting_time,
                                                self.action_animation_cooldown,
                                                self.action_frames))
            elif self.state == STATE_DIVING:
                self.dive_animation_starting_time, self.dive_animation_frame_count = (
                    self.change_animation_frame(self.dive_animations,
                                                self.dive_animation_frame_count,
                                                self.dive_animation_starting_time,
                                                self.dive_animation_cooldown,
                                                self.dive_frames))
            elif self.state == STATE_RISING:
                self.rise_animation_starting_time, self.rise_animation_frame_count = (
                    self.change_animation_frame(self.rise_animations,
                                                self.rise_animation_frame_count,
                                                self.rise_animation_starting_time,
                                                self.rise_animation_cooldown,
                                                self.rise_frames))
        else:
            self.hitbox = self.rect.inflate(-TILE_SIZE * 2, -TILE_SIZE * 2)
            self.despawn_animation_starting_time, self.despawn_animation_frame_count = (
                self.change_animation_frame(self.despawn_animation,
                                            self.despawn_animation_frame_count,
                                            self.despawn_animation_starting_time,
                                            self.despawn_animation_cooldown,
                                            MONSTER_DEATH_FRAMES,
                                            True,
                                            True))
            if self.state == STATE_IDLE:
                self.deathPlayed = True

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        if self.state == STATE_IDLE:
            if self.direction_label == UP_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            elif self.direction_label == DOWN_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            elif self.direction_label == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0
            elif self.direction_label == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            else:
                # Illegal move, ignore
                return
        elif self.state == STATE_WALKING or self.state == STATE_RISING:
            x_displacement = self.rect.centerx - game.Level().player.rect.centerx
            y_displacement = self.rect.centery - game.Level().player.rect.centery
            self.direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
            if self.direction_vector.magnitude() != 0:
                self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision(VERTICAL_LABEL)

        self.rect.center = self.hitbox.center

    def attack(self):
        pass

    def take_damage(self, amount, direction):
        super().take_damage(amount, direction)

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.isSpawned and not self.isDead:
            if not self.is_above_ground:
                if (self.isSpawned
                        and current_time - self.direction_starting_time >= self.direction_cooldown):
                    self.direction_label = random.choice([UP_LABEL, DOWN_LABEL, LEFT_LABEL, RIGHT_LABEL])
                    self.direction_starting_time = current_time
                    self.direction_cooldown = random.randrange(500, 2000, 100)

            self.move()

            if self.health <= 0:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                self.isDead = True
                self.monster_despawn_sound.play()

        self.animate()
        self.cooldowns()

        if self.state != STATE_IDLE:
            pygame.display.get_surface().blit(self.image, self.rect.topleft)
