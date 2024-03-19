import abc
import random
import tileset
import pygame
import level as game
from settings import *
from abc import ABC


class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self, owner_pos, owner_direction_vector, groups):
        super().__init__(groups)

        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]
        self.owner_direction_vector = pygame.math.Vector2(owner_direction_vector)
        self.direction_vector = pygame.math.Vector2()
        self.speed = 0
        self.bypasses_shield = False

        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.move_animations = []
        self.move_animation_cooldown = 100
        self.move_animation_timer_start = pygame.time.get_ticks()
        self.move_animation_frame_count = 0
        self.frame_id = 0
        self.nb_frames = 0

        self.affects_player = False
        self.affects_enemy = False

        self.collision_damage = 0

        # is_active must be set to True when created, and depending on the particle, set to False when it must be killed
        # It might be upon collision with intended target, upon a timer, or when going outside screen bounds. Or it
        # might be killed by summoning Entity.
        self.is_active = False

    @abc.abstractmethod
    def load_animation_frames(self, tile_set):
        for i in range(self.nb_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(tile_set.get_sprite_image(self.frame_id + tiles_offset))

    @abc.abstractmethod
    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < self.nb_frames - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

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
        self.move()
        self.animate()
        self.collision('')
        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class PWoodenSword(Particle):
    def __init__(self,
                 owner_pos,
                 owner_direction_vector,
                 owner_direction_label,
                 groups,
                 enemy_sprites,
                 particle_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.enemy_sprites = enemy_sprites
        self.particle_sprites = particle_sprites

        self.direction_label = owner_direction_label
        if owner_direction_label == UP_LABEL:
            self.pos_x += 6
            self.pos_y -= 22
            self.direction_vector.x = 0
            self.direction_vector.y = -1
        elif owner_direction_label == RIGHT_LABEL:
            self.pos_x += 20
            self.pos_y += 2
            self.direction_vector.x = 1
            self.direction_vector.y = 0
        elif owner_direction_label == DOWN_LABEL:
            self.pos_x += 14
            self.pos_y += 22
            self.direction_vector.x = 0
            self.direction_vector.y = 1
        elif owner_direction_label == LEFT_LABEL:
            self.pos_x -= 20
            self.pos_y += 2
            self.direction_vector.x = -1
            self.direction_vector.y = 0

        self.move_animation_cooldown = 5
        self.move_animations = {
            UP_LABEL: [],
            RIGHT_LABEL: [],
            DOWN_LABEL: [],
            LEFT_LABEL: []
        }

        self.frame_id = WOOD_SWORD_RIGHT_FRAME_ID
        self.nb_frames = WOOD_SWORD_ATTACK_FRAMES
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)
        
        self.image = self.move_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        # Hitbox will stay at full sword length despite the animation, because it is extremely fast and doesn't really
        # improve gameplay at all.
        if owner_direction_label == UP_LABEL or owner_direction_label == DOWN_LABEL:
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

    def load_animation_frames(self, particle_tile_set):
        for i in range(self.nb_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations[UP_LABEL].append(particle_tile_set.get_sprite_image(
                WOOD_SWORD_UP_FRAME_ID + tiles_offset))
            self.move_animations[RIGHT_LABEL].append(particle_tile_set.get_sprite_image(
                WOOD_SWORD_RIGHT_FRAME_ID + tiles_offset))
            self.move_animations[DOWN_LABEL].append(particle_tile_set.get_sprite_image(
                WOOD_SWORD_DOWN_FRAME_ID + tiles_offset))
            self.move_animations[LEFT_LABEL].append(
                pygame.transform.flip(
                    particle_tile_set.get_sprite_image(self.frame_id + tiles_offset),
                    True,
                    False))

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.direction_label][self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < self.nb_frames - 1:
                self.move_animation_frame_count += 1

    def collision(self, direction):
        # Collision with a monster
        for enemy in self.enemy_sprites:
            if enemy.hitbox.colliderect(self.hitbox):
                enemy.take_damage(self.collision_damage, self.direction_label)

        # Collision with a lootable particle
        for particle in self.particle_sprites:
            if (particle.hitbox.colliderect(self.hitbox)
                    and particle.affects_player
                    and particle.collision_damage == 0):
                particle.effect()
                particle.kill()

    def move(self):
        # This particle is animated, but doesn't move.
        pass

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        super().update()


class PBoomerang(Particle):
    def __init__(self, owner_pos,
                 owner_direction_vector,
                 owner_direction_label,
                 groups,
                 enemy_sprites,
                 particle_sprites,
                 border_sprites,
                 player):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.direction_vector = pygame.math.Vector2(owner_direction_vector)
        self.direction_label = owner_direction_label
        self.enemy_sprites = enemy_sprites
        self.particle_sprites = particle_sprites
        self.border_sprites = border_sprites
        self.player_ref = player

        if self.direction_vector.x == 0 and self.direction_vector.y == 0:
            if owner_direction_label == UP_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = -1
            elif owner_direction_label == RIGHT_LABEL:
                self.direction_vector.x = 1
                self.direction_vector.y = 0
            elif owner_direction_label == DOWN_LABEL:
                self.direction_vector.x = 0
                self.direction_vector.y = 1
            elif owner_direction_label == LEFT_LABEL:
                self.direction_vector.x = -1
                self.direction_vector.y = 0

        self.move_animation_cooldown = 100

        self.frame_id = BOOMERANG_FRAME_ID
        self.nb_frames = BOOMERANG_FRAMES
        self.load_animation_frames(tileset.ITEMS_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.hitbox = self.rect.inflate(-22, -16)
        self.hitbox.center = self.rect.center

        self.affects_enemy = True
        self.collision_damage = BOOMERANG_DMG
        self.speed = BOOMERANG_SPEED

        self.boomerang_attack_sound = pygame.mixer.Sound(SOUND_BOOMERANG_ATTACK)
        self.boomerang_attack_sound.set_volume(0.5)
        self.boomerang_attack_sound.play(loops=-1)

        self.is_active = True
        self.go_back = False

    def load_animation_frames(self, item_tile_set):
        self.move_animations.append(
            item_tile_set.get_sprite_image(self.frame_id))
        self.move_animations.append(
            pygame.transform.flip(
                item_tile_set.get_sprite_image(self.frame_id),
                True,
                False))

    def animate(self):
        super().animate()

    def collision(self, direction):
        # Collision with a monster
        for enemy in self.enemy_sprites:
            if (not self.go_back
                    and enemy.hitbox.colliderect(self.hitbox)
                    and not enemy.invulnerable):
                self.go_back = True
                self.affects_enemy = False
                enemy.take_damage(self.collision_damage, self.direction_label)

        # Collision with a lootable particle
        for particle in self.particle_sprites:
            if (not self.go_back
                    and particle.hitbox.colliderect(self.hitbox)
                    and particle.affects_player
                    and particle.collision_damage == 0):
                particle.effect()
                particle.kill()
                self.go_back = True
                self.affects_enemy = False

        # Collision with screen borders
        for border in self.border_sprites:
            if not self.go_back and border.hitbox.colliderect(self.hitbox):
                self.go_back = True
                self.affects_enemy = False

        if self.go_back and self.player_ref.hitbox.colliderect(self.hitbox):
            self.kill()

    def move(self):
        if self.go_back:
            x_displacement = self.rect.left - self.player_ref.rect.left
            y_displacement = self.rect.top - self.player_ref.rect.top
            self.direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
            if self.direction_vector.magnitude() != 0:
                self.direction_vector = self.direction_vector.normalize()

        self.hitbox.x += self.direction_vector.x * self.speed
        self.rect.x += self.direction_vector.x * self.speed
        self.hitbox.y += self.direction_vector.y * self.speed
        self.rect.y += self.direction_vector.y * self.speed

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        super().update()

    def kill(self):
        self.boomerang_attack_sound.stop()
        self.player_ref.is_boomerang_thrown = False
        super().kill()


class Rock(Particle):
    def __init__(self,
                 owner_pos,
                 owner_direction_vector,
                 groups,
                 owner_direction_label,
                 obstacle_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        if owner_direction_label == UP_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = -1
        elif owner_direction_label == RIGHT_LABEL:
            self.direction_vector.x = 1
            self.direction_vector.y = 0
        elif owner_direction_label == DOWN_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = 1
        elif owner_direction_label == LEFT_LABEL:
            self.direction_vector.x = -1
            self.direction_vector.y = 0

        self.frame_id = ROCK_FRAME_ID
        self.nb_frames = ROCK_FRAMES
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -12)
        self.hitbox.left = self.rect.left
        self.hitbox.top = self.rect.top + 4

        self.affects_player = True
        self.collision_damage = ROCK_DMG
        self.speed = ROCK_SPEED

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        # This particle moves, but isn't animated
        pass

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if (sprite.hitbox.colliderect(self.hitbox)
                    and sprite.type != LIMIT_WATER_INDEX
                    and sprite.type != LIMIT_LADDER_INDEX
                    and sprite.type != LIMIT_LAKE_BORDER_INDEX):
                self.kill()

    def move(self):
        self.hitbox.x += self.direction_vector.x * self.speed
        self.rect.x += self.direction_vector.x * self.speed
        self.hitbox.y += self.direction_vector.y * self.speed
        self.rect.y += self.direction_vector.y * self.speed

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        super().update()


class Arrow(Particle):
    def __init__(self,
                 owner_pos,
                 owner_direction_vector,
                 groups,
                 owner_direction_label,
                 obstacle_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        if owner_direction_label == UP_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = -1
        elif owner_direction_label == RIGHT_LABEL:
            self.direction_vector.x = 1
            self.direction_vector.y = 0
        elif owner_direction_label == DOWN_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = 1
        elif owner_direction_label == LEFT_LABEL:
            self.direction_vector.x = -1
            self.direction_vector.y = 0

        self.frame_up_id = ARROW_FRAME_UP_ID
        self.frame_right_id = ARROW_FRAME_RIGHT_ID
        self.nb_frames = ARROW_FRAMES

        self.move_animations = {
            UP_LABEL: [],
            RIGHT_LABEL: [],
            DOWN_LABEL: [],
            LEFT_LABEL: []
        }
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.image = self.move_animations[owner_direction_label][0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -12)
        self.hitbox.left = self.rect.left
        self.hitbox.top = self.rect.top + 4

        self.affects_player = True
        self.collision_damage = ARROW_DMG
        self.speed = ARROW_SPEED

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        for i in range(self.nb_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations[UP_LABEL].append(
                particle_tile_set.get_sprite_image(self.frame_up_id + tiles_offset))
            self.move_animations[DOWN_LABEL].append(
                pygame.transform.flip(
                    particle_tile_set.get_sprite_image(self.frame_up_id + tiles_offset),
                    False,
                    True))
            self.move_animations[RIGHT_LABEL].append(
                particle_tile_set.get_sprite_image(self.frame_right_id + tiles_offset))
            self.move_animations[LEFT_LABEL].append(
                pygame.transform.flip(
                    particle_tile_set.get_sprite_image(self.frame_right_id + tiles_offset),
                    True,
                    False))

    def animate(self):
        # This particle moves, but isn't animated
        pass

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if (sprite.hitbox.colliderect(self.hitbox)
                    and sprite.type != LIMIT_TREE_INDEX
                    and sprite.type != LIMIT_WATER_INDEX
                    and sprite.type != LIMIT_LADDER_INDEX
                    and sprite.type != LIMIT_LAKE_BORDER_INDEX):
                self.kill()

    def move(self):
        self.hitbox.x += self.direction_vector.x * self.speed
        self.rect.x += self.direction_vector.x * self.speed
        self.hitbox.y += self.direction_vector.y * self.speed
        self.rect.y += self.direction_vector.y * self.speed

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        super().update()


class MagicMissile(Particle):
    def __init__(self,
                 owner_pos,
                 owner_direction_vector,
                 groups,
                 obstacle_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        self.frame_id = MAGIC_MISSILE_FRAME_ID
        self.nb_frames = MAGIC_MISSILE_FRAMES

        self.move_animations = []
        self.move_animation_cooldown = 100
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -12)
        self.hitbox.left = self.rect.left
        self.hitbox.top = self.rect.top + 6

        x_displacement = self.rect.centerx - game.Level().player.rect.centerx
        y_displacement = self.rect.centery - game.Level().player.rect.centery
        self.direction_vector = pygame.math.Vector2(-x_displacement, -y_displacement)
        if self.direction_vector.magnitude() != 0:
            self.direction_vector = self.direction_vector.normalize()

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = MAGIC_MISSILE_DMG
        self.speed = MAGIC_MISSILE_SPEED

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        for i in range(self.nb_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.move_animations.append(
                particle_tile_set.get_sprite_image(self.frame_id + tiles_offset))

    def animate(self):
        super().animate()

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if (sprite.hitbox.colliderect(self.hitbox)
                    and sprite.type != LIMIT_TREE_INDEX
                    and sprite.type != LIMIT_WATER_INDEX
                    and sprite.type != LIMIT_LADDER_INDEX
                    and sprite.type != LIMIT_LAKE_BORDER_INDEX):
                self.kill()

    def move(self):
        self.hitbox.x += self.direction_vector.x * self.speed
        self.rect.x += self.direction_vector.x * self.speed
        self.hitbox.y += self.direction_vector.y * self.speed
        self.rect.y += self.direction_vector.y * self.speed

    def effect(self):
        # None, it's a damaging particle
        pass

    def update(self):
        super().update()


class Heart(Particle):
    def __init__(self, owner_pos, groups, obstacle_sprites):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        self.frame_id = HEART_FRAME_ID
        self.nb_frames = HEART_FRAMES
        self.load_animation_frames(tileset.CONSUMABLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.heart_pickup_sound = pygame.mixer.Sound(SOUND_TINY_PICKUP)
        self.heart_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        super().animate()

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        self.heart_pickup_sound.play()
        game.Level().player_pick_up(HEART_LABEL, 1)

    def update(self):
        super().update()


class Rupee(Particle):
    def __init__(self, owner_pos, groups, obstacle_sprites, amount):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites
        self.amount = amount

        self.frame_id = RUPEE_FRAME_ID
        self.nb_frames = RUPEE_FRAMES
        self.load_animation_frames(tileset.CONSUMABLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        super().animate()

    def collision(self, direction):
        # This doesn't move, so it won't collide with things.
        # But things will collide with it, and they will handle the collision
        pass

    def move(self):
        # This doesn't move
        pass

    def effect(self):
        game.Level().player_pick_up(RUPEE_LABEL, self.amount)

    def update(self):
        super().update()


class CBomb(Particle):
    def __init__(self, owner_pos, groups, obstacle_sprites):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        self.frame_id = CBOMB_FRAME_ID
        self.nb_frames = CBOMB_FRAMES
        self.load_animation_frames(tileset.CONSUMABLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.bomb_pickup_sound = pygame.mixer.Sound(SOUND_SMALL_PICKUP)
        self.bomb_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

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
        game.Level().player_pick_up(BOMB_LABEL, PLAYER_BOMB_LOOT_AMOUNT)

    def update(self):
        super().update()


class Fairy(Particle):
    def __init__(self, owner_pos, groups, obstacle_sprites):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.obstacle_sprites = obstacle_sprites

        self.frame_id = FAIRY_FRAMES_ID
        self.nb_frames = FAIRY_FRAMES
        self.load_animation_frames(tileset.CONSUMABLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, 0)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0
        self.speed = FAIRY_SPEED

        self.direction_starting_time = 0
        self.direction_cooldown = random.randrange(500, 2000, 100)

        self.fairy_pickup_sound = pygame.mixer.Sound(SOUND_SMALL_PICKUP)
        self.fairy_pickup_sound.set_volume(0.3)

        self.is_active = True

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        super().animate()

    def collision(self, direction):
        # This flies, so it will only collide with screen border obstacles, that are given in obstacles_sprites
        # Be careful when creating a fairy !
        if direction == HORIZONTAL_LABEL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == VERTICAL_LABEL:
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
        self.collision(HORIZONTAL_LABEL)
        self.hitbox.y += self.direction_vector.y * self.speed
        self.collision(VERTICAL_LABEL)

        self.rect.center = self.hitbox.center

    def effect(self):
        self.fairy_pickup_sound.play()
        game.Level().player_pick_up(FAIRY_LABEL, PLAYER_HEALTH_MAX)

    def update(self):
        super().update()


class Bomb(Particle):
    def __init__(self, owner_pos,
                 owner_direction_vector,
                 owner_direction_label,
                 groups,
                 secret_bomb_sprites):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.secret_bomb_sprites = secret_bomb_sprites

        self.owner_pos = owner_pos
        self.groups = groups

        self.frame_id = PBOMB_FRAME_ID
        self.nb_frames = PBOMB_FRAMES
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.collision_damage = 0

        self.bomb_drop_sound = pygame.mixer.Sound(SOUND_BOMB_DROP)
        self.bomb_drop_sound.set_volume(0.3)
        self.bomb_drop_sound.play()
        self.bomb_explode_sound = pygame.mixer.Sound(SOUND_BOMB_EXPLODE)
        self.bomb_explode_sound.set_volume(0.3)

        if owner_direction_label == UP_LABEL:
            self.pos_x = owner_pos[0]
            self.pos_y = owner_pos[1] - 32
        elif owner_direction_label == RIGHT_LABEL:
            self.pos_x = owner_pos[0] + 24
            self.pos_y = owner_pos[1]
        elif owner_direction_label == DOWN_LABEL:
            self.pos_x = owner_pos[0]
            self.pos_y = owner_pos[1] + 32
        elif owner_direction_label == LEFT_LABEL:
            self.pos_x = owner_pos[0] - 24
            self.pos_y = owner_pos[1]
        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(24, 32)

        self.is_active = True

        self.ignited_starting_time = pygame.time.get_ticks()
        self.explosion_cooldown = 1000

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        pass

    def collision(self, direction):
        for secret_passage in self.secret_bomb_sprites:
            if (secret_passage.hitbox.colliderect(self.hitbox)
                    and not secret_passage.is_revealed):
                secret_passage.reveal()

    def move(self):
        pass

    def effect(self):
        self.bomb_explode_sound.play()
        # Generate smoke effect
        BombSmoke((self.pos_x - 16, self.pos_y), self.groups)
        BombSmoke((self.pos_x + 16, self.pos_y + 16), self.groups)
        BombSmoke((self.pos_x, self.pos_y + 24), self.groups)
        BombSmoke((self.pos_x + 8, self.pos_y - 8), self.groups)
        BombSmoke((self.pos_x - 16, self.pos_y), self.groups)
        # Destroy fragile walls nearby
        self.collision('')

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.ignited_starting_time >= self.explosion_cooldown:
            self.effect()
            self.kill()
        else:
            pygame.display.get_surface().blit(self.image, self.rect.topleft)


class BombSmoke(Particle):
    def __init__(self, effect_pos, groups):
        owner_direction_vector = pygame.math.Vector2()
        super().__init__(effect_pos, owner_direction_vector, groups)

        self.frame_id = PBOMB_SMOKE_FRAME_ID
        self.nb_frames = PBOMB_SMOKE_FRAMES
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-32, -32)

        self.collision_damage = 0

        self.is_active = True

        self.smoke_starting_time = self.move_animation_timer_start
        self.move_animation_cooldown = 150
        self.smoke_cooldown = PBOMB_SMOKE_FRAMES * self.move_animation_cooldown

    def load_animation_frames(self, particle_tile_set):
        super().load_animation_frames(particle_tile_set)

    def animate(self):
        super().animate()

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
            super().update()


class Flame(Particle):
    def __init__(self, owner_pos,
                 owner_direction_vector,
                 owner_direction_label,
                 groups,
                 enemy_sprites,
                 secret_flame_sprites,
                 player):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.enemy_sprites = enemy_sprites
        self.secret_flame_sprites = secret_flame_sprites
        self.player_ref = player

        self.direction_label = owner_direction_label
        if owner_direction_label == UP_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = -1
            self.pos_x = owner_pos[0]
            self.pos_y = owner_pos[1] - TILE_SIZE
        elif owner_direction_label == RIGHT_LABEL:
            self.direction_vector.x = 1
            self.direction_vector.y = 0
            self.pos_x = owner_pos[0] + TILE_SIZE
            self.pos_y = owner_pos[1]
        elif owner_direction_label == DOWN_LABEL:
            self.direction_vector.x = 0
            self.direction_vector.y = 1
            self.pos_x = owner_pos[0]
            self.pos_y = owner_pos[1] + TILE_SIZE
        elif owner_direction_label == LEFT_LABEL:
            self.direction_vector.x = -1
            self.direction_vector.y = 0
            self.pos_x = owner_pos[0] - TILE_SIZE
            self.pos_y = owner_pos[1]

        self.distance_travelled = 0
        self.max_distance = TILE_SIZE

        self.move_animation_cooldown = 100

        self.frame_id = FLAME_FRAME_ID
        self.nb_frames = FLAME_FRAMES
        self.load_animation_frames(tileset.PARTICLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect

        self.is_active = True
        self.collision_damage = FLAME_DMG
        self.speed = FLAME_SPEED

        self.flame_sound = pygame.mixer.Sound(SOUND_FLAME)
        self.flame_sound.set_volume(0.3)
        self.flame_sound.play()

        self.ignited_starting_time = pygame.time.get_ticks()
        self.extinction_cooldown = 600

    def load_animation_frames(self, particle_tile_set):
        self.move_animations.append(
            particle_tile_set.get_sprite_image(self.frame_id))
        self.move_animations.append(
            pygame.transform.flip(
                particle_tile_set.get_sprite_image(self.frame_id),
                flip_x=True,
                flip_y=False))

    def animate(self):
        super().animate()

    def collision(self, direction):
        # Collision with a monster
        for enemy in self.enemy_sprites:
            if enemy.hitbox.colliderect(self.hitbox):
                # Enemy is pushed back in the direction the flame is moving, or if it's not moving, pushed backward
                if self.distance_travelled < self.max_distance:
                    direction = self.direction_label
                else:
                    direction = ''
                enemy.take_damage(self.collision_damage, direction)

        # Collision with a flammable tile
        for secret_passage in self.secret_flame_sprites:
            if (secret_passage.rect.colliderect(self.hitbox)
                    and not secret_passage.is_revealed):
                secret_passage.reveal()

    def move(self):
        if self.distance_travelled < self.max_distance:
            self.hitbox.x += self.direction_vector.x * self.speed
            self.rect.x += self.direction_vector.x * self.speed
            self.hitbox.y += self.direction_vector.y * self.speed
            self.rect.y += self.direction_vector.y * self.speed
            self.distance_travelled += self.speed

    def effect(self):
        pass

    def kill(self):
        self.player_ref.is_candle_lit = False
        super().kill()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.ignited_starting_time >= self.extinction_cooldown:
            self.kill()
        else:
            super().update()


class HeartReceptacle(Particle):
    def __init__(self, owner_pos, groups, level_id):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level_id = level_id

        self.frame_id = HEARTRECEPTACLE_FRAME_ID
        self.nb_frames = HEARTRECEPTACLE_FRAMES
        self.load_animation_frames(tileset.CONSUMABLES_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, consumable_tile_set):
        super().load_animation_frames(consumable_tile_set)

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
        MAP_ITEMS[self.level_id][HEARTRECEPTACLE_LABEL] = False
        game.Level().player_pick_up(HEARTRECEPTACLE_LABEL)

    def update(self):
        super().update()


class Ladder(Particle):
    def __init__(self, owner_pos, groups, level_id):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level_id = level_id

        self.frame_id = LADDER_FRAME_ID
        self.nb_frames = LADDER_FRAMES
        self.load_animation_frames(tileset.ITEMS_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tile_set):
        super().load_animation_frames(items_tile_set)

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
        MAP_ITEMS[self.level_id][LADDER_LABEL] = False
        game.Level().player_pick_up(LADDER_LABEL)

    def update(self):
        super().update()


class RedCandle(Particle):
    def __init__(self, owner_pos, groups, level_id):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level_id = level_id

        self.frame_id = RED_CANDLE_FRAME_ID
        self.nb_frames = RED_CANDLE_FRAMES
        self.load_animation_frames(tileset.ITEMS_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tile_set):
        super().load_animation_frames(items_tile_set)

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
        MAP_ITEMS[self.level_id][CANDLE_LABEL] = False
        game.Level().player_pick_up(CANDLE_LABEL)

    def update(self):
        super().update()


class Boomerang(Particle):
    def __init__(self, owner_pos, groups, level_id):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level_id = level_id

        self.frame_id = BOOMERANG_FRAME_ID
        self.nb_frames = BOOMERANG_FRAMES
        self.load_animation_frames(tileset.ITEMS_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tile_set):
        super().load_animation_frames(items_tile_set)

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
        MAP_ITEMS[self.level_id][BOOMERANG_LABEL] = False
        game.Level().player_pick_up(BOOMERANG_LABEL)

    def update(self):
        super().update()


class WoodenSword(Particle):
    def __init__(self, owner_pos, groups, level_id):

        owner_direction_vector = pygame.math.Vector2()
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.level_id = level_id

        self.frame_id = WOOD_SWORD_FRAME_ID
        self.nb_frames = WOOD_SWORD_FRAMES
        self.load_animation_frames(tileset.ITEMS_TILE_SET)

        self.image = self.move_animations[0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.hitbox = self.rect.inflate(-16, -16)

        self.affects_player = True
        self.bypasses_shield = True
        self.collision_damage = 0

        self.is_active = True

    def load_animation_frames(self, items_tile_set):
        super().load_animation_frames(items_tile_set)

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
        MAP_ITEMS[self.level_id][WOOD_SWORD_LABEL] = False
        game.Level().player_pick_up(WOOD_SWORD_LABEL)

    def update(self):
        super().update()
