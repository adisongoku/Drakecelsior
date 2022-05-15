import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.math.Vector2()

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

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else: 
            return 0


