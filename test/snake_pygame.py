import pygame
import random
import time
import asyncio
from enum import Enum
from collections import namedtuple
from astar import *

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.SysFont('arial', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y),
                      ]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def convert(self, point):
        x = point.x/20
        y = point.y/20

        return (x, y)

    def play_step(self):
        # 1. collect user input
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             self.direction = Direction.LEFT
        #         elif event.key == pygame.K_RIGHT:
        #             self.direction = Direction.RIGHT
        #         elif event.key == pygame.K_UP:
        #             self.direction = Direction.UP
        #         elif event.key == pygame.K_DOWN:
        #             self.direction = Direction.DOWN

        path = self.astar()

        direction = tuple(
            map(lambda i, j: i - j, path[1], self.convert(self.head)))

        print(direction)

        if direction == (0.0, -1.0):
            self.direction = Direction.UP
            print("up")
        elif direction == (0.0, 1.0):
            self.direction = Direction.DOWN
            print("down")
        elif direction == (-1.0, 0.0):
            self.direction = Direction.LEFT
            print("left")
        elif direction == (1.0, 0.0):
            self.direction = Direction.RIGHT
            print("right")

        # 2. move
        self._move(self.direction)  # update the head (remove the last head)

        self.snake.insert(0, self.head)  # insert the upbove head

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
            # self.snake.pop()  # the snake never increase
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            print("cham vo vien", self.snake)
            return True
        # hits itself
        if self.head in self.snake[1:]:
            print("cham vo nguoi", self.snake)
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)
        print(self.snake)

    def astar(self):
        start = (int(self.head.x/20), int(self.head.y/20))
        end = (int(self.food.x/20), int(self.food.y/20))
        path = get_path(start, end, self.snake)
        return path


if __name__ == '__main__':

    game = SnakeGame()

    # game loop
    while True:

        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
