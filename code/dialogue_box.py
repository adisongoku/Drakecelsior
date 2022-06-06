import pygame
from support import *
from settings import *

#WORK IN PROGRESS

class DIALOGUE_BOX:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 3)
    
    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh


    
    def draw_dialogue(self, text, character):
        box_surf = pygame.image.load("../graphics/ui/Drakecelsior_dialogue_box.png").convert_alpha()
        box_rect = box_surf.get_rect(center = (WIDTH/2 + 60,HEIGHT-100))

        if character == "drake":
            face_img = pygame.image.load("../graphics/player/face_img/drake_face.png").convert_alpha()
            face_rect = face_img.get_rect(topright = box_rect.topleft)
        elif character == "cat":
            face_img = pygame.image.load("../graphics/monsters/cat_boss/face_img/cat_boss_face_img.png").convert_alpha()
            face_rect = face_img.get_rect(topright = box_rect.topleft)

        self.display_surface.blit(face_img,face_rect)
        self.display_surface.blit(box_surf,box_rect)
        self.renderTextCenteredAt(text,self.font,"white",box_rect.centerx , box_rect.top + 30,self.display_surface,box_surf.get_width() - 30)

    