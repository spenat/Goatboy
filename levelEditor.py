'''
@author: mikael
@author: arvid
'''
import random
from gameObjects import Block, Door, Flameboy, Flamenemy, GameObject, Upgrade
import gameLogic

class LevelEditor(GameObject):
    '''
    Leveleditor
    '''
    entity = 0
    images = ['blockgrass.bmp', 'block.bmp', 'flamenemy.bmp', 'door.bmp', 'flameboy.bmp','block.bmp', 'upgrade.bmp', 'stone.bmp']
    filename = images[0]
    def createGO(self, gameState):
        gs = gameState
        
        if self.entity == 0:
            block = Block()
            block.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addBlock(block)    
        elif self.entity in [1, 5, 7]:
            block = Block()
            block.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            block.setimage(self.images[self.entity], -1 if self.entity in [5,7] else None)
            if self.entity == 5:
                block.rightlimit = block.x + random.randint(100, 20000)
                block.leftlimit = block.x - random.randint(100, 20000)
                block.dx = random.randint(0, 30) - 15
            gs.map.addBlock(block)
        elif self.entity == 2:
            enemy = Flamenemy()
            enemy.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addEnemy(enemy)
        elif self.entity == 3:
            door = Door()
            import guiTools
            door.setTargetDoor( guiTools.ask(gs.screen, "Which map number should the door lead to?") )
            door.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addDoor(door)
        elif self.entity == 4:
            flameboy = Flameboy()
            flameboy.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addEnemy(flameboy)
        elif self.entity == 6:
            upgrade = Upgrade()
            upgrade.setposition(self.x - gs.scrollx, self.y - gs.scrolly)
            gs.map.addUpgrade(upgrade)

        gameLogic.loadvisible(gs)

    def changeGO(self):
        self.entity = (self.entity + 1) % 8
        transparents = [0, 2, 3, 4, 6, 7]
        if self.entity in transparents:
            self.setimage(self.images[self.entity], -1)
        else:
            self.setimage(self.images[self.entity], None)

    def update(self):
        self.rect.topleft = self.x, self.y
