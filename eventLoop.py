'''
@author: arvid
@author: mikael
'''

import pygame, os
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT

def proceed(gameState):
    gs = gameState
    gs.clock.tick(60)   # Delay
    gs.screen.blit(gs.background, (0, 0)) # Rita bakgrunden
        
    gs.thor.update(gs)
    #gs.leveleditor.update()
    gs.map.update(gs)
    
    if pygame.event.peek(): # Titta om det finns en event i event-kon
        if not handleInput(pygame.event.get(), gs):  # Om det finns skicka event till input()
            return False
    gs.allsprites.draw(gs.screen) # Rita alla sprites
    pygame.display.flip()   # vand fram dubbelbufferten
    
    return True
    
    
def handleInput(events, gameState):
    '''
    Input - hanteraren
    '''
    gs = gameState
    
    thor = gs.thor
    map = gs.map
    leveleditor = gs.leveleditor
    
    for event in events:
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == 275 or event.key == 100:         # Tryck hoger lr d
                thor.move_right()
            elif event.key == 276 or event.key == 97:        # Tryck vanster lr a
                thor.move_left()
            elif event.key == 274:                    # Tryck ner
                thor.move_down()
            elif event.key == 273 or event.key == 119:        # Tryck upp lr w
                thor.move_up()
            elif event.key == 120:      # Tryck x for att andra spridning pa skotten
                thor.changeweapon()
            elif event.key == 27:        # Tryck escape
                return False
            elif event.key == 112:        # Tryck p for save current map
                map.savemap(os.path.join('data', map.name))
            elif event.key == 111:      # Tryck o for save-as current map
                map.savemapAs(gs)
            elif event.key == 32 or event.key == 102:        # Tryck space for SKJUT!
                thor.shooting = True
            else:
                print event
        elif event.type == KEYUP:
            if event.key == 275 or event.key == 276 or event.key == 100 or event.key == 97: # Lyft hoger eller vanster
                thor.stop()
            elif event.key == 32 or event.key == 102:
                thor.shooting = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:         # Tryck vanster musknapp for skapa valt objekt
                leveleditor.createGO(gs)
            elif event.button == 3:        # Tryck hoger  mosknapp for vaxla objekt
                leveleditor.changeGO()
        elif event.type == MOUSEMOTION:
                leveleditor.setposition(event.pos[0], event.pos[1]) # muspekaren flyttar leveleditorn
        else:
            print event

    return True