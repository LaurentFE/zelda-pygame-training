import abc
import pygame
import random
from settings import *
from debug import debug
from entities import Entity


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, particle_sprites, enemies_tile_set, uses_projectiles=False):
        super().__init__(groups, obstacle_sprites, particle_sprites)

        self.direction_label = random.choice(['up', 'down', 'left', 'right'])
        self.state = 'walking'
        self.speed = 1

        # HOW DO ATTACK PROJECTILE ?
        self.load_animation_frames(enemies_tile_set)

        self.image = self.walking_animations[self.direction_label][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

        # Monster actions cooldowns
        # Monsters always move, except if shooting, or special mechanic such as flying, jumping, diving(water/land)
        self.uses_projectiles = uses_projectiles
        self.can_attack = self.uses_projectiles
        self.attack_cooldown = 500
        self.attack_starting_time = 0
        self.can_move = True
        self.direction_cooldown = 200
        self.direction_starting_time = 0
        self.hurt_starting_time = 0
        self.hurt_animation_cooldown = MONSTER_HURT_ANIMATION_COOLDOWN
        self.hurt_cooldown = MONSTER_HURT_FRAMES * self.hurt_animation_cooldown
        self.invulnerability_cooldown = 1.5 * self.hurt_cooldown

        self.despawn_animation_frame_count = 0
        self.despawn_animation_starting_time = 0
        self.despawn_animation_cooldown = MONSTER_DEATH_ANIMATION_COOLDOWN

        # Monster stats
        self.health = 0
        self.collision_damage = 0
        self.invulnerable = False
        self.current_speed = self.speed
        self.isDead = False
        self.deathPlayed = False

    @abc.abstractmethod
    def load_animation_frames(self, enemies_tile_set):
        pass

    @abc.abstractmethod
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.uses_projectiles:
            if not self.can_attack:
                if current_time - self.attack_starting_time >= self.attack_cooldown:
                    self.can_attack = True
                    self.attack_cooldown = random.randrange(1200, 3600, 100)
                if self.state == 'attacking':
                    if current_time - self.attack_starting_time >= self.action_animation_cooldown * 2.5:
                        self.state = 'walking'

        if 'hurt' in self.state:
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = 'idle'

        if 'hurt' not in self.state:
            if current_time - self.hurt_starting_time >= self.invulnerability_cooldown:
                self.invulnerable = False

    @abc.abstractmethod
    def animate(self):
        pass

    @abc.abstractmethod
    # Monsters don't collide with other Monsters : NES compliant
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction_vector.x < 0:
                        self.hitbox.left = sprite.hitbox.right
            for particle in self.particle_sprites:
                if particle.hitbox.colliderect(self.hitbox):
                    if 'hurt' not in self.state and not self.invulnerable:
                        self.state = 'hurt_h'
                        self.hurt_starting_time = pygame.time.get_ticks()
                        self.invulnerable = True
                        self.direction_vector.y = 0
                        if self.hitbox.centerx - particle.hitbox.centerx <= 0:
                            self.direction_vector.x = -1
                            self.hitbox.x -= self.current_speed
                        else:
                            self.direction_vector.x = 1
                            self.hitbox.x += self.current_speed
                        self.health -= particle.collision_damage

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
            for particle in self.particle_sprites:
                if particle.hitbox.colliderect(self.hitbox):
                    if 'hurt' not in self.state and not self.invulnerable:
                        self.state = 'hurt_v'
                        self.hurt_starting_time = pygame.time.get_ticks()
                        self.invulnerable = True
                        self.direction_vector.x = 0
                        if self.hitbox.centerx - particle.hitbox.centerx <= 0:
                            self.direction_vector.y = -1
                            self.hitbox.y -= self.current_speed
                        else:
                            self.direction_vector.y = 1
                            self.hitbox.y += self.current_speed
                        self.health -= particle.collision_damage

    @abc.abstractmethod
    def move(self):
        if self.state == 'walking':
            match self.direction_label:
                case 'up':
                    self.direction_vector.x = 0
                    self.direction_vector.y = -1
                case 'down':
                    self.direction_vector.x = 0
                    self.direction_vector.y = 1
                case 'left':
                    self.direction_vector.x = -1
                    self.direction_vector.y = 0
                case 'right':
                    self.direction_vector.x = 1
                    self.direction_vector.y = 0
                case _:
                    debug(f"Monster tried to move {self.direction_label} !")

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    @abc.abstractmethod
    def update(self):
        current_time = pygame.time.get_ticks()
        if 'hurt' not in self.state:
            self.current_speed = self.speed
            if current_time - self.direction_starting_time >= self.direction_cooldown:
                self.direction_label = random.choice(['up', 'down', 'left', 'right'])
                self.direction_starting_time = current_time
                self.direction_cooldown = random.randrange(500, 2000, 100)
            if self.can_attack:
                self.state = 'attacking'
                self.attack_starting_time = current_time
                self.can_attack = False
        else:
            self.current_speed = (MONSTER_HURT_FRAMES - self.hurt_animation_frame_count)
        if not self.isDead:
            if self.state != 'attacking':
                self.move()
            if self.health <= 0:
                self.isDead = True

        self.animate()
        self.cooldowns()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class RedOctorock(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, particle_sprites, enemies_tile_set):
        super().__init__(pos, groups, obstacle_sprites, particle_sprites, enemies_tile_set, True)
        self.health = RED_OCTOROCK_HEALTH
        self.collision_damage = RED_OCTOROCK_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = OCTOROCK_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = OCTOROCK_ACTION_ANIMATION_COOLDOWN
        self.hurt_animation_cooldown = OCTOROCK_HURT_ANIMATION_COOLDOWN

    def load_animation_frames(self, enemies_tile_set):
        for i in range(OCTOROCK_WALKING_FRAMES):
            self.walking_animations['up'].append(
                pygame.transform.flip(
                    enemies_tile_set.get_sprite_image(OCTOROCK_WALKING_DOWN_FRAME_ID + (2 * i)),
                    False,
                    True))
            self.walking_animations['right'].append(
                pygame.transform.flip(
                    enemies_tile_set.get_sprite_image(OCTOROCK_WALKING_LEFT_FRAME_ID + (2 * i)),
                    True,
                    False))
            self.walking_animations['down'].append(
                enemies_tile_set.get_sprite_image(OCTOROCK_WALKING_DOWN_FRAME_ID + (2 * i)))
            self.walking_animations['left'].append(
                enemies_tile_set.get_sprite_image(OCTOROCK_WALKING_LEFT_FRAME_ID + (2 * i)))
        for i in range(MONSTER_HURT_FRAMES):
            self.hurt_animations['up'].append(
                pygame.transform.flip(
                    enemies_tile_set.get_sprite_image(OCTOROCK_HURT_DOWN_FRAME_ID + (2 * i)),
                    False,
                    True))
            self.hurt_animations['right'].append(
                pygame.transform.flip(
                    enemies_tile_set.get_sprite_image(OCTOROCK_HURT_LEFT_FRAME_ID + (2 * i)),
                    True,
                    False))
            self.hurt_animations['down'].append(
                enemies_tile_set.get_sprite_image(OCTOROCK_HURT_DOWN_FRAME_ID + (2 * i)))
            self.hurt_animations['left'].append(
                enemies_tile_set.get_sprite_image(OCTOROCK_HURT_LEFT_FRAME_ID + (2 * i)))
        for i in range(MONSTER_DEATH_FRAMES):
            self.despawn_animation.append(enemies_tile_set.get_sprite_image(MONSTER_DEATH_FRAME_ID + 2 * i))

    def cooldowns(self):
        super().cooldowns()

    def animate(self):
        current_time = pygame.time.get_ticks()

        # Going through the motions of multiple frames, with a timer per frame
        if not self.isDead:
            self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
            if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
                self.walking_animation_starting_time = pygame.time.get_ticks()
                if self.walking_animation_frame_count < OCTOROCK_WALKING_FRAMES - 1:
                    self.walking_animation_frame_count += 1
                else:
                    self.walking_animation_frame_count = 0
        else:
            self.image = self.despawn_animation[self.despawn_animation_frame_count]
            if current_time - self.despawn_animation_starting_time >- self.despawn_animation_cooldown:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                if self.despawn_animation_frame_count < MONSTER_DEATH_FRAMES - 1:
                    self.despawn_animation_frame_count += 1
                else:
                    self.deathPlayed = True


    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def update(self):
        super().update()

        # THIS CODE IS PROBABLY FOR MOBLIN ANIMATE()
        # current_time = pygame.time.get_ticks()
        # if self.state == 'idle':
        #     # Stops all animation, resetting to 1st walking frame of the current direction
        #     # Monsters don't idle, they walk while not moving
        #     # self.image = self.walking_animations[self.direction_label][0]
        #     pass
        # elif self.state == 'walking':
        #     # Going through the motions of multiple frames, with a timer per frame
        #     self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
        #     if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
        #         self.walking_animation_starting_time = pygame.time.get_ticks()
        #         if self.walking_animation_frame_count < PLAYER_WALKING_FRAMES - 1:
        #             self.walking_animation_frame_count += 1
        #         else:
        #             self.walking_animation_frame_count = 0
        # elif self.state == 'attacking':
        #     # Until projectile is shot : walking[dir][0], then walking[dir][1] for half as long, then walking[dir][0]
        #     if current_time - self.attack_animation_starting_time <= self.attack_animation_cooldown:
        #         self.image = self.walking_animations[self.direction_label][0]
        #     else:
        #         if current_time - self.attack_animation_starting_time <= self.attack_animation_cooldown*1.5:
        #             self.image = self.walking_animations[self.direction_label][0]
        #         else:
        #             self.image = self.walking_animations[self.direction_label][1]
        # else:
        #     debug(f'Error : animate({self.state}) does not exist')
