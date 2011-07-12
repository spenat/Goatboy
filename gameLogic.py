'''
	Goatboy : The jumpin' jackass
	
@note: hejhej    
@author: Mikael					    
'''

import os, pygame
from pygame.locals import RLEACCEL


def loadvisible(gameState):
    gs = gameState
    gs.allsprites = pygame.sprite.RenderPlain(sum([gs.map.shots, gs.map.blocks, gs.map.enemies, gs.map.doors, [gs.leveleditor, gs.thor]], [])) # Alla sprites som ska ritas

def reset(gameState):
    gs = gameState
    '''
    Satt alla varden till utgangsvarden
	'''
    gs.scrollx, gs.scrolly, gs.thor.dx, gs.thor.ddx, gs.thor.dy, gs.scoore = 0, 0, 0, 0, 0, 0
    gs.map.reset()
    gs.thor.setposition(300, 150)
    gs.background.blit(gs.back_surface, (0, 0))
    loadvisible(gs)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is - 1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
