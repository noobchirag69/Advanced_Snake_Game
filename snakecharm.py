# Importing libraries
import pygame
from pygame.locals import *
import time
import random

SIZE = 40

# Class for the apple
class Apple:

    # Initialize Apple
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Images/apple.png").convert()
        self.x = SIZE * random.randint(1, 24)
        self.y = SIZE * random.randint(1, 19)

    # Draw Apple on screen
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # Function to move apple when eaten
    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

# Class for the snake
class Snake:

    # Initialize Snake
    def __init__(self, parent_screen, length):
        
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Images/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    # Function to  Move snake
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'   

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    # Function to increase length of the snake when it eats the apple
    def increaseLength(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

# Class for the game
class Game:

    # Initialize the game
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game by Chirag Chakraborty")

        # Initialize background music
        pygame.mixer.init()
        self.playBackgroundMusic()

        # Setting the window
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((77, 34, 52))

        # Draw the snake
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        
        # Draw the apple
        self.apple = Apple(self.surface)
        self.apple.draw()

    # Function to add background music
    def playBackgroundMusic(self):
        pygame.mixer.music.load('Music/tarzan.mp3')
        pygame.mixer.music.play(-1, 0)

    # Function for collision
    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    # Function for background image
    def renderBackground(self):
        bg = pygame.image.load("Images/background.jpg")
        self.surface.blit(bg, (0, 0))

    # Function to display score
    def displayScore(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 3}", True, (0, 0, 0))
        self.surface.blit(score, (850, 10))

    # Playing logic
    def play(self):
        self.renderBackground()
        self.snake.walk()
        self.apple.draw()
        self.displayScore()
        pygame.display.flip()

        # Snake colliding with apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increaseLength()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"
    
    # Game Over logic
    def showGameOver(self):
        self.renderBackground()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length - 3}.", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    # Reset game
    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    # Running logic
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.showGameOver()
                pause = True
                self.reset()
                
            
            time.sleep(0.25)

# Main function
if __name__ == "__main__":
    game = Game()
    game.run()