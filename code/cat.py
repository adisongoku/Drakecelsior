from dialogue_box import DIALOGUE_BOX
from entity import Entity
from support import *
from enemy import Enemy
from settings import *
from tile import *
import pygame
import numpy
import time
class CAT(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, stop_bgm):
        super().__init__(monster_name, pos, groups, obstacle_sprites, damage_player)

        self.intro_finished = False
        self.status = 'waiting'
        stop_bgm()
        self.music = pygame.mixer.Sound('../audio/cat_theme.mp3')
        self.music.set_volume(0.4)
        self.cutscene_played = False
        self.dialogue = [(CAT_DIAL1,"cat"),(DIALOGUE1,"drake"),(DIALOGUE2,"drake"),(DIALOGUE3,"drake"),(CAT_DIAL2,"cat"),(CAT_DIAL3,"cat"),(DIALOGUE4,"drake"), (CAT_DIAL4,"cat")]
        self.dialogue_index = 0
        self.dialogue_tick = 1
        self.can_progress_dialogue = False

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if self.intro_finished != False:
            if distance <= self.attack_radius and self.can_attack == True:
                if self.status != 'attack':
                    self.frame_index = 0
                self.status = 'attack'
            elif(not self.vulnerable):
                self.status = 'damaged'
            elif distance <= self.notice_radius:
                self.status = 'move'
            else:
                self.status = 'idle'
            player.set_can_move(True)
    
    def check_death(self):
        if self.health <= 0:
            pygame.mixer.fadeout(5000)
            self.kill()

    def cat_set_intro_status(self, player):
        if self.status == "waiting":
            self.music.play()
            self.status = 'intro'
            player.set_can_move(False)

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[], 'intro':[], "damaged":[], "waiting":[]}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation) 

    def animate(self):
        animation = self.animations[self.status]
        if self.frame_index < 50:
            self.animation_speed = 0.0666
        else:
            self.animation_speed = 0.05
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'intro':
                self.intro_finished = True
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0
        if self.status != "intro" and self.status != "waiting" and self.cutscene_played == False:
            self.play_cutscene(self.dialogue)

        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def play_cutscene(self, dialogue):
        box = DIALOGUE_BOX()
        keys = pygame.key.get_pressed()
        if self.dialogue_index < len(dialogue):
            box.draw_dialogue(dialogue[self.dialogue_index][0],dialogue[self.dialogue_index][1])
            if keys[pygame.K_SPACE]:
                self.dialogue_tick = pygame.time.get_ticks()
                if self.can_progress_dialogue:
                    self.dialogue_index += 1
        else:
            self.cutscene_played = True

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
        if current_time - self.dialogue_tick >= 500:
            self.can_progress_dialogue = True 
        else: 
            self.can_progress_dialogue = False

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)        
        elif self.status == 'move' and self.cutscene_played:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
        
        

  

    

            
