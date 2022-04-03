import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *

class Level:
    def __init__(self):
        #get the sicplay surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #replacing default pygame sprite group with our custom one, to create a functional camera
        self.obstacles_sprites = pygame.sprite.Group()
        
        #sprite setup
        self.create_map()

    def create_map(self):

        layout = {
                "boundary" : import_csv_layout("../map/map_FloorBlocks_borders.csv")
        }

        for style,layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x,y),[self.obstacles_sprites], "invisible", surface = pygame.Surface((TILESIZE,TILESIZE)))
        #         if col == "x":
        #             Tile((x,y),[self.visible_sprites,self.obstacles_sprites]) #creates an instance of Tile class passing the position and list with sprites 
        #         if col == "p":
        #             self.player = Player((x,y),[self.visible_sprites],self.obstacles_sprites) #here we create a plater and pass to it its position along with putting the player into the list of visible sprites, then we pass the list of obstacle sprites INTO the player class but the player is not into obstacle sprites itslef
        
        self.player = Player((300,500),[self.visible_sprites],self.obstacles_sprites)

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YsortCameraGroup(pygame.sprite.Group): #YSort means that we're sorting sprites by Y coordinate and thanks to that we're going to give them some overlap
    def __init__(self):

        #general setup
        super().__init__()    
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

        #creating the floor
        self.floor_surf = pygame.image.load("../graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #offset for floor
        offset_floor_rect = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,offset_floor_rect)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #CENTER Y!
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)