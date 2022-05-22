import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from ui import UI
from weapon import Weapon
import numpy as np
from enemy import *
from os.path import exists


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
        self.collectibles_path = "../map/level_1_collectibles.csv"
        self.coin_arr = []
        
        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #replacing default pygame sprite group with our custom one, to create a functional camera
        self.obstacles_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.special_sprites = pygame.sprite.Group()
        self.shadow_sprites = YsortCameraShadowGroup()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # coin sprites
        self.collided_coins = None

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
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_1_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_1_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_1_shadows.csv"),
                "entities": import_csv_layout("../map/level_1_enemy.csv")
        }

        level_2 = {
                "clutter": import_csv_layout("../map/level_2_clutter.csv"),
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_2_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_2_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_2_shadows.csv")
        }

        level_3 = {
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_3_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_3_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_3_shadows.csv")
        }

        graphics = {
                "clutter": import_folder("../graphics/clutter"),
                "objects": import_folder("../graphics/objects"),
                "collectibles": import_folder("../graphics/collectibles"),
                "walls": import_folder("../graphics/walls"),
                "shadows": import_folder("../graphics/shadows")
        }

        levels = [level_1,level_2,level_3]

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
                        if style == 'entities':
                            Enemy('orc', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player)

        self.player = Player(self.player_pos,[self.visible_sprites],self.obstacles_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


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

                #check for coin pos
                coin_pos = coin.get_pos()
                #establish saving path and check if it already exists if it does, modify positions in already existing file
                save_path = self.collectibles_path
                if "map" in save_path:
                    save_path = save_path.replace("map", "saves")
                if exists(save_path):
                    coin_arr = import_csv_layout(save_path)
                else:
                    coin_arr = import_csv_layout(self.collectibles_path)

                #find coin in the array and delete it from layout
                for row in range(len(coin_arr)):
                   for col in range(len(coin_arr[row])):
                        if coin_arr[row][col] == "0":
                            if row * TILESIZE == coin_pos[1] and col * TILESIZE == coin_pos[0]:
                                coin_arr[row][col] = "-1"

                #export new layout to a different file
                self.coin_arr = np.asarray(coin_arr)
                np.savetxt(save_path, self.coin_arr, fmt='%s',delimiter=",")

    #check for a collision with a tile responisble for level transition
    def check_special_collisions(self):
        collided = pygame.sprite.spritecollide(self.player, self.special_sprites, False)
        if(collided):
            for collided_tile in collided:
                collided_tile_pos = collided_tile.get_pos()
            #transition to level 2
            if collided_tile_pos == (3712,0) or collided_tile_pos == (3840,0):
                self.level_index = 1
                self.player_pos = (1202,2207)
                self.floor_surf = pygame.image.load("../graphics/tilemap/level2_ground.png").convert()
                floor_width = self.floor_surf.get_width() * 2
                floor_height = self.floor_surf.get_height() * 2
                self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))  
                if exists("../saves/level_2_collectibles.csv"):
                    self.collectibles_path = "../saves/level_2_collectibles.csv"
                else:
                    self.collectibles_path = "../map/level_2_collectibles.csv"
            #transition to level 3  
            elif collided_tile_pos == (2432,2048) or collided_tile_pos == (2432,2176):
                self.level_index = 2
                self.player_pos = (200,5900)
                self.floor_surf = pygame.image.load("../graphics/tilemap/level3_ground.png").convert()
                floor_width = self.floor_surf.get_width() * 2
                floor_height = self.floor_surf.get_height() * 2
                self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                if exists("../saves/level_3_collectibles.csv"):
                    self.collectibles_path = "../saves/level_3_collectibles.csv"
                else:
                    self.collectibles_path = "../map/level_3_collectibles.csv"
            #transition to level 1
            elif collided_tile_pos == (6272, 5888) or collided_tile_pos == (6272, 6016) or collided_tile_pos == (1152, 2432) or collided_tile_pos == (1280, 2432) :
                self.level_index = 0
                self.player_pos = (3758,219)
                self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
                floor_width = self.floor_surf.get_width() * 2
                floor_height = self.floor_surf.get_height() * 2
                self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                if exists("../saves/level_1_collectibles.csv"):
                    self.collectibles_path = "../saves/level_1_collectibles.csv"
                else:
                    self.collectibles_path = "../map/level_1_collectibles.csv"
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

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, True)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'clutter':
                           target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player, self.floor_surf, self.floor_rect)
        self.shadow_sprites.shadow_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        self.check_coin_collisons()
        self.check_special_collisions()
        self.shadow_sprites.update()
        debug(self.player.rect.topleft)
        debug(self.level_index,30,10)

#test


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
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)

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

