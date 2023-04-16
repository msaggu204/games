import pygame
from pygame.locals import *
import sys
import time
import random

def startGame():
    pygame.init()
    
    pygame.display.set_caption('Snake Game')

def score_display(choice, color, font, size):
    score_font = pygame.font.SysFont(font,size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    displaysurf.blit(score_surface, score_rect)
    
def game_over():
    font = pygame.font.SysFont('calibri', 50)
    game_over_surface = font.render('Final Score: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width/2, window_height/4)
    
    displaysurf.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    time.sleep(2)
    
    pygame.quit()
    
    quit

if __name__ == "__main__":
    startGame()
    # Initialize a 720x480 window
    window_width = 720
    window_height = 480
    displaysurf = pygame.display.set_mode((window_width, window_height))

    fps = pygame.time.Clock()
    
    #snake starting position
    snake = [100, 50]
    #snake is 4 blocks by default
    snake_body = [  [100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]        
                ]

    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)

    #default snake direction
    direction = 'RIGHT'
    change_direction = direction
    
    #random food spawn
    food_position = [random.randrange(1, (window_width//10)) * 10,
                     random.randrange(1, (window_height//10)) * 10]
    food_spawn = True
    
    score = 0
    
    while True:
        #direction changes from key inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_direction = 'UP'
                if event.key == pygame.K_RIGHT:
                    change_direction = 'RIGHT'
                if event.key == pygame.K_DOWN:
                    change_direction = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_direction = 'LEFT'
        
        # Snake cannot turn 180 degrees
        if change_direction == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_direction == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_direction == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_direction == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        
        if direction == 'UP':
            snake[1] -= 10
        if direction == 'RIGHT':
            snake[0] += 10
        if direction == 'DOWN':
            snake[1] += 10
        if direction == 'LEFT':
            snake[0] -= 10
            
        # Snake eating food, grow body by one block
        snake_body.insert(0, list(snake))
        if snake[0] == food_position[0] and snake[1] == food_position[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()        
        
        if not food_spawn:
            food_position = [random.randrange(1, (window_width//10)) * 10,
                            random.randrange(1, (window_height//10)) * 10]
        # Reinitiate a food spawn
        food_spawn = True
        # Screen background is black
        displaysurf.fill(black)
        # Create the snake body
        for pos in snake_body:
            pygame.draw.rect(displaysurf, green, pygame.Rect(pos[0], pos[1], 10, 10))
        # Create the block of food
        pygame.draw.rect(displaysurf, white, pygame.Rect(food_position[0], food_position[1], 10, 10))
        
        # End game if you reach the borders of the screen
        if snake[0] < 0 or snake[0] > window_width - 10:
            game_over()
        if snake[1] < 0 or snake[1] > window_height - 10:
            game_over()
            
        # End game if snake runs into itself
        for block in snake_body[1:]:
            if snake[0] == block[0] and snake[1] == block[1]:
                game_over()
        
        # Call score_display function to always display updated score        
        score_display(1, white, 'calibri', 20)
        
        pygame.display.update()
        # Set snake speed as the frames per second update
        snake_speed = 15
        fps.tick(snake_speed)