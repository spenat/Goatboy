#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
'''

import gameLogic, eventLoop, gameState, mapLogic, pygame, os

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


gameState = gameState.GameState()
initializeGame(gameState)

while True:
    eventLoop.proceed(gameState)
