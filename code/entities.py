import abc
import pygame
from abc import ABC


class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, groups, obstacle_sprites, particle_sprites):
        super().__init__(groups)

        self.obstacle_sprites = obstacle_sprites
        self.particle_sprites = particle_sprites
        self.walking_animations = {
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
        self.despawn_animation = []
        self.direction_vector = pygame.math.Vector2()
        self.direction_label = ''
        self.state = ''
        self.speed = 0

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = 50
        self.action_animation_cooldown = 50
        self.hurt_animation_cooldown = 50

        # Time at which animation frame started
        self.walking_animation_starting_time = 0
        self.action_animation_starting_time = 0
        self.hurt_animation_starting_time = 0
        # Index of animation being played
        self.walking_animation_frame_count = 0
        self.action_animation_frame_count = 0
        self.hurt_animation_frame_count = 0

        self.health = 0

    @abc.abstractmethod
    def load_animation_frames(self, entity_tile_set):
        pass

    @abc.abstractmethod
    def cooldowns(self):
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
    def update(self):
        pass
