# Defines the custom library to aide with event handling in pygame.

import pygame, sys
from math import acos, degrees, pow, sqrt

if __name__ == '__main__':
    print('''
    This file is used to define a set of MxRyDev devloped
    custom tools for use with pygame.
    
    It includes (or will soon include):
    - Event handling (Event_exe and Conductor classes)
    - finding game rotation
    
    
    
    
    This ".
    on its own, it provides no functionality.
    
    HAFF A GUD DAY
    ''')



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::: FIND INGAME ROTATION :::::::::::::::::::::::#
'''
FUNCTION:
Finds the rotation between two points.
The first point is the 'orgin' ie: the center of your player
360 degrees is on the left, decreasing as you move clockwise.
 
'''

def find_rotation(data1, data2, data3 = '', data4 = ''):
    if data3 == '' and type(data1) == tuple:
        x1,y1 = data1
        x2,y2 = data2
        # assuming function was passed two tuples as points
    else: x1,y1,x2,y2 = data1, data2, data3, data4
    
    
    adj = x1 - x2
    hyp = sqrt( pow(adj,2) + pow(   (y1 - y2)   ,2))
    
    if adj == 0:
        adj += .00000000001
        print('fixed divide by zero issue')
    if hyp == 0:
        hyp += .00000000001
        print('fixed divide by zero issue')
    raw_angle = degrees(acos(adj/hyp)) # 'raw_angle' does not account for quadrant
    
    # adjust for cursor being below x-axis of player's orgin
    if y1 > y2:
        angle = (180 - raw_angle) + 180
    else:
        angle = raw_angle    
    return(angle)

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::: EVENT HANDLING (2 classes) :::::::::::::::::::#
def ignore():
    pass


# EVENT_EXE class
'''
Each object needs to be passed a pygame event and 
two fucntions or "actions" upon creation.
The first will occur when the pygame event is a KEYDOWN
and the second will respond to KEYUP.

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

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::