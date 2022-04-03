import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups) #initialises the parent class passing the groups variable into it
        #self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()

        self.sprite_type = sprite_type
        self.image = surface

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)