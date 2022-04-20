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
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        #level information
        self.level_index = 0
        self.player_pos = (193,2363)
        self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
        floor_width = self.floor_surf.get_width() * 2
        floor_height = self.floor_surf.get_height() * 2
        self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))

        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #replacing default pygame sprite group with our custom one, to create a functional camera
        self.obstacles_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.special_sprites = pygame.sprite.Group()
        self.shadow_sprites = YsortCameraShadowGroup()
        
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
                "walls": import_csv_layout("../map/level_1_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_1_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_1_shadows.csv")
        }

        level_2 = {
                "clutter": import_csv_layout("../map/level_2_clutter.csv"),
                "collectibles": import_csv_layout("../map/level_2_collectibles.csv"),
                "walls": import_csv_layout("../map/level_2_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_2_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_2_shadows.csv")
        }

        graphics = {
                "clutter": import_folder("../graphics/clutter"),
                "objects": import_folder("../graphics/objects"),
                "collectibles": import_folder("../graphics/collectibles"),
                "walls": import_folder("../graphics/walls"),
                "shadows": import_folder("../graphics/shadows")
        }

        levels = [level_1,level_2]
        

        for style,layout in levels[self.level_index].items():
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
                        if style == "special_tiles":
                            Tile((x,y),[self.special_sprites],"special",surf)
                        if style == "shadows":
                            surf = graphics["shadows"][int(col) - 1]
                            Tile((x,y),[self.shadow_sprites],"shadows",surf)

        self.player = Player(self.player_pos,[self.visible_sprites],self.obstacles_sprites)

    #empty all sprite groups and refill them with new set of sprites from the other level
    def update_map(self):
        self.special_sprites.empty()
        self.visible_sprites.empty()
        self.shadow_sprites.empty()
        self.collectible_sprites.empty()
        self.obstacles_sprites.empty()
        self.create_map()
        
    def check_coin_collisons(self):
        collided_coins = pygame.sprite.spritecollide(self.player, self.collectible_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)

    #check for a collision with a tile responisble for level transition
    def check_special_collisions(self):
        collided = pygame.sprite.spritecollide(self.player, self.special_sprites, False)
        if(collided):
            if self.level_index == 0:
                self.level_index += 1
                self.player_pos = (1202,2207)
                self.floor_surf = pygame.image.load("../graphics/tilemap/level2_ground.png").convert()
                floor_width = self.floor_surf.get_width() * 2
                floor_height = self.floor_surf.get_height() * 2
                self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
            else:
                self.level_index -= 1
                self.player_pos = (3758,219)
                self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
                floor_width = self.floor_surf.get_width() * 2
                floor_height = self.floor_surf.get_height() * 2
                self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
            self.fade()
            self.update_map()

    def fade(self):
            fade_surf = pygame.Surface((WIDTH,HEIGHT))
            fade_surf.fill((0,0,0))
            for alpha in range (0, 100):
                fade_surf.set_alpha(alpha)
                self.display_surface.blit(fade_surf, (0,0))
                debug(alpha)
                pygame.display.update()
                pygame.time.delay(5)

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player, self.floor_surf, self.floor_rect)
        self.shadow_sprites.shadow_draw(self.player)
        self.check_coin_collisons()
        self.check_special_collisions()
        self.visible_sprites.update()   
        self.shadow_sprites.update() 
        debug(self.player.rect.topleft)
        


class YsortCameraGroup(pygame.sprite.Group): #YSort means that we're sorting sprites by Y coordinate and thanks to that we're going to give them some overlap
    def __init__(self):

        #general setup
        super().__init__()    
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

    def custom_draw(self, player, floor_surf, floor_rect):

        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #offset for floor
        offset_floor_rect = floor_rect.topleft - self.offset
        self.display_surface.blit(floor_surf,offset_floor_rect)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #CENTER Y!
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class YsortCameraShadowGroup(pygame.sprite.Group): 
    def __init__(self):

        super().__init__()    
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() 

    def shadow_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites(): #CENTER Y!
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)