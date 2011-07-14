'''
@author: mikael
@author: arvid
'''

from gameObjects import Block, Door, Flameboy, Flamenemy, GameObject
import gameLogic

class LevelEditor(GameObject):
    '''
    Leveleditor
    '''
    entity = 0
    images = ['blockgrass.bmp', 'block.bmp', 'flamenemy.bmp', 'door.bmp', 'flameboy.bmp']
    filename = images[0]
    def createGO(self, gameState):
        gs = gameState
        
        if self.entity == 0:
            block = Block()
            block.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addBlock(block)    
        elif self.entity == 1:
            block = Block()
            block.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            block.setimage(self.images[self.entity], None)
            gs.map.addBlock(block)
        elif self.entity == 2:
            enemy = Flamenemy()
            enemy.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addEnemy(enemy)
        elif self.entity == 3:
            door = Door()
            door.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addDoor(door)
        elif self.entity == 4:
            flameboy = Flameboy()
            flameboy.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addEnemy(flameboy)
        
        gameLogic.loadvisible(gs)

    def changeGO(self):
        self.entity = (self.entity + 1) % 5
        if self.entity == 0 or self.entity == 2 or self.entity == 3 or self.entity == 4: # For bilderna som vill ha en transparentcolor
            self.setimage(self.images[self.entity], -1)
        else:                                  # For bilderna som inte vill
            self.setimage(self.images[self.entity], None)

    def update(self):
        self.rect.topleft = self.x, self.y
