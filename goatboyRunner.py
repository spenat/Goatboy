#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
'''

import gameLogic, eventLoop, gameState, mapLogic, pygame, os, time

def initializeGame(gameState):
    gs = gameState
    
    pygame.init()
        
    gs.window = pygame.display.set_mode(pygame.display.list_modes()[0]) # Fonsterstorlek
    gs.screen = pygame.display.get_surface() # Skarmyta
    gs.back_file_name = os.path.join("data", "background.bmp") # bakgrundsfilnamnsokvag
    gs.back_surface = pygame.image.load(gs.back_file_name)
    gs.clock = pygame.time.Clock()
    gs.background = pygame.Surface(gs.screen.get_size())
    gs.scrollx = 0
    gs.scrolly = 0
    gs.scoore = 0
    gs.scooresurface = pygame.Surface((50, 25))
    gs.leveleditor = None
    
    pygame.display.set_caption('Goatboy: the hoorned avanger') #Fonstertitel
    pygame.display.flip()
    gs.background.blit(gs.back_surface, (0, 0))
    
    gs.map = mapLogic.Map()     # skapa ett map-objekt
    gs.map.loadmap("map1.map") # ladda banan fran fil

    from gameObjects import Goatboy
    gs.thor = Goatboy(gs) # skapa ett goatboy-objekt =)
    from gameObjects import LevelEditor
    gs.leveleditor = LevelEditor()
    
    gameLogic.loadvisible(gs)


###### Module body #############

gameState = gameState.GameState()   # Create a state object
initializeGame(gameState)           # Initialize a new game in the state object

frameCounter = 0                    # Set up FPS counter
startingTime = time.time()          #

while eventLoop.proceed(gameState): # The condition of this while-loop is where
    frameCounter = frameCounter + 1 # the games is actually taking place

playingTime = time.time() - startingTime  
    
print "You played the game for %i seconds, during which %i frames were rendered. That gives an average FPS of %i " % (playingTime, frameCounter, frameCounter/playingTime)

###### End of module body ###########