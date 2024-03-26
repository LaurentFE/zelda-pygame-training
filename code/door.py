import pygame
import code.tileset as tileset
import code.level as game
import code.settings as cfg


class Door(pygame.sprite.Sprite):
    def __init__(self, groups, door_position, door_type=cfg.DOOR_KEY_LABEL):
        super().__init__()
        for group in groups:
            self.add(group)

        self.door_position = door_position
        self.type = door_type
        if door_position == cfg.UP_LABEL:
            self.image_position = cfg.DOOR_UP_POS
            if door_type == cfg.DOOR_KEY_LABEL:
                self.sprite_id = cfg.DOOR_KEY_UP_FRAME_ID
            else:
                self.sprite_id = cfg.DOOR_EVENT_UP_FRAME_ID
        elif door_position == cfg.RIGHT_LABEL:
            self.image_position = cfg.DOOR_RIGHT_POS
            if door_type == cfg.DOOR_KEY_LABEL:
                self.sprite_id = cfg.DOOR_KEY_RIGHT_FRAME_ID
            else:
                self.sprite_id = cfg.DOOR_EVENT_RIGHT_FRAME_ID
        elif door_position == cfg.DOWN_LABEL:
            self.image_position = cfg.DOOR_DOWN_POS
            if door_type == cfg.DOOR_KEY_LABEL:
                self.sprite_id = cfg.DOOR_KEY_DOWN_FRAME_ID
            else:
                self.sprite_id = cfg.DOOR_EVENT_DOWN_FRAME_ID
        else:
            self.image_position = cfg.DOOR_LEFT_POS
            if door_type == cfg.DOOR_KEY_LABEL:
                self.sprite_id = cfg.DOOR_KEY_LEFT_FRAME_ID
            else:
                self.sprite_id = cfg.DOOR_EVENT_LEFT_FRAME_ID
        self.image = tileset.DOORS_TILE_SET.get_sprite_image(self.sprite_id)
        self.rect = self.image.get_rect(topleft=self.image_position)
        self.hitbox = self.rect.inflate(-4, -4)
        self.door_sound = pygame.mixer.Sound(cfg.SOUND_DOOR)
        self.door_sound.set_volume(0.3)
        self.door_sound.play()

    def open(self):
        level_id = str(game.Level().current_map) + str(game.Level().current_map_screen)
        cfg.DUNGEON_DOORS[level_id].pop(self.door_position)
        if self.type == cfg.DOOR_EVENT_LABEL:
            cfg.MONSTER_KILL_EVENT.pop(level_id)
        self.door_sound.play()
        self.kill()

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
