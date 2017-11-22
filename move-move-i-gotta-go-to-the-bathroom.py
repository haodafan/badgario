# November 22nd 2017
# Haoda Fan
# This module provides all the necessary functions to move the files required to customize bosses.

# ----------------------------------------------------------------
# Move! Outta my way!
# I gotta go to the bathroom!
# You gotta move! I gotta poop!
# I gotta poop I gotta poop I gotta poop I gotta poop!
# *trumpets*
# MOVE! My belly hurts so bad, and now I GOTTA CLIMB THE STAIRS?!
# OH SHIT I LET A LITTLE OUT
# *trumpets*
# HURRY!! GET OUT OF THE BATHROOM!!
# I gotta fucking shit so hard!
# MOVE! I GOTTA POOP! YOU REALLY NEED TO MOVE!
# GET OUT OF THE BATHROOM!!
# MOOOVE I GOTTA FUCKING POOP!!!!!!
# ----------------------------------------------------------------

#### LIBRARIES ####

import shutil
import os

#### DIRECTORIES ####
thisdir = os.getcwd() #current directory

ACTIVE_DIR = thisdir + "\\data\\active"
BOSSES_DIR = thisdir + "\\data\\bosses"

## More Variables ##
fileNames = ["\\img.png", "\\eat.ogg", "\\eaten.ogg", "\\ohno.ogg", "\\touch.ogg", "\\view.ogg"]

#### FUNCTIONS ####

# This function activates a particular boss
def activate(folderName):
    jobsDone = False
    
    #Loops through every filename
    for (fileName in fileNames):
        shutil.copy2(BOSSES_DIR + "\\" + folderName + fileName, ACTIVE_DIR + fileName)

    jobsDone = True
    return jobsDone
    
    
# This function returns the number of custom bosses
def bossCount():
    # Based on code from
    # https://arstechnica.com/civis/viewtopic.php?f=20&t=1111535
    numfiles = return len([f for f in os.listdir(BOSSES_DIR)) and f[0] != '.'])
