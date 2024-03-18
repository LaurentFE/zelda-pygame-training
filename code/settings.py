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
NONE_LABEL = 'None'
GAME_NAME = 'A Zelda NES homage in Python'
GAME_OVER_TEXT = 'game over'
BLACK_LABEL = 'black'
RED1_LABEL = 'red1'
RED2_LABEL = 'red2'
RED3_LABEL = 'red3'
RED4_LABEL = 'red4'
RED_LIST = [RED1_LABEL, RED2_LABEL, RED3_LABEL, RED4_LABEL]
FONT_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz,!\'&."?- '
HORIZONTAL_LABEL = 'horizontal'
VERTICAL_LABEL = 'vertical'
# Error messages
UNKNOWN_TILE_TYPE = 'tile_type must be a declared value in TILE_TYPES'
INCOMPATIBLE_PALETTES = 'Both palettes[Colors] must be of the same length'
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
# Pick up animation labels are also Player states
ONE_HANDED = 'pickup_one_handed'
TWO_HANDED = 'pickup_two_handed'
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
# Graphics paths
GRAPHICS_EXTENSION = '.png'
GRAPHICS_PATH = '../graphics/'
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
MAPS_PATH = '../map/'
MAPS_ENEMIES = '_Enemies'
MAPS_ITEMS = '_Items'
MAPS_LIMITS = '_Limits'
MAPS_BOMB = '_Secrets_Bomb'
MAPS_FLAME = '_Secrets_Flame'
MAPS_WARP = '_Warps'
# Tile sets types
TILE_CONSUMABLES = 'consumables'
TILE_ENEMIES = 'enemies'
TILE_FONTS = 'font'
TILE_HUD = 'hud'
TILE_ITEMS = 'items'
TILE_LEVELS = 'levels'
TILE_NPCS = 'npcs'
TILE_PARTICLES = 'particles'
TILE_PLAYER = 'player'
TILE_WARPS = 'warps'
TILE_TYPES = [TILE_CONSUMABLES, TILE_ENEMIES, TILE_FONTS, TILE_HUD, TILE_ITEMS,
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
# Audio paths
AUDIO_PATH = '../audio/'
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

# HEALTH & DAMAGES STATS
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
PLAYER_INITIAL_ITEM_A = NONE_LABEL
PLAYER_INITIAL_ITEM_B = NONE_LABEL
PLAYER_BOMBS_MAX = 8
PLAYER_BOMB_LOOT_AMOUNT = 4
WOOD_SWORD_DMG = 16
WHITE_SWORD_DMG = 32
MAGICAL_SWORD_DMG = 64
BOOMERANG_DMG = 16
BLUE_RING_DMG_REDUCTION = 0.5
RED_RING_DMG_REDUCTION = 0.75
FLAME_DMG = 16
RED_OCTOROCK_HEALTH = 16
RED_OCTOROCK_DMG = 128
BLUE_OCTOROCK_HEALTH = 32
BLUE_OCTOROCK_DMG = 128
ROCK_DMG = 128
ROCK_SPEED = 2
RED_MOBLIN_HEALTH = 32
RED_MOBLIN_DMG = 128
ARROW_DMG = 128
ARROW_SPEED = 4
BLACK_MOBLIN_HEALTH = 48
BLACK_MOBLIN_DMG = 128

LOOT_DROP_PERCENTAGE = 100
LOOT_BIG_RUPEE_PERCENTAGE = 20

# PLAYER ANIMATION & COOLDOWNS
#
# Player has no Left sprite (Left=Right flipped)
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
    WOOD_SWORD_LABEL: ONE_HANDED
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

# OCTOROCK ANIMATION & COOLDOWNS
# Octorock has no Up (flip Down) nor Right (flip Left)
OCTOROCK_WALKING_FRAMES = 2
OCTOROCK_WALKING_DOWN_FRAME_ID = 0
OCTOROCK_WALKING_LEFT_FRAME_ID = 4
OCTOROCK_WALKING_ANIMATION_COOLDOWN = 100
OCTOROCK_HURT_DOWN_FRAME_ID = 88
OCTOROCK_HURT_LEFT_FRAME_ID = 94
OCTOROCK_ACTION_ANIMATION_COOLDOWN = 250

# MOBLIN ANIMATION & COOLDOWNS
# Moblin has no Right (Flip Left); and animation for  Up/Down is flip(x)
MOBLIN_WALKING_FRAMES = 2
MOBLIN_WALKING_DOWN_FRAME_ID = 44
MOBLIN_WALKING_UP_FRAME_ID = 46
MOBLIN_WALKING_LEFT_FRAME_ID = 48
MOBLIN_WALKING_ANIMATION_COOLDOWN = 100
MOBLIN_HURT_DOWN_FRAME_ID = 132
MOBLIN_HURT_UP_FRAME_ID = 138
MOBLIN_HURT_LEFT_FRAME_ID = 144
MOBLIN_ACTION_ANIMATION_COOLDOWN = 250

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

# GAME OVER ANIMATION DETAILS
#
MAP_DEATH_FADE_COOLDOWN = 500

# MENU ACCESS AND SELECTOR
#
LEVEL_KEY_PRESSED_COOLDOWN = 150
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
     PLAYER_POS_LABEL: (200, 200),
     STAIRS_LABEL: False,
     HELP_LABEL: 'This (A) is the exit of dungeon0_0 to level4'},
    {MAP_LABEL: 'dungeon0_',
     SCREEN_LABEL: '0',
     PLAYER_POS_LABEL: NEW_LEVEL_BOTTOM_CENTER_POS,
     STAIRS_LABEL: True,
     HELP_LABEL: 'This (B) is the entrance of dungeon0_0 from level4'},
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
     PLAYER_POS_LABEL: (96, HUD_OFFSET + 32),
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
    DUNGEON_LABEL: 3
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
LIMIT_TREE_INDEX = 20
LIMIT_WATER_INDEX = 30
LIMIT_ROCK_INDEX = 40
LIMIT_LADDER_INDEX = 50
# Secret passages sprite frame id
SECRET_CAVE_FRAME_ID = 0
SECRET_STAIRS_FRAME_ID = 2
SECRET_HORIZONTAL_WALL_FRAME_ID = 4
SECRET_VERTICAL_WALL_FRAME_ID = 6
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
SHOPS = {
    'sword_cave0': {ITEMS_LABEL: {WOOD_SWORD_LABEL: 0},
                    NPC_ID_LABEL: OLD_MAN_ID,
                    TEXT_LABEL: 'it\'s dangerous to go alone, take this !'},
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
                          TEXT_LABEL: 'hey mister hero. you\'ll need this.'}
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

# GAME STARTING COORDINATES
#
PLAYER_START_X = SCREEN_WIDTH // 2 - TILE_SIZE
PLAYER_START_Y = (SCREEN_HEIGHT + HUD_OFFSET) // 2 - TILE_SIZE
STARTING_MAP = LEVEL_PREFIX_LABEL
STARTING_SCREEN = '10'
