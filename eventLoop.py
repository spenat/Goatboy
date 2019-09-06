'''
@author: arvid
@author: mikael
'''

import pygame, os, random
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION

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


input_config = {
    'moveLeft': [276, 97],
    'moveRight': [275, 100],
    'jump': [273, 119],
    'saveMap': [112],
    'saveMapAs': [111],
    'newMap': [110],
    'shoot': [32, 102],
    'quit': [27]
}

def handleInput(events, gameState):
    '''
    Input - hanteraren
    '''
    gs = gameState

    thor = gs.thor
    map = gs.map
    leveleditor = gs.leveleditor
    def changesound():
        pass #gs.changesound.stop()
        #gs.changesound.play()
    for event in events:
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key in input_config['moveRight']:         # Tryck hoger lr d
                thor.move_right()
            elif event.key in input_config['moveLeft']:        # Tryck vanster lr a
                thor.move_left()
            #elif event.key in :                    # Tryck ner
            #    thor.move_down()
            elif event.key in input_config['jump']:        # Tryck upp lr w
                thor.move_up()
            elif event.key == 120:
                # Tryck x for att andra spridning pa skotten
                thor.changeweapon()
                changesound()
            elif event.key in input_config['quit']:        # Tryck escape
                return False
            elif event.key in input_config['saveMap']:        # Tryck p for save current map
                map.savemap(os.path.join('data', map.name))
            elif event.key in input_config['saveMapAs']:      # Tryck o for save-as current map
                map.savemapAs(gs)
            elif event.key in input_config['newMap']:      # Tryck n for att borja bygga pa en tom, ny karta.
                map.newMapFromScratch(gs)
            elif event.key in input_config['shoot']:        # Tryck space for SKJUT!
                thor.shooting = True
            else:
                print event
        elif event.type == KEYUP:
            if event.key in input_config['moveRight'] + input_config['moveLeft']:
            # Lyft hoger eller vanster
                thor.stop()
            elif event.key in input_config['shoot']:
                thor.shooting = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
            # Tryck vanster musknapp for skapa valt objekt
                leveleditor.createGO(gs)
            elif event.button == 3:
            # Tryck hoger  mosknapp for vaxla objekt
                leveleditor.changeGO()
        elif event.type == MOUSEMOTION:
                leveleditor.setposition(event.pos[0], event.pos[1])
                # muspekaren flyttar leveleditorn
        elif event.type == JOYBUTTONDOWN:
            if event.button == 0:
               thor.shooting = True
               gs.shotsounds[random.randint(0, len(gs.shotsounds) - 1)].play()
            if event.button == 1:
               thor.move_up()
            if event.button == 5:
               thor.changeweapon()
               changesound()
            else:
               print event
        elif event.type == JOYBUTTONUP:
            if event.button == 0:
               thor.shooting = False
            else:
               print event
        elif event.type == JOYHATMOTION:
            v1, v2 = event.value
            if v1 == 1 and v2 == 0:
               thor.move_right()
            elif v1 == 0 and v2 == 0:
               thor.stop()
            elif v1 == -1 and v2 == 0:
               thor.move_left()
            elif v1 == 0 and v2 == 1:
               thor.move_up()
            else:
               print event
        else:
            print event
            print event.type

    return True
