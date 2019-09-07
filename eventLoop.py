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

    if gs.thor:
        gs.thor.update(gs)
    elif gs.leveleditor:
        gs.leveleditor.update()

    if gs.map:
        gs.map.update(gs)

    if gs.allsprites:
        gs.allsprites.draw(gs.screen) # Rita alla sprites
    pygame.display.flip()   # vand fram dubbelbufferten

    if pygame.event.peek(): # Titta om det finns en event i event-kon
        if not gs.handleInput(pygame.event.get()):  # Om det finns skicka event till input()
            return False

    return True
