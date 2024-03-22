import pygame


class Npc(pygame.sprite.Sprite):
    def __init__(self, pos, groups, images: list):
        super().__init__()
        for group in groups:
            self.add(group)

        self.pos = pos

        self.images = images
        self.move_animation_frame_count = 0
        self.move_animation_timer_start = pygame.time.get_ticks()
        self.move_animation_cooldown = 100

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -4)

    def animate(self):
        current_time = pygame.time.get_ticks()

        self.image = self.images[self.move_animation_frame_count]
        if current_time - self.move_animation_timer_start >= self.move_animation_cooldown:
            self.move_animation_timer_start = pygame.time.get_ticks()
            if self.move_animation_frame_count < len(self.images) - 1:
                self.move_animation_frame_count += 1
            else:
                self.move_animation_frame_count = 0

    def update(self):
        self.animate()
        pygame.display.get_surface().blit(self.image, self.pos)
