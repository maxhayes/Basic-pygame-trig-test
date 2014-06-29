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
from constants import *


# PLAYER CLASS:
class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, start_x = 0, start_y = 0, 
                 player_speed = [PLAYER_SPEED_a, PLAYER_SPEED_b], 
                 walking_speed = WALKING_SPEED):
        
        self.frame = 0
        # inherited class init
        pygame.sprite.Sprite.__init__(self)
        
        # setup image
        self.image = image
        self.orig_image = image
        self.rect = self.image.get_rect()    
        
        # setup pos/speed
        self.rect.x = start_x
        self.rect.y = start_y
        self.pos_x = start_x
        self.pos_y = start_y
        
        self.walk_speed = walking_speed
        self.speeda = player_speed[0]
        self.speedb = player_speed[1]
        self.changex, self.changey = 0,0
        
    
        # add object to lists
        all_sprites_list.add(self)
        player_list.add(self)
        
    # --- define class methods --- #
    
    # light methods
    
    def moveup(self):
        self.changey -= self.speeda
    def movedown(self):
        self.changey += self.speedb
    def moveleft(self):
        self.changex -=self.speeda
    def moveright(self):
        self.changex += self.speedb
        
    def stopup(self):
        self.changey += self.speeda
    def stopdown(self):
        self.changey -= self.speedb
    def stopleft(self):
        self.changex +=self.speeda
    def stopright(self):
        self.changex -= self.speedb
        
    def move(self):
        self.frame += 1
        self.choose_feet_frame()
        self.rotate()
        self.rect.x += self.changex
        self.rect.y += self.changey
        
    def draw(self):
        self.move()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.feet_image, (self.rect.x, self.rect.y))
        self.draw_laser()
        
        
    # heavy methods
    
    def choose_feet_frame(self, current_frame = FRAME):
        
        self.feet_image = self.orig_image
        
        if self.changex == 0 and self.changey == 0:
            self.start_frame = self.frame
            
        else:
            # player moving, animate

            # select frame
            step = (self.frame - self.start_frame)//self.walk_speed
            if step == len(walking_frames):
                self.start_frame = self.frame
                step = 0
            print(step)
            self.feet_image = walking_frames[step]
        
    
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
        #print(angle)
        
        # get center:
        self.pos_x, self.pos_y = self.rect.center
        
        # rotate image
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.feet_image = pygame.transform.rotate(self.feet_image, self.angle)
        
        # correct rotation jitter by explicetly setting center
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        
    
    
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