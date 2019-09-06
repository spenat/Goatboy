'''
Created on 12 jul 2011

@author: arvid
'''

class GameState(object):
    '''
    This class holds the state of the game.

    (Ex for future development:)
    Sandbox <gamemode> <userpriv?> state
    Menu <gamemode> <userpriv?> state
    Inventory <gamemode> state
    gamemode is editing or mortal
    userpriv is player or root
    '''
    allsprites = None
    background = None
    back_surface = None
    clock = None
    defaultLevel = None
    frameCounter = 0
    leveleditor = None
    map = None
    mapname = None
    screen = None
    scrollx = 0
    scrolly = 0
    scoore = 0
    scoreFromPreviousLevel = 0
    scooresurface = None
    startingTime = 0
    thor = None
    window = None
