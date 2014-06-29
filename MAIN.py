#`````````````````````````````````````````````````````````````````````````````````#
# _____________________________----- SETUP -----_________________________________ #

# IMPORTS:
import pygame, math
from pygame.locals import *
from constants import *
from player_class import *
from event_handling import *

import pygame.mixer
pygame.mixer.pre_init(48000, -16, 1, 512)
pygame.mixer.init()

# create game objects:
player = Player(player_image, res_x/2, res_y/2)

# create event/actions & conductor using event_handling
exes = []

p1_up = Event_exe(K_w, player.moveup, player.stopup, exes)
p1_down = Event_exe(K_s, player.movedown, player.stopdown, exes)
p1_left = Event_exe(K_a, player.moveleft, player.stopleft, exes)
p1_right = Event_exe(K_d, player.moveright, player.stopright, exes)
p1_fire = Event_exe('LMB', player.fire, ignore, exes)
p1_laseron = Event_exe('RMB', player.laser_on, player.laser_off, exes)

conductor = Event_conductor(exes)



#`````````````````````````````````````````````````````````````````````````````````#
# _________________________----- Main Loop -----_________________________________ #
while True:
    
    # handle events
    conductor.handle_events(pygame.event.get(), pygame.mouse.get_pressed())
    
    # move/update objects
    for object in all_sprites_list:
        object.move()
        
    all_sprites_list.update()
            
    # --- drawing ---
    
    # draw background
    screen.blit(background, (0,0))
    box = pygame.Rect(122, 122, 250,250)
    pygame.draw.rect(screen, BLUE, box, 0) # creates box to play with transparency

    # draw objects
    Mx, My = pygame.mouse.get_pos()
    screen.blit(crosshair, (Mx - cursor_size[0]/2, My - cursor_size[1]/2))
    player.draw()
    all_sprites_list.draw(screen)
    
    # update screen
    pygame.display.flip()
    # limit fps
    clock.tick(60)
    FRAME += 1