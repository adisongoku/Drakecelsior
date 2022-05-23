import pygame
from settings import BAR_HEIGHT, ENERGY_BAR_WIDTH, ENERGY_COLOR, HEALTH_BAR_WIDTH, HEALTH_COLOR, UI_BG_COLOR, UI_BORDER_COLOR, UI_FONT, UI_FONT_SIZE
from support import *

class UI:
    def __init__(self, surface):

        # setup 
        self.display_surface = surface
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 20, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 44, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        #coins
        self.coin = pygame.image.load('../graphics/collectibles/1.png')
        self.coin_rect = self.coin.get_rect(topleft = (50, 161))
        self.font = pygame.font.Font('../graphics/ui/Minecraft.ttf', 30)
    #kdjasgdkja
    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width


        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        

    
    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        




    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, '#FFC42A')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)