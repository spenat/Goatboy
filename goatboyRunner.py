#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
'''

import gameLogic, eventLoop, gameState, mapLogic, pygame, os, time
from pygame.locals import *

def initializeGame(gameState):
    gs = gameState

    pygame.init()
    pygame.joystick.init() #initialise joystick/gamepad
    if pygame.joystick.get_count() > 0:
       print "Gamepad found!"
       gs.gamepads = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
       print gs.gamepads
       for gp in gs.gamepads:
          print gp
          gp.init()
          print gp.get_init()
    resolution = (1366, 768)
    gs.window = pygame.display.set_mode(resolution) #, flags^FULLSCREEN) #pygame.display.list_modes()[0]) # Fonsterstorlek
    print pygame.display.list_modes()

    gs.screen = pygame.display.get_surface() # Skarmyta

    flags = gs.screen.get_flags()
    gs.window = pygame.display.set_mode(resolution, flags) # ^FULLSCREEN)
    gs.back_file_name = os.path.join("data", "bg2.png") # bakgrundsfilnamnsokvag
    gs.back_surface = pygame.image.load(gs.back_file_name)
    gs.back_surface = pygame.transform.scale(gs.back_surface,gs.screen.get_size())
    gs.clock = pygame.time.Clock()
    gs.background = pygame.Surface(gs.screen.get_size())
    gs.scrollx = 0
    gs.scrolly = 0
    gs.scoore = 0
    pygame.mixer.init()
    gs.tracks = []
    # tracknumbers = [6, 9, 12, 19, 24, 43]
    paths = [os.path.join("ost", "track") + str(n) + ".mp3" for n in range(1,7)]
    gs.tracks += paths
    gs.lasttrack = 0
    pygame.mixer.music.load(os.path.join("data", gs.tracks[gs.lasttrack]))
    pygame.mixer.music.play(-1)
    gs.shotsounds = []
    kicks = ["kick_03.wav","laser.wav","kick_05.wav","perc01.wav",]
    gs.shotsounds += [pygame.mixer.Sound(os.path.join("data", fn)) for fn in kicks]
    gs.changesound = pygame.mixer.Sound(os.path.join("data", "fx05.wav"))
    #gs.shotsounds
    for i in range(len(gs.shotsounds)):
       gs.shotsounds[i].set_volume(0.2)
    gs.enemydeathsound = pygame.mixer.Sound(os.path.join("data","spinkick.wav"))
    gs.enemydeathsound.set_volume(0.8)
    gs.deathsound = pygame.mixer.Sound(os.path.join("data","bongo01.wav"))
    gs.scooresurface = pygame.Surface((50, 25))
    gs.successound = pygame.mixer.Sound(os.path.join("data","door.wav"))
    pygame.display.set_caption('Goatboy: the hoorned avanger') #Fonstertitel
    pygame.display.flip()
    gs.background.blit(gs.back_surface, (0, 0))
    #screen.get_flags()

    gs.map = mapLogic.Map()     # skapa ett map-objekt
    gs.map.loadmap("map1.map") # ladda banan fran fil

    from gameObjects import Goatboy
    gs.thor = Goatboy(gs) # skapa ett goatboy-objekt =)
    from levelEditor import LevelEditor
    gs.leveleditor = LevelEditor()

    gameLogic.loadvisible(gs)

    gs.frameCounter = 0                    # Set up FPS counter
    gs.startingTime = time.time()          #


def endGame(gameState):
    playingTime = time.time() - gameState.startingTime

    print "You played the game for %i seconds, during which %i frames were rendered. That gives an average FPS of %i \n" % (playingTime, gameState.frameCounter, gameState.frameCounter/playingTime)

    gameLogic.highscore(gameState.scoore)


def main():
    gs = gameState.GameState()   # Create a state object
    initializeGame(gs)           # Initialize a new game in the state object

    while eventLoop.proceed(gs):              # The condition of this while-loop is where
        gs.frameCounter = gs.frameCounter + 1 # the games is actually taking place

    endGame(gs)


###### Module body #############

if __name__ == '__main__': main()

###### End of module body ###########

