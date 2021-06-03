import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550

IMAGE_PIPE = (pygame.image.load(os.path.join('imgs','pipe.png')))
IMAGE_BASE = (pygame.image.load(os.path.join('imgs','base.png')))
IMAGE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('imgs','bg.png')),(500,550))
IMAGE_BIRD = [
    (pygame.image.load(os.path.join('imgs','bird1.png'))),
    (pygame.image.load(os.path.join('imgs','bird2.png'))),
    (pygame.image.load(os.path.join('imgs','bird3.png')))
]

pygame.font.init()
POINT_SOURCE = pygame.font.SysFont('arial',30)

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
            
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center_position = self.image.get_rect(topleft=(self.x,self.y)).center
        rectangle = rotated_image.get_rect(center=image_center_position)
        screen.blit(rotated_image,rectangle.topleft)
        
    def get_mask(self):
       return pygame.mask.from_surface(self.image)
    
    

class Pipe:
    DISTANCE = 170
    SPEED = 5
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_base = 0
        self.TOP_PIPE = pygame.transform.flip(IMAGE_PIPE, False,True)
        self.BASE_PIPE = IMAGE_PIPE
        self.surpassed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(31,281)
        self.pos_top = self.height - self.TOP_PIPE.get_height()
        self.pos_base = self.height + self.DISTANCE
    
    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.TOP_PIPE,(self.x, self.pos_top))
        screen.blit(self.BASE_PIPE,(self.x, self.pos_base))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        base_mask = pygame.mask.from_surface(self.BASE_PIPE)
        
        distane_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distane_base = (self.x - bird.x, self.pos_base - round(bird.y))
        
        top_point = bird_mask.overlap(top_mask,distane_top)
        base_point = bird_mask.overlap(base_mask,distane_base)
        
        if base_point or top_point:
            return True
        else:
            return False
        
class Base:
    SPEED = 5
    WIDTH = IMAGE_BASE.get_width()
    IMAGE = IMAGE_BASE
    
    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x1 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x2 + self.WIDTH
    
    def draw(self,screen):
        screen.blit(self.IMAGE,(self.x1, self.y))
        screen.blit(self.IMAGE,(self.x2, self.y))
        

def draw_screen(screen,birds,pipes,base,points):
    screen.blit(IMAGE_BACKGROUND, (0,0))
    
    for bird in birds:
        bird.draw(screen)
        
    for pipe in pipes:
        pipe.draw(screen)
        
    text = POINT_SOURCE.render(f"Pontuação: {points}", 1, (255,255,255))
    screen.blit(text,(SCREEN_WIDTH - 10 - text.get_width(),10))
    base.draw(screen)
    pygame.display.update()
    

def main():
    birds = [Bird(130,350)]
    base = Base(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    points = 0
    clock  = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
                        
        for bird in birds:
            bird.move()
        base.move()
        
        add_pipe = False
        remove_pipe = []
        
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                                 
                if not pipe.surpassed and bird.x > pipe.x:
                    add_pipe = True
                    pipe.surpassed = True

            pipe.move()
            if pipe.x +  pipe.TOP_PIPE.get_width() < 0:
                remove_pipe.append(pipe)
                
        if add_pipe:
            points += 1
            pipes.append(Pipe(500))
        for pipe in  remove_pipe:
            pipes.remove(pipe)
            
        for i,bird in enumerate(birds):
            if bird.y + bird.image.get_height() > base.y or bird.y <0:
                birds.pop(i)
                
        
        draw_screen(screen,birds,pipes,base,points)

if __name__ == '__main__':
    main()