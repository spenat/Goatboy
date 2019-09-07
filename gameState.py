'''
Created on 12 jul 2011

@author: arvid
@author: Mikael
'''
import pygame, os, mapLogic, gameLogic, guiTools
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION


input_config = {
    'moveLeft': [276, 97],
    'moveRight': [275, 100],
    'moveUp': [273, 119],
    'moveDown': [274, 115],
    'jump': [273, 119],
    'saveMap': [112],
    'saveMapAs': [111],
    'newMap': [110],
    'shoot': [32, 102],
    'quit': [27],
    'shootButton': [1, 2, 5],
    'jumpButton': [0, 4],
    'quitButton': [3, 7],
    'hatLeft': [4],
    'hatRight': [2],
    'hatStop': [0]
}


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
    fullscreen = False
    defaultLevel = None
    frameCounter = 0
    leveleditor = None
    map = None
    screen = None
    scrollx = 0
    scrolly = 0
    scoore = 0
    scoreFromPreviousLevel = 0
    scooresurface = None
    startingTime = 0
    thor = None
    window = None

    def init_sound(self):
        pass

    def init_display(self):
        resolution = pygame.display.list_modes()[1]
        self.window = pygame.display.set_mode(resolution)
        self.screen = pygame.display.get_surface() # Skarmyta

        flags = self.screen.get_flags()
        if self.fullscreen:
            self.window = pygame.display.set_mode(resolution, flags^FULLSCREEN)
        self.back_file_name = os.path.join("data", "bg2.png") # bakgrundsfilnamnsokvag
        self.back_surface = pygame.image.load(self.back_file_name)
        self.back_surface = pygame.transform.scale(self.back_surface,self.screen.get_size())

        self.scooresurface = pygame.Surface((50, 25))

        self.background = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption('Goatboy: the hoorned avanger') #Fonstertitel
        pygame.display.flip()

        self.background.blit(self.back_surface, (0, 0))

    def init_map(self, mapName):
        pass

    def init_clock(self):
        self.clock = pygame.time.Clock()

    def init_controllables(self):
        pass

    def handleInput(self, events):
        print events
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key in input_config['quit']:
                    return False
        return True


class PlayState(GameState):

    def __init__(self):
        self.init_action_map()

    hat_map = {
        (0, 0): 0, # stop
        (0, 1): 1,
        (1, 0): 2, # right
        (1, 1): 3,
        (-1, 0): 4, # left
        (-1, -1): 5
    }
 
    def move_right(self):
        self.thor.move_right()
        return True

    def move_left(self):
        self.thor.move_left()
        return True

    def jump(self):
        self.thor.move_up()
        return True

    def shoot(self):
        self.thor.shooting = True
        return True

    def stop_moving(self):
        self.thor.stop()
        return True

    def stop_shooting(self):
        self.thor.shooting = False
        return True

    def quit(self):
        return False

    def init_action_map(self):
        action_map = {
            (KEYDOWN, 'moveRight') : self.move_right,
            (KEYDOWN, 'moveLeft') : self.move_left,
            (KEYDOWN, 'jump') : self.jump,
            (KEYDOWN, 'quit') : self.quit,
            (KEYDOWN, 'shoot') : self.shoot,
            (KEYUP, 'moveRight') : self.stop_moving,
            (KEYUP, 'moveLeft') : self.stop_moving,
            (KEYUP, 'shoot') : self.stop_shooting,
            (JOYBUTTONDOWN, 'shootButton') : self.shoot,
            (JOYBUTTONDOWN, 'jumpButton') : self.jump,
            (JOYBUTTONDOWN, 'quitButton') : self.quit,
            (JOYBUTTONUP, 'shootButton') : self.stop_shooting,
            (JOYHATMOTION, 'hatLeft') : self.move_left,
            (JOYHATMOTION, 'hatRight') : self.move_right,
            (JOYHATMOTION, 'hatStop') : self.stop_moving,
        }
        new_action_map = {}
        for key in action_map.keys():
            for int_key in input_config[key[1]]:
                new_action_map[(key[0], int_key)] = action_map[key]
        self.action_map = new_action_map

    def init_sound(self):
        pygame.mixer.init()
        self.tracks = []
        paths = [os.path.join("ost", "track") + str(n) + ".mp3" for n in range(1,7)]
        self.tracks += paths
        self.lasttrack = 0
        pygame.mixer.music.load(os.path.join("data", self.tracks[self.lasttrack]))
        pygame.mixer.music.play(-1)
        self.shotsounds = []
        kicks = ["kick_03.wav","laser.wav","kick_05.wav","perc01.wav",]
        self.shotsounds += [pygame.mixer.Sound(os.path.join("data", fn)) for fn in kicks]
        self.changesound = pygame.mixer.Sound(os.path.join("data", "fx05.wav"))
        for i in range(len(self.shotsounds)):
           self.shotsounds[i].set_volume(0.2)
        self.enemydeathsound = pygame.mixer.Sound(os.path.join("data","spinkick.wav"))
        self.enemydeathsound.set_volume(0.8)
        self.deathsound = pygame.mixer.Sound(os.path.join("data","bongo01.wav"))
        self.successound = pygame.mixer.Sound(os.path.join("data","door.wav"))

    def init_map(self, mapName):
        self.map = mapLogic.Map() # skapa ett map-objekt
        self.map.loadmap(mapName) # ladda banan fran fil

    def init_controllables(self):
        from gameObjects import Goatboy
        self.thor = Goatboy(self)

    def handleInput(self, events):
        for event in events:
            try:
                if hasattr(event, 'key'):
                    return self.action_map[(event.type, event.key)]()
                elif hasattr(event, 'button'):
                    return self.action_map[(event.type, event.button)]()
                elif hasattr(event, 'value'):
                    return self.action_map[(event.type, self.hat_map[event.value])]()
            except Exception as e:
                print e
                print event
        return True


class MenuState(GameState):

    current = 0
    alternatives = ['New Game', 'Editor', 'Options', 'Highscore', 'Quit']
    pointer = '- - '

    def init_display(self):
        super(MenuState, self).init_display()
        self.update_menu()

    def update_menu(self):
        current_menu = []
        for n, alt in enumerate(self.alternatives):
            if n == self.current:
                current_menu.append(self.pointer + alt)
            else:
                current_menu.append(alt)
        guiTools.display_boxes(self.background, current_menu, 300)

    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key in input_config['quit']:
                    return False
                elif event.key in input_config['moveUp']:
                    self.current = (self.current - 1) % len(self.alternatives)
                    self.update_menu()
                elif event.key in input_config['moveDown']:
                    self.current = (self.current + 1) % len(self.alternatives)
                    self.update_menu()
                elif event.key in input_config['shoot'] + input_config['moveRight']:
                    if self.alternatives[self.current] == 'Highscore':
                        guiTools.display_boxes(self.background, gameLogic.highscore(2).split("\n")[:-2], 500)
                        return True
                    return False
                else:
                    print event
        return True


class EditState(GameState):

    def init_map(self, mapName):
        self.map = mapLogic.Map()     # skapa ett map-objekt
        self.map.loadmap(mapName) # ladda banan fran fil
        self.move_map = False

    def init_controllables(self):
        from levelEditor import LevelEditor
        self.leveleditor = LevelEditor()

    def handleInput(self, events):
        leveleditor = self.leveleditor
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key in input_config['quit']:        # Tryck escape
                    return False
                elif event.key in input_config['saveMap']:        # Tryck p for save current map
                    self.map.savemap(os.path.join('data', self.map.name))
                elif event.key in input_config['saveMapAs']:      # Tryck o for save-as current map
                    self.map.savemapAs(self)
                elif event.key in input_config['newMap']:      # Tryck n for att borja bygga pa en tom, ny karta.
                    self.map.newMapFromScratch(self)
                elif event.key in input_config['shoot']:
                    self.move_map = True
            elif event.type == KEYUP:
                if event.key in input_config['shoot']:
                    self.move_map = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                # Tryck vanster musknapp for skapa valt objekt
                    leveleditor.createGO(self)
                elif event.button == 3:
                # Tryck hoger  mosknapp for vaxla objekt
                    leveleditor.changeGO()
            elif event.type == MOUSEMOTION:
                if not self.move_map:
                    leveleditor.setposition(event.pos[0], event.pos[1])
                    # muspekaren flyttar leveleditorn
                else:
                    self.scrollx = self.scrollx + ((self.screen.get_width() / 2 - event.pos[0]) / 100)
                    self.scrolly = self.scrolly + ((self.screen.get_height() / 2 - event.pos[1]) / 100)
        return True
