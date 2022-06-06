from turtle import bgcolor, screensize
import pygame,sys
from support import *
from settings import * #the star makes it to import everything from settings
from debug import debug
from level import Level
from ui import UI
from pygame import Surface, mixer

#pygame.mixer.music.load('../audio/game_music.wav')
#pygame.mixer.music.play(-1)

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Drakcelsior")
        self.bgm = pygame.mixer.Sound("../audio/Drakecelsior.mp3")
        self.bgm.play(-1)

        #ui
        self.ui = UI(self.screen)


        self.coins = 0
        self.level = Level(self.change_coins, self.stop_bgm)

    def change_coins(self, amount):
        self.coins += amount
        coin_sound = pygame.mixer.Sound('../audio/coin.wav')
        coin_sound.set_volume(0.1)
        coin_sound.play(0)

    def stop_bgm(self):
        self.bgm.stop()
    

    def run(self):
        pygame.display.set_caption("Menu")
        while True:

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    clean_files() #deletes coin position files
                    pygame.quit()
                    sys.exit()


            self.screen.fill("black")
            self.level.run()
            self.ui.show_coins(self.coins)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()


    #7h one at 2:30:00 weapons
