import pygame
import random
from enum import Enum
from collections import namedtuple
from astar import *

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 255, 153)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

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

    def _convert(self, point):
        x = point.x/BLOCK_SIZE
        y = point.y/BLOCK_SIZE

        return (x, y)

    def _step(self):

        path = self.astar()  # call the a star algorithm

        if path == None:
            game_over = True
            return game_over, self.score

        direction = tuple(
            map(lambda i, j: i - j, path[1], self._convert(self.head)))  # get the next move

        # set the direction
        if direction == (0.0, -1.0):
            self.direction = Direction.UP
        elif direction == (0.0, 1.0):
            self.direction = Direction.DOWN
        elif direction == (-1.0, 0.0):
            self.direction = Direction.LEFT
        elif direction == (1.0, 0.0):
            self.direction = Direction.RIGHT

        self._move(self.direction)

        self.snake.insert(0, self.head)

        # check if game over
        game_over = False
        if self._is_hit():
            game_over = True
            return game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()

        else:
            self.snake.pop()

        # update ui and clock

        self._update_screen()
        self.clock.tick(SPEED)

        # return game over and score
        return game_over, self.score

    def _is_hit(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            print("Touch the boundary", self.snake)
            return True
        # hits itself
        if self.head in self.snake[1:]:
            print("Touch the body", self.snake)
            return True

        return False

    def _update_screen(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, YELLOW, pygame.Rect(
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

    def astar(self):
        start = (int(self.head.x/BLOCK_SIZE), int(self.head.y/BLOCK_SIZE))
        end = (int(self.food.x/BLOCK_SIZE), int(self.food.y/BLOCK_SIZE))
        path = get_path(start, end, self.snake)  # call algorithm

        return path


if __name__ == '__main__':

    game = SnakeGame()

    # game loop
    while True:

        game_over, score = game._step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
