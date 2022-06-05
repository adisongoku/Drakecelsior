from calendar import c
# from readline import set_history_length
import pygame
import sys
from settings import *
from debug import debug
from support import import_folder
from entity import Entity
from pygame import mixer

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, status, transitioning):
        super().__init__(groups) #initialises the parent class passing the groups variable into it
        self.image = pygame.image.load("../graphics/test/drake.png").convert_alpha()
        self.player_height = self.image.get_height()
        self.player_width = self.image.get_width()
        self.image = pygame.transform.scale(self.image, (self.player_width *3.2, self.player_height*3.2))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-20,-60)
        self.transitioning = transitioning

        #graphics setup
        self.import_player_assets()
        self.status = status


        #movement
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # long dist weapon
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health' : 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import sound
        self.wepon_attack_sound = pygame.mixer.Sound('../audio/fireball.wav')
        self.wepon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking and not self.transitioning:
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            #sprint
            if keys[pygame.K_LSHIFT]:
                self.speed = 30
            else:
                self.speed = 5

            #attack mele input
            if keys[pygame.K_x]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.wepon_attack_sound.play()

            #magic input
            if keys[pygame.K_z]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            # switching weapons
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.attack_time = pygame.time.get_ticks()


                # if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    # self.weapon_index += 1
                # else:
                    # self.weapon_index = 0

                # self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
            # if self.can_switch_weapon:
                # if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                    # self.can_switch_weapon = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        if self.status == "right_idle" or self.status == "left_idle" or self.status == "up_idle" or self.status == "down_idle" or self.status == "left" or self.status == "right"or self.status == "up" or self.status == "down":
            animation = self.animations[self.status]
            #loop over the frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

            #set the image

            self.image = animation[int(self.frame_index)]
            self.image = pygame.transform.scale(self.image, (self.player_width *3.2, self.player_height*3.2))
            self.rect = self.image.get_rect(center = self.hitbox.center)
            if not self.vulnerable:
                alpha = self.wave_value()
                self.image.set_alpha(alpha)
            else:
                self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_player_direction(self):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(self.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()


        return (distance, direction)

    def update(self):
        self.input()
        self.transitioning = False
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
       
