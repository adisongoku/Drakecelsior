import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from ui import UI

class Level:
    def __init__(self, change_coins):
        #get the sicplay surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #replacing default pygame sprite group with our custom one, to create a functional camera
        self.obstacles_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        
        #sprite setup
        self.create_map()

        #ui
        self.ui = UI(self.display_surface)
        self.change_coins = change_coins
   

    def create_map(self):

        level_1 = {
                "boundary" : import_csv_layout("../map/level_1_boundaries.csv"),
                "clutter": import_csv_layout("../map/level_1_clutter.csv"),
                "objects": import_csv_layout("../map/level_1_objects.csv"),
                "collectibles": import_csv_layout("../map/level_1_collectibles.csv"),
                "walls": import_csv_layout("../map/level_1_walls.csv")
        }

        graphics = {
                "clutter": import_folder("../graphics/clutter"),
                "objects": import_folder("../graphics/objects"),
                "collectibles": import_folder("../graphics/collectibles"),
                "walls": import_folder("../graphics/walls")
        }

        

        for style,layout in level_1.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x,y),[self.obstacles_sprites], "boundary", surface = pygame.Surface((TILESIZE,TILESIZE)))
                        if style == "clutter":
                            random_clutter_image = choice(graphics["clutter"])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"clutter",random_clutter_image) #creates an instance of Tile class passing the position and list with sprites 
                        if style == "objects":
                            surf = graphics["objects"][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"objects",surf)
                        if style == "walls":
                            surf = graphics["walls"][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],"walls",surf)
                        if style == "collectibles":
                            surf = graphics["collectibles"][int(col)]
                            Tile((x,y),[self.visible_sprites, self.collectible_sprites],"collectibles",surf)

        self.player = Player((60,1130),[self.visible_sprites],self.obstacles_sprites)
        
    def check_coin_collisons(self):
        collided_coins = pygame.sprite.spritecollide(self.player, self.collectible_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.check_coin_collisons()
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
        self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
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