import pygame
import mxrydevtools

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (44,179,44)
BLUE = (0,0,255)

# init pygame stuff:
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 90)

FRAME = 0 # used in main loop to see how many frames have passed

# display init stuff
display_info = pygame.display.Info()
res_x, res_y = display_info.current_w, display_info.current_h
res_x -= 100
res_y -= 100
screen = pygame.display.set_mode([(res_x), (res_y)])
pygame.mouse.set_visible(False)


background = pygame.Surface(screen.get_size())
background.convert()
background.fill((50,50,50))


# game experience constants

PLAYER_SPEED = 4
WALKING_DURATION = 9
RECOIL_DURATION = 1
RELOAD_DURATION = 5



# lists
all_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()

# sizes

# :::::::::: IMAGES :::::::::::::::::::
player_image = pygame.image.load("images\Swat_player.png").convert()
player_image.set_colorkey(WHITE)
#player_image.set_alpha(100)

crosshair = pygame.image.load("images\crosshair.png").convert()
crosshair.set_colorkey(WHITE)
crosshair.set_alpha(150) # makes it see through
cursor_size = crosshair.get_size()

# sprite sheet walking animation:
p_walking_ani = pygame.image.load("images/ani_feet_walking_sheet.png").convert()
p_walking_ani.set_colorkey(WHITE)
walking_animation = mxrydevtools.Animation(p_walking_ani, 8, WALKING_DURATION)

# sprite sheet recoil animation:
p_recoil_ani = pygame.image.load("images/ani_body_recoil.png").convert()
p_recoil_ani.set_colorkey(WHITE)
recoil_animation = mxrydevtools.Animation(p_recoil_ani, 7, RECOIL_DURATION) 

# sprite sheet reload animation
p_reload_ani = pygame.image.load("images/ani_reload_sheet.png").convert()
p_reload_ani.set_colorkey(WHITE)
reload_animation = mxrydevtools.Animation(p_reload_ani, 12, RELOAD_DURATION,
                                          columns=3, rows=4)
    
# :::::::::::::::::: SOUNDS ::::::::::::::::::::::::::
gunshot_silenced = pygame.mixer.Sound('sound_fx\silenced_gunshot.wav')
laser_on = pygame.mixer.Sound('sound_fx\laser_toggle_on.wav')
laser_off = pygame.mixer.Sound('sound_fx\laser_toggle_off.wav')









if __name__ == '__main__':
    print('finished script')
    
    