import pygame
import sys
import copy

"""
pygame.init()
screen = pygame.display.set_mode((1200, 800))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
"""


class Field:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.cells = [ [0] * width for _ in range(height) ]

    def draw_console(self):
        for row in self.cells:
            for value in row:
                print("x" if value else ".", end='')
            print()

    def set_cells(self, new_cells):
        self.height = len(new_cells)
        row_lengths = set(len(row) for row in new_cells)
        if len(row_lengths) != 1: raise RuntimeError("Wrong cells")
        self.width = list(row_lengths)[0]

        self.cells = []
        for row in new_cells:
            self.cells.append(row[:])

    def __setitem__(self, index, value):
        a, b = index
        if a < 0 or a >= self.height: raise RuntimeError("Wrong row")
        if b < 0 or b >= self.width: raise RuntimeError("Wrong column")
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

    def occupied_cells(self):
        result = []
        for i, row in enumerate(self.shape.cells):
            for j, value in enumerate(row):
                if value:
                    result.append( (i + self.y, j + self.x) )
        return result

    def intersects_field(self, field):
        for (y, x) in self.occupied_cells():
            try:
                if field[y,x]:
                    return True
            except:
                return True
        return False

    def clone(self):
        cloned_piece = Piece(self.shape.cells)
        cloned_piece.x = self.x
        cloned_piece.y = self.y
        return cloned_piece

    def move_by(self, dy, dx, field = None):
        self.y += dy
        self.x += dx

        if field != None and self.intersects_field(field):
            self.y -= dy
            self.x -= dx
            return False

        return True

    def move_down(self, field = None):
        return self.move_by(1, 0, field)

    def move_left(self, field = None):
        return self.move_by(0, -1, field)

    def move_right(self, field = None):
        return self.move_by(0, 1, field)

    def move_up(self, field = None):
        return self.move_by(-1, 0, field)

    def rotate_cw(self, field = None): pass

    def rotate_ccw(self, field = None): pass

def generate_random_piece():
    return Piece([
        [0, 1, 1],
        [1, 1, 0],
    ])
    ## TODO: дописать

class Game:
    def __init__(self):
        self.piece = generate_random_piece()
        self.field = Field(20, 10)

    def step(self):
        if not self.piece.move_down(self.field):
            for coord in self.piece.occupied_cells():
                self.field[coord] = 1
            self.piece = generate_random_piece()


import os

game = Game()

while True:
    os.system("clear")
    field = game.field.clone()
    for coord in game.piece.occupied_cells():
        field[coord] = 1
    field.draw_console()
    input()
    game.step()


