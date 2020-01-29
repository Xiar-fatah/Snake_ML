#Author: Xiar 

import pygame
import random as random
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

class Snake(object):
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 20
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.hitbox)
        self.directions = [0,0,0,1] # Initial position is down   
    
        #Variables for the body of the snake
        self.bodies = 3
        self.positions = [[self.x,self.y],[self.x,self.y-self.y],[self.x,self.y-2*self.y], [self.x,self.y-3*self.y]]
        self.tail = self.positions[self.bodies-1]
        
        #Variables for machine learning
        #input_arr[0],input_arr[1],input_arr[2],input_arr[3] length to the left,right,up and down wall respectively
        self.input_arr = [0,0,0,0]
        
    #Move function is for the movement of the snake
    def move(self):
        
        #Updates the positions of the rest of the snake body
        for w in range(self.bodies-1,0,-1):
            self.positions[w][0] = self.positions[w-1][0]  
            self.positions[w][1] = self.positions[w-1][1]

        keys = pygame.key.get_pressed()

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

        #The position of the head is given by self.positions[0][0]
        
        #The total length to the left wall is the distance x-x_p = 0 - x_p
        self.input_arr[0] = 20 - self.positions[0][0]
        #The total length to the right wall is the distance x-x_p = 600 - x_p
        self.input_arr[1] = 600 - self.positions[0][0]
        #The total length to the top wall is the distance y-y_p = 0 - y_p
        self.input_arr[2] = 20 - self.positions[0][1]
        #The total length to the down wall is the distance y-y_p = 600 - y_p
        self.input_arr[3] = 600 - self.positions[0][1]
        #Note however we want the last distance to be 20, if it is 20 and the snake takes a step further
        #it will die.
    #Adds length to the snake
    def addlen(self):
        self.bodies += 1
        self.positions.append([self.x,self.y-1000])
        


        
    #Draw the snake
    def draw(self, screen, snake):
        
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

    def draw(self, screen, apple):

        pygame.draw.rect(screen, (100,255,242), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.height,  self.width) #Updating the position of the hitbox
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
    def is_collided_with(self, snake):
        return self.rect.colliderect(snake.rect)

###Draws the game
def redrawGameWindow(snake,apple,screen):
    snake.draw(screen, apple)
    apple.draw(screen, snake)

    
    pygame.display.update()

#Generates a random number for x and y between 0,20,40,....,500
def randGen(snake):
    x = np.linspace(0,500,26)
    y = np.linspace(0,500,26)
    rand_num = np.random.randint(0,26)
    
    while x[rand_num] == snake.x and y[rand_num] == snake.y:
        np.random.shuffle(x), np.random.shuffle(y)
        
    
    return x[rand_num],y[rand_num]

class SnakeNN(nn.Module):

    def __init__(self):
        super(SnakeNN, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x



#net = Net()
    
def main():
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    Bool = True
    snake = Snake(60, 60, 20, 20)
    apple = Apple(100, 100, 20, 20)
    while Bool:
        pygame.time.delay(120) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay

        for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                Bool = False

        #Check collision and generate new apple
        if apple.is_collided_with(snake):
            apple = Apple(randGen(snake)[0], randGen(snake)[1], 20, 20)
            #Calls addlen function to make the snake longer
            snake.addlen()
        #Check collision with the snake itself
        for i in range(1,len(snake.positions)):
            if snake.positions[0][1] == snake.positions[i][1] and snake.positions[0][0] == snake.positions[i][0]:
                main()
        if snake.x >= 600 or snake.x == -20 or snake.y >= 600 or snake.y == -20:
            main()

        #calls for movement of the snake
        snake.move()
        

        screen.fill((0,0,0))
        print(snake.input_arr)
        redrawGameWindow(snake,apple,screen)

    pygame.quit() 

#Starts the game
main()

