from entity import Entity
from support import import_folder
from enemy import Enemy
from settings import *
import pygame
class CAT(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(monster_name, pos, groups, obstacle_sprites, damage_player)

        self.intro_finished = False

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if self.intro_finished != False:
            if distance <= self.attack_radius and self.can_attack == True:
                if self.status != 'attack':
                    self.frame_index = 0
                self.status = 'attack'
            elif(not self.vulnerable):
                self.status = "damaged"
            elif distance <= self.notice_radius:
                self.status = 'move'
            else:
                self.status = 'idle'
        else:
            self.status = 'intro'


    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[], 'intro':[], "damaged":[]}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation) 

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'intro':
                self.intro_finished = True
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

            
