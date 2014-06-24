# pygame test to make player rotate to folow a mouse cursor


# import 3rd party libraries:
import pygame
from pygame.locals import *
import math

# import custom libraries:
from player_class import *

# init pygame stuff:
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_captopn('Cursor trace trig test')

# create game objects:
player = Player()

# screen stuff:
