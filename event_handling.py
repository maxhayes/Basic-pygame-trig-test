# Defines the custom library to aide with event handling in pygame.

import pygame, sys

if __name__ == '__main__':
    print('''
    This file is used to define a library that aides with 
    event handling in pygame.  It includes two classes.
    
    This ".
    on its own, it provides no functionality.
    
    HAFF A GUD DAY
    ''')



def ignore():
    pass


# EVENT_EXE class
'''
Each object needs to be passed a pygame event and 
two fucntions or "actions" upon creation.
The first will occur when the pygame event is a KEYDOWN
and the second will respond to KEYUP.

... at least that's the dream.

'''


class Event_exe():
    def __init__(self, event, press_action, release_action, actions_list):
        self.event = event
        self.press_action = press_action
        self.release_action = release_action
        actions_list.append(self)
    
    def pressed(self):
        self.press_action()
        
    def released(self):
        self.release_action()
        
    
    
class Event_conductor():
    def __init__(self, actions_list):
        self.actions_list = actions_list
        self.quit = False
        self.LMB = False
        self.MMB = False
        self.RMB= False
        
    def handle_events(self, events_list, mouse_state):
        self.mouse_state = mouse_state
        
        
        for event in events_list:
            for action in self.actions_list:
                
                
                # if the event is QUIT:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # if the event is keyup or keydown...
                elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    # and if it is a keypress we are looking for...
                    if event.key == action.event:
                        if event.type == pygame.KEYDOWN:
                            action.pressed()
                            
                        elif event.type == pygame.KEYUP:
                            action.released()
                            
                # handle mouse events:
                
                # left mouse button
                elif action.event == 'LMB':
                    if self.mouse_state[0] and self.LMB == False:
                        action.pressed()
                        self.LMB = True
                    if self.LMB:
                        if not self.mouse_state[0]:
                            action.released()
                            self.LMB = False
                        
                # middle mouse button
                elif action.event == 'MMB':
                    if self.mouse_state[1] and self.MMB == False:
                        action.pressed()
                        self.MMB = True
                    if self.MMB:
                        if not self.mouse_state[1]:
                            action.released()
                            self.MMB = False
            
                # right mouse button
                elif action.event == 'RMB':
                    if self.mouse_state[2] and self.RMB == False:
                        action.pressed()
                        self.RMB = True
                    if self.RMB:
                        if not self.mouse_state[2]:
                            action.released()
                            self.RMB= False
        
                            
                                
                                
# TO ADD:
'''
-add support for non-event key down/up events, so things like
Pygame.QUIT work.

-find ways to reduce end-user typing.
    (such as not having to specifiy "actions_list" for each object)
'''