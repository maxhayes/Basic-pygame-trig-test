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
from mxrydevtools import find_rotation, vector_collide


# PLAYER CLASS:
class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, start_x = 0, start_y = 0,
                 clip_size = 11,
                 ammo_count = 150):
        
        # inherited class init
        pygame.sprite.Sprite.__init__(self)        
        # setup image
        self.image = image
        self.orig_image = image
        self.rect = self.image.get_rect()
        self.hit_width = 120
        self.hit_height = 110
        self.hit_box = pygame.rect.Rect(0,0, self.hit_width, self.hit_height)
        self.hit_box.center = [start_x, start_y]
        # setup pos/speeds/variables
        
        self.clip_size = clip_size
        self.ammo_count = ammo_count
        self.current_clip = self.clip_size
        
        self.rect.x = start_x
        self.rect.y = start_y   
        self.speed = PLAYER_SPEED
        self.changex, self.changey = 0,0
        
        self.moving = False
        self.player_fired = False
        self.player_reloading = False
        self.started_reload = False
        self.laser_state = False
        self.pre_reload_laser = False
        
    
        # add object to lists
        player_list.add(self)
        
     
    # --- define class methods --- #   
    
    # increase fram counte each time its called, chooses framse from animations,
    # rotates them, moves them, and checks for collisions
    def move(self):      
        # see if player is moving
        if self.changex == 0 and self.changey == 0:
            self.moving = False
        else:
            self.moving = True 
        self.feet_image = walking_animation.frame_update(self.moving)
        self.recoil_image = recoil_animation.frame_update(self.player_fired, loop = False)
        if not self.recoil_image:
            self.player_fired = False        
        self.reload_image = reload_animation.frame_update(self.player_reloading, loop = False)
        
        if not self.reload_image:
            self.player_reloading = False
            self.laser_state = self.pre_reload_laser
            if self.started_reload:
                if self.ammo_count > self.clip_size:
                    self.current_clip = self.clip_size
                    self.ammo_count -= self.clip_size
                else: 
                    self.current_clip = self.ammo_count
                    self.ammo_count = 0
                self.started_reload = False
        else: 
            self.laser_state = False
            self.started_reload = True
            
        # decide which body image to use:
        if self.recoil_image: self.image = self.recoil_image
        if self.reload_image: self.image = self.reload_image
        if not self.recoil_image and not self.reload_image:
            self.image = self.orig_image
            
        self.rotate()
        self.move_collide_rect()
#

    
    # draws body, feet, and laser to screen after logic is finished
    def update(self):
        # make hitbox visible for collision debug.
        self.hit_box_vis = pygame.Surface([self.hit_box.width, self.hit_box.height])
        self.hit_box_vis.fill([0,125,125,5])
        
        
        self.move()
        if self.feet_image:
            screen.blit(self.feet_image, (self.rect.x, self.rect.y))
        if self.laser_state:
            self.draw_laser()
        # draw player body
        screen.blit(self.image, (self.rect.x, self.rect.y))   
        # draw score:
        self.ammo_readout = font.render("Ammo: %s/%s" % (self.current_clip, self.ammo_count), 0, GREEN)
        self.hud_rect = self.ammo_readout.get_rect()
        screen.blit(self.ammo_readout, (res_x - self.hud_rect.width,
                                        res_y - self.hud_rect.height))
#

    # rotates images from fram-choosing functions based on player/mouse pos
    def rotate(self):
        # find angle with MxRyDevtool
        self.angle = find_rotation(self.rect.center, pygame.mouse.get_pos())
        # get center:
        self.pos_x, self.pos_y = self.rect.center
        # rotate images
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.feet_image:
            self.feet_image = pygame.transform.rotate(self.feet_image, self.angle)
        # reset orig center
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.hit_box.center = self.rect.center
        # rotate hit box if thresholds are passed
        
        bounds = [26,136,205,325]
        if round(self.angle) in range (bounds[0],bounds[1]) or round(self.angle) in range(bounds[2],bounds[3]):
            self.hit_box.height = self.hit_width
            self.hit_box.width = self.hit_height
        else:
            self.hit_box.height = self.hit_height
            self.hit_box.width = self.hit_width           
#  
    
    # draws the laser (figures out how long to make the line)
    def draw_laser(self):
        Mx, My = pygame.mouse.get_pos()
        Px, Py = self.rect.center
        # create the "laser" endpoint further and further until it 'hits' something
        Lx, Ly, = Mx, My
        slope_x = (Mx - Px)
        slope_y = (My - Py)
        if slope_x == 0: slope_x += .00000000001
        if slope_y == 0: slope_y += .00000000001 
        sign_x = slope_x/abs(slope_x)
        sign_y = slope_y/abs(slope_y)
        delta_x = (slope_x/slope_y)*sign_y
        delta_y = (slope_y/slope_x)*sign_x      
        if abs(delta_x) > abs(delta_y):
            delta_y = sign_y    
        else:
            delta_x = sign_x
        # extend laser until it is off the screen
        while True:
            #extend laser
            last_lx = Lx
            last_ly = Ly
            Lx += delta_x*50
            Ly += delta_y*50
            # see if laser has moved off screen
            if Lx in range(0,res_x):
                pass
            elif Ly in range(0, res_y):
                pass
            else:
                break 
        # draw the laser
        pygame.draw.aaline(screen, (GREEN), [Px, Py], [(Lx), (Ly)], True)        
# 

    # updates player and hitbox position
    def move_collide_rect(self):
        # move up/down and collide check:
        self.rect.x += self.changex
        self.rect.y += self.changey
        self.hit_box.center = self.rect.center
        
        for block in block_list:
            if self.hit_box.colliderect(block.rect):
                # make the smallest change possible to get player out of the wall
                delta_left = block.rect.right - self.hit_box.left
                delta_right = self.hit_box.right - block.rect.left
                delta_top = block.rect.bottom - self.hit_box.top
                delta_bottom = self.hit_box.bottom - block.rect.top
                
                # add all deltas to a list:
                deltas = [delta_left, delta_right, delta_top, delta_bottom]
                
                if   deltas.index(min(deltas)) == 0: self.rect.x += min(deltas)
                elif deltas.index(min(deltas)) == 1: self.rect.x -= min(deltas)
                elif deltas.index(min(deltas)) == 2: self.rect.y += min(deltas)
                elif deltas.index(min(deltas)) == 3: self.rect.y -= min(deltas)
    # 
    
    # movement/keybinding methods:
    def fire(self):
        if self.current_clip:
            if not self.player_reloading:
                gunshot_silenced.play()
                self.player_fired = True  # starts animation
                # see if 'bullet' hits a block
                bullet_hits = vector_collide(self.rect.center, self.angle, block_list)
                if bullet_hits:
                    for block in bullet_hits:
                        block.kill()
                self.current_clip -= 1
        else:
            empty_clip.play()

            
    def moveup(self):
        self.changey -= self.speed
    def movedown(self):
        self.changey += self.speed
    def moveleft(self):
        self.changex -= self.speed
    def moveright(self):
        self.changex += self.speed
    def stopup(self):
        self.changey += self.speed
    def stopdown(self):
        self.changey -= self.speed
    def stopleft(self):
        self.changex +=self.speed
    def stopright(self):
        self.changex -= self.speed
        
    def laser_on(self):
        if not self.player_reloading:
            self.laser_state = True
            self.pre_reload_laser = self.laser_state
            laser_on.play()
    def laser_off(self):
        if not self.player_reloading:
            self.laser_state = False
            self.pre_reload_laser = self.laser_state
            laser_off.play()
    def laser_toggle(self):
        if not self.player_reloading:
            if self.laser_state:
                self.laser_off()
            else:
                self.laser_on()
                self.pre_reload_laser = self.laser_state
        
    def reload(self):
        if self.ammo_count != 0:
            if not self.player_reloading:
                reload_sound.play()
                self.player_reloading = True
                self.laser_state = False
                
        else:
            empty_clip.play()
    