import random

import pygame
from pygame.locals import *
import time

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
WINDOW_SIZE = (1000, 800)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("Resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, lenght):
        self.lenght = lenght
        self.parent_screen = parent_screen
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.x = [SIZE]*lenght
        self.y = [SIZE]*lenght
        self.direction = 'down'

    def increase_lenght(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.lenght-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.lenght):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load('Resources/bg_music_1.mp3')
        pygame.mixer.music.play()
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('Resources/background.jpg')
        self.surface.blit(bg, (0, 0))


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_lenght()
            self.apple.move()

        # collision with snake
        for i in range(3, self.snake.lenght):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Game over"

        # coillision with wall
        if not (0 <= self.snake.x[0] <= WINDOW_SIZE[0] and 0 <= self.snake.y[0] <= WINDOW_SIZE[1]):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.lenght-2}', True, (255, 255 , 225))
        self.surface.blit(score,(800,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)

        line1 = font.render(f'GAME OVER      Score: {self.snake.lenght-2}', True, (255, 255 , 225))
        self.surface.blit(line1, (350, 200))
        line2 = font.render('To play again please press Enter. To exit press Escape', True, (255, 255, 255))
        self.surface.blit(line2, (200, 300))

        pygame.display.flip()

        pygame.mixer.music.pause()
    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)


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

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
