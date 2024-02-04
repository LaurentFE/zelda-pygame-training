import abc
import pygame
from settings import *
from abc import ABC


# Probably a particle group at one point could be useful ... To despawn enemy particle at death when they are kill(), or
# maybe I can do it inside the kill() ??
# BUG : Particle is always on top of everything, which isn't bad, except for the sword, will destroy the hilt to correct
class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self, owner_pos, owner_direction_vector, groups):
        super().__init__(groups)

        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]
        self.direction_vector = owner_direction_vector
        self.speed = 0

        self.image = None

        self.move_animations = {
            'up': [],
            'right': [],
            'down': [],
            'left': []
        }
        self.move_animation_cooldown = 50
        self.move_animation_timer_start = 0
        self.move_animation_frame_count = 0

        self.affects_player = False
        self.affects_enemy = False

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
    def collision(self):
        pass

    @abc.abstractmethod
    def move(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass


class WoodenSword(Particle):
    def __init__(self, owner_pos, owner_direction_vector, owner_direction_label,
                 groups, enemy_sprites, particle_tileset):
        super().__init__(owner_pos, owner_direction_vector, groups)

        self.enemy_sprites = enemy_sprites

        self.owner_pos = owner_pos
        self.pos_x = owner_pos[0]
        self.pos_y = owner_pos[1]

        match owner_direction_label:
            case 'up':
                self.pos_x += 6
                self.pos_y -= 22
                self.direction_label = owner_direction_label
            case 'right':
                self.pos_x += 22
                self.pos_y += 4
                self.direction_label = owner_direction_label
            case 'down':
                self.pos_x += 12
                self.pos_y += 22
                self.direction_label = owner_direction_label
            case 'left':
                self.pos_x -= 22
                self.pos_y += 4
                self.direction_label = owner_direction_label

        self.move_animation_cooldown = PLAYER_ACTION_ANIMATION_COOLDOWN // WOOD_SWORD_FRAMES
        self.move_animation_timer_start = pygame.time.get_ticks()
        self.move_animation_frame_count = 0

        self.load_animation_frames(particle_tileset)
        
        self.image = self.move_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
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

        self.is_active = True

    def load_animation_frames(self, particle_tileset):
        # TODO : Create propre particles.png file
        for i in range(WOOD_SWORD_FRAMES):
            self.move_animations['up'].append(particle_tileset.get_sprite_image(WOOD_SWORD_UP_FRAME_ID + (2 * i)))
            self.move_animations['right'].append(particle_tileset.get_sprite_image(WOOD_SWORD_RIGHT_FRAME_ID + (2 * i)))
            self.move_animations['down'].append(particle_tileset.get_sprite_image(WOOD_SWORD_DOWN_FRAME_ID + (2 * i)))
            self.move_animations['left'].append(
                pygame.transform.flip(
                    particle_tileset.get_sprite_image(WOOD_SWORD_RIGHT_FRAME_ID + (2 * i)),
                    True,
                    False))
        # DAMN that's ugly that I do it this way
        for i in range(WOOD_SWORD_FRAMES - 1):
            self.move_animations['up'].append(particle_tileset.get_sprite_image(WOOD_SWORD_UP_FRAME_ID + 2 - (2 * i)))
            self.move_animations['right'].append(particle_tileset.get_sprite_image(WOOD_SWORD_RIGHT_FRAME_ID + 2 - (2 * i)))
            self.move_animations['down'].append(particle_tileset.get_sprite_image(WOOD_SWORD_DOWN_FRAME_ID + 2 - (2 * i)))
            self.move_animations['left'].append(
                pygame.transform.flip(
                    particle_tileset.get_sprite_image(WOOD_SWORD_RIGHT_FRAME_ID + 2 - (2 * i)),
                    True,
                    False))

    def animate(self):
        # TODO : Update hitbox to fit length of sword showing
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        self.image = self.move_animations[self.direction_label][self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < WOOD_SWORD_FRAMES - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def collision(self):
                pass

    def move(self):
        # This particle is animated, but doesn't move.
        pass

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
