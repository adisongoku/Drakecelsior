from support import import_folder
import pygame
class CAT:
    def __init__(self):
        self.animations = import_folder('../graphics/monsters/demon_cat')
        self.display_surf = pygame.display.get_surface()
        self.animation_speed = 0.03
        self.frame_index = 0
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def animate_cat(self, player):
        if self.frame_index < 35:
            self.animation_speed = 0.1
        else:
            self.animation_speed = 0.03
        
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

        self.image = self.animations[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3,self.image.get_height()*3))
        self.rect = self.image.get_rect(center = (1916,1200))
        offset_rect = self.rect.topleft - self.offset
        self.display_surf.blit(self.image,offset_rect)
        
