import pygame
from modules.constants import *
from random import randint



class Block(pygame.sprite.Sprite):
    def __init__(self, color, posx, posy, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        # internalize vars:
        self.color = color
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        
        
        # draw the surface
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        
        # position the surface
        self.rect.x, self.rect.y = self.posx, self.posy
        
        # add to lists:
        all_sprites_list.add(self)
        block_list.add(self)
        
    def move(self):
        pass
    
    def kill(self):
        all_sprites_list.remove(self)
        block_list.remove(self)
        block = Block(BLUE, randint(0,res_x-10), randint(0,res_y-10), 60,60)