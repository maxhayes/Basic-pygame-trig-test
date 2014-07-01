# Defines the player class to be imported into pong/MAIN

if __name__ == '__main__':
    print('''
    This file is used to define the PLAYER class for TRIG TEST.
    it is to be used within "localpong_main.py".
    on its own, it provides no functionality.
    
    HAFF A GUD DAY
    ''')
    
import pygame
from math import cos, acos, degrees, pow, sqrt
from fractions import Fraction
from modules.constants import *


# PLAYER CLASS:
class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, start_x = 0, start_y = 0, 
                 player_speed = [PLAYER_SPEED_a, PLAYER_SPEED_b], 
                 walking_speed = WALKING_SPEED,
                 recoil_speed = RECOIL_SPEED):
        
        self.frame = 0
        # inherited class init
        pygame.sprite.Sprite.__init__(self)
        
        # setup image
        self.image = image
        self.orig_image = image
        self.rect = self.image.get_rect()    
        self.radius = 50
        
        # setup pos/speed
        self.rect.x = start_x
        self.rect.y = start_y
        self.pos_x = start_x
        self.pos_y = start_y
        
        self.walk_speed = walking_speed
        self.recoil_speed = recoil_speed
        self.speeda = player_speed[0]
        self.speedb = player_speed[1]
        self.changex, self.changey = 0,0
        
        self.moving = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.player_fired = False
        self.laser_state = False
        
    
        # add object to lists
        #all_sprites_list.add(self)
        player_list.add(self)
        
    # --- define class methods --- #
    

    # heavy methods
    
    def choose_feet_frame(self):
        
        self.feet_image = walking_frames[0]
        
        if self.changex == 0 and self.changey == 0:
            self.walk_start_frame = self.frame
            
        else:
            # player moving, animate
            self.moving = True

            # select frame
            step = (self.frame - self.walk_start_frame)//self.walk_speed
            if step >= len(walking_frames):
                self.walk_start_frame = self.frame
                step = 0
            self.feet_image = walking_frames[step]
        
            
    def choose_body_frame(self, current_Frame = FRAME):
        if not self.player_fired:
            self.recoil_start_frame = self.frame
            self.image = self.orig_image
        if self.player_fired:
            # player firing (remember this does not loop)
            step = (self.frame - self.recoil_start_frame)//self.recoil_speed
            if step >= len(recoil_frames):
                self.player_fired = False
                self.image = self.orig_image
            else:
                self.image = recoil_frames[step]
        
        
    
    def rotate(self):
        
        # -- calculate angle between player/mouse line and x = 0 --
        # -- using Cos(A) = adj/hyp
        
        # get mouse coord
        (Mcoord) = pygame.mouse.get_pos()
        Mx, My = Mcoord[0], Mcoord[1]
        
        # get player coord:
        (Pcoord) = self.rect.center
        Px, Py = Pcoord[0], Pcoord[1]
        
        
        # find angle with cos(x) = adj/hyp
        adj = Px - Mx
        hyp = sqrt( pow(adj,2) + pow(   (Py - My)   ,2))
        
        if adj == 0:
            adj += .00000000001
            print('fixed divide by zero issue')
        if hyp == 0:
            hyp += .00000000001
            print('fixed divide by zero issue')
        raw_angle = degrees(acos(adj/hyp)) # 'raw_angle' does not account for quadrant
        
        # adjust for cursor being below x-axis of player's orgin
        if Py > My:
            self.angle = (180 - raw_angle) + 180
        else:
            self.angle = raw_angle
        
        # get center:
        self.pos_x, self.pos_y = self.rect.center
        
        
        # rotate image
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.moving:
            self.feet_image = pygame.transform.rotate(self.feet_image, self.angle)
        
        # correct rotation jitter by explicetly setting center
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        
        # see if rotation collided with anything:
        player_hit_block = pygame.sprite.spritecollide(self, block_list, False)
    
        
    
    
    def draw_laser(self):
        Mx, My = pygame.mouse.get_pos()
        Px, Py = self.rect.center

        # create the "laser" endpoint further and further until it 'hits' something
        Lx, Ly, = Mx, My
        delta_x = Mx - Px
        delta_y = My - Py
        
        # corrects for some sort of uncaught 'divide by zero' error
        if delta_x == 0: 
            delta_x += .00000000001
    
        if delta_y == 0: 
            delta_y += .00000000001
        
        while True:
            # all_sprite_list collision detection will be here to stop laser @ objects
            
            
            # if laser is still ending on screen
            Lx += delta_x
            Ly += delta_y
            
            if Lx in range(0,res_x):
                pass
            elif Ly in range(0, res_y):
                pass
            else:
                break
            

            
        pygame.draw.aaline(screen, (GREEN), [Px, Py], [(Lx), (Ly)], True)
        
        
        
        
    # light methods
    
    def moveup(self):
        self.changey -= self.speeda 
        self.moving_up = True
    def movedown(self):
        self.changey += self.speedb  
        self.moving_down = True
    def moveleft(self):
        self.changex -= self.speeda
        self.moving_left = True
    def moveright(self):
        self.changex += self.speedb
        self.moving_right = True
        
    def stopup(self):
        self.changey += self.speeda
        self.moving_up = False
    def stopdown(self):
        self.changey -= self.speedb
        self.moving_down = False
    def stopleft(self):
        self.changex +=self.speeda
        self.mobing_left = False
    def stopright(self):
        self.changex -= self.speedb
        self.moving_right = False
        
    def laser_on(self):
        self.laser_state = True
        laser_on.play()
    def laser_off(self):
        self.laser_state = False
        laser_off.play()
    def laser_toggle(self):
        if self.laser_state:
            self.laser_off()
        else:
            self.laser_on()
        
        
    def fire(self):
        gunshot_silenced.play()
        self.player_fired = True
        
    def move(self):      
        
        
        self.frame += 1
        self.choose_feet_frame()
        self.choose_body_frame()
        self.rotate()
        
                
        
        # move up/down and collide check:
        self.rect.x += self.changex
        self.rect.y += self.changey
        
        player_hit_block = pygame.sprite.spritecollide(self, block_list, False)
        for block in player_hit_block:
            # make the smallest change possible to get player out of the wall
            delta_left = block.rect.right - self.rect.left
            delta_right = self.rect.right - block.rect.left
            delta_top = block.rect.bottom - self.rect.top
            delta_bottom = self.rect.bottom - block.rect.top
            
            # add all deltas to a list:
            deltas = [delta_left, delta_right, delta_top, delta_bottom]
            print(deltas)
            print('%s: %s\n\n' % (deltas.index(min(deltas)), min(deltas)))
            
            if   deltas.index(min(deltas)) == 0: self.rect.x += min(deltas)
            elif deltas.index(min(deltas)) == 1: self.rect.x -= min(deltas)
            elif deltas.index(min(deltas)) == 2: self.rect.y += min(deltas)
            elif deltas.index(min(deltas)) == 3: self.rect.y -= min(deltas)

            

        
        
    def update(self):
        
        self.move()
        if self.moving:
            screen.blit(self.feet_image, (self.rect.x, self.rect.y))
        if self.laser_state:
            self.draw_laser()
            
        # make hitbox visible for collision debug.
        self.hit_box = pygame.Surface([self.rect.width, self.rect.height])
        self.hit_box.fill([0,125,125,5])
        screen.blit(self.hit_box, (self.rect.x, self.rect.y))
    
        # draw player body
        screen.blit(self.image, (self.rect.x, self.rect.y))
        

    
        
    