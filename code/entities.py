import abc
import pygame
from settings import *
from abc import ABC


class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, groups, visible_sprites, obstacle_sprites, particle_sprites, particle_tileset):
        super().__init__(groups)

        self.visible_sprites = visible_sprites
        self.obstacle_sprites = obstacle_sprites
        self.particle_sprites = particle_sprites
        self.particle_tileset = particle_tileset
        self.walking_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.gray_animation = {
            'down': []
        }
        self.action_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.hurt_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.spawn_animation = []
        self.despawn_animation = []

        self.direction_vector = pygame.math.Vector2()
        self.direction_label = ''
        self.state = ''
        self.speed = 0

        self.image = None
        self.rect = None
        self.hitbox = None

        self.walking_frames = 0
        self.is_up_flipped = False
        self.is_up_action_flipped = False
        self.is_right_flipped = False
        self.walking_up_frame_id = 0
        self.walking_down_frame_id = 0
        self.walking_left_frame_id = 0
        self.walking_right_frame_id = 0
        self.can_be_gray = False
        self.walking_down_gray_frame_id = 0
        self.action_frames = 0
        self.action_up_frame_id = 0
        self.action_down_frame_id = 0
        self.action_left_frame_id = 0
        self.action_right_frame_id = 0
        self.hurt_frames = 0
        self.hurt_up_frame_id = 0
        self.hurt_down_frame_id = 0
        self.hurt_left_frame_id = 0
        self.hurt_right_frame_id = 0
        self.spawn_frames = 0
        self.spawn_frame_id = 0
        self.despawn_frames = 0
        self.despawn_frame_id = 0

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = 50
        self.action_animation_cooldown = 50
        self.hurt_animation_cooldown = 50
        self.spawn_animation_cooldown = 50
        self.despawn_animation_cooldown = 50

        # Time at which animation frame started
        self.walking_animation_starting_time = 0
        self.action_animation_starting_time = 0
        self.hurt_animation_starting_time = 0
        self.spawn_animation_starting_time = 0
        self.despawn_animation_starting_time = 0

        # Index of animation being played
        self.walking_animation_frame_count = 0
        self.action_animation_frame_count = 0
        self.hurt_animation_frame_count = 0
        self.spawn_animation_frame_count = 0
        self.despawn_animation_frame_count = 0

        self.health = 0

    def load_walking_frames(self, entity_tile_set):
        for i in range(self.walking_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            if self.is_up_flipped:
                self.walking_animations['up'].append(
                    pygame.transform.flip(
                        entity_tile_set.get_sprite_image(self.walking_up_frame_id + tiles_offset),
                        False,
                        True))
            else:
                self.walking_animations['up'].append(
                    entity_tile_set.get_sprite_image(self.walking_up_frame_id + tiles_offset))

            self.walking_animations['left'].append(
                entity_tile_set.get_sprite_image(self.walking_left_frame_id + tiles_offset))

            self.walking_animations['down'].append(
                entity_tile_set.get_sprite_image(self.walking_down_frame_id + tiles_offset))

            if self.is_right_flipped:
                self.walking_animations['right'].append(
                    pygame.transform.flip(
                        entity_tile_set.get_sprite_image(self.walking_right_frame_id + tiles_offset),
                        True,
                        False))
            else:
                self.walking_animations['right'].append(
                    entity_tile_set.get_sprite_image(self.walking_right_frame_id + tiles_offset))

            if self.can_be_gray:
                self.gray_animation['down'].append(
                    entity_tile_set.get_sprite_image(self.walking_down_gray_frame_id + tiles_offset))

    def load_action_frames(self, entity_tile_set):
        for i in range(self.action_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            if self.is_up_action_flipped:
                self.action_animations['up'].append(
                    pygame.transform.flip(
                        entity_tile_set.get_sprite_image(self.action_up_frame_id + tiles_offset),
                        False,
                        True))
            else:
                self.action_animations['up'].append(
                    entity_tile_set.get_sprite_image(self.action_up_frame_id + tiles_offset))
            self.action_animations['left'].append(
                entity_tile_set.get_sprite_image(self.action_left_frame_id + tiles_offset))
            self.action_animations['down'].append(
                entity_tile_set.get_sprite_image(self.action_down_frame_id + tiles_offset))
            self.action_animations['right'].append(
                pygame.transform.flip(
                    entity_tile_set.get_sprite_image(self.action_right_frame_id + tiles_offset),
                    True,
                    False))

    def load_hurt_frames(self, entity_tile_set):
        for i in range(self.hurt_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            if self.is_up_flipped:
                self.hurt_animations['up'].append(
                    pygame.transform.flip(
                        entity_tile_set.get_sprite_image(self.hurt_up_frame_id + tiles_offset),
                        False,
                        True))
            else:
                self.hurt_animations['up'].append(
                    entity_tile_set.get_sprite_image(self.hurt_up_frame_id + tiles_offset))
            self.hurt_animations['left'].append(
                entity_tile_set.get_sprite_image(self.hurt_left_frame_id + tiles_offset))
            self.hurt_animations['down'].append(
                entity_tile_set.get_sprite_image(self.hurt_down_frame_id + tiles_offset))
            if self.is_right_flipped:
                self.hurt_animations['right'].append(
                    pygame.transform.flip(
                        entity_tile_set.get_sprite_image(self.hurt_right_frame_id + tiles_offset),
                        True,
                        False))
            else:
                self.hurt_animations['right'].append(
                    entity_tile_set.get_sprite_image(self.hurt_right_frame_id + tiles_offset))

    def load_spawn_frames(self, entity_tile_set):
        for i in range(self.spawn_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.spawn_animation.append(entity_tile_set.get_sprite_image(self.spawn_frame_id + tiles_offset))

    def load_despawn_frames(self, entity_tile_set):
        for i in range(self.despawn_frames):
            tiles_offset = SPRITE_SIZE // TILE_SIZE * i
            self.despawn_animation.append(entity_tile_set.get_sprite_image(self.despawn_frame_id + tiles_offset))

    @abc.abstractmethod
    def load_animation_frames(self, entity_tile_set):
        self.load_walking_frames(entity_tile_set)
        self.load_action_frames(entity_tile_set)
        self.load_hurt_frames(entity_tile_set)
        self.load_spawn_frames(entity_tile_set)
        self.load_despawn_frames(entity_tile_set)

    @abc.abstractmethod
    def cooldowns(self):
        pass

    @abc.abstractmethod
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
                    self.state = 'idle'

        return animation_starting_time, animation_frame_count

    @abc.abstractmethod
    def animate(self):
        current_time = pygame.time.get_ticks()

        if self.state == 'walking':
            self.walking_animation_starting_time, self.walking_animation_frame_count = (
                self.change_animation_frame(self.walking_animations[self.direction_label],
                                            self.walking_animation_frame_count,
                                            self.walking_animation_starting_time,
                                            self.walking_animation_cooldown,
                                            self.walking_frames))
        elif 'hurt' in self.state:
            self.hurt_animation_starting_time, self.hurt_animation_frame_count = (
                self.change_animation_frame(self.hurt_animations[self.direction_label],
                                            self.hurt_animation_frame_count,
                                            self.hurt_animation_starting_time,
                                            self.hurt_animation_cooldown,
                                            self.hurt_frames,
                                            False))

        elif 'action' in self.state:
            self.action_animation_starting_time, self.action_animation_frame_count = (
                self.change_animation_frame(self.action_animations[self.direction_label],
                                            self.action_animation_frame_count,
                                            self.action_animation_starting_time,
                                            self.action_animation_cooldown,
                                            self.action_frames))

    @abc.abstractmethod
    def collision(self, direction):
        pass

    @abc.abstractmethod
    def move(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass
