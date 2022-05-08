import pygame.display

#game setup
pygame.init()
info_obj = pygame.display.Info()
WIDTH = info_obj.current_w
HEIGHT = info_obj.current_h
# WIDTH = 800
# HEIGHT = 600
FPS = 60
TILESIZE = 128

weapon_data = {
    'fireball': {'cooldown': 100, 'damage': 15, 'graphic':'../graphics/weapons/fireball/full.png'}
}