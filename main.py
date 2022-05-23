from turtle import screensize
import pygame,sys
from support import *
from settings import * #the star makes it to import everything from settings
from debug import debug
from level import Level
from ui import UI

class Game:
    def __init__(self):
        
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Drakcelsior")

        #ui
        self.ui = UI(self.screen)


        self.coins = 0
        self.level = Level(self.change_coins)

    def change_coins(self, amount):
        self.coins += amount



    def run(self):
        while True:
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