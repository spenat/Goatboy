#!/usr/bin/python
'''
Created on 12 jul 2011

@author: Arvid
'''

import goatboyLogic
import eventLoop

goatboyLogic.initializeGame()

while True:
    eventLoop.proceed()