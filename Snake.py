#Author: Xiar 

import pygame
import random as random

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")

#Make it available to quit the client
Bool = True


class Snake(object):
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 20
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.hitbox)
        self.vel
        self.directions = [0,0,0,1] # Initial position is down   
    
        #TEST
        self.bodies = 3
        self.positions = [[self.x,self.y],[self.x,self.y-self.y],[self.x,self.y-2*self.y], [self.x,self.y-3*self.y]]
        self.tail = self.positions[self.bodies-1]
        
    #Move function is for the movement of the snake
    def move(self):
        #Updates the positions of the rest of the snake body
        for w in range(self.bodies-1,0,-1):
            self.positions[w][0] = self.positions[w-1][0]  
            self.positions[w][1] = self.positions[w-1][1]
            
        #Check if the key is pressed and then moves the snake in that direction
        #and is added to not allow the player to move backwards when it is moving forwards
        if keys[pygame.K_LEFT] and self.directions[1] != 1 :
            self.directions = [1,0,0,0]
            
        #Elif is added to only move in one direction at the time
        elif keys[pygame.K_RIGHT] and self.directions[0] != 1 : 
            self.directions = [0,1,0,0] 

        elif keys[pygame.K_UP] and self.directions[3] != 1 :
            self.directions = [0,0,1,0] 

        elif keys[pygame.K_DOWN] and self.directions[2] != 1 :
            self.directions = [0,0,0,1] 

        #To move with a constant velocity, directions was introduce, [1,0,0,0] makes the snake move only left
        if self.directions[0] == 1:
            self.x = self.x - self.vel
            self.positions[0][0] = self.x 
        #right
        elif self.directions[1] == 1:
            self.x = self.x + self.vel
            self.positions[0][0] = self.x 
        #down
        elif self.directions[2] == 1:
            self.y = self.y - self.vel
            self.positions[0][1] = self.y
        #up
        elif self.directions[3] == 1:
            self.y = self.y + self.vel
            self.positions[0][1] = self.y


        
    #add length to the snake
    def addlen(self):
        self.bodies += 1
        self.positions.append([self.x,self.y-1000])
        
#        self.positions.append([self.x,self.y])


        
    #Draw the snake
    def draw(self, screen):
        
        self.rect = pygame.Rect(self.hitbox) #Values gets updated heres
        pygame.draw.rect(screen, (254,255,242), (self.x, self.y, self.width, self.height))
        #Update the positions of the head in the list
        

        for i in range(0,self.bodies-1):
            pygame.draw.rect(screen, (254,255,242), (self.positions[i][0], self.positions[i][1], self.width, self.height))

           



        self.hitbox = (self.x, self.y, self.height,  self.width) #Updating the position of the hitbox
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
class Apple(object):
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height) #initial position of the hitbox
        self.test = (self.x, self.y, self.width, self.height)

        self.rect = pygame.Rect(self.test)

    def draw(self, screen):

        pygame.draw.rect(screen, (100,255,242), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.height,  self.width) #Updating the position of the hitbox
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
    def is_collided_with(self, snake):
        return self.rect.colliderect(snake.rect)


    
def redrawGameWindow():
    snake.draw(screen)
    apple.draw(screen)

    
    pygame.display.update()



Bool = True

snake = Snake(60, 60, 20, 20)
apple = Apple(100, 100, 20, 20)
vel = 5
while Bool:
    pygame.time.delay(200) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay

    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            Bool = False

    #Check collision and generate new apple
    if apple.is_collided_with(snake):
        apple = Apple(random.random()*500, random.random()*500, 20, 20)
        #Calls addlen function to make the snake longer
        snake.addlen()
    #Check collision with the snake itself
    for i in range(1,len(snake.positions)):
        if snake.positions[0][1] == snake.positions[i][1] and snake.positions[0][0] == snake.positions[i][0]:
            print("collision")




        
    keys = pygame.key.get_pressed()

    #calls for movement of the snake
    snake.move()

    screen.fill((0,0,0))
    
    redrawGameWindow()


pygame.quit() 



