'''
Created on 12 jul 2011

@author: arvid
'''

import pygame, gameObjects, string, os
import gameLogic

class Map():
    '''
    Map-classen
    '''
    blocks = []
    enemies = []
    doors = []
    shots = []
    upgrades = []
    initenemies = []
    initblocks = []
    initdoors = []
    name = None

    def addBlock(self, block):
        self.blocks.append(block)
        self.initblocks.append([block.x, block.y, block.leftlimit, block.rightlimit, block.dx])

    def addEnemy(self, enemy):
        self.enemies.append(enemy)
        self.initenemies.append([enemy.x, enemy.y, enemy.kind])

    def addDoor(self, door):
        self.doors.append(door)
        self.initdoors.append([door.x, door.y, door.targetMap])

    def addShot(self, shot):
        self.shots.append(shot)

    def addUpgrade(self, upgrade):
        self.upgrades.append(upgrade)

    def update(self, gameState):
        gs = gameState

        def static_update(gameObject):
            gameObject.rect.topleft = gameObject.x + gs.scrollx, gameObject.y + gs.scrolly

        if gs.thor:
            for block in self.blocks:
                block.update(gs)
            for enemy in self.enemies:
                enemy.update(gs)
            for door in self.doors:
                door.update(gs)
            for shot in self.shots:
                shot.update(gs)
            for upgrade in self.upgrades:
                upgrade.update(gs)
        else:
            for block in self.blocks:
                static_update(block)
            for enemy in self.enemies:
                static_update(enemy)
            for door in self.doors:
                static_update(door)

        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render(str(gs.scoore), 1, (255, 5, 5))
            textpos = text.get_rect()
            textpos.centerx = gs.background.get_rect().centerx
            gs.background.blit(gs.scooresurface, textpos)
            gs.background.blit(text, textpos)

    def reset(self):
        for index, block in enumerate(self.blocks):
            block.setposition(self.initblocks[index][0], self.initblocks[index][1])
            block.setlimits(self.initblocks[index][2], self.initblocks[index][3])
            block.setdx(self.initblocks[index][4])
        for index, enemy in enumerate(self.enemies):
            enemy.setposition(self.initenemies[index][0], self.initenemies[index][1])
            enemy.reset()
        for index, door in enumerate(self.doors):
            door.setposition(int(self.initdoors[index][0]), int(self.initdoors[index][1]))
        self.shots = []
        self.upgrades = []

    def savemap(self, filename):
        f = open(filename, 'w')
        for index, block in enumerate(self.blocks):
            f.write(string.join(["block",
                                 str(self.initblocks[index][0]),
                                 str(self.initblocks[index][1]),
                                 str(self.initblocks[index][2]),
                                 str(self.initblocks[index][3]),
                                 str(self.initblocks[index][4]),
                                 block.filename], ':'))
            f.write('\n')
        for index in enumerate(self.enemies):
            index = index[0]
            f.write(string.join(["flamenemy",
                                 str(self.initenemies[index][0]),
                                 str(self.initenemies[index][1]),
                                 str(self.initenemies[index][2])], ':'))
            f.write('\n')
        for index in enumerate(self.doors):
            index = index[0]
            f.write(string.join(["door",
                                 str(self.initdoors[index][0]),
                                 str(self.initdoors[index][1]),
                                 self.initdoors[index][2]], ':'))
            f.write('\n')

    def savemapAs(self, gameState):
        import guiTools
        mapNumber = guiTools.ask(gameState.screen, "Save map as (number)", str( gameLogic.getHighestMapNumber() + 1 ) )
        self.savemap( os.path.join('data', "map" + str(mapNumber)  + ".map") )

    def newMapFromScratch(self, gameState):
        startingBlock = gameObjects.Block()
        startingBlock.setposition(300, 400)
        newMap = Map()
        newMap.addBlock(startingBlock)
        newMapFileName = "map" + str( gameLogic.getHighestMapNumber()+1 )  + ".map"
        newMap.savemap( os.path.join('data', newMapFileName) )
        self.loadmap(newMapFileName)
        gameLogic.reset(gameState)

    def loadmap(self, filename):
        self.name = filename
        self.blocks = []
        self.enemies = []
        self.doors = []
        self.initblocks = []
        self.initenemies = []
        self.initdoors = []
        f = open(os.path.join('data', filename), 'r')
        for line in f:
            entity = string.split(line, ':')
            if entity[0] == 'block':
                block = gameObjects.Block()
                block.setposition(int(entity[1]), int(entity[2]))
                block.setlimits(int(entity[3]), int(entity[4]))
                block.setdx(int(entity[5]))
                transparents = ['blockgrass.bmp', 'coin.bmp', 'stone.bmp']
                if string.strip(entity[6]) in transparents:
                    block.setimage(string.strip(entity[6]), -1)
                else:
                    block.setimage(string.strip(entity[6]), None)
                self.addBlock(block)
            elif entity[0] == 'flamenemy':
                if len(entity) > 3:
                    if int(entity[3]) == 0:
                        enemy = gameObjects.Flamenemy()
                    elif int(entity[3]) == 1:
                        enemy = gameObjects.Flameboy()
                else:
                    enemy = gameObjects.Flamenemy()
                enemy.setposition(int(entity[1]), int(entity[2]))
                self.addEnemy(enemy)
            elif entity[0] == 'door':
                door = gameObjects.Door()
                door.setposition(int(entity[1]), int(entity[2]))
                door.targetMap = string.strip(entity[3])
                self.addDoor(door)
