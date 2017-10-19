# CONFIGURATION PYTHON FILE

# GENERAL SETTINGS
#MAPSIZE_X = 1600
#MAPSIZE_Y = 1200

SCREENSIZE_X = 1366
SCREENSIZE_Y = 768
HALF_SCREENSIZE_X = int(SCREENSIZE_X/2)
HALF_SCREENSIZE_Y = int(SCREENSIZE_Y/2)

FPS = 30

CAMERASLACK = 90 

# GAME SETTINGS
NAME = 'Player'
MOVERATE = 8

STARTSIZE = 25
EATSIZE = STARTSIZE - 15
WINSIZE = 200

GAMEOVERTIME = 4

NUMENEMIES = 30
ENEMYMINSIZE = 8
MINSPEED = 1
MAXSPEED = 4
DIRCHANGEFREQ = 3 # % chance of direction change per frame

ENGULF_THRESHOLD_MULTIPLIER = 1.3 #You have to be this much times the size to engulf
ENGULF_THRESHOLD_CONSTANT = 20 #You have to be this many sizes bigger to engulf

ENGULF_EFFICIENCY = 0.6 #How much size you gain from engulfing the other object

#BOSS SETTINGS
BOSS_SIZE = 190
BOSS_SPEED = 5

BOSS_START_X = SCREENSIZE_X
BOSS_START_Y = SCREENSIZE_Y

#CUSTOMIZED BOSS
BOSS_DIR = "data/active/img.png"
EAT_DIR = "data/active/eat.ogg"
EATEN_DIR = "data/active/eaten.ogg"
OHNO_DIR = "data/active/ohno.ogg"
VIEW_DIR = "data/active/view.ogg"
TOUCH_DIR = "data/active/touch.ogg"


# CONSTANTS
LEFT = 'left'
RIGHT = 'right'

# COLOUR CONSTANTS
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GRAY   = ( 64,  64,  64)

RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
PURPLE = (128,   0, 128)

BALLCOLOUR = [RED, GREEN, BLUE, YELLOW, PURPLE]




