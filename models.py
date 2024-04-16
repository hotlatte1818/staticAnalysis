# -*- coding: utf-8 -*-

from  start_game_sea_battle import *

#________________________________________________________________________________________________________________
class Player(object):
    def __init__(self,name, ai_mode):
        self.name = name
        self.ai_mode = ai_mode
        self.shots_count = 0
    def __str__(self):
        return ("Игрок {}".format(self.name))
#________________________________________________________________________________________________________________
class Field(object):
    def __init__(self, player):
        self.size = FIELD_SIZE
        self.player = player
        self.field = []



        for i in range(0,self.size):
            self.field.append([[0,0]])
            for j in range(0,self.size-1):
                self.field[i].append([0,0])
    def __str__(self):
        return ("Поле {}".format(self.player.name))
    def square(self,x,y,opened):
        if self.field[x][y][0] == EMPTY_SQUARE:
            sq = "|_"
        elif self.field[x][y][0] == SHIP_HERE and opened == True:
            sq = "|O"
        elif self.field[x][y][0] in [SHIP_HERE,SHIP_AREA] and opened == False:
            sq = "|_"

        elif self.field[x][y][0] == SHOT_FAULT:
            sq = "|*"
        elif self.field[x][y][0] == SHOT_SUCCESS:
            sq = "|x"
        elif self.field[x][y][0] == SHIP_KILLED:
            sq = "|X"
        elif self.field[x][y][0] == SHIP_KILLED_AREA:
            sq = "|#"
        elif self.field[x][y][0] == SHIP_AREA and opened == True:
            sq = "|:"
        else:
            sq = "|?"
        return sq
    def print_field(self, opened = True):
        for j  in range(0,self.size):
            line = ""
            for i in range(0,self.size):
                line = line +self.square(j,i,opened)
            print(line)
        print(SEPARATOR)

        for row in self.field:
            print(row)
#________________________________________________________________________________________________________________
class Ships(object):
    def __init__(self, player, type, x, y, d, ship_storage, field):
        self.player = player
        self.type = type
        self.x = x
        self.y = y
        self.d = d
        ship_storage.add_ship(self)
        self.lives = type
        self.type_view = "O" * type


        for i in self.ship_area():
            field.field[i[0]][i[1]][0] = SHIP_AREA

        if d == 1:
            for i in range(0, self.type):
                field.field[x][y+i][0] = SHIP_HERE
                field.field[x][y+i][1] = self
        if d == 2:
            for j in range(0, self.type):
                field.field[x+j][y][0] = SHIP_HERE
                field.field[x+j][y][1] = self


    def __str__(self):
        return ("Корабль игрока {}, тип {}-палубный, координаты {}:{}, направление {}".format(self.player.name, self.type, self.x+1, self.y+1, self.d))


    def ship_area(self):
        return ship_area_func(self.type, self.x, self.y, self.d)

#________________________________________________________________________________________________________________
class Ships_storage(object):
    def __init__(self):
        self.box = []
    def add_ship(self, ship):
        self.box.append(ship)