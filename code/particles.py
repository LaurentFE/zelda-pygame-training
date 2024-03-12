import abc
import random

import pygame
from settings import *
from abc import ABC


class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self, owner_pos, owner_direction_vector, groups):
        super().__init__(groups)

        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]
        self.owner_direction_vector = owner_direction_vector
        self.direction_vector = pygame.math.Vector2()
        self.speed = 0
        self.bypasses_shield = False

        self.image = None

        self.move_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.move_animation_cooldown = 100
        self.move_animation_timer_start = 0
        self.move_animation_frame_count = 0

        self.affects_player = False
        self.affects_enemy = False

        self.collision_damage = 0

        # is_active must be set to True when created, and depending on the particle, set to False when it must be killed
        # It might be upon collision with intended target, upon a timer, or when going outside screen bounds. Or it
        # might be killed by summoning Entity.
        self.is_active = False

    @abc.abstractmethod
    def load_animation_frames(self, tile_set):
        pass

    @abc.abstractmethod
    def animate(self):
        pass

    @abc.abstractmethod
    def collision(self, direction):
        pass

    @abc.abstractmethod
    def move(self):
        pass

    @abc.abstractmethod
    def effect(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass


class PWoodenSword(Particle):
    def __init__(self, owner_pos, owner_direction_vector, owner_direction_label,
                 groups, particle_tileset):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        match owner_direction_label:
            case 'up':
                self.pos_x += 6
                self.pos_y -= 22
                self.direction_label = owner_direction_label
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            case 'right':
                self.pos_x += 20
                self.pos_y += 2
                self.direction_label = owner_direction_label
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            case 'down':
                self.pos_x += 14
                self.pos_y += 22
                self.direction_label = owner_direction_label
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            case 'left':
                self.pos_x -= 20
                self.pos_y += 2
                self.direction_label = owner_direction_label
                self.direction_vector.x = -1
                self.direction_vector.y = 0

        self.move_animation_cooldown = 5
        self.move_animation_timer_start = pygame.time.get_ticks()
        self.move_animation_frame_count = 0

        self.load_animation_frames(particle_tileset)
        
        self.image = self.move_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        # Hitbox will stay at full sword length despite the animation, because it is extremely fast and doesn't really
        # improve gameplay at all.
        if owner_direction_label == 'up' or owner_direction_label == 'down':
            self.hitbox = self.rect.inflate(-26, 0)
            self.hitbox.left = self.rect.left + 4
            self.hitbox.top = self.rect.top
        else:
            self.hitbox = self.rect.inflate(0, -26)
            self.hitbox.left = self.rect.left
            self.hitbox.top = self.rect.top + 14

        self.affects_enemy = True
        self.collision_damage = WOOD_SWORD_DMG

        self.sword_attack_sound = pygame.mixer.Sound(SOUND_SWORD_ATTACK)
        self.sword_attack_sound.set_volume(0.5)
        self.sword_attack_sound.play()

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        for i in range(WOOD_SWORD_FRAMES):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations['up'].append(particle_tileset.get_sprite_image(
                WOOD_SWORD_UP_FRAME_ID + tiles_offset))
            self.move_animations['right'].append(particle_tileset.get_sprite_image(
                WOOD_SWORD_RIGHT_FRAME_ID + tiles_offset))
            self.move_animations['down'].append(particle_tileset.get_sprite_image(
                WOOD_SWORD_DOWN_FRAME_ID + tiles_offset))
            self.move_animations['left'].append(
                pygame.transform.flip(
                    particle_tileset.get_sprite_image(WOOD_SWORD_RIGHT_FRAME_ID + tiles_offset),
                    True,
                    False))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.direction_label][self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < WOOD_SWORD_FRAMES - 1:
                self.move_animation_frame_count += 1

    def collision(self, direction):
        pass

    def move(self):
        # This particle is animated, but doesn't move.
        pass

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Rock(Particle):
    def __init__(self, owner_pos,
                 owner_direction_vector,
                 groups,
                 owner_direction_label,
                 particle_tileset,
                 obstacle_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        match owner_direction_label:
            case 'up':
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            case 'right':
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            case 'down':
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            case 'left':
                self.direction_vector.x = -1
                self.direction_vector.y = 0

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -12)
        self.hitbox.left = self.rect.left
        self.hitbox.top = self.rect.top + 4

        self.affects_player = True
        self.collision_damage = ROCK_DMG

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        self.move_animations.append(particle_tileset.get_sprite_image(ROCK_FRAME_ID))

    def animate(self):
        # This particle moves, but isn't animated
        pass

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.kill()

    def move(self):
        self.hitbox.x += self.direction_vector.x * ROCK_SPEED
        self.rect.x += self.direction_vector.x * ROCK_SPEED
        self.hitbox.y += self.direction_vector.y * ROCK_SPEED
        self.rect.y += self.direction_vector.y * ROCK_SPEED

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        self.move()
        self.collision('')
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Heart(Particle):
    def __init__(self, owner_pos, groups, particle_tileset, obstacle_sprites, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites
        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.heart_pickup_sound = pygame.mixer.Sound(SOUND_TINY_PICKUP)
        self.heart_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        for i in range(HEART_FRAMES):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(particle_tileset.get_sprite_image(HEART_FRAME_ID + tiles_offset))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < HEART_FRAMES - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.heart_pickup_sound.play()
        self.level.heal_player(1)

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Rupee(Particle):
    def __init__(self, owner_pos, groups, particle_tileset, obstacle_sprites, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites
        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.rupee_pickup_sound = pygame.mixer.Sound(SOUND_TINY_PICKUP)
        self.rupee_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        for i in range(RUPEE_FRAMES):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(particle_tileset.get_sprite_image(RUPEE_FRAME_ID + tiles_offset))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < RUPEE_FRAMES - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.rupee_pickup_sound.play()
        self.level.add_money(1)

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class CBomb(Particle):
    def __init__(self, owner_pos, groups, particle_tileset, obstacle_sprites, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites
        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.bomb_pickup_sound = pygame.mixer.Sound(SOUND_SMALL_PICKUP)
        self.bomb_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        self.move_animations.append(particle_tileset.get_sprite_image(CBOMB_FRAME_ID))

    def animate(self):
        # This doesn't animate
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.bomb_pickup_sound.play()
        self.level.add_bombs(PLAYER_BOMB_LOOT_AMOUNT)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Fairy(Particle):
    def __init__(self, owner_pos, groups, particle_tileset, obstacle_sprites, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites
        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0
        self.speed = 1

        self.direction_starting_time = 0
        self.direction_cooldown = random.randrange(500, 2000, 100)

        self.fairy_pickup_sound = pygame.mixer.Sound(SOUND_SMALL_PICKUP)
        self.fairy_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        for i in range(FAIRY_FRAMES):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(particle_tileset.get_sprite_image(FAIRY_FRAMES_ID + tiles_offset))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < FAIRY_FRAMES - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def collision(self, direction):
        # This flies, so it will only collide with screen border obstacles, that are given in obstacles_sprites
        # Be careful when creating a fairy !
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self):
        # Moves randomly in any direction
        current_time = pygame.time.get_ticks()
        if current_time - self.direction_starting_time >= self.direction_cooldown:
            self.direction_cooldown = random.randrange(500, 2000, 100)
            self.direction_starting_time = current_time

            self.direction_vector.x = random.randint(-1, 1)
            self.direction_vector.y = random.randint(-1, 1)
            if self.direction_vector.magnitude() != 0:
                self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction_vector.y * self.speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def effect(self):
        self.fairy_pickup_sound.play()
        self.level.heal_player(PLAYER_HEALTH_MAX)

    def update(self):
        self.animate()
        self.move()
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Bomb(Particle):
    def __init__(self, owner_pos, owner_direction_vector, owner_direction_label, groups, particle_tileset):
        super().__init__(owner_pos, owner_direction_vector, groups)
        # Will later give a group of destructible sprites to check if the bomb is close enough to break it
        self.owner_pos = owner_pos
        self.groups = groups

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.particle_tileset = particle_tileset
        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(32, 32)
        self.hitbox.center = self.rect.center

        self.collision_damage = 0

        self.bomb_drop_sound = pygame.mixer.Sound(SOUND_BOMB_DROP)
        self.bomb_drop_sound.set_volume(0.3)
        self.bomb_drop_sound.play()
        self.bomb_explode_sound = pygame.mixer.Sound(SOUND_BOMB_EXPLODE)
        self.bomb_explode_sound.set_volume(0.3)

        self.is_active = True

        self.ignited_starting_time = pygame.time.get_ticks()
        self.explosion_cooldown = 1000

        match owner_direction_label:
            case 'up':
                self.pos_x = owner_pos[0]
                self.pos_y = owner_pos[1] - 32
            case 'right':
                self.pos_x = owner_pos[0] + 16
                self.pos_y = owner_pos[1]
            case 'down':
                self.pos_x = owner_pos[0]
                self.pos_y = owner_pos[1] + 32
            case 'left':
                self.pos_x = owner_pos[0] - 16
                self.pos_y = owner_pos[1]

    def load_animation_frames(self, particle_tileset):
        self.move_animations.append(particle_tileset.get_sprite_image(PBOMB_FRAME_ID))

    def animate(self):
        pass

    def collision(self, direction):
        pass

    def move(self):
        pass

    def effect(self):
        self.bomb_explode_sound.play()
        # Generate smoke effect
        BombSmoke((self.pos_x - 16, self.pos_y), self.groups, self.particle_tileset)
        BombSmoke((self.pos_x + 16, self.pos_y + 16), self.groups, self.particle_tileset)
        BombSmoke((self.pos_x, self.pos_y + 24), self.groups, self.particle_tileset)
        BombSmoke((self.pos_x + 8, self.pos_y - 8), self.groups, self.particle_tileset)
        BombSmoke((self.pos_x - 16, self.pos_y), self.groups, self.particle_tileset)
        # Destroy fragile walls nearby
        pass

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.ignited_starting_time >= self.explosion_cooldown:
            self.effect()
            self.kill()
        else:
            pygame.display.get_surface().blit(self.image, (self.pos_x, self.pos_y))


class BombSmoke(Particle):
    def __init__(self, effect_pos, groups, particle_tileset):
        owner_direction_vector = pygame.math.Vector2()
        super().__init__(effect_pos, owner_direction_vector, groups)

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(particle_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-32, -32)

        self.collision_damage = 0

        self.is_active = True

        self.smoke_starting_time = self.move_animation_timer_start = pygame.time.get_ticks()
        self.move_animation_cooldown = 150
        self.smoke_cooldown = PBOMB_SMOKE_FRAMES * self.move_animation_cooldown

    def load_animation_frames(self, particle_tileset):
        for i in range(PBOMB_SMOKE_FRAMES):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(particle_tileset.get_sprite_image(PBOMB_SMOKE_FRAME_ID + tiles_offset))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < PBOMB_SMOKE_FRAMES - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def collision(self, direction):
        pass

    def move(self):
        pass

    def effect(self):
        pass

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.smoke_starting_time >= self.smoke_cooldown:
            self.kill()
        else:
            self.animate()
            pygame.display.get_surface().blit(self.image, (self.pos_x, self.pos_y))


class HeartReceptacle(Particle):
    def __init__(self, owner_pos, groups, consumable_tileset, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(consumable_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        # Only one frame
        self.move_animations.append(particle_tileset.get_sprite_image(HEARTRECEPTACLE_FRAME_ID))

    def animate(self):
        # No animation
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.level.player_pick_up(HEARTRECEPTACLE_LABEL)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Ladder(Particle):
    def __init__(self, owner_pos, groups, items_tileset, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(items_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tileset):
        # Only one frame
        self.move_animations.append(items_tileset.get_sprite_image(LADDER_FRAME_ID))

    def animate(self):
        # No animation
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.level.player_pick_up(LADDER_LABEL)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class RedCandle(Particle):
    def __init__(self, owner_pos, groups, items_tileset, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(items_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tileset):
        # Only one frame
        self.move_animations.append(items_tileset.get_sprite_image(RED_CANDLE_FRAME_ID))

    def animate(self):
        # No animation
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.level.player_pick_up(CANDLE_LABEL)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class Boomerang(Particle):
    def __init__(self, owner_pos, groups, items_tileset, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(items_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tileset):
        # Only one frame
        self.move_animations.append(items_tileset.get_sprite_image(BOOMERANG_FRAME_ID))

    def animate(self):
        # No animation
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.level.player_pick_up(BOOMERANG_LABEL)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class WoodenSword(Particle):
    def __init__(self, owner_pos, groups, items_tileset, level):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level = level

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        self.move_animation_frame_count = 0
        self.move_animations = []

        self.load_animation_frames(items_tileset)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tileset):
        # Only one frame
        self.move_animations.append(items_tileset.get_sprite_image(WOOD_SWORD_FRAME_ID))

    def animate(self):
        # No animation
        pass

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.level.player_pick_up(WOOD_SWORD_LABEL)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
