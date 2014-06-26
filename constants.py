import pygame

# init pygame stuff:
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 90)

# display init stuff
display_info = pygame.display.Info()
res_x, res_y = display_info.current_w, display_info.current_h
res_x -= 100
res_y -= 100
screen = pygame.display.set_mode([(res_x), (res_y)])
print("Current Resolution: %sx%s" % (res_x, res_y))


background = pygame.Surface(screen.get_size())
background.convert()
background.fill((0,0,0))


# game experience constants

PLAYER_SPEED = 3.5

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (44,179,44)
BLUE = (0,0,255)

# lists
all_sprites_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

# sizes

# images
player_image = pygame.image.load("player.png").convert()
player_image.set_colorkey(WHITE)
