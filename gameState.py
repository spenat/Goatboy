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
    'hatStop': [0],
    'hatUp': [1],
    'hatDown': [6],
    'mouseLeft': [1],
    'mouseRight': [3],
    'mouseMotion': [0]
}

hat_map = {
    (0, 0): 0, # stop
    (0, 1): 1, # up
    (1, 0): 2, # right
    (1, 1): 3,
    (-1, 0): 4, # left
    (-1, -1): 5,
    (0, -1): 6 # down
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
        for event in events:
            try:
                if hasattr(event, 'key'):
                    return self.action_map[(event.type, event.key)]()
                elif hasattr(event, 'button'):
                    return self.action_map[(event.type, event.button)]()
                elif hasattr(event, 'value'):
                    return self.action_map[(event.type, hat_map[event.value])]()
                elif hasattr(event, 'pos'):
                    return self.action_map[(event.type, 0)](event.pos)
            except Exception as e:
                print(f'exception : {e}')
                print(event)
        return True

    def generate_actionmap(self, action_map):
        new_action_map = {}
        for key in action_map.keys():
            for int_key in input_config[key[1]]:
                new_action_map[(key[0], int_key)] = action_map[key]
        return new_action_map

    def quit(self):
        return False


class PlayState(GameState):

    def __init__(self):
        self.init_action_map()

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
        self.action_map = self.generate_actionmap(action_map)

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


class MenuState(GameState):

    current = 0
    top_menu = ['New Game', 'Editor', 'Options', 'Highscore', 'Quit']
    options = ["Display", "Sound", "Controls", "Back to Menu"]
    pointer = '- - '

    def __init__(self):
        self.init_action_map()
        self.alternatives = self.top_menu

    def init_display(self):
        super(MenuState, self).init_display()
        self.update_menu()

    def init_action_map(self):
        action_map = {
            (KEYDOWN, 'moveRight') : self.select_item,
            (KEYDOWN, 'moveLeft') : self.quit,
            (KEYDOWN, 'moveDown') : self.next_item,
            (KEYDOWN, 'moveUp') : self.prev_item,
            (KEYDOWN, 'shoot') : self.select_item,
            (KEYDOWN, 'quit') : self.quit,
            (JOYBUTTONDOWN, 'shootButton') : self.select_item,
            (JOYBUTTONDOWN, 'jumpButton') : self.select_item,
            (JOYBUTTONDOWN, 'quitButton') : self.quit,
            (JOYHATMOTION, 'hatLeft') : self.quit,
            (JOYHATMOTION, 'hatRight') : self.select_item,
            (JOYHATMOTION, 'hatDown') : self.next_item,
            (JOYHATMOTION, 'hatUp') : self.prev_item,
        }
        self.action_map = self.generate_actionmap(action_map)

    def next_item(self):
        self.current = (self.current + 1) % len(self.alternatives)
        self.update_menu()
        return True

    def prev_item(self):
        self.current = (self.current - 1) % len(self.alternatives)
        self.update_menu()
        return True 

    def select_item(self):
        if self.alternatives[self.current] == "Highscore":
            guiTools.display_boxes(self.background, gameLogic.highscore(2).split("\n")[:-2], 500)
            return True
        elif self.alternatives[self.current] == "Options":
            self.top_menu = self.alternatives
            self.alternatives = self.options
            self.current = 0
            self.update_menu()
            return True
        elif self.alternatives[self.current] == "Back to Menu":
            self.alternatives = self.top_menu 
            self.current = 0
            self.update_menu()
            return True
        return False

    def update_menu(self):
        current_menu = []
        for n, alt in enumerate(self.alternatives):
            if n == self.current:
                current_menu.append(self.pointer + alt)
            else:
                current_menu.append(alt)
        guiTools.display_boxes(self.background, current_menu, 300)


class EditState(GameState):

    def __init__(self):
        self.init_action_map()
 
    def init_map(self, mapName):
        self.map = mapLogic.Map()     # skapa ett map-objekt
        self.map.loadmap(mapName) # ladda banan fran fil
        self.move_map = False

    def init_controllables(self):
        from levelEditor import LevelEditor
        self.leveleditor = LevelEditor()

    def init_action_map(self):
        action_map = {
            (KEYDOWN, 'moveRight') : self.move_right,
            (KEYDOWN, 'moveLeft') : self.move_left,
            (KEYDOWN, 'moveUp') : self.move_up,
            (KEYDOWN, 'moveDown') : self.move_down,
            (KEYDOWN, 'shoot') : self.move_map,
            (KEYDOWN, 'saveMap') : self.save_map,
            (KEYDOWN, 'quit') : self.quit,
            (KEYUP, 'shoot') : self.stop_moving_map,
            (JOYBUTTONDOWN, 'quitButton') : self.quit,
            (JOYHATMOTION, 'hatLeft') : self.move_left,
            (JOYHATMOTION, 'hatRight') : self.move_right,
            (JOYHATMOTION, 'hatUp') : self.move_up,
            (JOYHATMOTION, 'hatDown') : self.move_down,
            (MOUSEBUTTONDOWN, 'mouseLeft') : self.create_gameobject,
            (MOUSEBUTTONDOWN, 'mouseRight') : self.change_gameobject,
            (MOUSEMOTION, 'mouseMotion') : self.mouse_move
        }
        self.action_map = self.generate_actionmap(action_map)

    def create_gameobject(self):
        self.leveleditor.createGO(self)
        return True

    def change_gameobject(self):
        self.leveleditor.changeGO()
        return True

    def save_map(self):
        self.map.savemap(os.path.join('data', self.map.name))
        return True

    def move_up(self):
        self.scrolly += 100
        return True

    def move_right(self):
        self.scrollx += -100
        return True

    def move_down(self):
        self.scrolly += -100
        return True

    def move_left(self):
        self.scrollx += 100
        return True

    def move_map(self):
        self.move_map = True
        return True

    def stop_moving_map(self):
        self.move_map = False
        return True

    def mouse_move(self, pos):
        if not self.move_map:
            self.leveleditor.setposition(pos[0], pos[1])
        else:
            self.scrollx = self.scrollx + ((self.screen.get_width() / 2 - pos[0]) / 50)
            self.scrolly = self.scrolly + ((self.screen.get_height() / 2 - pos[1]) / 50)
        return True
