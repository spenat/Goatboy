#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
@author: Mikael
'''

import gameLogic, eventLoop, gameState, mapLogic, pygame, os, time
from pygame.locals import *

def initializeGame(gameState):
    gs = gameState

    pygame.init()
    pygame.joystick.init() #initialise joystick/gamepad
    if pygame.joystick.get_count() > 0:
       print "Gamepad found!"
       gs.gamepads = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
       print gs.gamepads
       for gp in gs.gamepads:
          print gp
          gp.init()
          print gp.get_init()
    # resolution = (1366, 768)
    print pygame.display.list_modes()
    gs.init_sound()
    gs.init_display()
    gs.init_clock()
    gs.init_map("map1.map")
    gs.init_controllables()
    gameLogic.loadvisible(gs)

    gs.frameCounter = 0                    # Set up FPS counter
    gs.startingTime = time.time()          #


def endGame(gameState):
    playingTime = time.time() - gameState.startingTime

    print "You played the game for %i seconds, during which %i frames were rendered. That gives an average FPS of %i \n" % (playingTime, gameState.frameCounter, gameState.frameCounter/playingTime)

    print gameLogic.highscore(gameState.scoore)


def main():
    play_state = None
    edit_state = gameState.EditState()
    menu_state = gameState.MenuState()

    initializeGame(edit_state)
    initializeGame(menu_state)

    running = True

    while running:
        if play_state:
            menu_state.background = play_state.screen
            menu_state.update_menu()
        while eventLoop.proceed(menu_state):              # The condition of this while-loop is where
            menu_state.frameCounter = menu_state.frameCounter + 1 # the games is actually taking place

        if menu_state.alternatives[menu_state.current] == 'New Game':
            play_state = gameState.PlayState()
            initializeGame(play_state)           # Initialize a new game in the state object
            current_state = play_state
            if menu_state.alternatives[0] == 'New Game':
                menu_state.alternatives = ['Resume Game'] + menu_state.alternatives
                menu_state.update_menu()
        elif menu_state.alternatives[menu_state.current] == 'Resume Game':
            current_state = play_state
        elif menu_state.alternatives[menu_state.current] == 'Editor':
            current_state = edit_state
            if play_state:
                edit_state.init_map(play_state.map.name)
            gameLogic.loadvisible(edit_state)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
        elif menu_state.alternatives[menu_state.current] == 'Quit':
            running = False

        while running and eventLoop.proceed(current_state):              # The condition of this while-loop is where
            current_state.frameCounter = current_state.frameCounter + 1 # the games is actually taking place

    if play_state:
        endGame(play_state)


###### Module body #############

if __name__ == '__main__': main()

###### End of module body ###########

