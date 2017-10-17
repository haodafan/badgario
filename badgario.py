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

    gameWonSurf2 = BASICFONT.render('(press "r" to restart)')
    gameWonRect2 = gameWonSurf2.get_rect()
    gameWonRect2.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    #Camera
    cameraX = 0
    cameraY = 0

    objOtherBalls = []
    objBossBall = [] #Potentially used later

    objPlayer = {'name': NAME
                 'size': STARTSIZE
                 'x' : HALF_SCREENSIZE_X
                 'y' : HALF_SCREENSIZE_Y}
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    
    #################
    ### GAME LOOP ###
    #################

    while True:
        ## Draw background ##
        SURF.fill(WHITE)
        
        ## Move enemy balls ##
        for objBall in objOtherBalls:
            objBall['x'] += objBall['movex']
            objBall['y'] += objBall['movey']

            #random chance they change direction
            if random.randint(0, 99) < DIRCHANGEFREQ:
                objBall['movex'] = getRandomVelocity()
                objBall['movey'] = getRandomVelocity()
                
        ## Removing out-of-screen balls ##
        for i in range(len(objOtherBalls) -1, -1, -1):
            if isOutsideActiveArea(cameraX, cameraY, objOtherBalls[i]):
                del objOtherBalls[i]

        ## Adding more balls ##
        while len(objOtherBalls) < NUMENEMIES:
            objOtherBalls.append(makeNewBall(cameraX, cameraY))
            
        ## Moving the camera ##
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

        ## Draw Enemy Balls ##
        for objBall in objOtherBalls:

            """
            # BALL CREATION
            #Random color
            chooser = random.randint(0, len(BALLCOLOUR) - 1)
            #Random Size
            MaxSize = STARTSIZE + 25
            if MaxSize > WINSIZE - 50:
                MaxSize = WINSIZE - 50
            size = random.randint(ENEMYMINSIZE, MaxSize)

            ## UNFINISHED!!!!! ##
            objBall['circle'] = pygame.circle(SURF, BALLCOLOUR[chooser], size, 0)
            """

            objBall['circle'] = pygame.circle((objBall['x'] - cameraX,
                                               objBall['y'] - cameraY),
                                              obJBall['size'])
            pygame.draw.objBall['circle']

        ## Draw Player Ball ##
        if not gameOverMode:
            objPlayer['circle'] = pygame.circle((objPlayer['x'] - cameraX,
                                                 objPlayer['y'] - cameraY),
                                                objPlayer['size'], 0)
            pygame.draw.objBall['circle']
                                                
        ## EVENT HANDLING LOOP ##
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                elif gameWon and event.key == K_r:
                    return

            elif event.type == KEYUP:
                #stop moving
                if event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False
                elif event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
            elif event.key == K_ESCAPE:
                terminate()

            # Moving the Player
            if not gameOverMode:
                #actually move the player
                if moveLeft:
                    objPlayer['x'] -= MOVERATE
                if moveRight:
                    objPlayer['x'] += MOVERATE
                if moveUp:
                    objPlayer['y'] -= MOVERATE
                if moveDown:
                    objPlayer['y'] += MOVERATE

                #Collision Detection

                ### FUCKIT IL DO THAT LATER

            else:
                #Game is over. Show "gameover" text
                SURF.blit(gameOverSurf, gameOverRect)
                #displays it for GAMEOVERTIME seconds...
                if time.time() - gameOverStartTime > GAMEOVERTIME:
                    return #End the current game

            if winMode:
                SURF.blit(winSurf, winRect)
                SURF.blit(winSurf2, winRect2)

            pygame.display.update()
            FPSCLOCK.tick()
        
# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

#Terminate function
def terminate():
    pygame.quit()
    sys.exit()



# GET RANDOM VELOCITY
# This function returns a value between MINSPEED and MAXSPEED (from the config file)
def getRandomVelocity():
    if random.randint(0,1) == 0:
        return random.randint(MINSPEED, MAXSPEED)
    else:
        return - random.randint(MINSPEED, MAXSPEED)

def getRandomOffCameraPos(cameraX, camerY, objRadius):
    #create a rect view of the camera view
    cameraRect = pygame.Rect(cameraX, cameraY, SCREENSIZE_X, SCREENSIZE_Y)
    while True:
        x = random.randint(cameraX - SCREENSIZE_X, cameraX + (2 * SCREENSIZE_X))
        y = random.randint(cameraX - SCREENSIZE_Y, cameraY + (2 * SCREENSIZE_Y))

        #create a rect object with the random coordinates and use collidirect()???

        # to make sure the right edge isn't in the camera view...
        objRect = pygame.colliderect(cameraRect):
            return x, y
        

#MAKE NEW BALLS
def makeNewBall(cameraX, cameraY):
    #Your code here
