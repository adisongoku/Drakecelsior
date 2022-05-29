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
from enemy import Enemy
from os.path import exists
from magic import MagicPlayer
from particles import AnimationPlayer


class Level:
    def __init__(self, change_coins):
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        #level information
        self.level_index = 0
        self.player_pos = (193,2363)
        self.player_status = "right"
        self.transitioning = False
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

        # particles
        self.animation_player = AnimationPlayer()

        self.magic_player = MagicPlayer(self.animation_player)


    def create_map(self):

        level_1_1 = {
                "boundary" : import_csv_layout("../map/level_1_boundaries.csv"),
                "clutter": import_csv_layout("../map/level_1_clutter.csv"),
                "objects": import_csv_layout("../map/level_1_objects.csv"),
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_1_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_1_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_1_shadows.csv"),
                "entities": import_csv_layout("../map/level_1_enemy.csv")
        }


        level_1_2 = {
                "clutter": import_csv_layout("../map/level_2_clutter.csv"),
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_2_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_2_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_2_shadows.csv"),
                "entities": import_csv_layout("../map/level_2_enemy.csv")
        }

        level_1_3 = {
                "clutter": import_csv_layout("../map/level1_3_clutter.csv"),
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level1_3_walls.csv"),
                "special_tiles": import_csv_layout("../map/level1_3_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level1_3_shadows.csv"),
                "entities": import_csv_layout("../map/level1_3_enemy.csv")
        }

        level_2_1 = {
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_3_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_3_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_3_shadows.csv"),
                "entities": import_csv_layout("../map/level_3_enemy.csv")
        }

        level_2_2 = {
                "collectibles": import_csv_layout(self.collectibles_path),
                "walls": import_csv_layout("../map/level_4_walls.csv"),
                "special_tiles": import_csv_layout("../map/level_4_special_tiles.csv"),
                "shadows": import_csv_layout("../map/level_4_shadows.csv"),
                "entities": import_csv_layout("../map/level_4_enemy.csv")
        }

        graphics = {
                "clutter": import_folder("../graphics/clutter"),
                "objects": import_folder("../graphics/objects"),
                "collectibles": import_folder("../graphics/collectibles"),
                "walls": import_folder("../graphics/walls"),
                "shadows": import_folder("../graphics/shadows")
        }

        levels = [level_1_1,level_1_2,level_1_3,level_2_1,level_2_2]

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

        self.player = Player(self.player_pos,[self.visible_sprites],self.obstacles_sprites, self.create_attack, self.destroy_attack, self.create_magic, self.player_status, self.transitioning)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])


        print(style)
        print(strength)
        print(cost)

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
                coin_pos = coin.get_pos()

                #establish saving path and check if it already exists. If it does, modify positions in already existing file
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
                print(collided_tile_pos)

                #this assures that player's sprite direction won't get overriden by input from keyboard while transitionning to another level
                self.transitioning = True

            #first checking what level we are on and then checking which door we go through
            match self.level_index:

                #level 1_1
                case 0:
                    match collided_tile_pos:

                        #transition to level 1_2
                        case (3712,0) | (3840,0):
                            self.level_index = 1
                            self.player_pos = (1076,4325)
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level_1_2_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level_2_collectibles.csv"):
                                self.collectibles_path = "../saves/level_2_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level_2_collectibles.csv"

                        #transition to level 1_3
                        case (4864, 4736) | (4736, 4736) | (4992, 4736):
                            self.level_index = 2
                            self.player_pos = (506, 4663)
                            self.player_status = "up"
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level1_3_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level1_3_collectibles.csv"):
                                self.collectibles_path = "../saves/level1_3_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level1_3_collectibles.csv"
                        #transition to level 2_1
                        case (1152, 1792):
                            self.level_index = 3
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

                #level 1_2
                case 1:
                    match collided_tile_pos:

                        #transition to level 1_1
                        case (1024, 4480) | (1152, 4480):
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
                        case (1792, 5120) | (1792, 5248):
                            self.level_index = 0
                            self.player_pos = (3758,219)
                            self.player_status = "down"
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level_1_collectibles.csv"):
                                self.collectibles_path = "../saves/level_1_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level_1_collectibles.csv"
                        #transition to level 1_3
                        case (6144, 896) | (6144, 1024):
                            self.level_index = 2
                            self.player_pos = (268,545)
                            self.player_status = "right"
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level1_3_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level1_3_collectibles.csv"):
                                self.collectibles_path = "../saves/level1_3_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level1_3_collectibles.csv"

                #level 1_3
                case 2:
                    match collided_tile_pos:

                        #transition to level 1_1
                        case (384, 4864) | (512, 4864):
                            self.level_index = 0
                            self.player_pos = (4835, 4521)
                            self.player_status = "up"
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level_1_collectibles.csv"):
                                self.collectibles_path = "../saves/level_1_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level_1_collectibles.csv"

                        #transition to level 1_2
                        case (0, 512) | (0, 640):
                            self.level_index = 1
                            self.player_pos = (5832, 947)
                            self.player_status = "left"
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level_1_2_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level_2_collectibles.csv"):
                                self.collectibles_path = "../saves/level_2_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level_2_collectibles.csv"

                #level 2_1
                case 3:
                    match collided_tile_pos:

                        #transition to level 2.2
                        case (6272, 5888) | (6272, 6016):
                            self.level_index = 4
                            self.player_pos = (300,5900)
                            self.floor_surf = pygame.image.load("../graphics/tilemap/level4_ground.png").convert()
                            floor_width = self.floor_surf.get_width() * 2
                            floor_height = self.floor_surf.get_height() * 2
                            self.floor_surf = pygame.transform.scale(self.floor_surf,(floor_width, floor_height))
                            self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
                            if exists("../saves/level_4_collectibles.csv"):
                                self.collectibles_path = "../saves/level_4_collectibles.csv"
                            else:
                                self.collectibles_path = "../map/level_4_collectibles.csv"
                #level 2_2
                case 4:
                    match collided_tile_pos:

                        #transition to level 1_1
                        case (1408, 0) | (1536, 0):
                            self.level_index = 0
                            self.player_pos = (1150,2005)
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
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player, self.floor_surf, self.floor_rect)
        self.shadow_sprites.shadow_draw(self.player)
        self.check_coin_collisons()
        self.check_special_collisions()
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
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
