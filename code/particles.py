import pygame


# TODO : DECIDE HOW TO IMPLEMENT
# Sprite => Particle => Weapon/Projectile/Misc
# or something else ?
# animation & move should be in update()
class Particle(pygame.sprite.Sprite):
    def __init__(self, owner_pos, groups, obstacle_sprites, tile_set):
        super().__init__(groups)
        self.owner_pos = owner_pos
        self.obstacle_sprites = obstacle_sprites
        self.load_animation_frames(tile_set)

    def load_animation_frames(self, tile_set):
        pass

    def animate(self):
        pass

    def collision(self):
        pass

    def move(self):
        pass

    def cooldowns(self):
        pass

    def update(self):
        pass
