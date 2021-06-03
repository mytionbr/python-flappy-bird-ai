import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

IMAGE_PIPE = pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','pipi.png')))
IMAGE_BASE = pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGE_BACKGROUND =IMAGE_BASE = pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMAGE_BIRD = [
    pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.tranform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))
]

pygame.font.init()
POINT_SOURCE = pygame.font.SysFont('arial',50)

class Bird:
    IMGS = IMAGE_BIRD
    MAXIMUM_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMGS[0]
    
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y
        
    def move(self):
        self.time += 1
        shift = 1.5 * (self.time**2) + self.speed * self.time
        
        if shift > 16:
            shift = 26
        elif shift < 0:
            shift -=2
        
        self.y += shift
        
        if shift < 0 or self.y < (self.height + 50):
            if self.angle < self.MAXIMUM_ROTATION:
                self.angle = self.MAXIMUM_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED
    
    def draw(self,screen):
        self.image_count += 1
        
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.image_count >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0 
            
        
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2
            
        rotated_image = pygame.trasform.rotate(self.image, self.angle)
        image_center_position = self.image.get_rect(topleft=(self.x,self.y)).center
        rectangle = rotated_image.get_rect(center=image_center_position)
        screen.blit(rotated_image,rectangle.topleft)
        
        def get_mask(self):
            pygame.mask.from_surface(self.image)
    
    pass

class Pipe:
    pass

class Base:
    pass