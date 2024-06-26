# INPUTS CONST ARE IN INPUT MODULE

# SCREEN & TILE INFO
#
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 464
FPS = 60
SPRITE_SIZE = 32
FONT_SPRITE_SIZE = 16
TEXT_MARGIN = 4
MAX_CHAR_PER_ROW = SCREEN_WIDTH // FONT_SPRITE_SIZE - 2 * TEXT_MARGIN
TILE_SIZE = 16
NB_TILE_WIDTH = SCREEN_WIDTH//TILE_SIZE
NB_TILE_HEIGHT = SCREEN_HEIGHT//TILE_SIZE
TEXT_OFFSET = TEXT_MARGIN * FONT_SPRITE_SIZE

# CONSTANT STR
#
SAVE_FILE_PATH = "./save_file"
NONE_LABEL = 'None'
GAME_NAME = 'A Zelda NES homage in Python'
VICTORY_TEXT = 'congratulations !\n\n\n\n\n\n\n\n\n\nthe kingdom is safe,\nand you\'re a winner !!!'
GAME_OVER_TEXT = 'game over\n\npress enter to continue\npress escape to exit'
BLACK_LABEL = 'black'
RED1_LABEL = 'red1'
RED2_LABEL = 'red2'
RED3_LABEL = 'red3'
RED4_LABEL = 'red4'
RED_LIST = [RED1_LABEL, RED2_LABEL, RED3_LABEL, RED4_LABEL]
WHITE1_LABEL = 'white1'
WHITE2_LABEL = 'white2'
WHITE3_LABEL = 'white3'
WHITE4_LABEL = 'white4'
WHITE_LIST = [WHITE1_LABEL, WHITE2_LABEL, WHITE3_LABEL, WHITE4_LABEL]
FONT_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz,!\'&."?- '
HORIZONTAL_LABEL = 'horizontal'
VERTICAL_LABEL = 'vertical'
# Error messages
UNKNOWN_TILE_TYPE = 'tile_type must be a declared value in TILE_TYPES'
INCOMPATIBLE_PALETTES = 'Both palettes[Colors] must be of the same length'
WORD_TOO_LONG_FOR_TEXTBLOCK = 'Word is too long (>' + str(MAX_CHAR_PER_ROW) + ') for TextBlock : '
TEXTBLOCK_CHAR_SPRITE_NOT_DEFINED = 'Character in TextBlock string doesn\'t have a defined sprite : '
# Directions
UP_LABEL = 'up'
RIGHT_LABEL = 'right'
DOWN_LABEL = 'down'
LEFT_LABEL = 'left'
# Entity states
STATE_IDLE = 'idle'
STATE_WALKING = 'walking'
STATE_HURT = 'hurt'
STATE_ACTION = 'action'
# Player states
STATE_WARPING = 'warping'
STATE_WARPING_DUNGEON = STATE_WARPING + '_dungeon'
STATE_STAIRS = 'stairs'
STATE_ACTION_A = STATE_ACTION + 'A'
STATE_ACTION_B = STATE_ACTION + 'B'
STATE_DYING = 'dying'
STATE_SPINNING = 'spinning'
STATE_GRAY = 'gray'
STATE_DESPAWN = 'despawn'
STATE_IDLE_DOWN = STATE_IDLE + '_down'
PICKUP_PREFIX = 'pickup'
STATE_HURT_HORIZONTAL = STATE_HURT + '_h'
STATE_HURT_VERTICAL = STATE_HURT + '_v'
STATE_HURT_PARTICLE = STATE_HURT + '_p'
# Enemy states
STATE_RISING = 'rising'
STATE_DIVING = 'diving'
DASH_LABEL = 'dash'
MAGIC_LABEL = 'magic'
STATE_STUN = 'stun'
# Pick up animation labels are also Player states
ONE_HANDED = 'pickup_one_handed'
TWO_HANDED = 'pickup_two_handed'
STATE_TRIFORCE = 'pickup_triforce'
# Shop data structure
ITEMS_LABEL = 'items'
NPC_ID_LABEL = 'npc_id'
TEXT_LABEL = 'text'
# Map size definition structure
OVERWORLD_LABEL = 'Overworld'
DUNGEON_LABEL = 'Dungeon'
LEVEL_PREFIX_LABEL = 'level'
DUNGEON_PREFIX_LABEL = 'dungeon'
# Overworld <-> Underworld map warp structure
MAP_LABEL = 'map'
STAIRS_LABEL = 'stairs'
SCREEN_LABEL = 'screen'
PLAYER_POS_LABEL = 'player_pos'
HELP_LABEL = 'help'
# Dungeon Doors labels
DOOR_KEY_LABEL = "Key locked door"
DOOR_EVENT_LABEL = "Event locked door"
# Event label
OPEN_DOORS_LABEL = 'open doors'
# Graphics paths
GRAPHICS_EXTENSION = '.png'
GRAPHICS_PATH = './graphics/'
ENEMIES_PATH = GRAPHICS_PATH + 'enemies/'
FONT_PATH = GRAPHICS_PATH + 'font/'
HUD_PATH = GRAPHICS_PATH + 'hud/'
ITEMS_PATH = GRAPHICS_PATH + 'items/'
LEVELS_PATH = GRAPHICS_PATH + 'levels/'
NPCS_PATH = GRAPHICS_PATH + 'npcs/'
PLAYER_PATH = GRAPHICS_PATH + 'player/'
PAUSE_MENU_PATH = HUD_PATH + 'pause_menu.png'
HUD_PERMA_PATH = HUD_PATH + 'hud_perma.png'
BLACK_PATH = LEVELS_PATH + 'black.png'
# Maps file paths
MAPS_EXTENSION = '.csv'
MAPS_PATH = './map/'
MAPS_ENEMIES = '_Enemies'
MAPS_ITEMS = '_Items'
MAPS_LIMITS = '_Limits'
MAPS_BOMB = '_Secrets_Bomb'
MAPS_FLAME = '_Secrets_Flame'
MAPS_WARP = '_Warps'
# Tile sets types
TILE_CONSUMABLES = 'consumables'
TILE_DOORS = 'doors'
TILE_ENEMIES = 'enemies'
TILE_FONTS = 'font'
TILE_HUD = 'hud'
TILE_ITEMS = 'items'
TILE_LEVELS = 'levels'
TILE_NPCS = 'npcs'
TILE_PARTICLES = 'particles'
TILE_PLAYER = 'player'
TILE_WARPS = 'warps'
TILE_TYPES = [TILE_CONSUMABLES, TILE_DOORS, TILE_ENEMIES, TILE_FONTS, TILE_HUD, TILE_ITEMS,
              TILE_LEVELS, TILE_NPCS, TILE_PARTICLES, TILE_PLAYER, TILE_WARPS]
# Warps types
WARP_WARPS = 'warps'
WARP_BOMB = 'secrets_bomb'
WARP_FLAME = 'secrets_flame'
# Map transitions
MAP_TRANSITION_WARP = 'Warp'
MAP_TRANSITION_UP = 'Warp_U'
MAP_TRANSITION_RIGHT = 'Warp_R'
MAP_TRANSITION_DOWN = 'Warp_D'
MAP_TRANSITION_LEFT = 'Warp_L'
MAP_TRANSITION_STAIRS = 'Stairs'
MAP_TRANSITION_SILENT = 'Silent'
MAP_TRANSITION_DONE = 'Done'
# Items labels
LADDER_LABEL = 'Ladder'
BOOMERANG_LABEL = 'Boomerang'
BOMB_LABEL = 'Bomb'
CANDLE_LABEL = 'Candle'
HEARTRECEPTACLE_LABEL = 'Heart Receptacle'
WOOD_SWORD_LABEL = 'Wood Sword'
HEART_LABEL = 'Heart'
RUPEE_LABEL = 'Rupee'
FAIRY_LABEL = 'Fairy'
KEY_LABEL = 'Key'
TRIFORCE_LABEL = 'Triforce'
# Audio paths
AUDIO_PATH = './audio/'
THEME_OVERWORLD = AUDIO_PATH + 'Overworld.mp3'
THEME_DUNGEON = AUDIO_PATH + 'Dungeon.mp3'
SOUND_GAME_OVER = AUDIO_PATH + 'Game_Over.wav'
SOUND_SHIELD_BLOCK = AUDIO_PATH + 'Shield_Block.wav'
SOUND_PLAYER_HURT = AUDIO_PATH + 'Player_Hurt.wav'
SOUND_RUPEE_ACQUIRED = AUDIO_PATH + 'Rupee.wav'
SOUND_RUPEES_ACQUIRED = AUDIO_PATH + 'Rupee_Multiple.wav'
SOUND_LOW_HEALTH = AUDIO_PATH + 'Low_Health.wav'
SOUND_PLAYER_DESPAWN = AUDIO_PATH + 'Player_Despawn.wav'
SOUND_MONSTER_HURT = AUDIO_PATH + 'Monster_Hurt.wav'
SOUND_MONSTER_DESPAWN = AUDIO_PATH + 'Monster_Despawn.wav'
SOUND_SWORD_ATTACK = AUDIO_PATH + 'Sword_Attack.wav'
SOUND_BOOMERANG_ATTACK = AUDIO_PATH + 'Boomerang.wav'
SOUND_TINY_PICKUP = AUDIO_PATH + 'Tiny_Pick_Up.wav'
SOUND_SMALL_PICKUP = AUDIO_PATH + 'Small_Pick_Up.wav'
SOUND_PICKUP = AUDIO_PATH + 'Pick_Up.wav'
SOUND_BOMB_DROP = AUDIO_PATH + 'Bomb_Drop.wav'
SOUND_BOMB_EXPLODE = AUDIO_PATH + 'Bomb_Explode.wav'
SOUND_STAIRS = AUDIO_PATH + 'Stairs.wav'
SOUND_FLAME = AUDIO_PATH + 'Flame.wav'
SOUND_EVENT_CLEARED = AUDIO_PATH + 'Event_Cleared.wav'
SOUND_TRIFORCE_OBTAINED = AUDIO_PATH + 'Triforce_Obtained.wav'
SOUND_DOOR = AUDIO_PATH + 'Door.wav'

# COLOR PALETTE INFO
COLOR_KEY = (116, 116, 116)
PALETTE_NATURAL_LEVEL = [
    (0, 0, 0),  # Main Black
    (0, 168, 0),  # Main Green
    (252, 216, 168),  # Main Beige
    (32, 56, 236)  # Main Blue
]
PALETTE_NATURAL_DUNGEON = [
    (0, 0, 0),
    (24, 60, 92),
    (0, 128, 136),
    (0, 232, 216)
]
PALETTE_NATURAL_CAVE = [
    (0, 0, 0),
    (216, 40, 0),
    (252, 152, 56),
    (252, 116, 96)
]
PALETTE_DEATH = {
    RED1_LABEL: [
        (0, 0, 0),
        (200, 76, 12),
        (216, 40, 0),
        (252, 116, 96)
    ],
    RED2_LABEL: [
        (0, 0, 0),
        (164, 0, 0),
        (200, 76, 12),
        (216, 40, 0)
    ],
    RED3_LABEL: [
        (0, 0, 0),
        (124, 8, 0),
        (164, 0, 0),
        (216, 40, 0)
    ],
    RED4_LABEL: [
        (0, 0, 0),
        (0, 0, 0),
        (124, 8, 0),
        (164, 0, 0)
    ]
}
PALETTE_TRIFORCE = {
    WHITE1_LABEL: [
        (0, 0, 0),
        (116, 116, 116),
        (188, 188, 188),
        (255, 255, 255),
    ],
    WHITE2_LABEL: [
        (0, 0, 0),
        (116, 116, 116),
        (116, 116, 116),
        (188, 188, 188),
    ],
    WHITE3_LABEL: [
        (0, 0, 0),
        (0, 0, 0),
        (116, 116, 116),
        (116, 116, 116),
    ],
    WHITE4_LABEL: [
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    ],
}

# HEALTH & DAMAGES STATS
#
PLAYER_HEALTH_PER_HEART = 256
PLAYER_HEALTH_MAX = 16 * PLAYER_HEALTH_PER_HEART
PLAYER_INITIAL_HEALTH = 4 * PLAYER_HEALTH_PER_HEART
PLAYER_INITIAL_MONEY = 0
PLAYER_INITIAL_KEY = 0
PLAYER_INITIAL_BOMB = 0
PLAYER_INITIAL_HAS_BOMB = False
PLAYER_INITIAL_HAS_BOOMERANG = False
PLAYER_INITIAL_HAS_RED_CANDLE = False
PLAYER_INITIAL_HAS_LADDER = False
PLAYER_INITIAL_HAS_WOOD_SWORD = False
PLAYER_INITIAL_ITEM_A = NONE_LABEL
PLAYER_INITIAL_ITEM_B = NONE_LABEL
PLAYER_BOMBS_MAX = 16
PLAYER_BOMB_LOOT_AMOUNT = 4
DUNGEON_RUPEE_AMOUNT = 20
WOOD_SWORD_DMG = 16
WHITE_SWORD_DMG = 32
MAGICAL_SWORD_DMG = 64
BOOMERANG_DMG = 16
BLUE_RING_DMG_REDUCTION = 0.5
RED_RING_DMG_REDUCTION = 0.75
FLAME_DMG = 8
RED_OCTOROCK_HEALTH = 16
RED_OCTOROCK_DMG = PLAYER_HEALTH_PER_HEART // 2
BLUE_OCTOROCK_HEALTH = 32
BLUE_OCTOROCK_DMG = PLAYER_HEALTH_PER_HEART
BLUE_OCTOROCK_SPEED = 2
ROCK_DMG = PLAYER_HEALTH_PER_HEART // 2
ROCK_SPEED = 3
RED_MOBLIN_HEALTH = 32
RED_MOBLIN_DMG = PLAYER_HEALTH_PER_HEART // 2
BLACK_MOBLIN_HEALTH = 48
BLACK_MOBLIN_DMG = PLAYER_HEALTH_PER_HEART
BLACK_MOBLIN_SPEED = 2
ARROW_DMG = PLAYER_HEALTH_PER_HEART // 2
ARROW_SPEED = 6
ZORA_HEALTH = 48
ZORA_DMG = PLAYER_HEALTH_PER_HEART
MAGIC_MISSILE_DMG = PLAYER_HEALTH_PER_HEART
MAGIC_MISSILE_SPEED = 4
LEEVER_HEALTH = 48
LEEVER_DMG = PLAYER_HEALTH_PER_HEART // 2
STALFOS_HEALTH = 48
STALFOS_DMG = PLAYER_HEALTH_PER_HEART + PLAYER_HEALTH_PER_HEART // 2
GORIYA_HEALTH = 48
GORIYA_DMG = PLAYER_HEALTH_PER_HEART
GORIYA_BOOMERANG_TIMERANGE = 600
DARKNUT_HEALTH = 48
DARKNUT_DMG = PLAYER_HEALTH_PER_HEART
DARKNUT_DEF = 8
DARKNUT_MAGIC_DMG = PLAYER_HEALTH_PER_HEART
DARKNUT_SPEED = 1
DARKNUT_DASH_SPEED = 4
DARKNUT_STUN_COOLDOWN = 2000

# LOOT RANDOM FACTORS
#
LOOT_DROP_PERCENTAGE = 65
LOOT_BIG_RUPEE_PERCENTAGE = 20

# PLAYER ANIMATION & COOLDOWNS
#
# Player has no Left sprite (Left=Right flipped)
PLAYER_HITBOX_X_OFFSET = 4
PLAYER_HITBOX_Y_OFFSET = 12
PLAYER_HITBOX_X_DEFLATE = 2 * PLAYER_HITBOX_X_OFFSET
PLAYER_HITBOX_Y_DEFLATE = PLAYER_HITBOX_Y_OFFSET + 2
PLAYER_BATTLE_HITBOX_DEFLATE = 16
SHIELD_OFFSET = 2
SHIELD_HORIZONTAL_WIDTH = TILE_SIZE * 2 - 2 * SHIELD_OFFSET
SHIELD_HORIZONTAL_HEIGHT = 6
SHIELD_VERTICAL_WIDTH = 6
SHIELD_VERTICAL_HEIGHT = TILE_SIZE * 2 - 2 * SHIELD_OFFSET
SHIELD_DOWN_X = SHIELD_OFFSET
SHIELD_DOWN_Y = TILE_SIZE * 2 - SHIELD_HORIZONTAL_HEIGHT // 2
SHIELD_UP_X = SHIELD_OFFSET
SHIELD_UP_Y = SHIELD_HORIZONTAL_HEIGHT // 2
SHIELD_LEFT_X = -SHIELD_HORIZONTAL_HEIGHT // 2
SHIELD_LEFT_Y = SHIELD_OFFSET
SHIELD_RIGHT_X = TILE_SIZE * 2 - SHIELD_HORIZONTAL_HEIGHT // 2
SHIELD_RIGHT_Y = SHIELD_OFFSET
PLAYER_TRANSPARENT_FRAME_ID = 34
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
PLAYER_PICKUP_ONE_HANDED_FRAMES = 1
PLAYER_PICKUP_ONE_HANDED_FRAME_ID = 30
PLAYER_PICKUP_ONE_HANDED_ANIMATION_COOLDOWN = 100
PLAYER_PICKUP_ONE_HANDED_COOLDOWN = 1500
PLAYER_PICKUP_TWO_HANDED_FRAMES = 1
PLAYER_PICKUP_TWO_HANDED_FRAME_ID = 32
PLAYER_PICKUP_TWO_HANDED_ANIMATION_COOLDOWN = 100
PLAYER_PICKUP_TWO_HANDED_COOLDOWN = 1500
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
WOOD_SWORD_ATTACK_FRAMES = 3
WOOD_SWORD_UP_FRAME_ID = 0
WOOD_SWORD_RIGHT_FRAME_ID = 6
WOOD_SWORD_DOWN_FRAME_ID = 12

ROCK_FRAME_ID = 40
ROCK_FRAMES = 1
ARROW_FRAME_UP_ID = 42
ARROW_FRAME_RIGHT_ID = 44
ARROW_FRAMES = 1
MAGIC_MISSILE_FRAME_ID = 80
MAGIC_MISSILE_FRAMES = 2
MAGIC_EXPLOSION_TOP_LEFT_SPRITE = 130

# ITEMS SPRITES & INFO
#
RAFT_FRAME_ID = 0
MAGIC_TOME_FRAME_ID = 2
RED_RING_FRAME_ID = 4
LADDER_FRAME_ID = 6
LADDER_FRAMES = 1
MAGIC_KEY_FRAME_ID = 8
POWER_BRACELET_FRAME_ID = 10
BOOMERANG_FRAME_ID = 24
BOOMERANG_FRAMES = 2
BOOMERANG_SPEED = 6
BOMB_FRAME_ID = 26
BOW_ARROW_FRAME_ID = 28
RED_CANDLE_FRAME_ID = 30
RED_CANDLE_FRAMES = 1
RECORDER_FRAME_ID = 48
MEAT_FRAME_ID = 50
MEDICINE_FRAME_ID = 52
MAGICAL_ROD_FRAME_ID = 54
WOOD_SWORD_FRAME_ID = 32
WOOD_SWORD_FRAMES = 1
TRIFORCE_FRAME_ID = 58
TRIFORCE_FRAMES = 1

# USABLE ITEM SPRITES
#
PBOMB_FRAMES = 1
PBOMB_FRAME_ID = 48
PBOMB_SMOKE_FRAMES = 3
PBOMB_SMOKE_FRAME_ID = 50
FLAME_FRAMES = 2
FLAME_FRAME_ID = 56
FLAME_SPEED = 1

# CONSUMABLE SPRITES & INFO
#
HEART_FRAME_ID = 0
HEART_FRAMES = 2
RUPEE_FRAME_ID = 4
RUPEE_FRAMES = 2
CBOMB_FRAME_ID = 8
CBOMB_FRAMES = 1
FAIRY_FRAMES_ID = 10
FAIRY_FRAMES = 2
FAIRY_SPEED = 1
HEARTRECEPTACLE_FRAME_ID = 14
HEARTRECEPTACLE_FRAMES = 1
KEY_FRAME_ID = 16
KEY_FRAMES = 1

# PICKUP ANIMATION PER ITEM LABEL
#
ITEM_PICKUP_ANIMATION = {
    LADDER_LABEL: TWO_HANDED,
    BOOMERANG_LABEL: ONE_HANDED,
    CANDLE_LABEL: ONE_HANDED,
    HEARTRECEPTACLE_LABEL: TWO_HANDED,
    WOOD_SWORD_LABEL: ONE_HANDED,
    TRIFORCE_LABEL: TRIFORCE_LABEL
}

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
MONSTER_ABOVE_GROUND_COOLDOWN = 3000
MONSTER_UNDER_GROUND_COOLDOWN = 4000
MONSTER_ATTACK_RANGE_START = 1600
MONSTER_ATTACK_RANGE_STOP = 4800

# OCTOROCK ANIMATION & COOLDOWNS
# Octorock has no Up (flip Down) nor Right (flip Left)
OCTOROCK_WALKING_FRAMES = 2
RED_OCTOROCK_WALKING_DOWN_FRAME_ID = 0
RED_OCTOROCK_WALKING_LEFT_FRAME_ID = 4
BLUE_OCTOROCK_WALKING_DOWN_FRAME_ID = 8
BLUE_OCTOROCK_WALKING_LEFT_FRAME_ID = 12
OCTOROCK_WALKING_ANIMATION_COOLDOWN = 100
OCTOROCK_HURT_DOWN_FRAME_ID = 88
OCTOROCK_HURT_LEFT_FRAME_ID = 94
OCTOROCK_ACTION_ANIMATION_COOLDOWN = 250
BLUE_OCTOROCK_ATTACK_RANGE_START = 800
BLUE_OCTOROCK_ATTACK_RANGE_STOP = 3000

# MOBLIN ANIMATION & COOLDOWNS
# Moblin has no Right (Flip Left); and animation for  Up/Down is flip(x)
MOBLIN_WALKING_FRAMES = 2
RED_MOBLIN_WALKING_DOWN_FRAME_ID = 44
RED_MOBLIN_WALKING_UP_FRAME_ID = 46
RED_MOBLIN_WALKING_LEFT_FRAME_ID = 48
BLACK_MOBLIN_WALKING_DOWN_FRAME_ID = 52
BLACK_MOBLIN_WALKING_UP_FRAME_ID = 54
BLACK_MOBLIN_WALKING_LEFT_FRAME_ID = 56
MOBLIN_WALKING_ANIMATION_COOLDOWN = 100
MOBLIN_HURT_DOWN_FRAME_ID = 132
MOBLIN_HURT_UP_FRAME_ID = 138
MOBLIN_HURT_LEFT_FRAME_ID = 144
MOBLIN_ACTION_ANIMATION_COOLDOWN = 250
BLACK_MOBLIN_ATTACK_RANGE_START = 800
BLACK_MOBLIN_ATTACK_RANGE_STOP = 3000

# STALFOS ANIMATION & COOLDOWNS
# Stalfos has only one sprite. Animation is flip(x) in any direction
STALFOS_WALKING_FRAMES = 2
STALFOS_WALKING_FRAME_ID = 264
STALFOS_WALKING_ANIMATION_COOLDOWN = 100
STALFOS_HURT_FRAME_ID = 266
STALFOS_ACTION_ANIMATION_COOLDOWN = 100
STALFOS_RANDOM_DURATION = 2500
STALFOS_PLAYER_SEEKING_DURATION = 3500

# GORIYA ANIMATION & COOLDOWNS
# Goriya has no Right (Flip Left); and animation for Up/Down is flip(x)
GORIYA_WALKING_FRAMES = 2
GORIYA_WALKING_DOWN_FRAME_ID = 308
GORIYA_WALKING_UP_FRAME_ID = 310
GORIYA_WALKING_LEFT_FRAME_ID = 312
GORIYA_WALKING_ANIMATION_COOLDOWN = 150
GORIYA_HURT_DOWN_FRAME_ID = 316
GORIYA_HURT_UP_FRAME_ID = 322
GORIYA_HURT_LEFT_FRAME_ID = 272
GORIYA_ACTION_ANIMATION_COOLDOWN = 250

# ZORA ANIMATION & COOLDOWNS
# Zora doesn't walk, but dives
ZORA_DIVE_FRAMES = 2
ZORA_DIVE_FRAME_ID = 176
ZORA_DIVE_ANIMATION_COOLDOWN = 150
ZORA_WALKING_FRAMES = 1
ZORA_WALKING_UP_FRAME_ID = 182
ZORA_WALKING_DOWN_FRAME_ID = 180
ZORA_WALKING_ANIMATION_COOLDOWN = 100
ZORA_HURT_UP_FRAME_ID = 190
ZORA_HURT_DOWN_FRAME_ID = 184
ZORA_ACTION_ANIMATION_COOLDOWN = 250

# LEEVER ANIMATION & COOLDOWNS
# Leever dives
LEEVER_DIVE_FRAMES = 3
LEEVER_DIVE_FRAME_ID = 220
LEEVER_DIVE_ANIMATION_COOLDOWN = 300
LEEVER_WALKING_FRAMES = 2
LEEVER_WALKING_FRAME_ID = 226
LEEVER_WALKING_ANIMATION_COOLDOWN = 100
LEEVER_HURT_FRAME_ID = 230
LEEVER_ACTION_ANIMATION_COOLDOWN = 250

# DARKNUT ANIMATION & COOLDOWNS
# Darknut has no Right frame, it's Left flipped(x) and up animation is flip(x)
DARKNUT_WALKING_FRAMES = 2
DARKNUT_WALKING_DOWN_FRAME_ID = 352
DARKNUT_WALKING_UP_FRAME_ID = 356
DARKNUT_WALKING_LEFT_FRAME_ID = 360
DARKNUT_WALKING_ANIMATION_COOLDOWN = 200
DARKNUT_HURT_DOWN_FRAME_ID = 396
DARKNUT_HURT_UP_FRAME_ID = 402
DARKNUT_HURT_LEFT_FRAME_ID = 408
DARKNUT_HURT_ANIMATION_COOLDOWN = 75
DARKNUT_ACTION_ANIMATION_COOLDOWN = 300
DARKNUT_DASH_COOLDOWN = 2000
DARKNUT_MAGIC_COOLDOWN = 3000
DARKNUT_SHIELD_OFFSET = 4
DARKNUT_VERTICAL_SHIELD_HEIGHT = TILE_SIZE * 2 - DARKNUT_SHIELD_OFFSET * 2
DARKNUT_VERTICAL_SHIELD_WIDTH = 8
DARKNUT_VERTICAL_SHIELD_Y_OFFSET = DARKNUT_SHIELD_OFFSET
DARKNUT_HORIZONTAL_SHIELD_HEIGHT = 8
DARKNUT_HORIZONTAL_SHIELD_WIDTH = TILE_SIZE * 2 - DARKNUT_SHIELD_OFFSET * 2
DARKNUT_HORIZONTAL_SHIELD_X_OFFSET = DARKNUT_SHIELD_OFFSET
DARKNUT_SHIELD_DOWN_X = DARKNUT_HORIZONTAL_SHIELD_X_OFFSET
DARKNUT_SHIELD_DOWN_Y = TILE_SIZE * 2 - DARKNUT_HORIZONTAL_SHIELD_HEIGHT // 2
DARKNUT_SHIELD_UP_X = DARKNUT_HORIZONTAL_SHIELD_X_OFFSET
DARKNUT_SHIELD_UP_Y = -DARKNUT_HORIZONTAL_SHIELD_HEIGHT // 2
DARKNUT_SHIELD_LEFT_X = -DARKNUT_VERTICAL_SHIELD_WIDTH // 2
DARKNUT_SHIELD_LEFT_Y = DARKNUT_VERTICAL_SHIELD_Y_OFFSET
DARKNUT_SHIELD_RIGHT_X = TILE_SIZE * 2 - DARKNUT_VERTICAL_SHIELD_WIDTH // 2
DARKNUT_SHIELD_RIGHT_Y = DARKNUT_VERTICAL_SHIELD_Y_OFFSET

# DISPLAY POSITIONS
#
HUD_TILE_HEIGHT = 7
HUD_TILE_WIDTH = 32
HUD_OFFSET = HUD_TILE_HEIGHT * TILE_SIZE
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

# GAME WON ANIMATION DETAILS
#
MAP_VICTORY_FADE_COOLDOWN = 2000

# GAME OVER ANIMATION DETAILS
#
MAP_DEATH_FADE_COOLDOWN = 500

# MENU ACCESS AND SELECTOR
#
LEVEL_KEY_PRESSED_COOLDOWN = 75
MENU_ITEM_SELECTOR_FRAMES = 2
MENU_ITEM_SELECTOR_FRAME_ID = 6
MENU_ITEM_SELECTOR_COOLDOWN = 200

# MENU ITEM SPRITE COORDINATES
#
# Selected item frame
MENU_SELECTED_ITEM_TOPLEFT = (128, 96)
# Passive items
MENU_RAFT_TOPLEFT = (256, 48)
MENU_MAGIC_TOME_TOPLEFT = (296, 48)
MENU_RING_TOPLEFT = (320, 48)
MENU_LADDER_TOPLEFT = (352, 48)
MENU_MAGICAL_KEY_TOPLEFT = (386, 48)
MENU_POWER_BRACELET_TOPLEFT = (408, 48)
# Selectable items
MENU_BOOMERANG_TOPLEFT = (256, 96)
MENU_BOMBS_TOPLEFT = (304, 96)
MENU_BOW_AND_ARROW_TOPLEFT = (352, 96)
MENU_CANDLE_TOPLEFT = (400, 96)
MENU_RECORDER_TOPLEFT = (256, 128)
MENU_MEAT_TOPLEFT = (304, 128)
MENU_MEDICINE_TOPLEFT = (352, 128)
MENU_MAGICAL_ROD_TOPLEFT = (400, 128)

# DUNGEON DOORS SPRITES
#
DOOR_TILE_SIZE = 4
DOOR_KEY_UP_FRAME_ID = 0
DOOR_KEY_RIGHT_FRAME_ID = 4
DOOR_KEY_DOWN_FRAME_ID = 8
DOOR_KEY_LEFT_FRAME_ID = 12
DOOR_EVENT_UP_FRAME_ID = 64
DOOR_EVENT_RIGHT_FRAME_ID = 68
DOOR_EVENT_DOWN_FRAME_ID = 72
DOOR_EVENT_LEFT_FRAME_ID = 76
# Door coordinates
DOOR_UP_POS = (14 * TILE_SIZE, HUD_OFFSET)
DOOR_RIGHT_POS = (28 * TILE_SIZE, HUD_OFFSET + 9 * TILE_SIZE)
DOOR_DOWN_POS = (14 * TILE_SIZE, SCREEN_HEIGHT - 4 * TILE_SIZE)
DOOR_LEFT_POS = (0, HUD_OFFSET + 9 * TILE_SIZE)

# FONTS
#
FONT_CHARACTERS_PER_ROW = 10
FONT_NUMBER_OF_ROWS = 5
FONT_NUMBER_OF_SPECIALS = 9

# OVERWORLD <-> UNDERWORLD MAP WARPS/STAIRS
#
# As a reminder, the first entry of this dict corresponds to a change_id of 4
# See 'help' for a reminder of who is what
NEW_LEVEL_BOTTOM_CENTER_POS = (SCREEN_WIDTH / 2 - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 3 - 1)
NEW_LEVEL_TOP_CENTER_POS = (SCREEN_WIDTH / 2 - TILE_SIZE, HUD_OFFSET + TILE_SIZE + 1)
NEW_DUNGEON_BOTTOM_CENTER_POS = (SCREEN_WIDTH / 2 - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 5 - 1)
UNDERWORLD_STAIRS = [
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '10',
     PLAYER_POS_LABEL: (128, 32 + HUD_OFFSET + TILE_SIZE + 1),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (4) is the exit from the sword_cave0 to level10'},
    {MAP_LABEL: 'sword_cave',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (5) is the entrance of sword_cave0 from level10'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '6',
     PLAYER_POS_LABEL: (192, HUD_OFFSET + 160),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (6) is the exit of pay_for_my_door0 to level6'},
    {MAP_LABEL: 'pay_for_my_door',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (7) is the secret entrance of pay_for_my_door0 from level6'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '11',
     PLAYER_POS_LABEL: (144, HUD_OFFSET + 112),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (8) is the exit of shop00 to level11'},
    {MAP_LABEL: 'shop0',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (9) is the entrance of shop00 from level11'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '4',
     PLAYER_POS_LABEL: (224, HUD_OFFSET + 272),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (A) is the exit of dungeon0_10 to level4'},
    {MAP_LABEL: 'dungeon0_',
     SCREEN_LABEL: '10',
     PLAYER_POS_LABEL: NEW_DUNGEON_BOTTOM_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (B) is the entrance of dungeon0_10 from level4'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '9',
     PLAYER_POS_LABEL: (32, HUD_OFFSET + 32),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (C) is the exit of secret_to_everybody0 to level9'},
    {MAP_LABEL: 'secret_to_everybody',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (D) is the entrance of secret_to_everybody0 from level9'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '7',
     PLAYER_POS_LABEL: (96, HUD_OFFSET + 64),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (E) is the top exit of secret_tunnel0 to level7'},
    {MAP_LABEL: 'secret_tunnel',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (F) is the bottom entrance of secret_tunnel0 from level7'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '7',
     PLAYER_POS_LABEL: (128, HUD_OFFSET + 224),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (G) is the bottom exit of secret_tunnel0 to level7'},
    {MAP_LABEL: 'secret_tunnel',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_TOP_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (H) is the top entrance of secret_tunnel0 from level7'},
    {MAP_LABEL: LEVEL_PREFIX_LABEL,
     SCREEN_LABEL: '3',
     PLAYER_POS_LABEL: (384, HUD_OFFSET + 192),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (I) is the exit of you_ll_need_this0 to level7'},
    {MAP_LABEL: 'you_ll_need_this',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (J) is the entrance of you_ll_need_this0 from level3'},
]

# MAP SYSTEM
#
# Map sizes
NB_MAPS_PER_ROW = {
    OVERWORLD_LABEL: 4,
    DUNGEON_LABEL: 4
}
NB_MAPS_PER_COL = {
    OVERWORLD_LABEL: 4,
    DUNGEON_LABEL: 3
}
# Map scrolling animation
MAP_SCROLL_FRAMES_COUNT = 100

# CSV FILES INDEXES
#
# Map CSV indexes and obstacle types
OBSTACLE_NPC = 0
LIMIT_BORDER_INDEX = 10
LIMIT_LAKE_BORDER_INDEX = 11
LIMIT_TREE_INDEX = 20
LIMIT_WATER_INDEX = 30
LIMIT_ROCK_INDEX = 40
LIMIT_LADDER_INDEX = 50
# Secret passages sprite frame id
SECRET_CAVE_FRAME_ID = 0
SECRET_STAIRS_FRAME_ID = 2
SECRET_WALL_FRAME_ID = 4
# Secret content in maps
# When a secret passage has been revealed, an entry 'level_id': True is created.
# Warning : with this system, there can't be multiple secrets in one screen (both fire & bomb for instance)
MAP_SECRETS_REVEALED = {
}
# Item content in maps
MAP_ITEMS = {
    LEVEL_PREFIX_LABEL + '3': {HEARTRECEPTACLE_LABEL: True},
    LEVEL_PREFIX_LABEL + '5': {HEARTRECEPTACLE_LABEL: True},
    LEVEL_PREFIX_LABEL + '9': {HEARTRECEPTACLE_LABEL: True},
    LEVEL_PREFIX_LABEL + '14': {LADDER_LABEL: True},
    DUNGEON_PREFIX_LABEL + '0_3': {TRIFORCE_LABEL: True},
    DUNGEON_PREFIX_LABEL + '0_8': {HEARTRECEPTACLE_LABEL: True},
    DUNGEON_PREFIX_LABEL + '0_11': {KEY_LABEL: True}
}

# NPCS
#
NO_NPC_ID = 0
OLD_MAN_ID = 2
OLD_WOMAN_ID = 4
MERCHANT_ID = 6
MOBLIN_ID = 8
NPC_FLAME_ID = 10
ANIMATED_FLIPPED_NPCS = [MOBLIN_ID, NPC_FLAME_ID]

# SHOP SPRITES COORDINATES
#
ITEM_Y = HUD_OFFSET + TEXT_OFFSET + 9 * TILE_SIZE
NPC_X = 15 * TILE_SIZE
NPC_Y = ITEM_Y - 4 * TILE_SIZE
FLAME_1_POS = (NPC_X - 6 * TILE_SIZE, NPC_Y)
FLAME_2_POS = (NPC_X + 6 * TILE_SIZE, NPC_Y)

# SHOPS AND SHOP CONTENT
#
# Warning : using ", " in the text of the shop will crash the game when the player loads their save file.
SHOPS = {
    'sword_cave0': {ITEMS_LABEL: {WOOD_SWORD_LABEL: 0},
                    NPC_ID_LABEL: OLD_MAN_ID,
                    TEXT_LABEL: 'it\'s dangerous to go alone,\ntake this !'},
    'shop00': {ITEMS_LABEL: {CANDLE_LABEL: 30,
                             BOMB_LABEL: 15,
                             HEART_LABEL: 5},
               NPC_ID_LABEL: MERCHANT_ID,
               TEXT_LABEL: 'welcome to my shop.'},
    'pay_for_my_door0': {ITEMS_LABEL: {RUPEE_LABEL: 25},
                         NPC_ID_LABEL: OLD_WOMAN_ID,
                         TEXT_LABEL: 'that is for my door !'},
    'secret_to_everybody0': {ITEMS_LABEL: {RUPEE_LABEL: -80},
                             NPC_ID_LABEL: MOBLIN_ID,
                             TEXT_LABEL: 'it\'s a secret to everybody.'},
    'you_ll_need_this0': {ITEMS_LABEL: {KEY_LABEL: 0},
                          NPC_ID_LABEL: OLD_MAN_ID,
                          TEXT_LABEL: 'hey mister hero. you\'ll need this.'},
    'dungeon0_4': {ITEMS_LABEL: {BOMB_LABEL: 20},
                   NPC_ID_LABEL: MOBLIN_ID,
                   TEXT_LABEL: 'a heavy armored monster once told me that bombs are quite shocking.'}
}
# SHOP_dict name indicates the tile set
# Key is label of item
# Value is frame_id of the item in the tile set
SHOP_CONSUMABLES = {
    BOMB_LABEL: CBOMB_FRAME_ID,
    HEARTRECEPTACLE_LABEL: HEARTRECEPTACLE_FRAME_ID,
    HEART_LABEL: HEART_FRAME_ID,
    RUPEE_LABEL: RUPEE_FRAME_ID,
    KEY_LABEL: KEY_FRAME_ID
}
SHOP_ITEMS = {
    LADDER_LABEL: LADDER_FRAME_ID,
    BOOMERANG_LABEL: BOOMERANG_FRAME_ID,
    CANDLE_LABEL: RED_CANDLE_FRAME_ID,
    WOOD_SWORD_LABEL: WOOD_SWORD_FRAME_ID
}

# MONSTER KILL EVENTS LOCATION
#
MONSTER_KILL_EVENT = {
    DUNGEON_PREFIX_LABEL + '0_0': KEY_LABEL,
    DUNGEON_PREFIX_LABEL + '0_6': BOOMERANG_LABEL,
    DUNGEON_PREFIX_LABEL + '0_9': BOMB_LABEL,
    DUNGEON_PREFIX_LABEL + '0_2': OPEN_DOORS_LABEL
}

# DUNGEON MONSTER DECIMATION TRACKER
#
DUNGEON_DECIMATION = {
    DUNGEON_PREFIX_LABEL + '0_0': False,
    DUNGEON_PREFIX_LABEL + '0_1': False,
    DUNGEON_PREFIX_LABEL + '0_2': False,
    DUNGEON_PREFIX_LABEL + '0_3': False,
    DUNGEON_PREFIX_LABEL + '0_4': False,
    DUNGEON_PREFIX_LABEL + '0_5': False,
    DUNGEON_PREFIX_LABEL + '0_6': False,
    DUNGEON_PREFIX_LABEL + '0_7': False,
    DUNGEON_PREFIX_LABEL + '0_8': False,
    DUNGEON_PREFIX_LABEL + '0_9': False,
    DUNGEON_PREFIX_LABEL + '0_10': False,
    DUNGEON_PREFIX_LABEL + '0_11': False
}

# DUNGEON DOORS TRACKER
#
DUNGEON_DOORS = {
    DUNGEON_PREFIX_LABEL + '0_1': {RIGHT_LABEL: DOOR_KEY_LABEL},
    DUNGEON_PREFIX_LABEL + '0_2': {RIGHT_LABEL: DOOR_EVENT_LABEL},
    DUNGEON_PREFIX_LABEL + '0_5': {UP_LABEL: DOOR_KEY_LABEL},
    DUNGEON_PREFIX_LABEL + '0_6': {LEFT_LABEL: DOOR_KEY_LABEL}
}

# GAME STARTING COORDINATES
#
OVERWORLD_PLAYER_START_POS = (SCREEN_WIDTH // 2 - TILE_SIZE, (SCREEN_HEIGHT + HUD_OFFSET) // 2 - TILE_SIZE)
DUNGEON_PLAYER_START_POS = NEW_DUNGEON_BOTTOM_CENTER_POS
OVERWORLD_STARTING_MAP = LEVEL_PREFIX_LABEL
OVERWORLD_STARTING_SCREEN = '10'
DUNGEON_STARTING_MAP = DUNGEON_PREFIX_LABEL + '0_'
DUNGEON_STARTING_SCREEN = '10'
STARTING_MAP = OVERWORLD_STARTING_MAP
STARTING_SCREEN = OVERWORLD_STARTING_SCREEN
