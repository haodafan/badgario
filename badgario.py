#@Author: Haoda Fan
#Development start: October 16th 2017
#Current Build: October 16th 2017

# ---------------------------------------------------
# LIBRARIES
# ---------------------------------------------------
import pygame, sys, random, time, math
from pygame.locals import *

#Local modular libraries
from config import *

# ---------------------------------------------------
# MAIN FUNCTION / INITIALIZATION
# ---------------------------------------------------

def main():
    global FPSCLOCK, SURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock() #Sets game clock
    pygame.display.set_caption('Shitty Agario')
    SURF = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y))

    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    #

    while True:
        runGame()

# ---------------------------------------------------
# RUN FUNCTION / GAME LOOP
# ---------------------------------------------------
def runGame():
    #Set Variables for a new game
    gameOver = False      # If the player has lost
    gameOverStartTime = 0 # Time the player lost
    gameWon = False       # If the player has won

    #Game text
    gameOverSurf = BASICFONT.render('YOU LOSE, WHOSE SHITTY NOW?', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    gameWonSurf = BASICFONT.render('YOUR BALLS ARE SO BIG, YOU ARE UNSTOPPABLE!', True, WHITE)
    gameWonRect = gameWonSurf.get_rect()
    gameWonRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    #Camera
    cameraX = 0
    cameraY = 0

    objOtherBalls = []
    objBossBall = [] #Potentially used later

    ###############
    ## GAME LOOP ##
    ###############

    while True:
        #Move enemy balls
        for objBall in objOtherBalls:
            objBall['x'] += objBall['movex']
            objBall['y'] += objBall['movey']

        #random chance they change direction
        if random.randint(0, 99) < DIRCHANGEFREQ:
            objBall['movex'] = getRandomVelocity()
            objBall['movey'] = getRandomVelocity()

        
        #Removing out-of-screen balls
        for i in range(len(objOtherBalls) -1, -1, -1):
            if isOutsideActiveArea(cameraX, cameraY, objOtherBalls[i]):
                del objOtherBalls[i]

        #Adding more balls
        while len(objOtherBalls) < NUMENEMIES:
            objOtherBalls.append(makeNewBall(cameraX, cameraY))

        #Moving the camera
        playerCenterX = objPlayer['x'] #Note this is different from tutorial, since we're using balls
        playerCenterY = objPlayer['y']
        # Right-Left
        if (cameraX + HALF_SCREENSIZE_X) - playerCenterX > CAMERASLACK):
            cameraX = playerCenterX + CAMERASLACK - HALF_SCREENSIZE_X
        elif playerCenterX - (cameraX + HALF_SCREENSIZE_X) > CAMERASLACK):
            cameraX = playerCenterX - CAMERASLACK - HALF_SCREENSIZE_X
        # Down-Up
        if (cameraY + HALF_SCREENSIZE_Y) - playerCenterY > CAMERASLACK):
            cameraY = playerCenterY + CAMERASLACK - HALF_SCREENSIZE_Y
        elif playerCenterX - (cameraY + HALF_SCREENSIZE_Y) > CAMERASLACK):
            cameraY = playerCenterY - CAMERASLACK - HALF_SCREENSIZE_Y

        #Draw background
        SURF.fill(WHITE)

        #Draw Enemy Balls
        for objBall in objOtherBalls:

            #Random color
            chooser = random.randint(0, len(BALLCOLOUR) - 1)
            #Random Size
            MaxSize = STARTSIZE + 25
            if MaxSize > WINSIZE - 50:
                MaxSize = WINSIZE - 50
            size = random.randint(ENEMYMINSIZE, MaxSize)

            ## UNFINISHED!!!!! ##
            objBall['circle'] = pygame.circle(SURF, BALLCOLOUR[chooser], (???), size, 0)
            
# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

# GET RANDOM VELOCITY
# This function returns a value between MINSPEED and MAXSPEED (from the config file)
def getRandomVelocity():
    return random.randint(MINSPEED, MAXSPEED)


