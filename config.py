# CONFIGURATION PYTHON FILE

# GENERAL SETTINGS
SCREENSIZE_X = 1366
SCREENSIZE_Y = 768
HALF_SCREENSIZE_X = int(SCREENSIZE_X/2) #(do not touch)
HALF_SCREENSIZE_Y = int(SCREENSIZE_Y/2) #(do not touch)

FPS = 30

CAMERASLACK = 90

# GAME SETTINGS
NAME = 'Player' #Player name
MOVERATE = 13 #Player initial speed

    # Set player speed and player speed decrease rate

    # 0.08 settings: Starting speed: 9, Starting size: 25, Rate: -1 SPEED / 50 SIZE
    #       SIZE    25  -  75  -  125  -  175  -  225  -  275
    #       SPEED    9  -   8  -   7   -   6   -   5   -   4

    # 0.08D settings: Starting speed: 13, Starting Size: 25, Rate: -1 SPEED / 25 SIZE
    #       SIZE    25  -  50  -  75  -  100  -  125  -  150  -  175  -  200  -  225  -  250
    #       SPEED   13  -  12  -  11  -   10  -   9   -   8   -   7   -   6   -   5   -   4

    # 0.08E settings: Starting speed: 11, Starting Size: 33, Rate: -1 SPEED / 33 SIZE
    #       SIZE    33  -  66  -  99  -  132  -  156  -  198  -  231  -  264
    #       SPEED   11  -  10  -   9  -   8   -   7   -   6   -   5   -   4
    # Current settings: 0.08E
STARTSIZE = 33
STAGESIZE = 33
EATSIZE = STARTSIZE - 15 # not implemented
WINSIZE = 200 # not implemented

GAMEOVERTIME = 4

NUMENEMIES = 30
ENEMYMINSIZE = 10
MINSPEED = 1
MAXSPEED = 4
DIRCHANGEFREQ = 3 # % chance of direction change per frame

# Not implemented
ENGULF_THRESHOLD_MULTIPLIER = 1.3 #You have to be this much times the size to engulf
ENGULF_THRESHOLD_CONSTANT = 20 #You have to be this many sizes bigger to engulf

ENGULF_EFFICIENCY = 0.5 #How much size you gain from engulfing the other object

#BOSS SETTINGS
BOSS_SIZE = 215
BOSS_SPEED = 4

BOSS_START_X = SCREENSIZE_X
BOSS_START_Y = SCREENSIZE_Y

#CUSTOMIZED BOSS (Do not touch)
BOSS_DIR = "data/active/img.png"
EAT_DIR = "data/active/eat.ogg"
EATEN_DIR = "data/active/eaten.ogg"
OHNO_DIR = "data/active/ohno.ogg"
VIEW_DIR = "data/active/view.ogg"
TOUCH_DIR = "data/active/touch.ogg"

#RED ARROW INDICATOR (Do not touch)
ARROW_PAD = 50
ARROW_SIZE = 40
REDUP_DIR = 'redUp.png'
REDUPLEFT_DIR = 'redUpRight.png'


# CONSTANTS (do not touch)
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
TURQ   = ( 50, 198, 166) #TURQOISE :D

BALLCOLOUR = [RED, GREEN, BLUE, YELLOW, PURPLE, TURQ]
