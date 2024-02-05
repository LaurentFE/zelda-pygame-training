# TILE FILE
#
TILE_SIZE = 16
COLOR_KEY = (116, 116, 116)

# Health & Damages Stats
PLAYER_HEALTH_PER_HEART = 256
PLAYER_HEALTH_MAX = 16 * PLAYER_HEALTH_PER_HEART
PLAYER_INITIAL_HEALTH = 3 * PLAYER_HEALTH_PER_HEART
WOOD_SWORD_DMG = 16
WHITE_SWORD_DMG = 32
MAGICAL_SWORD_DMG = 64
BLUE_RING_DMG_REDUCTION = 0.5
RED_RING_DMG_REDUCTION = 0.75
# RED_OCTOROCK_HEALTH should be 16, doubled for now to test the hurt mechanic on it
RED_OCTOROCK_HEALTH = 32
RED_OCTOROCK_DMG = 128
BLUE_OCTOROCK_HEALTH = 32
BLUE_OCTOROCK_DMG = 128
ORANGE_MOBLIN_HEALTH = 32
ORANGE_MOBLIN_DMG = 128
BLACK_MOBLIN_HEALTH = 48
BLACK_MOBLIN_DMG = 128

# PLAYER ANIMATION & COOLDOWNS
# PLAYER HAS NO LEFT TILES, EQUAL TO FLIP(RIGHT)
PLAYER_WALKING_FRAMES = 2
PLAYER_WALKING_DOWN_FRAME_ID = 0
PLAYER_WALKING_RIGHT_FRAME_ID = 4
PLAYER_WALKING_UP_FRAME_ID = 8
PLAYER_WALKING_ANIMATION_COOLDOWN = 150
PLAYER_ACTION_FRAMES = 1
PLAYER_ACTION_DOWN_FRAME_ID = 24
PLAYER_ACTION_RIGHT_FRAME_ID = 26
PLAYER_ACTION_UP_FRAME_ID = 28
PLAYER_ACTION_ANIMATION_COOLDOWN = 375
PLAYER_PICKUP_MINOR_FRAMES = 1
PLAYER_PICKUP_MINOR_FRAME_ID = 30
PLAYER_PICKUP_MINOR_ANIMATION_COOLDOWN = 100
PLAYER_PICKUP_MAJOR_FRAMES = 1
PLAYER_PICKUP_MAJOR_FRAME_ID = 32
PLAYER_PICKUP_MAJOR_ANIMATION_COOLDOWN = 100
PLAYER_HURT_FRAMES = 3
PLAYER_HURT_DOWN_FRAME_ID = 48
PLAYER_HURT_RIGHT_FRAME_ID = 72
PLAYER_HURT_UP_FRAME_ID = 96
PLAYER_HURT_ANIMATION_COOLDOWN = 100
PLAYER_GRAY_WALKING_DOWN_FRAME_ID = 120
PLAYER_GRAY_COOLDOWN = 1000
PLAYER_DEATH_FRAMES = 2
PLAYER_DEATH_FRAME_ID = 144
PLAYER_DEATH_ANIMATION_COOLDOWN = 150
PLAYER_DEATH_SPIN_AMOUNT = 3
PLAYER_DEATH_SPIN_DURATION = 500
PLAYER_DEATH_HURT_COOLDOWN = 1500
# SWORD IS 16*32 or 32*16, how to handle it ?
WOOD_SWORD_FRAMES = 3
WOOD_SWORD_UP_FRAME_ID = 0
WOOD_SWORD_RIGHT_FRAME_ID = 6
WOOD_SWORD_DOWN_FRAME_ID = 12
WOOD_SWORD_DURATION = 500
WTF_IS_THIS = 130

# MONSTER ANIMATION & COOLDOWNS
MONSTER_SPAWN_FRAMES = 3
MONSTER_SPAWN_FRAME_ID = 100
MONSTER_SPAWN_ANIMATION_COOLDOWN = 200
MONSTER_HURT_FRAMES = 3
MONSTER_DEATH_FRAMES = 2
MONSTER_DEATH_FRAME_ID = 18
MONSTER_DEATH_ANIMATION_COOLDOWN = 200
MONSTER_HURT_ANIMATION_COOLDOWN = 100
# OCTOROCK ANIMATION & COOLDOWNS
# OCTOROCK HAS NO UP (REVERSE DOWN) NOR RIGHT (REVERSE LEFT)
OCTOROCK_WALKING_FRAMES = 2
OCTOROCK_WALKING_DOWN_FRAME_ID = 0
OCTOROCK_WALKING_LEFT_FRAME_ID = 4
OCTOROCK_WALKING_ANIMATION_COOLDOWN = 100
OCTOROCK_HURT_DOWN_FRAME_ID = 88
OCTOROCK_HURT_LEFT_FRAME_ID = 94
OCTOROCK_ACTION_ANIMATION_COOLDOWN = 250

# DISPLAY
#
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 464
FPS = 60
MENU_TILE_HEIGHT = 7
MENU_TILE_WIDTH = 32
MENU_MONEY_HUNDREDS_POSITION = (192, 32)
MENU_MONEY_TENS_POSITION = (192+16, 32)
MENU_MONEY_UNITS_POSITION = (192+32, 32)
MENU_KEYS_HUNDREDS_POSITION = (192, 64)
MENU_KEYS_TENS_POSITION = (192+16, 64)
MENU_KEYS_UNITS_POSITION = (192+32, 64)
MENU_BOMBS_HUNDREDS_POSITION = (192, 80)
MENU_BOMBS_TENS_POSITION = (192+16, 80)
MENU_BOMBS_UNITS_POSITION = (192+32, 80)
MENU_FIRST_HEART_POSITION_X = 352
MENU_FIRST_HEART_POSITION_Y = 80
MENU_FULL_HEART_FRAME_ID = 2
MENU_HALF_HEART_FRAME_ID = 1
MENU_EMPTY_HEART_FRAME_ID = 0
MENU_NB_HEARTS_PER_LINE = 8

MAP_DEATH_FADE_COOLDOWN = 500

# FONTS
FONT_CHARACTERS_PER_ROW = 10
FONT_NUMBER_OF_ROWS = 5
FONT_NUMBER_OF_SPECIALS = 9
FONT_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz,!\'&."?- '
