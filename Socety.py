from tkinter import *
import random
import math
import keyboard


CELL_TYPES = [
    ["#FFFFFF", False, 2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    ["#FF0000", False, 1, 1, 1, 1, 1, 1, 1],
    ["#FFFF00", False, 1, 1, 1, 1, -1, 0, 0],
    ["#00FF7F", False, 1, 1, 1, -1, -1, -1, 0],
    ["#00BFFF", False, 1, -1, -1, -1, 1, -1, 0],
    ["#FF7581", False, 1, -2, -1, 1, 2, -1, 0]
]

#UNCELL_TYPES = [
#    ["#0A0A0A", False, 0, 0, 0],
#    ["#1C080C", False, 0, 1, 1],
#    ["#2B2517", False, 0, -1, 1]
#]

TAKEN_LINES = 2
CELL_TYPES_COUNT = 6
CELLS = []
CONTROLED_CELLS = []


#   <===>Всякое техническое<===>
#<Ширина окна>
WIDTH = 960
#<Высота окна>
HEIGHT = 720
#<Тик (Раз в сколько мс происходит действие)>
TICK = 50

#   <===>Основные настройки<===>
#<Размер клетки>
CELL_SIZE = 4
#<Хитбокс клетки>
CELL_COLISION = CELL_SIZE
#<Доля артикуляции/тик>
ARTIC_PART = 7
#<Модификатор скорости клетки>
CELL_SPEED = 1
#<Скорость контролируемых клеток>
CONTROLER_CELL_SPEED = 3
#<Кол-во клеток>
COUNT = 100
#<Радиус зрения>
VISION = 100


#   <===>Преднастройки<===>
#Обычный режим
Basic_Mode = False
#Большие колонии
Big_Mode = False

if Basic_Mode == True:
    CELL_COLISION = CELL_SIZE*4
    VISION = 100
elif Big_Mode == True:
    CELL_COLISION = CELL_SIZE
    VISION = 300
    CONTROLER_CELL_SPEED = 4


class Cell:
    def __init__(self, type, cell_type, canvas, root, x, y):
        self.types = type
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.canvas = canvas
        self.root = root
        self.canvas_obj = canvas.create_oval(
            self.x, self.y, self.x + CELL_SIZE, self.y + CELL_SIZE,
            fill=self.types[self.cell_type][0], 
            outline=self.types[self.cell_type][0]
        )
        self.xartic = 0
        self.yartic = 0
        if self.types[self.cell_type][1] != False:
            self.Tailer()
    
    def Tailer(self):
        for _ in range(CELL_TYPES[self.cell_type][1]):
            tail_part = Tail(self.canvas, self.root, self.x, self.y)
        self.root.after(TICK, tail_part.move)

    def gettype(self):
        return(self.cell_type)
    
    def positive_negative(self, number):
        if number > 0:
            return(1)
        if number < 0:
            return(-1)
        if number == 0:
            return(0)
    
    def getcoords(self):
        return(self.canvas.coords(self.canvas_obj))
    
    def moveteacher(self):
        horizmovement = 0
        vertmovement = 0
        horizpositiveblock = False
        horiznegativeblock = False
        vertpositiveblock = False
        vertnegativeblock = False
        coords = self.getcoords()
        for cell in CELLS:
            if cell == self:
                continue
            modifier = 0
            cell_coords = cell.getcoords()
            cell_distanse = math.sqrt((cell_coords[0] - coords[0])**2 +(cell_coords[1] - coords[1])**2)
            if cell_distanse > VISION:
                continue
            elif cell_distanse <= VISION:
                modifier = 1
            elif HEIGHT - cell_distanse <= VISION:
                modifier = -1
            if cell_distanse < CELL_COLISION:
                if cell_coords[0] < coords[0]:
                    horiznegativeblock = True
                elif cell_coords[0] > coords[0]:
                    horizpositiveblock = True
                else:
                    continue
                if cell_coords[1] < coords[1]:
                    vertnegativeblock = True
                elif cell_coords[1] > coords[1]:
                    vertpositiveblock = True
            else:
                if cell_coords[0] < coords[0]:
                    horizmovement -= self.types[self.cell_type][cell.gettype()+TAKEN_LINES]*modifier
                elif cell_coords[0] > coords[0]:
                    horizmovement += self.types[self.cell_type][cell.gettype()+TAKEN_LINES]*modifier
                else:
                    continue
                if cell_coords[1] < coords[1]:
                    vertmovement -= self.types[self.cell_type][cell.gettype()+TAKEN_LINES]*modifier 
                elif cell_coords[1] > coords[1]:
                    vertmovement += self.types[self.cell_type][cell.gettype()+TAKEN_LINES]*modifier
                else:
                    continue
        if horiznegativeblock == True and horizmovement < 0:
            horizmovement = 0
        if horizpositiveblock == True and horizmovement > 0:
            horizmovement = 0
        if vertnegativeblock == True and vertmovement < 0:
            vertmovement = 0
        if vertpositiveblock == True and vertmovement > 0:
            vertmovement = 0
        if horizmovement == 0 and vertmovement == 0:
            horizmovement = random.randint(-1, 1)
            vertmovement = random.randint(-1, 1)
        return(round(horizmovement*CELL_SPEED), round(vertmovement*CELL_SPEED))

    def move(self):
        coords = self.getcoords()
        x, y = self.moveteacher()
        self.xartic += x
        self.yartic += y
        if coords[3] > self.canvas.winfo_height():
            xmove = round(self.xartic/ARTIC_PART)
            self.xartic -= round(self.xartic/ARTIC_PART)
            self.canvas.move(self.canvas_obj, xmove, -coords[3]+10)
            self.root.after(TICK, self.move)
        elif coords[2] > self.canvas.winfo_width():
            ymove = round(self.yartic/ARTIC_PART)
            self.yartic -= round(self.yartic/ARTIC_PART)
            self.canvas.move(self.canvas_obj, -coords[2]+10, ymove)
            self.root.after(TICK, self.move)
        elif coords[1] < 0:
            xmove = round(self.xartic/ARTIC_PART)
            self.xartic -= round(self.xartic/ARTIC_PART)
            self.canvas.move(self.canvas_obj, xmove, HEIGHT-10)
            self.root.after(TICK, self.move)
        elif coords[0] < 0:
            ymove = round(self.yartic/ARTIC_PART)
            self.yartic -= round(self.yartic/ARTIC_PART)
            self.canvas.move(self.canvas_obj, WIDTH-10, ymove)
            self.root.after(TICK, self.move)
        else:
            xmove = round(self.xartic/ARTIC_PART)
            self.xartic -= round(self.xartic/ARTIC_PART)
            ymove = round(self.yartic/ARTIC_PART)
            self.yartic -= round(self.yartic/ARTIC_PART)
            self.canvas.move(self.canvas_obj, xmove, ymove)
            self.root.after(TICK, self.move)


class Tail():
    def __init__(self, canvas, root, x, y):
            self.x = x
            self.y = y
            self.canvas = canvas
            self.root = root
            self.canvas_obj = canvas.create_oval(
                self.x, self.y, self.x + CELL_SIZE, self.y + CELL_SIZE,
                fill="#FF7581", 
                outline="#FF7581"
            )
    
    def getcoords(self):
        return(self.canvas.coords(self.canvas_obj))

    def moveteacher(self):
        horizmovement = 0
        vertmovement = 0
        coords = self.getcoords()
        for cell in CELLS:
            if cell == self:
                continue
            cell_coords = cell.getcoords()
            cell_distanse = math.sqrt((cell_coords[0] - coords[0])**2 +(cell_coords[1] - coords[1])**2)
#            if cell_distanse > VISION:
#                continue
            if cell.cell_type != 5:
                continue
            elif cell is not Tail:
                continue
            if cell_coords[0] < coords[0] and cell_distanse > CELL_COLISION:
                horizmovement -= 1
            elif cell_coords[0] > coords[0] and cell_distanse > CELL_COLISION:
                horizmovement += 1
            else:
                continue
            cell_coords = cell.getcoords()
            if cell_coords[1] < coords[1] and cell_distanse > CELL_COLISION:
                vertmovement -= 1
            elif cell_coords[1] > coords[1] and cell_distanse > CELL_COLISION:
                vertmovement += 1
            else:
                continue
        if horizmovement == 0 and vertmovement == 0:
            horizmovement = random.randint(-1, 1)
            vertmovement = random.randint(-1, 1)
        return(horizmovement, vertmovement)
    
    def move(self):
        coords = self.getcoords()
        x, y = self.moveteacher()
        if coords[3] > self.canvas.winfo_height():
#            print('Collide down')
#            print(coords)
#            self.count += 1
            self.canvas.move(self.canvas_obj, x, -coords[3]+10)
            self.root.after(TICK, self.move)
        elif coords[2] > self.canvas.winfo_width():
#            print('Collide right')
#            print(coords)
#            self.count += 1
            self.canvas.move(self.canvas_obj, -coords[2]+10, y)
            self.root.after(TICK, self.move)
        elif coords[1] < 0:
#            print('Collide up')
#            print(coords)
#            self.count += 1
            self.canvas.move(self.canvas_obj, x, HEIGHT-10)
            self.root.after(TICK, self.move)
        elif coords[0] < 0:
#            print('Collide left')
#           print(coords)
#            self.count += 1
            self.canvas.move(self.canvas_obj, WIDTH-10, y)
            self.root.after(TICK, self.move)
        else:
#           print(coords)
#            self.count += 1
            self.canvas.move(self.canvas_obj, x, y)
            self.root.after(TICK, self.move)

class Fabric:
    def __init__(self, canvas, root):
        self.count = COUNT
        self.root = root
        self.canvas = canvas

    def create_cell(self):
        for _ in range(0, self.count):
            cellx = random.randint(0, WIDTH)
            celly = random.randint(0, HEIGHT)
            cell_type = random.randint(0, 5)
            if cell_type == 0:
                the_cell = Cell(CELL_TYPES, cell_type, self.canvas, self.root, WIDTH/2, HEIGHT/2)
                CONTROLED_CELLS.append(the_cell)
            else:
                the_cell = Cell(CELL_TYPES, cell_type, self.canvas, self.root, cellx, celly)
            CELLS.append(the_cell)
            self.root.after(TICK, the_cell.move)
        
#        for _ in range(0, self.count):
#            cellx = random.randint(0, WIDTH)
#            celly = random.randint(0, HEIGHT)
#            the_cell = Cell(UNCELL_TYPES, random.randint(0, 1), self.canvas, self.root, cellx, celly)
#            CELLS.append(the_cell)
#            self.root.after(TICK, the_cell.move)

    def moveup(self):
        for cell in CONTROLED_CELLS:
            cell.yartic -=CONTROLER_CELL_SPEED*CELL_SPEED
    
    def movedown(self):
        for cell in CONTROLED_CELLS:
            cell.yartic +=CONTROLER_CELL_SPEED*CELL_SPEED
    
    def moveleft(self):
        for cell in CONTROLED_CELLS:
            cell.xartic -=CONTROLER_CELL_SPEED*CELL_SPEED
    
    def moveright(self):
        for cell in CONTROLED_CELLS:
            cell.xartic +=CONTROLER_CELL_SPEED*CELL_SPEED
    
    def stop(self):
        for cell in CONTROLED_CELLS:
            cell.xartic = 0
            cell.yartic = 0


def main():
    root = Tk()
    root.title("Society")
    root.geometry(f'{WIDTH}x{HEIGHT}')
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, background="#151f2e")
    canvas.pack(anchor=CENTER, expand=1)
    fabric = Fabric(canvas, root)
    fabric.create_cell()
    keyboard.add_hotkey("w", lambda:Fabric.moveup(Fabric))
    keyboard.add_hotkey("s", lambda:Fabric.movedown(Fabric))
    keyboard.add_hotkey("a", lambda:Fabric.moveleft(Fabric))
    keyboard.add_hotkey("d", lambda:Fabric.moveright(Fabric))
    keyboard.add_hotkey("space", lambda:Fabric.stop(Fabric))
    root.mainloop()

if __name__ == "__main__":
    main()
