# Defines the player class to be imported into pong/MAIN

if __name__ == '__main__':
    print('''
    This file is used to define the PLAYER class for TRIG TEST.
    it is to be used within "localpong_main.py".
    on its own, it provides no functionality.
    
    HAFF A GUD DAY
    ''')
    
import pygame
from math import acos, degrees, pow, sqrt
from constants import *



# PLAYER CLASS:
class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, start_x = 0, start_y = 0, player_speed = PLAYER_SPEED):
        
        # inherited class init
        pygame.sprite.Sprite.__init__(self)
        
        # init this class
       
        # setup image
        self.image = image
        self.orig_image = image
        self.rect = self.image.get_rect()
        
        # setup pos/speed
        self.rect.x = start_x
        self.rect.y = start_y
        self.pos_x = start_x
        self.pos_y = start_y
        
        self.speed = player_speed
        self.changex, self.changey = 0,0
    
        # add object to lists
        all_sprites_list.add(self)
        player_list.add(self)
        
    # --- define class methods --- #
    
    # light methods
    
    def moveup(self):
        self.changey -= self.speed
    def movedown(self):
        self.changey += self.speed
    def moveleft(self):
        self.changex -=self.speed    
    def moveright(self):
        self.changex += self.speed
        
    def move(self):
        self.rotate()
        self.rect.x += self.changex
        self.rect.y += self.changey  
        
        
    # heavy methods
    
    def rotate(self):
        
        # -- calculate angle between player/mouse line and x = 0 --
        # -- using Cos(A) = adj/hyp
        
        # get mouse coord
        (Mcoord) = pygame.mouse.get_pos()
        Mx, My = Mcoord[0], Mcoord[1]
        
        # get player coord:
        (Pcoord) = self.rect.center
        Px, Py = Pcoord[0], Pcoord[1]
        
        # find angle with c(x) = adj/hyp
        adj = Px - Mx
        hyp = sqrt( pow(adj,2) + pow(   (Py - My)   ,2))
        raw_angle = degrees(acos(adj/hyp)) # 'raw_angle' does not account for quadrant
        
        # adjust for cursor being below x-axis of player's orgin
        if Py > My:
            angle = (180 - raw_angle) + 180
        else:
            angle = raw_angle
        print(angle)
        
        # get center:
        self.pos_x, self.pos_y = self.rect.center
        
        # rotate image
        self.image = pygame.transform.rotate(self.orig_image, angle)
        
        # correct rotation jitter
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        

        
    
    