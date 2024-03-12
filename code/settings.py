# INPUTS CONST ARE IN INPUT MODULE

# SCREEN & TILE INFO
#
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 464
FPS = 60
SPRITE_SIZE = 32
FONT_SPRITE_SIZE = 16
TILE_SIZE = 16
NB_TILE_WIDTH = SCREEN_WIDTH//TILE_SIZE
NB_TILE_HEIGHT = SCREEN_HEIGHT//TILE_SIZE
COLOR_KEY = (116, 116, 116)

# Health & Damages Stats
#
PLAYER_HEALTH_PER_HEART = 256
PLAYER_HEALTH_MAX = 16 * PLAYER_HEALTH_PER_HEART
PLAYER_INITIAL_HEALTH = 3 * PLAYER_HEALTH_PER_HEART
PLAYER_INITIAL_MONEY = 0
PLAYER_INITIAL_KEY = 0
PLAYER_INITIAL_BOMB = 0
PLAYER_INITIAL_HAS_BOMB = False
PLAYER_INITIAL_HAS_BOOMERANG = False
PLAYER_INITIAL_HAS_RED_CANDLE = False
PLAYER_INITIAL_HAS_LADDER = False
PLAYER_INITIAL_HAS_WOOD_SWORD = False
PLAYER_INITIAL_ITEM_A = "None"
PLAYER_INITIAL_ITEM_B = "None"
PLAYER_BOMBS_MAX = 8
PLAYER_BOMB_LOOT_AMOUNT = 4
WOOD_SWORD_DMG = 16
WHITE_SWORD_DMG = 32
MAGICAL_SWORD_DMG = 64
BLUE_RING_DMG_REDUCTION = 0.5
RED_RING_DMG_REDUCTION = 0.75
# For test purposes, RED_OCTOROCK_HEALTH has been changed from 16 to 32
RED_OCTOROCK_HEALTH = 32
RED_OCTOROCK_DMG = 128
BLUE_OCTOROCK_HEALTH = 32
BLUE_OCTOROCK_DMG = 128
ROCK_DMG = 128
ROCK_SPEED = 2
ORANGE_MOBLIN_HEALTH = 32
ORANGE_MOBLIN_DMG = 128
BLACK_MOBLIN_HEALTH = 48
BLACK_MOBLIN_DMG = 128

LOOT_DROP_PERCENTAGE = 100

# PLAYER ANIMATION & COOLDOWNS
#
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
PLAYER_PICKUP_MAJOR_COOLDOWN = 1500
PLAYER_HURT_FRAMES = 3
PLAYER_HURT_DOWN_FRAME_ID = 48
PLAYER_HURT_RIGHT_FRAME_ID = 72
PLAYER_HURT_UP_FRAME_ID = 96
PLAYER_HURT_ANIMATION_COOLDOWN = 150
PLAYER_GRAY_WALKING_DOWN_FRAME_ID = 120
PLAYER_GRAY_COOLDOWN = 1000
PLAYER_DEATH_FRAMES = 2
PLAYER_DEATH_FRAME_ID = 144
PLAYER_DEATH_ANIMATION_COOLDOWN = 150
PLAYER_DEATH_SPIN_AMOUNT = 3
PLAYER_DEATH_SPIN_DURATION = 500
PLAYER_DEATH_HURT_COOLDOWN = 3 * PLAYER_HURT_FRAMES * PLAYER_HURT_ANIMATION_COOLDOWN
PLAYER_STAIRS_FRAMES = 4
PLAYER_STAIRS_FRAME_ID = 148
PLAYER_STAIRS_ANIMATION_COOLDOWN = 150
PLAYER_STAIRS_DURATION = PLAYER_STAIRS_FRAMES * PLAYER_STAIRS_ANIMATION_COOLDOWN
WOOD_SWORD_FRAMES = 3
WOOD_SWORD_UP_FRAME_ID = 0
WOOD_SWORD_RIGHT_FRAME_ID = 6
WOOD_SWORD_DOWN_FRAME_ID = 12
WOOD_SWORD_DURATION = 500
ROCK_FRAME_ID = 40
MAGIC_EXPLOSION_TOP_LEFT_SPRITE = 130

# ITEMS LABEL
#
LADDER_LABEL = 'Ladder'
BOOMERANG_LABEL = 'Boomerang'
BOMB_LABEL = 'Bomb'
CANDLE_LABEL = 'Candle'
HEARTRECEPTACLE_LABEL = 'Heart Receptacle'
WOOD_SWORD_LABEL = 'Wood Sword'

# ITEMS SPRITES
#
RAFT_FRAME_ID = 0
MAGIC_TOME_FRAME_ID = 2
RED_RING_FRAME_ID = 4
LADDER_FRAME_ID = 6
MAGIC_KEY_FRAME_ID = 8
POWER_BRACELET_FRAME_ID = 10
BOOMERANG_FRAME_ID = 24
BOMB_FRAME_ID = 26
BOW_ARROW_FRAME_ID = 28
RED_CANDLE_FRAME_ID = 30
RECORDER_FRAME_ID = 48
MEAT_FRAME_ID = 50
MEDICINE_FRAME_ID = 52
MAGICAL_ROD_FRAME_ID = 54
WOOD_SWORD_FRAME_ID = 32

# USABLE ITEM SPRITES
#
PBOMB_FRAME_ID = 48
PBOMB_SMOKE_FRAMES = 3
PBOMB_SMOKE_FRAME_ID = 50

# CONSUMABLE SPRITES
#
HEART_FRAME_ID = 0
HEART_FRAMES = 2
RUPEE_FRAME_ID = 4
RUPEE_FRAMES = 2
CBOMB_FRAME_ID = 8
CBOMB_FRAMES = 1
FAIRY_FRAMES_ID = 10
FAIRY_FRAMES = 2
HEARTRECEPTACLE_FRAME_ID = 14
HEARTRECEPTACLE_FRAMES = 1

# MONSTER ANIMATION & COOLDOWNS
#
MONSTER_SPAWN_FRAMES = 3
MONSTER_SPAWN_FRAME_ID = 16
MONSTER_SPAWN_ANIMATION_COOLDOWN = 200
MONSTER_HURT_FRAMES = 3
MONSTER_DEATH_FRAMES = 3
MONSTER_DEATH_FRAME_ID = 100
MONSTER_DEATH_ANIMATION_COOLDOWN = 200
MONSTER_HURT_ANIMATION_COOLDOWN = 150
# OCTOROCK ANIMATION & COOLDOWNS
# OCTOROCK HAS NO UP (REVERSE DOWN) NOR RIGHT (REVERSE LEFT)
OCTOROCK_WALKING_FRAMES = 2
OCTOROCK_WALKING_DOWN_FRAME_ID = 0
OCTOROCK_WALKING_LEFT_FRAME_ID = 4
OCTOROCK_WALKING_ANIMATION_COOLDOWN = 100
OCTOROCK_HURT_DOWN_FRAME_ID = 88
OCTOROCK_HURT_LEFT_FRAME_ID = 94
OCTOROCK_ACTION_ANIMATION_COOLDOWN = 250

# DISPLAY POSITIONS
#
HUD_TILE_HEIGHT = 7
HUD_TILE_WIDTH = 32
HUD_MONEY_HUNDREDS_POSITION = (192, 32)
HUD_MONEY_TENS_POSITION = (192+16, 32)
HUD_MONEY_UNITS_POSITION = (192+32, 32)
HUD_KEYS_HUNDREDS_POSITION = (192, 64)
HUD_KEYS_TENS_POSITION = (192+16, 64)
HUD_KEYS_UNITS_POSITION = (192+32, 64)
HUD_BOMBS_HUNDREDS_POSITION = (192, 80)
HUD_BOMBS_TENS_POSITION = (192+16, 80)
HUD_BOMBS_UNITS_POSITION = (192+32, 80)
HUD_FIRST_HEART_POSITION_X = 352
HUD_FIRST_HEART_POSITION_Y = 80
HUD_FULL_HEART_FRAME_ID = 4
HUD_HALF_HEART_FRAME_ID = 2
HUD_EMPTY_HEART_FRAME_ID = 0
HUD_NB_HEARTS_PER_LINE = 8

GAME_OVER_DEATH_FLOORS = ['red1', 'red2', 'red3']
MAP_DEATH_FADE_COOLDOWN = 500
LEVEL_KEY_PRESSED_COOLDOWN = 150
MENU_ITEM_SELECTOR_FRAMES = 2
MENU_ITEM_SELECTOR_FRAME_ID = 6
MENU_ITEM_SELECTOR_COOLDOWN = 200

# MENU ITEM SPRITE COORDINATES
# SELECTED ITEM FRAME
MENU_SELECTED_ITEM_TOPLEFT = (128, 96)
# PASSIVE ITEMS
MENU_RAFT_TOPLEFT = (256, 48)
MENU_MAGIC_TOME_TOPLEFT = (296, 48)
MENU_RING_TOPLEFT = (320, 48)
MENU_LADDER_TOPLEFT = (352, 48)
MENU_MAGICAL_KEY_TOPLEFT = (386, 48)
MENU_POWER_BRACELET_TOPLEFT = (408, 48)
# SELECTABLE ITEMS
MENU_BOOMERANG_TOPLEFT = (256, 96)
MENU_BOMBS_TOPLEFT = (304, 96)
MENU_BOW_AND_ARROW_TOPLEFT = (352, 96)
MENU_CANDLE_TOPLEFT = (400, 96)
MENU_RECORDER_TOPLEFT = (256, 128)
MENU_MEAT_TOPLEFT = (304, 128)
MENU_MEDICINE_TOPLEFT = (352, 128)
MENU_MAGICAL_ROD_TOPLEFT = (400, 128)

# FONTS
FONT_CHARACTERS_PER_ROW = 10
FONT_NUMBER_OF_ROWS = 5
FONT_NUMBER_OF_SPECIALS = 9
FONT_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz,!\'&."?- '

# SOUNDS
AUDIO_PATH = '../audio/'
THEME_OVERWORLD = AUDIO_PATH + 'Overworld.mp3'
THEME_DUNGEON = AUDIO_PATH + 'Dungeon.mp3'
SOUND_GAME_OVER = AUDIO_PATH + 'Game_Over.wav'
SOUND_SHIELD_BLOCK = AUDIO_PATH + 'Shield_Block.wav'
SOUND_PLAYER_HURT = AUDIO_PATH + 'Player_Hurt.wav'
SOUND_RUPEE_ACQUIRED = AUDIO_PATH + 'Rupee.wav'
SOUND_LOW_HEALTH = AUDIO_PATH + 'Low_Health.wav'
SOUND_PLAYER_DESPAWN = AUDIO_PATH + 'Player_Despawn.wav'
SOUND_MONSTER_HURT = AUDIO_PATH + 'Monster_Hurt.wav'
SOUND_MONSTER_DESPAWN = AUDIO_PATH + 'Monster_Despawn.wav'
SOUND_SWORD_ATTACK = AUDIO_PATH + 'Sword_Attack.wav'
SOUND_TINY_PICKUP = AUDIO_PATH + 'Tiny_Pick_Up.wav'
SOUND_SMALL_PICKUP = AUDIO_PATH + 'Small_Pick_Up.wav'
SOUND_PICKUP = AUDIO_PATH + 'Pick_Up.wav'
SOUND_BOMB_DROP = AUDIO_PATH + 'Bomb_Drop.wav'
SOUND_BOMB_EXPLODE = AUDIO_PATH + 'Bomb_Explode.wav'
SOUND_STAIRS = AUDIO_PATH + 'Stairs.wav'

# Underworld map id
NEW_LEVEL_BOTTOM_CENTER_POS = (SCREEN_WIDTH / 2 - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 3 - 1)
UNDERWORLD_STAIRS = [
    {'map': 'level',
     'screen': '10',
     'player_pos': (128, 32 + HUD_TILE_HEIGHT * TILE_SIZE + TILE_SIZE + 1),
     'stairs': False},
    {'map': 'sword_cave',
     'screen': '0',
     'player_pos': NEW_LEVEL_BOTTOM_CENTER_POS,
     'stairs': True},
    {'map': 'level',
     'screen': '6',
     'player_pos': (192, HUD_TILE_HEIGHT * TILE_SIZE + 160),
     'stairs': False},
    {'map': 'pay_for_my_door',
     'screen': '0',
     'player_pos': NEW_LEVEL_BOTTOM_CENTER_POS,
     'stairs': False},
    {'map': 'level',
     'screen': '0',
     'player_pos': (200, 200),
     'stairs': False},
    {'map': 'shop0',
     'screen': '0',
     'player_pos': NEW_LEVEL_BOTTOM_CENTER_POS,
     'stairs': True},
    {'map': 'level',
     'screen': '0',
     'player_pos': (200, 200),
     'stairs': False},
    {'map': 'dungeon0_',
     'screen': '0',
     'player_pos': NEW_LEVEL_BOTTOM_CENTER_POS,
     'stairs': True},
    {'map': 'level',
     'screen': '0',
     'player_pos': (200, 200),
     'stairs': False}
]

# Map system
NB_MAPS_PER_ROW = {
    'Overworld': 4,
    'Dungeon': 3
}
NB_MAPS_PER_COL = {
    'Overworld': 4,
    'Dungeon': 3
}

MAP_SCROLL_FRAMES_COUNT = 100

# Map CSV indexes
#
LIMIT_BORDER_INDEX = 10
LIMIT_TREE_INDEX = 20
LIMIT_WATER_INDEX = 30
LIMIT_ROCK_INDEX = 40
LIMIT_LADDER_INDEX = 50

# Item content in maps
MAP_ITEMS = {
    'level9': {HEARTRECEPTACLE_LABEL: True},
    'level11': {LADDER_LABEL: True},
    'sword_cave0': {WOOD_SWORD_LABEL: True}
}
