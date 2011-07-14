'''
Based on inputbox.py by Timothy Downs, changed a bit by Arvid for use in Goatboy

@author: Timothy Downs
@author: arvid
'''
import pygame.font, pygame.event, pygame.draw, string
from pygame.locals import KEYDOWN, K_BACKSPACE, K_RETURN

def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    300,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    304,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()

def ask(screen, question, prefill=""):
    "ask(screen, question, [prefill]) -> answer"
    pygame.font.init()
    current_string = [prefill]
    display_box(screen, question + ": " + string.join(current_string,""))
    while True:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + string.join(current_string,""))
    return string.join(current_string,"")
