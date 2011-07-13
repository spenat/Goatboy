'''
@author: arvid
@author: mikael
'''

import gameLogic, pygame, sys, os
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT

def proceed(gameState):
    gs = gameState
    
    gs.clock.tick(60)                     # Delay
    gs.screen.blit(gs.background, (0, 0)) # Rita bakgrunden
    if gs.thor.boneRect.collidelist(gs.map.blocks) != -1:                     # Testa goatboys ben mot alla block
        if gs.thor.dy > 0:             # Om man nuddar ett block pa vagen ner,
            gs.thor.dy = 0             # faller man inte langre nedat
            gs.thor.onGround = True    # och har fotterna pa fast mark.
    else:
        gs.thor.onGround = False # nuddar man inget block, star man inte pa marken
    if gs.thor.rect.collidelist(gs.map.enemies) != -1:
        gameLogic.reset(gs)
    elif gs.thor.rect.collidelist(gs.map.doors) != -1:
        gs.map.doors[gs.thor.rect.collidelist(gs.map.doors)].open(gs) # Oppna dorren
        gameLogic.reset(gs)
    gs.thor.update(gs)
    #gs.leveleditor.update()
    gs.map.update(gs)
    if pygame.event.peek(): # Titta om det finns en event i event-kon
        handleInput(pygame.event.get(), gs) # Om det finns skicka event till input()
    gs.allsprites.draw(gs.screen) # Rita alla sprites
    pygame.display.flip()   # vand fram dubbelbufferten
    
    
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
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == 275 or event.key == 100:         # Tryck hoger lr d
                thor.move_right()
            elif event.key == 276 or event.key == 97:        # Tryck vanster lr a
                thor.move_left()
            elif event.key == 274:                    # Tryck ner
                thor.move_down()
            elif event.key == 273 or event.key == 119:        # Tryck upp lr w
                thor.move_up()
            elif event.key == 120:
                thor.changeweapon()
            elif event.key == 27:        # Tryck escape
                sys.exit()
            elif event.key == 112:        # Tryck p for save current map
                map.savemap(os.path.join('data', map.name))
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
                leveleditor.createGO()
            elif event.button == 3:        # Tryck hoger  mosknapp for vaxla objekt
                leveleditor.changeGO()
        elif event.type == MOUSEMOTION:
                leveleditor.setposition(event.pos[0], event.pos[1]) # muspekaren flyttar leveleditorn
        else:
            print event
