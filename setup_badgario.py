# THIS PORTION IS UNUSED AND STILL IN DEVELOPMENT.
#

# ----------------------------------------------------
from badgario import *
# ----------------------------------------------------

pygame.init()

class GameMenu():
    def __init__(self, screen):
        self.screen = screen
        self.bgColor = BLACK
        self.clock = pygame.time.Clock()

        ## Main running menu function ##
        def run(self):
            mainLoop = True
            
            ## Main menu loop ##
            while mainLoop:
                #Limit frame speed to FPS
                self.clock.tick(FPS)

                ## Event Listeners ##
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mainLoop = False
                        terminate()
                    

    if __name__ == "__main__":
        #Create the screen
        screen = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), 0, 32)
        pygame.display.set_caption("Badgario - A shitty agario, by Haoda Fan")
        gm = GameMenu(screen)
        gm.run()
