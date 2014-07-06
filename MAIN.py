#`````````````````````````````````````````````````````````````````````````````````#
# _____________________________----- SETUP -----_________________________________ #

# IMPORTS:
import pygame, math
from pygame.locals import *
from random import randint
from modules.constants import *
from modules.player_class import *
from modules.block_class import *
from mxrydevtools import *



# create game objects:
player = Player(player_image, res_x/2, res_y/2)
for i in range(20):
    block = Block(WHITE, randint(0,res_x-10), randint(0,res_y-10), 60,60)

# create event/actions & conductor using event_handling
exes = []

p1_up = Event_exe(K_w, player.moveup, player.stopup, exes)
p1_down = Event_exe(K_s, player.movedown, player.stopdown, exes)
p1_left = Event_exe(K_a, player.moveleft, player.stopleft, exes)
p1_right = Event_exe(K_d, player.moveright, player.stopright, exes)
p1_fire = Event_exe('LMB', player.fire, ignore, exes)
p1_laseron = Event_exe('RMB', player.laser_on, player.laser_off, exes)
p1_lasertog = Event_exe(K_t, player.laser_toggle, ignore, exes)
p1_reload = Event_exe(K_r, player.reload, ignore, exes)

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
   
    # draw objects
    all_sprites_list.draw(screen)
    Mx, My = pygame.mouse.get_pos()
    screen.blit(crosshair, (Mx - cursor_size[0]/2, My - cursor_size[1]/2))
    player.update()
    
    
    # update screen
    pygame.display.flip()
    # limit fps
    clock.tick(60)
    FRAME += 1