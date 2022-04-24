import pygame
from support import *

class UI:
    def __init__(self, surface):

        # setup 
        self.display_surface = surface

        #coins
        self.coin = pygame.image.load('../graphics/collectibles/1.png')
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        self.font = pygame.font.Font('../graphics/ui/Minecraft.ttf', 30)



    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, '#FFC42A')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)