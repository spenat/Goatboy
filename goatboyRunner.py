'''
Created on 12 jul 2011

@author: Arvid
'''

import goatboyLogic, pygame

goatboyLogic.startGame()

# -- The Main Loop -- #

while True:
    transientThor = goatboyLogic.getThor()
    transientMap = goatboyLogic.getMap()
    
    goatboyLogic.getClock().tick(60)                     # Delay
    goatboyLogic.getScreen().blit(goatboyLogic.getBackground(), (0, 0)) # Rita bakgrunden
    if transientThor.boneRect.collidelist(transientMap.blocks) != -1:                     # Testa goatboys ben mot alla block
        if transientThor.dy > 0:             # Om man nuddar ett block pa vagen ner,
            transientThor.dy = 0             # faller man inte langre nedat
            transientThor.onGround = True    # och har fotterna pa fast mark.
    else:
        transientThor.onGround = False # nuddar man inget block, star man inte pa marken
    if transientThor.rect.collidelist(transientMap.enemies) != -1:
        goatboyLogic.reset()
    elif transientThor.rect.collidelist(transientMap.doors) != -1:
        map.doors[transientThor.rect.collidelist(transientMap.doors)].open() # Oppna dorren
        goatboyLogic.reset()
    transientThor.update()
    goatboyLogic.getLeveleditor().update()
    transientMap.update()
    if pygame.event.peek(): # Titta om det finns en event i event-kon
        goatboyLogic.input(pygame.event.get()) # Om det finns skicka event till input()
    goatboyLogic.getAllSprites().draw(goatboyLogic.getScreen()) # Rita alla sprites
    pygame.display.flip()   # vand fram dubbelbufferten

