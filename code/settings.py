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
    'fireball': {'cooldown': 100, 'damage': 1, 'graphic':'../graphics/weapons/fireball/full.png'}
}

# enemy 
monster_data = {
    'orc': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'speed': 5, 'resistance': 3, 'attack_radius': 80, 'notice_radius' : 360}
}