import pygame
import numpy as np


size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")

#Make it available to quit the client
Bool = True


class player(object):
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x, self.y, self.width, self.height)




    def draw(self, screen):
        
        
        pygame.draw.rect(screen, (254,255,242), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.height,  self.width) #Updating the position of the hitbox
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
class apple(object):
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height) #initial position of the hitbox



    def draw(self, screen):

        pygame.draw.rect(screen, (100,255,242), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.height,  self.width) #Updating the position of the hitbox
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)


    
def redrawGameWindow():
    man.draw(screen)
    points.draw(screen)

    
    pygame.display.update()






man = player(50, 50, 15, 15)
points = apple(100, 100, 15, 15)
vel = 5
while Bool:
    pygame.time.delay(10) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay

    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            Bool = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        man.x -= vel

    if keys[pygame.K_RIGHT]:
        man.x += vel

    if keys[pygame.K_UP]:
        man.y -= vel

    if keys[pygame.K_DOWN]:
        man.y += vel

    screen.fill((0,0,0))
    

    redrawGameWindow()


pygame.quit() 




