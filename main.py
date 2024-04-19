import os
import pygame
import sys
import copy
import random

pygame.init()
screen = pygame.display.set_mode((400, 800))


class Field:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.cells = [[0] * width for _ in range(height)]

    def draw_console(self):
        for row in self.cells:
            for value in row:
                print("x" if value else ".", end='')
            print()

    def set_cells(self, new_cells):
        self.height = len(new_cells)
        row_lengths = set(len(row) for row in new_cells)
        if len(row_lengths)!= 1: raise RuntimeError("Wrong cells")
        self.width = list(row_lengths)[0]

        self.cells = []
        for row in new_cells:
            self.cells.append(row[:])

    def __setitem__(self, index, value):
        a, b = index
        if a < 0 or a >= self.height: return #raise RuntimeError("Wrong row")
        if b < 0 or b >= self.width: return #raise RuntimeError("Wrong column")
        self.cells[a][b] = value

    def __getitem__(self, index):
        a, b = index
        if a < 0 or a >= self.height: raise RuntimeError("Wrong row")
        if b < 0 or b >= self.width: raise RuntimeError("Wrong column")
        return self.cells[a][b]

    def clone(self):
        cloned_field = Field(self.width, self.height)
        cloned_field.set_cells(self.cells)
        return cloned_field


class Piece:
    def __init__(self, shape):
        self.shape = Field(0, 0)
        self.shape.set_cells(shape)
        self.x = 0
        self.y = 0
        # TODO: добавить параметр "центр вращения"
        # TODO: добавить очки, уничтожение рядов, музыку, главное меню

    def occupied_cells(self):
        result = []
        for i, row in enumerate(self.shape.cells):
            for j, value in enumerate(row):
                if value:
                    result.append((i + self.y, j + self.x))
        return result

    def intersects_field(self, field):
        for (y, x) in self.occupied_cells():
            try:
                if field[y, x]:
                    return True
            except:
                return True
        return False

    def clone(self):
        cloned_piece = Piece(self.shape.cells)
        cloned_piece.x = self.x
        cloned_piece.y = self.y
        return cloned_piece

    def move_by(self, dy, dx, field=None):
        self.y += dy
        self.x += dx

        if field and self.intersects_field(field):
            self.y -= dy
            self.x -= dx
            return False

        return True

    def move_down(self, field=None):
        return self.move_by(1, 0, field)

    def move_left(self, field=None):
        return self.move_by(0, -1, field)

    def move_right(self, field=None):
        return self.move_by(0, 1, field)

    def move_up(self, field=None):
        return self.move_by(-1, 0, field)

    def rotate_cw(self):
        new_shape = Field(self.shape.width, self.shape.height)
        for x in range(self.shape.width):
            for y in range(self.shape.height):
                new_shape[x, self.shape.height-1-y] = self.shape[y,x]
        self.shape.set_cells(new_shape.cells)

    def rotate_ccw(self):
        new_shape = Field(self.shape.width, self.shape.height)
        for x in range(self.shape.width):
            for y in range(self.shape.height):
                new_shape[self.shape.width-1-x, y] = self.shape[y,x]
        self.shape.set_cells(new_shape.cells)

    def safe_rotate_cw(self, field):
        self.rotate_cw()
        if self.intersects_field(field): self.rotate_ccw()

    def safe_rotate_ccw(self, field):
        self.rotate_ccw()
        if self.intersects_field(field): self.rotate_cw()


def generate_random_piece():
    pieces = [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],

        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],

        [[1, 1, 0],
         [1, 1, 0],
         [0, 0, 0]],

        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[1, 1, 1],
         [0, 1, 0],
         [0, 0, 0]],

        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],

        [[1, 1, 0],
         [1, 0, 0],
         [1, 0, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [1, 0, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]],

        [[1, 0, 0],
         [1, 0, 0],
         [1, 0, 0],
         [1, 0, 0]]
    ]

    return Piece(random.choice(pieces))


class Game:
    def __init__(self):
        self.piece = generate_random_piece()
        self.field = Field(20, 10)
        self.timer = 0

        self.keys_used = set()


    def step(self):
        if not self.piece.move_down(self.field):
            for coord in self.piece.occupied_cells():
                self.field[coord] = 1
                self.piece = generate_random_piece()


    def redraw(self):
        screen.fill((0, 0, 0))
        for row in range(self.field.height):
            for col in range(self.field.width):
                if self.field[row, col]:
                    pygame.draw.rect(screen, (255, 255, 255), (col * 40, row * 40, 40, 40))

        for coord in self.piece.occupied_cells():
            pygame.draw.rect(screen, (255, 0, 0), (coord[1] * 40, coord[0] * 40, 40, 40))

        pygame.display.flip()

    def process_keys(self):
        keys = pygame.key.get_pressed()
        keynames = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        keyactions = [
            (lambda: self.piece.move_left(self.field)),
            (lambda: self.piece.move_right(self.field)),
            (lambda: self.piece.safe_rotate_ccw(self.field)),
            (lambda: self.piece.safe_rotate_cw(self.field)),
        ]

        for i, name in enumerate(keynames):
            action = keyactions[i]

            if keys[name]:
                if name not in self.keys_used:
                    self.keys_used.add(name)
                    action()
            else:
                self.keys_used.discard(name)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.process_keys()

            clock.tick(180)
            self.timer += 1
            self.timer %= 180

            if self.timer % TICKS_PER_FRAME == 0: self.redraw()
            if self.timer % TICKS_PER_UPDATE == 0: self.step()


DIFFICULTY_SPEEDS = [10, 20, 30, 60, 180]
TICKS_PER_FRAME = 3
TICKS_PER_UPDATE = DIFFICULTY_SPEEDS[2]

game = Game()
game.run()
