from turtle import *
import random


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert(isinstance(other, XY))
        return XY(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'{self.x}, {self.y}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Field:
    def __init__(self, size, cell_size):
        self.size = size
        self.cell_size = cell_size
        self.origin = XY(-cell_size * size.x // 2, -cell_size * size.y // 2)
        self.cells = [[0] * size.y for _ in range(size.x)]
        self.fill_random()

    def fill_random(self):
        self.cells = [[0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                      [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                      [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                      [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                      [0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                      [0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
                      [0, 1, 0, 0, 0, 0, 1, 0, 1, -1]]

    def isallowed(self, pos):
        return 0 <= pos.x < self.size.x and 0 <= pos.y < self.size.y and self.cells[pos.x][pos.y] <= 0

    def draw(self):
        speed(0)
        tracer(100000)
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.draw_cell(self.cells[x][y], x, y)
        update()

    def draw_cell(self, cell, ax, ay):
        x0 = self.origin.x + self.cell_size * ax
        y0 = self.origin.y + self.cell_size * ay
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        penup()
        goto(x0, y0)
        pendown()
        if cell != 0:
            if cell == -1:
                fillcolor('maroon')
            else:
                fillcolor('black')
            begin_fill()
        goto(x0, y1)
        goto(x1, y1)
        goto(x1, y0)
        goto(x0, y0)
        if self.cells[ax][ay] != 0:
            end_fill()
        penup()

    def cell_center(self, pos):
        x = self.origin.x + self.cell_size * pos.x + self.cell_size // 2
        y = self.origin.y + self.cell_size * pos.y + self.cell_size // 2
        return XY(x, y)


class Player:
    def __init__(self, _shape, field, size):
        shape(_shape)
        turtlesize(size, size)
        penup()
        self.field = field
        self.pos = None

    def up(self):
        self.step(XY(0, 1))


    def down(self):
        self.step(XY(0, -1))

    def left(self):
        self.step(XY(-1, 0))

    def right(self):
        self.step(XY(1, 0))

    def step(self, shift):
        npos = self.pos + shift
        if self.field.isallowed(npos):
            self.move(npos)
        if npos == XY(9, 9):
            ans = textinput("Вы прошли уровень!", 'Продолжить игру?')
            while True:
                if ans == "да":
                    clearscreen()
                    main()
                    break
                if ans == 'нет':
                    bye()
                    break
                else:
                    ans = textinput("Неверный ввод. Ппробуй ещё раз.", 'Введи только да или нет')


    def go(self, pos):
        self.move(pos)
        onkeypress(self.up, "Up")
        onkeypress(self.down, "Down")
        onkeypress(self.left, "Left")
        onkeypress(self.right, "Right")
        listen()
        mainloop()

    def move(self, pos):
        apos = self.field.cell_center(pos)
        goto(apos.x, apos.y)
        self.pos = pos
        update()


def main():
    field = Field(XY(10, 10), 37)
    player = Player('square', field, 2)
    field.draw()
    player.go(XY(0, 0))


main()
