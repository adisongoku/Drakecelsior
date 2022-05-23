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

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80

# general colors 
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
UI_FONT = '../graphics/ui/Minecraft.ttf'
UI_FONT_SIZE = 18

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'


weapon_data = {
    'fireball': {'cooldown': 100, 'damage': 15, 'graphic':'../graphics/weapons/fireball/full.png'}
}

# enemy 
monster_data = {
    'orc': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'speed': 5, 'resistance': 3, 'attack_radius': 80, 'notice_radius' : 360}
}