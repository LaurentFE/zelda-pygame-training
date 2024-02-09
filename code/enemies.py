import abc
import pygame
import random
from settings import *
from debug import debug
from entities import Entity
from particles import Rock


# Known issue : Monster waits for 'attacking' to end before getting hurt
class Enemy(Entity):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites,
                 enemies_tile_set, particle_tileset, uses_projectiles=False):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites, particle_tileset)

        self.direction_label = random.choice(['up', 'down', 'left', 'right'])
        self.state = 'walking'
        self.speed = 1

        self.load_animation_frames(enemies_tile_set)

        # Set first image of the monster appearing when created, and generating corresponding hitbox
        self.image = self.spawn_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        # Monster actions cooldowns
        # Monsters always move, except if shooting, or special mechanic such as flying, jumping, diving(water/land)
        self.uses_projectiles = uses_projectiles
        self.can_attack = self.uses_projectiles
        self.has_attacked = True
        self.attack_cooldown = random.randrange(1600, 4800, 100)
        self.attack_starting_time = pygame.time.get_ticks()
        self.can_move = True
        self.direction_cooldown = 200
        self.direction_starting_time = 0
        self.hurt_starting_time = 0
        self.hurt_animation_cooldown = MONSTER_HURT_ANIMATION_COOLDOWN
        self.hurt_cooldown = (MONSTER_HURT_FRAMES + 1) * self.hurt_animation_cooldown

        self.spawn_animation_frame_count = 0
        self.spawn_animation_starting_time = 0
        self.spawn_animation_cooldown = MONSTER_SPAWN_ANIMATION_COOLDOWN
        self.despawn_animation_frame_count = 0
        self.despawn_animation_starting_time = 0
        self.despawn_animation_cooldown = MONSTER_DEATH_ANIMATION_COOLDOWN

        # Monster stats
        self.health = 0
        self.collision_damage = 0
        self.invulnerable = False
        self.current_speed = self.speed
        self.isSpawned = False
        self.isDead = False
        self.deathPlayed = False

    @abc.abstractmethod
    def load_animation_frames(self, enemies_tile_set):
        pass

    @abc.abstractmethod
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Monster can shoot if he isn't in the hurt animation. Attack cooldown is randomized
        if self.uses_projectiles and 'hurt' not in self.state:
            if self.has_attacked:
                if current_time - self.attack_starting_time >= self.attack_cooldown:
                    self.has_attacked = False
                    self.attack_cooldown = random.randrange(1600, 4800, 100)
                if self.state == 'attacking':
                    if current_time - self.attack_starting_time >= self.action_animation_cooldown * 2:
                        self.state = 'walking'
        # Hurt monster is invulnerable during animation, this is reset here
        if 'hurt' in self.state:
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = 'walking'
                self.invulnerable = False
                self.hurt_animation_frame_count = 0

    @abc.abstractmethod
    def animate(self):
        pass

    @abc.abstractmethod
    def animate_spawn(self, current_time):
        self.image = self.spawn_animation[self.spawn_animation_frame_count]
        if current_time - self.spawn_animation_starting_time >= self.spawn_animation_cooldown:
            self.spawn_animation_starting_time = pygame.time.get_ticks()
            if self.spawn_animation_frame_count < MONSTER_SPAWN_FRAMES - 1:
                self.spawn_animation_frame_count += 1
            else:
                self.spawn_animation_frame_count = 0
                self.isSpawned = True

    @abc.abstractmethod
    def animate_despawn(self, current_time):
        self.image = self.despawn_animation[self.despawn_animation_frame_count]
        self.hitbox = self.rect.inflate(-32, -32)
        if current_time - self.despawn_animation_starting_time >= self.despawn_animation_cooldown:
            self.despawn_animation_starting_time = pygame.time.get_ticks()
            if self.despawn_animation_frame_count < MONSTER_DEATH_FRAMES - 1:
                self.despawn_animation_frame_count += 1
            else:
                self.deathPlayed = True

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

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction_vector.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction_vector.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

        # Monster is repelled opposite of the direction_label of the particle that hits them
        for particle in self.particle_sprites:
            if particle.hitbox.colliderect(self.hitbox):
                if 'hurt' not in self.state and not self.invulnerable and particle.affects_enemy:
                    self.state = 'hurt'
                    self.hurt_starting_time = pygame.time.get_ticks()
                    self.hurt_animation_starting_time = self.hurt_starting_time
                    self.invulnerable = True
                    # Should I just copy particle vector ?
                    # Maybe for boomerang ? If Player's reaction to Particle works, use it here too
                    if particle.direction_label == 'left':
                        self.direction_vector.x = -1
                        self.direction_vector.y = 0
                        self.hitbox.x -= self.current_speed
                        self.direction_label = 'right'
                    elif particle.direction_label == 'right':
                        self.direction_vector.x = 1
                        self.direction_vector.y = 0
                        self.hitbox.x += self.current_speed
                        self.direction_label = 'left'
                    elif particle.direction_label == 'up':
                        self.direction_vector.y = -1
                        self.direction_vector.x = 0
                        self.hitbox.y -= self.current_speed
                        self.direction_label = 'down'
                    else:
                        self.direction_vector.y = 1
                        self.direction_vector.x = 0
                        self.hitbox.y += self.current_speed
                        self.direction_label = 'up'
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
    def attack(self):
        pass

    @abc.abstractmethod
    def update(self):
        current_time = pygame.time.get_ticks()

        # Attacks interrupt movements if available.
        if 'hurt' not in self.state:
            self.current_speed = self.speed
            if (self.isSpawned
                    and self.state == 'walking'
                    and current_time - self.direction_starting_time >= self.direction_cooldown):
                self.direction_label = random.choice(['up', 'down', 'left', 'right'])
                self.direction_starting_time = current_time
                self.direction_cooldown = random.randrange(500, 2000, 100)
            if self. isSpawned and self.can_attack and not self.has_attacked:
                self.state = 'attacking'
                self.attack_starting_time = current_time
        else:
            # While hurt, Monster is repelled with a fading speed
            self.current_speed = (MONSTER_HURT_FRAMES - self.hurt_animation_frame_count)
        if self.isSpawned and not self.isDead:
            if self.state == 'attacking' and not self.has_attacked:
                self.attack()
                self.has_attacked = True
            elif self.state != 'attacking':
                self.move()
            if self.health <= 0:
                self.despawn_animation_starting_time = pygame.time.get_ticks()
                self.isDead = True

        self.animate()
        self.cooldowns()

        pygame.display.get_surface().blit(self.image, self.rect.topleft)


class RedOctorock(Enemy):
    def __init__(self, pos, groups, visible_sprites, obstacle_sprites, particle_sprites,
                 enemies_tileset, particle_tileset):
        super().__init__(pos, groups, visible_sprites, obstacle_sprites, particle_sprites,
                         enemies_tileset, particle_tileset, True)
        self.health = RED_OCTOROCK_HEALTH
        self.collision_damage = RED_OCTOROCK_DMG

        # All cooldowns are in milliseconds
        # Cooldown between animation frames
        self.walking_animation_cooldown = OCTOROCK_WALKING_ANIMATION_COOLDOWN
        self.action_animation_cooldown = OCTOROCK_ACTION_ANIMATION_COOLDOWN

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
        for i in range(MONSTER_SPAWN_FRAMES):
            self.spawn_animation.append(enemies_tile_set.get_sprite_image(MONSTER_SPAWN_FRAME_ID + (2 * i)))
        for i in range(MONSTER_DEATH_FRAMES):
            self.despawn_animation.append(enemies_tile_set.get_sprite_image(MONSTER_DEATH_FRAME_ID + (2 * i)))

    def cooldowns(self):
        super().cooldowns()

    def animate_spawn(self, current_time):
        super().animate_spawn(current_time)

    def animate_despawn(self, current_time):
        super().animate_despawn(current_time)

    def animate(self):
        current_time = pygame.time.get_ticks()

        if not self.isSpawned:
            self.animate_spawn(current_time)
        elif not self.isDead:
            if self.state == 'walking':
                self.image = self.walking_animations[self.direction_label][self.walking_animation_frame_count]
                if current_time - self.walking_animation_starting_time >= self.walking_animation_cooldown:
                    self.walking_animation_starting_time = pygame.time.get_ticks()
                    if self.walking_animation_frame_count < OCTOROCK_WALKING_FRAMES - 1:
                        self.walking_animation_frame_count += 1
                    else:
                        self.walking_animation_frame_count = 0
            elif 'hurt' in self.state:
                self.image = self.hurt_animations[self.direction_label][self.hurt_animation_frame_count]
                if current_time - self.hurt_animation_starting_time >= self.hurt_animation_cooldown:
                    self.hurt_animation_starting_time = pygame.time.get_ticks()
                    if self.hurt_animation_frame_count < MONSTER_HURT_FRAMES - 1:
                        self.hurt_animation_frame_count += 1
                    else:
                        self.image = self.walking_animations[self.direction_label][0]

        else:
            self.animate_despawn(current_time)

    def collision(self, direction):
        super().collision(direction)

    def move(self):
        super().move()

    def attack(self):
        Rock(self.rect.topleft,
             self.direction_vector,
             [self.visible_sprites, self.particle_sprites],
             self.direction_label,
             self.particle_tileset,
             self.obstacle_sprites)

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
