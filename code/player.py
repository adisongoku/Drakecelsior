import pygame
import sys
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups) #initialises the parent class passing the groups variable into it
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-40,-60)
        self.direction = pygame.math.Vector2() #this gives us a vector that has x and y and by default they're both 0
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        #close game
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        #movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        #sprint
        if keys[pygame.K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5

    def move(self,speed):
        if self.direction.magnitude() != 0: #check length of the vector (if vector is 0 it can't be normalised)
            self.direction = self.direction.normalize() #if length of the vector is bigger than 1, normalize it 
        
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self,direction):
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

    def update(self):
        self.input()
        self.move(self.speed)



 
