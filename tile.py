import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups) #initialises the parent class passing the groups variable into it
        #self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self._pos = pos
        self.sprite_type = sprite_type
        self.image = surface
        #in case when an object is bigger than a tilesize, move it a bit further up so it doesn't overlap with other things on the map
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        if sprite_type == "collectibles":
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))

    def get_pos(self):
        return self._pos

            
