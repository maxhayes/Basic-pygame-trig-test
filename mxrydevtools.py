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
    
    
   
    This, on its own, it provides no functionality.
    
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
        x1,y1 = data1[0], data1[1]
        x2,y2 = data2[0], data2[1]
        # assuming function was passed two tuples as points
    else: x1,y1,x2,y2 = data1, data2, data3, data4
    adj = x1 - x2
    hyp = sqrt( pow(adj,2) + pow(   (y1 - y2)   ,2))
    
    if adj == 0:
        adj += .00000000001
    if hyp == 0:
        hyp += .00000000001
    raw_angle = degrees(acos(adj/hyp)) # 'raw_angle' does not account for quadrant
    
    # adjust for cursor being below x-axis of player's orgin
    if y1 > y2:
        angle = (180 - raw_angle) + 180
    else:
        angle = raw_angle    
    return(angle)



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::: VECTOR/ANBLE COLLISION TEST  :::::::::::::::::::#
'''
Function is given a projectile orgin point and game angle, as
well as a list of pygame.rect objects to check collision for.

It takes the projectile vector angle, and finds the angle
between the orgin point all four corers of the rect, then
checks to see if the projectile angle is in the range of 
the angles between origin point and the four .rect points

Function returns a sub list of objects that "were hit".
If no objects were hit, function returns flase.

*Hopefully these calcualtions won't be too slow.

'''

def vector_collide(orgin_pos, orgin_angle, object_list):
    orgin_angle = round(orgin_angle)
    for object in object_list:
        object_angles = []
        hit_objects = []
        corners = [object.rect.topleft, 
                   object.rect.topright, 
                   object.rect.bottomleft, 
                   object.rect.bottomright]
        for point in corners:
            object_angles.append(round(find_rotation(orgin_pos, point)))
        #print('%s, %s, %s' % (orgin_angle, min(object_angles), max(object_angles)))
        if orgin_angle in range(min(object_angles), max(object_angles)):
            hit_objects.append(object)
        elif min(object_angles) < 90 and max(object_angles) > 270:
            if not orgin_angle in range(min(object_angles), max(object_angles)):
                hit_objects.append(object)
    
    #print(hit_objects)        
    return(hit_objects)
    


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::::::::::: EVENT HANDLING (2 classes) :::::::::::::::::::#

# EVENT_EXE class
'''
Each object needs to be passed a pygame event and 
two fucntions or "actions" upon creation.
The first will occur when the pygame event is a KEYDOWN
and the second will respond to KEYUP.

'''

def ignore():
    pass

class Event_exe():
    def __init__(self, event, press_action = '', release_action = '', actions_list = ''):
        self.event = event
        self.press_action = press_action
        self.release_action = release_action
        actions_list.append(self) 
    def pressed(self):
        if self.press_action != '': self.press_action()     
    def released(self):
        if self.release_action != '': self.release_action()
        
    
    
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
                
                
                # the event is QUIT:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # the event is keyup or keydown...
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
        
        
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::: create animation object  :::::::::::::::::#

class Animation():
    
    def __init__(self, image, num_frames, duration, rows = None, columns = None):
        
        # init variables
        self.frame = 0
        self.image = image
        self.num_frames = num_frames
        self.duration = duration
        self.start_frame = self.frame
        
        frame_list = []
        sheet_size = self.image.get_rect()
        
        # create frames_list
        if not rows and not columns: # assume one vertical line of sprites
            for i in range(self.num_frames):
                size = [sheet_size.width, sheet_size.height/self.num_frames]
                pos = [0, (size[1] * (i))]
                frame_list.append(image.subsurface(pos, size))
            self.frame_list = frame_list
        
        else:
            size = [sheet_size.width/columns, sheet_size.height/rows]
            #print(sheet_size.width)
            #print(sheet_size.height)
            #print('')
            current_row = 0
            current_column = 0
            
            for i in range(self.num_frames):
                pos = [size[0]*current_column , size[1]*current_row]
                #print("%s: %s" % (i+1, pos))
                frame_list.append(image.subsurface(pos, size))
                current_column += 1
                if current_column == columns:
                    current_column = 0
                    current_row +=1
            self.frame_list = frame_list
            
    def frame_update(self, run, loop = True,):
        self.loop = loop
        
        if not run:
            self.start_frame = self.frame
        if run:
            self.frame += 1
            step = (self.frame - self.start_frame)//self.duration
            if step >= len(self.frame_list): # if we reached the end
                if not self.loop:
                    return(False)
                
                if self.loop:
                    self.start_frame = self.frame
            else:
                return(self.frame_list[step])
            
            

                            
# TO ADD:
'''
-add support for non-event key down/up events, so things like
Pygame.QUIT work.

-find ways to reduce end-user typing.
    (such as not having to specifiy "actions_list" for each object)
'''

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::