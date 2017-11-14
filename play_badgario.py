# This Menu is in Playable condition! PLAYABLE!! 

# ----------------------------------------------------
from badgario import *
from config import *

#import webbrowser #To externally open files
import os
# ----------------------------------------------------

#Initialize pygame
pygame.init()

class GameMenu():
    def __init__(self, screen):
        self.screen = screen
        self.bgColor = BLACK
        self.clock = pygame.time.Clock()

        #More of Initializing pygame
        pygame.display.set_caption('Shitty Agario')
        self.SURF = screen

        self.SMALLESTFONT = pygame.font.Font('freesansbold.ttf', 14)
        self.SMALLERFONT = pygame.font.Font('freesansbold.ttf', 20)
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 72)


    ### Main running menu function ###
    def run(self):
        mainLoop = True

        #Some button boolean flags
        playHover = False;
        configHover = False;
        bossHover = False;
        ####################
        ## Main menu loop ##
        ####################
        while mainLoop:
            #Limit frame speed to FPS
            self.clock.tick(15)


            ## Screen ##

            #Drawing the background
            self.SURF.fill(WHITE)
            #pygame.display.flip() #To be honest, not sure what this is supposed to do.


            #Titles
            textTitleSurf = self.BIGFONT.render("Badgario - A shitty version of Agar.io", True, BLACK)
            textTitleRect = textTitleSurf.get_rect()
            textTitleRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y - CAMERASLACK - 72)

            textSubSurf = self.SMALLERFONT.render("A silly half-baked game by Haoda Fan - the master of silly half-baked things.", True, BLACK)
            textSubRect = textSubSurf.get_rect()
            textSubRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y - CAMERASLACK)

            #Drawing the titles
            self.SURF.blit(textTitleSurf, textTitleRect)
            self.SURF.blit(textSubSurf, textSubRect)

            ## Buttons ##

            #Button 1: Play the game

            if playHover:
                textPlayColor = WHITE
                backPlayColor = BLACK
            else:
                textPlayColor = BLACK
                backPlayColor = WHITE

            pygame.draw.circle(self.SURF, backPlayColor, (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y + CAMERASLACK + 25), CAMERASLACK, 0)


            textPlaySurf = self.SMALLERFONT.render("Play game!", True, textPlayColor)
            textPlayRect = textPlaySurf.get_rect()
            textPlayRect.center = (HALF_SCREENSIZE_X, HALF_SCREENSIZE_Y + CAMERASLACK + 25)
            self.SURF.blit(textPlaySurf, textPlayRect)

            #Button 2: How to configure game

            if configHover:
                textConfigColor = WHITE
                backConfigColor = BLUE
            else:
                textConfigColor = BLUE
                backConfigColor = WHITE

            pygame.draw.circle(self.SURF, backConfigColor, (50 + CAMERASLACK, HALF_SCREENSIZE_Y + CAMERASLACK + 25), CAMERASLACK, 0)

            textConfigSurf = self.SMALLESTFONT.render("Game Settings", True, textConfigColor)
            textConfigRect = textConfigSurf.get_rect()
            textConfigRect.center = (50 + CAMERASLACK, HALF_SCREENSIZE_Y + CAMERASLACK + 25)
            self.SURF.blit(textConfigSurf, textConfigRect)

            #Button 3: How to customize boss

            if bossHover:
                textBossColor = WHITE
                backBossColor = RED
            else:
                textBossColor = RED
                backBossColor = WHITE

            pygame.draw.circle(self.SURF, backBossColor, (SCREENSIZE_X - CAMERASLACK - 50, HALF_SCREENSIZE_Y + CAMERASLACK + 25), CAMERASLACK, 0)

            textBossSurf = self.SMALLESTFONT.render("Customize Boss", True, textBossColor)
            textBossRect = textBossSurf.get_rect()
            textBossRect.center = (SCREENSIZE_X - CAMERASLACK - 50, HALF_SCREENSIZE_Y + CAMERASLACK + 25)
            self.SURF.blit(textBossSurf, textBossRect)

            #Coming soon! Buttons that do the work for you! (you lazy asshole)

            #Mouse recognition
            mouse = pygame.mouse.get_pos()
            #Note mouse[0] = x, mouse[1] = y

            # Mouse Hovering effects
            if GameMenu.isInRect(mouse[0], mouse[1], textPlayRect):
                playHover = True
                print("Hovering over play")
            elif GameMenu.isInRect(mouse[0], mouse[1], textConfigRect):
                configHover = True
                print("Hovering over config")
            elif GameMenu.isInRect(mouse[0], mouse[1], textBossRect):
                bossHover = True
                print("Hovering over boss")
            else:
                playHover = False
                configHover = False
                bossHover = False

            # Mouse clicking effects
            mouseClick = pygame.mouse.get_pressed()
            if mouseClick == (1,0,0) and playHover:
                time.sleep(0.2)
                main()
            elif mouseClick == (1,0,0) and configHover:
                os.system("notepad.exe more_instructions/config.txt")
            elif mouseClick == (1,0,0) and bossHover:
                os.system("notepad.exe more_instructions/customboss.txt")

            ## Event Listeners ##
            for event in pygame.event.get():
                # Quitting
                if event.type == pygame.QUIT:
                    mainLoop = False
                    terminate()

            #Updates the display
            pygame.display.update()

    # -------------------- #
    ### HELPER FUNCTIONS ###
    # -------------------- #
    def isInRect(x, y, objRect):
        newRect = pygame.Rect(x-1, y-1, 2, 2)
        return objRect.colliderect(newRect)


if __name__ == "__main__":
    #Create the screen
    screen = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), 0, 32)
    pygame.display.set_caption("Badgario - A shitty agario, by Haoda Fan")
    gm = GameMenu(screen)
    gm.run()
