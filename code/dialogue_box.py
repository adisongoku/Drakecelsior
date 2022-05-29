import pygame
from support import *
from settings import *


#WORK IN PROGRESS

class DIALOGUE_BOX:
    def __init__(self, surface):
        self.display_surface = surface
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.dialogue_box_rect = pygame.Rect(500,500,DIALOGUE_BOX_WIDTH,DIALOGUE_BOX_HEIGHT) 



    def draw_dialogue(self, image, text):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.dialogue_box_rect)
        self.font.render(text, False, '#FFC42A')