#`````````````````````````````````````````````````````````````````````````````````#
# _____________________________----- SETUP -----_________________________________ #

# IMPORTS:
import pygame, math
from pygame.locals import *
from constants import *
from player_class import *
from event_handling import *


# create game objects:
player = Player(player_image, res_x/2, res_y/2)

# create event/actions & conductor using event_handling
exes = []

p1_up = Event_exe(K_w, player.moveup, player.movedown, exes)
p1_down = Event_exe(K_s, player.movedown, player.moveup, exes)
p1_left = Event_exe(K_a, player.moveleft, player.moveright, exes)
p1_right = Event_exe(K_d, player.moveright, player.moveleft, exes)

conductor = Event_conductor(exes)

#`````````````````````````````````````````````````````````````````````````````````#
# _________________________----- Main Loop -----_________________________________ #
while True:
    
    # handle events
    conductor.handle_events(pygame.event.get())
    
    # move/update objects
    for object in all_sprites_list:
        object.move()
        
    all_sprites_list.update()
    
    
    # draw objects
    screen.blit(background, (0,0))
    all_sprites_list.draw(screen)
    
    # update screen
    pygame.display.flip()
    # limit fps
    clock.tick(60)