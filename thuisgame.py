import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_width = 1000
screen_height = 1000



screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')


#game vrariables
tile_size = 50


#load images
sun_img = pygame.image.load('sun.png')
background_img = pygame.image.load('sky.png')

class player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right,(40,80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jumped = False
        self.direction = 0 
        
    def update(self):
        screen.blit(self.image, self.rect)
        dx = 0
        dy = 0
        walk_cooldown = 5
        
        # key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped ==False:
           self.velocity_y = -15
           self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT] == True:
           dx -= 5 
           self.counter += 1
           self.direction = -1
        if key[pygame.K_RIGHT] == True:
           dx += 5     
           self.counter += 1
           self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]    
           
        #animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]    
        
        #gravity
        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y
        
        #check for collision
        
        #update player coords
        self.rect.x += dx
        self.rect.y += dy
        
class World():
    
    def __init__(self, data):
        self.tile_list = []
        
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size      
                    img_rect.y = row_count * tile_size  
                    tile = (img, img_rect)
                    self.tile_list.append(tile) 
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))  
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size      
                    img_rect.y = row_count * tile_size  
                    tile = (img, img_rect)
                    self.tile_list.append(tile)   
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            
        
        
        
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
]

player = player(100, screen_height - 130)
world = World(world_data)
        
            
        
run = True
while run == True:


    clock.tick(fps)
    screen.blit(background_img,(0, 0))
    screen.blit(sun_img,(100,100))
    
    world.draw()
    player.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
     
    pygame.display.update()       
pygame.quit()