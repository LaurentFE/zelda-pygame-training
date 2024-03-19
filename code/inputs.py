import pygame

# INPUT SETTINGS
UP_KEY_1 = pygame.K_UP
UP_KEY_2 = pygame.K_z
DOWN_KEY_1 = pygame.K_DOWN
DOWN_KEY_2 = pygame.K_s
LEFT_KEY_1 = pygame.K_LEFT
LEFT_KEY_2 = pygame.K_q
RIGHT_KEY_1 = pygame.K_RIGHT
RIGHT_KEY_2 = pygame.K_d
ACTION_A_KEY = pygame.K_SPACE
ACTION_B_KEY = pygame.K_LSHIFT
MENU_KEY = pygame.K_ESCAPE


def is_move_key_pressed(keys):
    if (is_up_key_pressed(keys)
            or is_down_key_pressed(keys)
            or is_left_key_pressed(keys)
            or is_right_key_pressed(keys)):
        return True
    return False


def is_up_key_pressed(keys):
    if (UP_KEY_1 in keys
            or UP_KEY_2 in keys):
        return True
    return False


def is_down_key_pressed(keys):
    if (DOWN_KEY_1 in keys
            or DOWN_KEY_2 in keys):
        return True
    return False


def is_left_key_pressed(keys):
    if (LEFT_KEY_1 in keys
            or LEFT_KEY_2 in keys):
        return True,
    return False


def is_right_key_pressed(keys):
    if (RIGHT_KEY_1 in keys
            or RIGHT_KEY_2 in keys):
        return True
    return False


def is_action_a_key_pressed(keys):
    if ACTION_A_KEY in keys:
        return True
    return False


def is_action_b_key_pressed(keys):
    if ACTION_B_KEY in keys:
        return True
    return False


def is_menu_key_pressed(keys):
    if MENU_KEY in keys:
        return True
    return False
