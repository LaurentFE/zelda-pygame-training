import abc
import pygame
import random
import tileset
from settings import *
from entities import Entity
from particles import Rock


# Known issue : Monster waits for 'action_attack' to end before getting hurt
class Enemy(Entity):
    def __init__(self, groups, visible_sprites, obstacle_sprites, particle_sprites, uses_projectiles=False):
        super().__init__(groups, visible_sprites, obstacle_sprites, particle_sprites)

        self.direction_label = random.choice(['up', 'down', 'left', 'right'])
        self.state = ''
        self.speed = 1

        # Initialisation of values common to all Enemy used to load the different animations
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
    def load_animation_frames(self, enemies_tile_set):
        super().load_animation_frames(enemies_tile_set)

    @abc.abstractmethod
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Monster can shoot if he isn't in the hurt animation. Attack cooldown is randomized
        if self.uses_projectiles and 'hurt' not in self.state:
            if self.has_attacked:
                if current_time - self.attack_starting_time >= self.attack_cooldown:
                    self.has_attacked = False
                    self.attack_cooldown = random.randrange(1600, 4800, 100)
                if self.state == 'action_attack':
                    if current_time - self.attack_starting_time >= self.action_animation_cooldown * 2:
                        self.state = 'walking'
        # Hurt monster is invulnerable during animation, this is reset here
        if 'hurt' in self.state:
            if current_time - self.hurt_starting_time >= self.hurt_cooldown:
                self.state = 'walking'
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
            if self.state == 'idle':
                self.isSpawned = True
                self.state = 'walking'
        elif not self.isDead:
            super().animate()
        else:
            self.hitbox = self.rect.inflate(-32, -32)
            self.despawn_animation_starting_time, self.despawn_animation_frame_count = (
                self.change_animation_frame(self.despawn_animation,
                                            self.despawn_animation_frame_count,
                                            self.despawn_animation_starting_time,
                                            self.despawn_animation_cooldown,
                                            MONSTER_DEATH_FRAMES,
                                            True,
                                            True))
            if self.state == 'idle':
                self.deathPlayed = True

    @abc.abstractmethod
    # Monsters don't collide with other Monsters : NES compliant
    # Monsters don't collide with particles. Particles collide with enemies
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
                    # Illegal move, ignore
                    return

        self.hitbox.x += self.direction_vector.x * self.current_speed
        self.collision('horizontal')
        self.hitbox.y += self.direction_vector.y * self.current_speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def take_damage(self, amount, direction):
        if 'hurt' not in self.state and not self.invulnerable:
            self.state = 'hurt'
            self.hurt_starting_time = pygame.time.get_ticks()
            self.hurt_animation_starting_time = self.hurt_starting_time
            self.invulnerable = True

            # If origin of damage is static, enemy is pushed back to where he came from
            if direction == '':
                match self.direction_label:
                    case 'up':
                        direction = 'down'
                    case 'right':
                        direction = 'left'
                    case 'down':
                        direction = 'up'
                    case _:
                        direction = 'right'

            if direction == 'left':
                self.direction_vector.x = -1
                self.direction_vector.y = 0
                self.hitbox.x -= self.current_speed
                self.direction_label = 'right'
            elif direction == 'right':
                self.direction_vector.x = 1
                self.direction_vector.y = 0
                self.hitbox.x += self.current_speed
                self.direction_label = 'left'
            elif direction == 'up':
                self.direction_vector.y = -1
                self.direction_vector.x = 0
                self.hitbox.y -= self.current_speed
                self.direction_label = 'down'
            else:
                self.direction_vector.y = 1
                self.direction_vector.x = 0
                self.hitbox.y += self.current_speed
                self.direction_label = 'up'

            self.health -= amount
            if self.health > 0:
                self.monster_hurt_sound.play()

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
                self.state = 'action_attack'
                self.attack_starting_time = current_time
        else:
            # While hurt, Monster is repelled with a fading speed
            self.current_speed = (MONSTER_HURT_FRAMES - self.hurt_animation_frame_count)
        if self.isSpawned and not self.isDead:
            if self.state == 'action_attack' and not self.has_attacked:
                self.attack()
                self.has_attacked = True
            elif self.state != 'action_attack':
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
        self.is_up_flipped = True
        self.is_up_action_flipped = True
        self.is_right_flipped = True
        self.walking_up_frame_id = OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_down_frame_id = OCTOROCK_WALKING_DOWN_FRAME_ID
        self.walking_left_frame_id = OCTOROCK_WALKING_LEFT_FRAME_ID
        self.walking_right_frame_id = OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_up_frame_id = OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_down_frame_id = OCTOROCK_WALKING_DOWN_FRAME_ID
        self.action_left_frame_id = OCTOROCK_WALKING_LEFT_FRAME_ID
        self.action_right_frame_id = OCTOROCK_WALKING_LEFT_FRAME_ID
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
