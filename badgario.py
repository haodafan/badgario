#@Author: Haoda Fan
#Development start: October 16th 2017
#Current Build: November 14th 2017

#Version: 0.0.8C

# ---------------------------------------------------
# LIBRARIES
# ---------------------------------------------------
import pygame, sys, random, time, math
from pygame.locals import *

#Local modular libraries
from config import *
from play_badgario import *

# ---------------------------------------------------
# MAIN FUNCTION / INITIALIZATION
# ---------------------------------------------------

def main():
    global FPSCLOCK, SURF, BASICFONT

    #Initialize sound
    pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

    #Initialize pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock() #Sets game clock
    pygame.display.set_caption('Shitty Agario')
    SURF = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y))

    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Image loading
    # (for some reason, it only works if it is a GLOBAL variable
    # So unfortunately I guess I'll just have to use globals. Whamp whamp
    global BOSS_IMG
    BOSS_IMG = pygame.image.load(BOSS_DIR)

    global REDUP_IMG
    REDUP_IMG = pygame.image.load(REDUP_DIR)
    global REDUPLEFT_IMG
    REDUPLEFT_IMG = pygame.image.load(REDUPLEFT_DIR)

    goBackToMenu = False
    while not goBackToMenu:
        goBackToMenu = runGame()
    if goBackToMenu:
        return #Go back

# ---------------------------------------------------
# RUN FUNCTION / GAME LOOP
# ---------------------------------------------------
def runGame():
    #Set Variables for a new game
    gameOver = False      # If the player has lost
    gameOverStartTime = 0 # Time the player lost
    gameWon = False       # If the player has won
    gameUnresolved = False# If the player is too fat to win or lose

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

    #       BOSS_SIZE: 215
    currentSpeed = MOVERATE # 11
    currentStage = STARTSIZE # 33
    nextStage = STARTSIZE + STAGESIZE # 33

    # Game text
    gameOverSurf = BASICFONT.render('OM NOM NOM, WHOSE SHITTY NOW?', True, GRAY)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    gameWonSurf = BASICFONT.render('YOUR BALLS ARE SO BIG, YOU ARE UNSTOPPABLE!', True, GRAY)
    gameWonRect = gameWonSurf.get_rect()
    gameWonRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    gameWonSurf2 = BASICFONT.render('(press "r" to restart, esc to return to menu)', True, GRAY)
    gameWonRect2 = gameWonSurf2.get_rect()
    gameWonRect2.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y + 45)

    NAMEFONT = pygame.font.Font('freesansbold.ttf', 8)
    playerNameSurf = NAMEFONT.render(NAME, True, WHITE)
    playerNameRect = playerNameSurf.get_rect()
    playerNameRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    gameUnresolvedSurf = BASICFONT.render("YOU'VE BECOME TOO FAT! NOW YOU CAN'T CHASE! GG EZ MID", True, GRAY)
    gameUnresolvedRect = gameUnresolvedSurf.get_rect()
    gameUnresolvedRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y)

    # Camera
    cameraX = 0
    cameraY = 0

    # Sound objects
    viewSound = pygame.mixer.Sound(VIEW_DIR)
    eatSound = pygame.mixer.Sound(EAT_DIR)
    eatenSound = pygame.mixer.Sound(EATEN_DIR)
    ohnoSound = pygame.mixer.Sound(OHNO_DIR)
    touchSound = pygame.mixer.Sound(TOUCH_DIR)

    #Ball objects
    objOtherBalls = [] #Stores all balls used in game

    #Boss ball object
    objBoss = {'surface' : pygame.transform.scale(BOSS_IMG, (BOSS_SIZE * 2, BOSS_SIZE * 2)),
               'size' : BOSS_SIZE,
               'speed' : BOSS_SPEED,
               'x' : BOSS_START_X,
               'y' : BOSS_START_Y,
               'canEaten' : False,
               'isEaten' : False}


    #Player ball object
    objPlayer = {'name': NAME,
                 'size': STARTSIZE,
                 'color' : BLACK,
                 'x' : HALF_SCREENSIZE_X,
                 'y' : HALF_SCREENSIZE_Y
                }
    #Indicator arrows
    arrowUp = pygame.transform.rotate(REDUP_IMG, 0)
    arrowLeft = pygame.transform.rotate(REDUP_IMG, 90)
    arrowDown = pygame.transform.rotate(REDUP_IMG, 180)
    arrowRight = pygame.transform.rotate(REDUP_IMG, 270)

    arrowUpLeft = pygame.transform.rotate(REDUPLEFT_IMG, 0)
    arrowDownLeft = pygame.transform.rotate(REDUPLEFT_IMG, 90)
    arrowDownRight = pygame.transform.rotate(REDUPLEFT_IMG, 180)
    arrowUpRight = pygame.transform.rotate(REDUPLEFT_IMG, 270)

    #Player movement booleans
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    #Gamestate booleans
    turnAround = False
    bossInScreen = True
    bossInTouch = False
    paused = False
    cheats = False

    #################
    ### GAME LOOP ###
    #################

    while True:

        #### THE ACTIVE GAME ####

        if not paused:

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
                objOtherBalls.append(makeNewBall(cameraX, cameraY, objPlayer))

            ## Moving the camera ##
            # Right-Left
            if (cameraX + HALF_SCREENSIZE_X) - objPlayer['x'] > CAMERASLACK:
                cameraX = objPlayer['x'] + CAMERASLACK - HALF_SCREENSIZE_X
            elif objPlayer['x'] - (cameraX + HALF_SCREENSIZE_X) > CAMERASLACK:
                cameraX = objPlayer['x'] - CAMERASLACK - HALF_SCREENSIZE_X
            # Down-Up
            if (cameraY + HALF_SCREENSIZE_Y) - objPlayer['y'] > CAMERASLACK:
                cameraY = objPlayer['y'] + CAMERASLACK - HALF_SCREENSIZE_Y
            elif objPlayer['y'] - (cameraY + HALF_SCREENSIZE_Y) > CAMERASLACK:
                cameraY = objPlayer['y'] - CAMERASLACK - HALF_SCREENSIZE_Y
            #DEBUGGING
            #print("CAMERA POSITION: " + str(cameraX) + ", " + str(cameraY))

            ## Moving the Boss ##
            boss_move_X = 0
            boss_move_Y = 0
            if isOutsideActiveArea(cameraX, cameraY, objBoss) and not turnAround:

                #The boss needs to catch up
                boss_move_X, boss_move_Y = bossCatchup(objBoss, objPlayer)
            elif turnAround:
                #Now the boss runs away from you!
                boss_move_X, boss_move_Y = bossAI(objBoss, objPlayer)
                boss_move_X = - boss_move_X
                boss_move_Y = - boss_move_Y
                #Debugging
                #print("Boss Reverses!!!")

            else:
                #Boss moves at normal speed
                boss_move_X, boss_move_Y = bossAI(objBoss, objPlayer)
                #Debugging
                #print("Boss Normal move")

            #Moving it
            if not gameWon:
                objBoss['x'] += boss_move_X
                objBoss['y'] += boss_move_Y


        elif paused:
            ## Draw background ##
            SURF.fill(GRAY)


        #### THE STATIC GAME ####

        ## Draw Enemy Balls ##
        for objBall in objOtherBalls:

            pygame.draw.circle(SURF, objBall['color'],
                               (objBall['x'] - cameraX, objBall['y'] - cameraY),
                               objBall['size'], 0)

        ## DRAW PLAYER/BOSS BALLS ##

        # OLD #
        """
        ## Draw Player Ball ##
        #Note: drawing the player after the enemies will ensure that im always on top if you know what I mean :^)
        if not gameOver:
            pygame.draw.circle(SURF, objPlayer['color'],
                               (objPlayer['x'] - cameraX, objPlayer['y'] - cameraY),
                               objPlayer['size'], 0)
            #Floating text name
            fontSize = int(objPlayer['size'] / 3)
            NAMEFONT = pygame.font.Font('freesansbold.ttf', fontSize)

            playerNameSurf = NAMEFONT.render(NAME, True, WHITE)
            playerNameRect = playerNameSurf.get_rect()
            playerNameRect.center = (objPlayer['x'] - cameraX, objPlayer['y'] - cameraY)
            SURF.blit(playerNameSurf, playerNameRect)

        ## Draw Boss Ball ##
        if not objBoss['isEaten']:
            objBoss['rect'] = pygame.Rect( (objBoss['x'] - cameraX, objBoss['y'] - cameraY,
                                           objBoss['size'] * 2, objBoss['size'] * 2))
            SURF.blit(objBoss['surface'], objBoss['rect'])
        """

        # NEW #
        # This new if statement allows the Player to be drawn in front of the boss when it's bigger
        if not turnAround:
            if not gameOver:
                drawPlayer(objPlayer, cameraX, cameraY) #Only draws the player ball if he isn't eaten
            drawBoss(objBoss, cameraX, cameraY)
        else:
            if not objBoss['isEaten']:
                drawBoss(objBoss, cameraX, cameraY) #Only draws the boss ball if he isn't eaten
            drawPlayer(objPlayer, cameraX, cameraY)


        ## If it's paused, then we draw some words
        if paused:
            gamePauseSurf = BASICFONT.render('GAME PAUSED.', True, WHITE)
            gamePauseRect = gamePauseSurf.get_rect()
            gamePauseRect.center = (HALF_SCREENSIZE_X, CAMERASLACK)
            SURF.blit(gamePauseSurf, gamePauseRect)


        #### GAME TRIGGERS ####

        ### EVENT HANDLING LOOP ###
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            ## Active events ##
            elif event.type == KEYDOWN and not paused:
                if event.key in (K_UP, K_w):
                    #moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    #moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    #moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    #moveLeft = False
                    moveRight = True

                elif event.key == K_p:
                    #Pause key
                    paused = True

                # CHEATS #
                elif event.key in (K_RCTRL, K_LCTRL):
                    cheats = True

                elif cheats and event.key == K_EQUALS:
                    #Add-size cheat
                    objPlayer['size'] += 10
                elif cheats and event.key == K_MINUS:
                    #Subtract-size cheat
                    objPlayer['size'] -= 10

                elif (gameWon or gameOver or gameUnresolved) and event.key == K_r:
                    return False #Game starts over if returns false

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

                elif event.key in (K_RCTRL, K_LCTRL):
                    cheats = False #Stops the cheats

                elif event.key == K_ESCAPE or event.key == K_m:
                    goBackToMenu = True
                    return True #Game goes back to menu if returns true

            ## Paused Events ##
            elif event.type == KEYDOWN and paused:
                if event.key == K_p:
                    #Pause key
                    paused = False

            ## This just fixes the bug where the player continues moving after paused ##
            if paused:
                moveUp = False
                moveDown = False
                moveRight = False
                moveLeft = False

        ### More Ingame Triggers ###
        if not gameOver:

            ## Moving the player ##
            if moveLeft:
                objPlayer['x'] -= currentSpeed
            if moveRight:
                objPlayer['x'] += currentSpeed
            if moveUp:
                objPlayer['y'] -= currentSpeed
            if moveDown:
                objPlayer['y'] += currentSpeed

            ## Collision Detection ##
            for i in range(len(objOtherBalls) - 1, -1, -1):
                # My collision detection will work a bit differently from the one in the Squirrel game Tutorial.
                # The squirrel game tutorial, you eat a squirrel when you touch the edge of its rectangle.
                # In shitty agario, you have at least partially engulf the other ball.

                # I will accomplish this by creating a separate rectangles for my ball, much smaller than my ball's actual drawn circle.
                # If the center point of the enemy ball is inside my rectangle, then I will consider myself eaten.
                objBall = objOtherBalls[i]
                if (canEngulf(objPlayer, objBall)):
                    objPlayer['size'] = doEngulf(objPlayer, objBall)
                    del objOtherBalls[i] # The other ball was eaten
                    print("OM NOM NOM")

                elif (canEngulf(objBall, objPlayer)):
                    #You have been engulfed by another ball! YOU LOSE!
                    #del objPlayer
                    gameOver = True
                    gameOverStartTime = time.time()
                    print("OH NOOOO")

                """
                #Old victory condition
                if (objPlayer['size'] > WINSIZE):
                    #You are over the victory threshold. For now, this will mean victory.
                    gameWon = True
                """

            ## Separate mechanic for collision with Boss ##
            if (bossEngulf(objBoss, objPlayer)) and not gameWon:
                pygame.mixer.Sound.play(eatSound)
                gameOverStartTime = time.time()
                gameOver = True
                print("AAAAAAAAAA")

            elif (bossEngulfInverted(objPlayer, objBoss)) and not gameWon:
                pygame.mixer.Sound.play(eatenSound)
                objBoss['isEaten'] = True
                gameWon = True


            ## Boss proximity detection and sound triggers ##
            #  We have the constants: bossInScreen and bossInTouch to keep track of its current state
                # Note that I have to subtract the boss's size from the camera to compensate for the boss's 'corner' coordinates.
                # I probably could have coded that better :P
            if not bossInScreen and not isOutsideCamera(cameraX - objBoss['size'], cameraY - objBoss['size'], objBoss):
                #print("THE BOSS HAS ENTERED YOUR CAMERA")
                bossInScreen = True
                if not turnAround:
                    pygame.mixer.Sound.play(viewSound)

            elif bossInScreen and isOutsideCamera(cameraX - objBoss['size'], cameraY - objBoss['size'], objBoss):
                #print("THE BOSS HAS LEFT YOUR CAMERA")
                bossInScreen = False

            if not bossInTouch and bossTouch(objBoss, objPlayer):
                #print("OH NO THE BOSS HAS TOUCHED YOU!!!!!!!!!!!")
                bossInTouch = True
                if not turnAround:
                    pygame.mixer.Sound.play(touchSound)
            elif bossInTouch and not bossTouch(objBoss, objPlayer):
                #print("Phew, he stopped touching you in that weird way. Ew gross")
                bossInTouch = False

            # Boss vs Player size detection and Turnaround trigger #
            #Turnaround point, where you can now eat the boss
            if not turnAround and objPlayer['size'] > objBoss['size']:
                turnAround = True
                print("!!TURNAROUND!!")
                pygame.mixer.Sound.play(ohnoSound)

            ## Red Indicator arrows ##
            #if isOutsideCamera(cameraX - objBoss['size'], cameraY - objBoss['size'], objBoss):
            if not bossInScreen:
                #First we use BossAI to figure out where the Boss is in relation to the player
                x, y = bossAI(objBoss, objPlayer)

                #DEBUGGING
                #print("x,y = " + str(x) + "," + str(y))

                # Reference:
                # +x = down, +y = right

                #objBoss['rect'] = pygame.Rect( (objBoss['x'] - cameraX, objBoss['y'] - cameraY,
                #                          objBoss['size'] * 2, objBoss['size'] * 2))
                #SURF.blit(objBoss['surface'], objBoss['rect'])
                if (y > 0 and x > 0):
                    #boss moves down-right
                    #Arrow points up-left
                    objArrow = pygame.Rect(ARROW_PAD, ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowUpLeft, objArrow)
                elif (y > 0 and x < 0):
                    #boss moves down-left
                    #Arrow points up-right
                    objArrow = pygame.Rect(SCREENSIZE_X - ARROW_PAD, ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowUpRight, objArrow)
                elif (y > 0 and x == 0):
                    #boss moves down
                    #Arrow points up
                    objArrow = pygame.Rect(HALF_SCREENSIZE_X, ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowUp, objArrow)
                elif (y < 0 and x > 0):
                    #boss moves up-right
                    #Arrow points down-left
                    objArrow = pygame.Rect(ARROW_PAD, SCREENSIZE_Y - ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowDownLeft, objArrow)
                elif (y < 0 and x < 0):
                    #boss moves up-left
                    #Arrow points down-right
                    objArrow = pygame.Rect(SCREENSIZE_X - ARROW_PAD, SCREENSIZE_Y - ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowDownRight, objArrow)
                elif (y < 0 and x == 0):
                    #boss moves up
                    #Arrow points down
                    objArrow = pygame.Rect(HALF_SCREENSIZE_X, SCREENSIZE_Y - ARROW_PAD, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowDown, objArrow)
                elif (y == 0 and x > 0):
                    #Boss moves right
                    #Arrow points left
                    objArrow = pygame.Rect(ARROW_PAD, HALF_SCREENSIZE_Y, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowLeft, objArrow)
                elif (y == 0 and x < 0):
                    #Boss moves left
                    #Arrow points right
                    objArrow = pygame.Rect(SCREENSIZE_X - ARROW_PAD, HALF_SCREENSIZE_Y, ARROW_SIZE, ARROW_SIZE)
                    SURF.blit(arrowRight, objArrow)
                else:
                    print("whoa he far! :O ")

                #DEBUGGING
                #Let's draw a big red circle for where the camera is
                #pygame.draw.circle(SURF, RED, (cameraX, cameraY), 10, 0)

            ## PLAYER DYNAMIC SPEED ##
            if objPlayer['size'] > nextStage:
                #If the player size is at the next stage...
                currentSpeed -= 1
                currentStage = nextStage #Currently not used but eh whatever
                nextStage += STAGESIZE

            # ANOTHER GAME OVER CONDITION!!! #
            if currentSpeed <= BOSS_SPEED:
                #You've become too fat!
                #Shows the 'you've become too fat' text
                SURF.blit(gameUnresolvedSurf, gameUnresolvedRect)
                SURF.blit(gameWonSurf2, gameWonRect2) #Displays some restarting info
                gameUnresolved = True
                gameOverStartTime = time.time()
                #displays it for GAMEOVERTIME seconds... (note: does not work lol)
                if time.time() - gameOverStartTime > GAMEOVERTIME:
                    return False #End the current game (restarts)


        else:
            #Game is over. Show "gameover" text
            SURF.blit(gameOverSurf, gameOverRect)
            SURF.blit(gameWonSurf2, gameWonRect2) #Displays some restarting info

            #displays it for GAMEOVERTIME seconds... (note: does not work lol)
            if time.time() - gameOverStartTime > GAMEOVERTIME:
                return False #End the current game (restarts)

        if gameWon:
            SURF.blit(gameWonSurf, gameWonRect)
            SURF.blit(gameWonSurf2, gameWonRect2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

#Terminate function
def terminate():
    pygame.quit()
    sys.exit()

#New menu function returns to the main menu
#def backToMenu():
#    goBackToMenu = False # This should stop the main loops

# GET RANDOM VELOCITY
# This function returns a value between MINSPEED and MAXSPEED (from the config file)
def getRandomVelocity():
    if random.randint(0,1) == 0:
        return random.randint(MINSPEED, MAXSPEED)
    else:
        return - random.randint(MINSPEED, MAXSPEED)

#Finding an off-camera spawn location
def getRandomOffCameraPos(cameraX, cameraY, objRadius):
    #create a rect view of the camera view
    cameraRect = pygame.Rect(cameraX, cameraY, SCREENSIZE_X, SCREENSIZE_Y)
    while True:
        #DEBUGGING
        #print("Calculation: ")
        #print("random.randint(" + str(cameraX) + "-" + str(SCREENSIZE_X) + ", " + str(cameraX) + " + (2 * " + str(SCREENSIZE_X) + ")")
        #print("random.randint(" + str(cameraY) + "-" + str(SCREENSIZE_Y) + ", " + str(cameraY) + " + (2 * " + str(SCREENSIZE_Y) + ")")
        x = random.randint(cameraX - SCREENSIZE_X, cameraX + (2 * SCREENSIZE_X))
        y = random.randint(cameraY - SCREENSIZE_Y, cameraY + (2 * SCREENSIZE_Y))

        #create a rect object with the random coordinates and use collidirect()???

        # to make sure the right edge isn't in the camera view...
        objRect = pygame.Rect(x, y, objRadius * 2, objRadius * 2)
        if not objRect.colliderect(cameraRect):
            return x, y


#MAKE NEW BALLS
def makeNewBall(cameraX, cameraY, objPlayer):
    #Your code here
    ball = {}

    # BALL CREATION
    #Random color
    chooser = random.randint(0, len(BALLCOLOUR) - 1)
    colour = BALLCOLOUR[chooser]

    #Random Size
    MaxSize = objPlayer['size'] + 35
    if MaxSize > WINSIZE - 50:
        MaxSize = WINSIZE - 50
    size = random.randint(ENEMYMINSIZE, MaxSize)

    ball['size'] = size
    ball['color'] = colour
    ball['x'], ball['y'] = getRandomOffCameraPos(cameraX, cameraY, size)
    ball['movex'] = getRandomVelocity()
    ball['movey'] = getRandomVelocity()

    #Debugging
    print("Ball created! Size:" + str(ball['size']) + " Colour: " + str(ball['color']))

    return ball

#Checking if outside the Active Map
def isOutsideActiveArea(cameraX, cameraY, obj):
    #Returns False if cameraX and cameraY are more than a half-window length beyond the edge of the window
    boundsLeftEdge = cameraX - SCREENSIZE_X
    boundsTopEdge = cameraY - SCREENSIZE_Y
    boundsRect = pygame.Rect(boundsLeftEdge, boundsTopEdge, SCREENSIZE_X * 3, SCREENSIZE_Y * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['size'] * 2, obj['size'] * 2)
    return not boundsRect.colliderect(objRect)

#Check if outside cameraview
def isOutsideCamera(cameraX, cameraY, obj):
    #Returns false if cameraX and cameraY are beyond the edge of the window
    boundsRect = pygame.Rect(cameraX, cameraY, SCREENSIZE_X, SCREENSIZE_Y)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['size'] * 2, obj['size'] * 2)
    return not boundsRect.colliderect(objRect)

#Check if touched
def bossTouch(objBoss, objA):
    boundsRectA = pygame.Rect(objA['x'] - objA['size'], objA['y'] - objA['size'], objA['size']*2, objA['size']*2)
    boundsRectBoss = pygame.Rect(objBoss['x'], objBoss['y'], objBoss['size']*2, objBoss['size']*2)
    return boundsRectA.colliderect(boundsRectBoss)

# canEngulf function
# canEngulf(objectA, objectB)
# This function returns False if object A can eat object B, False otherwise
def canEngulf(objA, objB):
    #First, let's create some values for the inner bounds of an abstract rectangle for object A
    halfSize = objA['size'] / 2
    leftEdge = objA['x'] - halfSize
    rightEdge = objA['x'] + halfSize
    topEdge = objA['y'] - halfSize
    bottomEdge = objA['y'] + halfSize

    #Now, let's check if the point of object B is inside object A
    if (objB['x'] > leftEdge and objB['x'] < rightEdge and objB['y'] > topEdge and objB['y'] < bottomEdge):
        print("Possible engulfing detected!")

        # We have two engulf thresholds, a multipler and a constant.
        # For this mechanic, we will use the smaller one.
        threshold = int(min(ENGULF_THRESHOLD_CONSTANT, (objB['size'] * ENGULF_THRESHOLD_MULTIPLIER)))

        if(objA['size'] > objB['size']):
            print("Object A can engulf object B")
            return True
        else:
            print("Object A cannot engulf object B")
            return False

# bossEngulf function...
# The boss works slightly differently in that he is a blitted rectangle
# So his x and y coordinates represent a CORNER instead of a CENTER
# This method calls the canEngulf function, using an object with the boss's CENTER coordinates
def bossEngulf(objBoss, objPlayer):
    objBossCenter = {'x' : objBoss['x'] + objBoss['size'],
                     'y' : objBoss['y'] + objBoss['size'],
                     'size' : objBoss['size']}
    return canEngulf(objBossCenter, objPlayer)

#This works similar to above except with the player engulfing the boss
def bossEngulfInverted(objPlayer, objBoss):
    objBossCenter = {'x' : objBoss['x'] + objBoss['size'],
                     'y' : objBoss['y'] + objBoss['size'],
                     'size' : objBoss['size']}
    return canEngulf(objPlayer, objBossCenter)


# doEngulf function
# This function will return the new size of object A
# This function will NOT remove object B. That must be done manually in the main game loop.
def doEngulf(objA, objB):
    #Size increase algorithm
    #I can't simply increase the 'radius', or else my ball will begin growing EXPONENTIALLY large

    # My algorithm for increasing the size of the ball must have to do with AREA
    # Algorithm: areaA = areaA + (ENGULF_EFFICIENCY * areaB)
    #            sizeA = sqrt(areaA)/pi
    areaA = 3.1415926 * objA['size'] * objA['size']
    areaB = 3.1415926 * objB['size'] * objB['size']

    newArea = areaA + (ENGULF_EFFICIENCY * areaB)

    #Your area will either increase by + 1 or by the New Area Algorithm, whichever one gives you more
    newSize = max(objA['size'] + 1, int( math.sqrt(newArea / 3.1415926) ) )

    #DEBUGGING
    print("ALGORITHM NEW SIZE: " + str(int( math.sqrt(newArea / 3.1415926) )))

    #OLD ALGORITHM
    #newSize = round( objA['size'] + ENGULF_EFFICIENCY * objB['size'] )

    #DEBUGGING
    print("NEW SIZE: " + str(newSize))
    return newSize

# Boss_AI determines the direction that the boss will go
# It returns two integers, x, y
def bossAI(objBoss, objPlayer):
    bossCenterX = objBoss['x'] + objBoss['size']
    bossCenterY = objBoss['y'] + objBoss['size']

    # The Difference represents how far the Boss needs to go in order to reach the player
    diff_X = bossCenterX - objPlayer['x']
    diff_Y = bossCenterY - objPlayer['y']

    #First let's handle the 0 cases
    if (diff_X == 0 or diff_Y == 0):
        proportion = 0
    else:
        proportion = diff_X / diff_Y

    # Case 1: Diagonal down-right
    # The Boss only goes down-right if the proportion of the differences X/Y are between 1/2 and 2/1, X negative
    if (proportion > 0.5 and proportion < 2 and diff_X < 0):
        return BOSS_SPEED, BOSS_SPEED
    # Case 2: Diagonal up-left
    # The Boss only goes up-left if the proportion of the differences X/Y are between 1/2 and 2/1, X positive
    elif (proportion > 0.5 and proportion < 2 and diff_X > 0):
        return - BOSS_SPEED, - BOSS_SPEED

    # Case 3: Diagonal up-right
    # The boss only goes up-right if proportion of the differences X/Y are between -1/2 and -2/1, X negative
    elif (proportion < -0.5 and proportion > -2 and diff_X < 0):
        return BOSS_SPEED, - BOSS_SPEED
    # Case 4: Diagonal down-left
    # The boss only goes down-left if proportion of the differences X/Y are between -1/2 and -2/1, X positive
    elif (proportion < -0.5 and proportion > -2 and diff_X > 0):
        return - BOSS_SPEED, BOSS_SPEED

    # Cases 5-8: straight directions
    elif (diff_X > 0 and math.fabs(diff_X) > math.fabs(diff_Y)):
        return - BOSS_SPEED, 0
    elif (diff_X < 0 and math.fabs(diff_X) > math.fabs(diff_Y)):
        return BOSS_SPEED, 0
    elif (diff_Y > 0 and math.fabs(diff_Y) > math.fabs(diff_X)):
        return 0, - BOSS_SPEED
    elif (diff_Y < 0 and math.fabs(diff_Y) > math.fabs(diff_X)):
        return 0, BOSS_SPEED
    else:
        return 0,0

#Method used to speed up the boss's movement based on the returned values of bossAI()
def bossCatchup(objBoss, objPlayer):
    print("Boss is tryna catch up!")
    x, y = bossAI(objBoss, objPlayer)
    diff_prop = MOVERATE / BOSS_SPEED
    catchup_multiplier = diff_prop * 2
    new_x = x * catchup_multiplier
    new_y = y * catchup_multiplier
    return new_x, new_y

## DRAWING PLAYER/BOSS FUNCTIONS ##
def drawPlayer(objPlayer, cameraX, cameraY):
    pygame.draw.circle(SURF, objPlayer['color'],
                       (objPlayer['x'] - cameraX, objPlayer['y'] - cameraY),
                       objPlayer['size'], 0)
    #Floating text name
    fontSize = int(objPlayer['size'] / 3)
    NAMEFONT = pygame.font.Font('freesansbold.ttf', fontSize)

    playerNameSurf = NAMEFONT.render(NAME, True, WHITE)
    playerNameRect = playerNameSurf.get_rect()
    playerNameRect.center = (objPlayer['x'] - cameraX, objPlayer['y'] - cameraY)
    SURF.blit(playerNameSurf, playerNameRect)

def drawBoss(objBoss, cameraX, cameraY):
    objBoss['rect'] = pygame.Rect( (objBoss['x'] - cameraX, objBoss['y'] - cameraY,
                                   objBoss['size'] * 2, objBoss['size'] * 2))
    SURF.blit(objBoss['surface'], objBoss['rect'])

#This starts the game if you run this file instead of play_badgario.py
if __name__ == '__main__':
    main()
