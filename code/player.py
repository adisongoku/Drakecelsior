import pygame
import sys
from settings import *
from debug import debug
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups) #initialises the parent class passing the groups variable into it
        self.image = pygame.image.load("../graphics/test/drake.png").convert_alpha()
        self.player_height = self.image.get_height()
        self.player_width = self.image.get_width()
        self.image = pygame.transform.scale(self.image, (self.player_width *3.2, self.player_height*3.2))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-20,-60)
        
        #graphics setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.1

        #movement
        self.direction = pygame.math.Vector2() #this gives us a vector that has x and y and by default they're both 0
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

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
        if not self.attacking:
            keys = pygame.key.get_pressed()

            #close game
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

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
                self.speed = 10
            else:
                self.speed = 5

            #attack mele input
            if keys[pygame.K_x]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
            
            #magic input
            if keys[pygame.K_z]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

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

    def move(self,speed):
        if self.direction.magnitude() != 0: #check length of the vector (if vector is 0 it can't be normalised)
            self.direction = self.direction.normalize() #if length of the vector is bigger than 1, normalize it 
        
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LCTRL]:
            if direction == "horizontal":
                for obstacle in self.obstacle_sprites:
                    if obstacle.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0: #moving right
                            self.hitbox.right = obstacle.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.hitbox.left = obstacle.hitbox.right

            if direction == "vertical":
                for obstacle in self.obstacle_sprites:
                    if obstacle.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0: #moving down
                            self.hitbox.bottom = obstacle.hitbox.top
                        if self.direction.y < 0: #moving up
                            self.hitbox.top = obstacle.hitbox.bottom            

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        #set the image
        if self.status == "right_idle" or self.status == "left_idle" or self.status == "up_idle" or self.status == "down_idle" or self.status == "left" or self.status == "right":
            self.image = animation[int(self.frame_index)]
            self.image = pygame.transform.scale(self.image, (self.player_width *3.2, self.player_height*3.2))
            self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)



 
