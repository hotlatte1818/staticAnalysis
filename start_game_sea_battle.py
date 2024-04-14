# -*- coding: utf-8 -*-

import sys
import random
import time


from models import *

SLEEP_PLACING = 1           #Задержка времени при размещении кораблей
SLEEP_BATTLE = 1            #Задержка времени при выстрелах

RULES = {
    "1":4,
    "2":3,
    "3":2,
    "4":1
}
FIELD_SIZE = 10

COMP_PLAYER1 = "Computer_1"
COMP_PLAYER2 = "Computer_2"

EMPTY_SQUARE = 0
SHIP_HERE = 1
SHIP_AREA = 2
SHOT_FAULT = 3
SHOT_SUCCESS = 4
SHIP_KILLED = 5
SHIP_KILLED_AREA = 6

GAME_STAGE_SHIPS_ADDING = 1
GAME_STAGE_BATTLE = 2

SEPARATOR = "__________________________________________________________________________________________________________"

#________________________________________________________________________________________________________________
if sys.version_info[0]==3:
    input_func = input
else:
    input_func = raw_input

#________________________________________________________________________________________________________________
def print_2_fields(fields, order, enemy, game_stage):

    def dec_str(n):
        number = (" " if n<10 else "")+str(n)
        return number

    f1 = fields[0]
    f2 = fields[1]
    #f1.print_field()
    #f2.print_field()

    print(" ")

    print("  {}{}{}".format(f1," "*(20-len(str(f1))+26),f2))
    print(u"  |A|B|C|D|E|F|G|H|I|J                      |A|B|C|D|E|F|G|H|I|J")

    for j in range(0,f1.size):
        line = dec_str(j+1)
        for i in range(0,f1.size * 2 + 20):
            if i==30: line = line + dec_str(j+1)
            if i < f1.size:
                line = line +f1.square(j,i,game_stage is not GAME_STAGE_BATTLE)
            elif (i >= f1.size and i<f1.size + 20):
                line = line + " "
            elif i >= f1.size + 20:
                line = line + f2.square(j,i - f1.size - 20, game_stage is not GAME_STAGE_BATTLE)
            else:
                    line = line + "???"

        print(line)

    if game_stage == GAME_STAGE_BATTLE:
        print("{}{}".format(" " *(10 if order == 1 else 52), "/\\"))
        print("{}{}".format(" " *(10 if order == 1 else 52), "||"))
        print("{}{}".format(" " *(6 if order == 1 else 48), "   ENEMY"))
    print(SEPARATOR)

#________________________________________________________________________________________________________________
def coord_convert(xy):

    letter_coord = {
        "a":1,
        "b":2,
        "c":3,
        "d":4,
        "e":5,
        "f":6,
        "g":7,
        "h":8,
        "i":9,
        "j":10,
    }

    y = xy[0].lower()

    correct = 0
    if y in letter_coord:
        correct = correct + 1
    else:
        pass

    if len(xy)==2:
        x = xy[1]
    elif len(xy)==3:
        x = xy[1:3]
    else:
        x = "?"

    try:
        if int(x) in range(1,11):
            correct = correct + 1
            x = int(x)
        else:
            pass
    except:
        pass

    if correct == 2:
        y = letter_coord[y] -1
        x = x -1

        return x, y, True
    else:
        return 0, 0, False

#________________________________________________________________________________________________________________
def coord_to_text(x,y):
    collums = {
        0:"a",
        1:"b",
        2:"c",
        3:"d",
        4:"e",
        5:"f",
        6:"g",
        7:"h",
        8:"i",
        9:"j",
    }
    coord = str(collums[y])+ str(x + 1)
    return coord

#________________________________________________________________________________________________________________
def ship_add_input(player, field, ships_storage):

    x_stroka = 0
    y_stolbec = 0

    ships_left, ships_left_null = ships_left_to_add(player, field, ships_storage, True)
    ship_param0 = ai_adding_ships(player, field, ships_storage)
    while True:
        try:
            if player.ai_mode == False:
                ship_param0 = input_func("---->> Новый корабль: {}, введите через пробел Координату(f5), Размер(1|2|3|4), Направление (1|2): ".format(player.name))
            else:
                print(u"Выбираю, куда расположить корабль ...")
                ship_param0 = ai_adding_ships(player, field, ships_storage)
            print("---->> Игрок {} ввел параметры корабля: {}".format(player.name, ship_param0))
            ship_param = ship_param0.split()

            all_correct = 0

            ship_type = int(ship_param[1])
            ship_direct = int(ship_param[2])
            x_stroka , y_stolbec, coord_correct = coord_convert(ship_param[0])


            if ship_type in range(1,5):
                all_correct += 1
            else:
                pass

            if ship_direct in range(1,3):
                all_correct += 1
            else:
                pass

            if coord_correct == True:
                all_correct += 1


                if able_to_place_ship(ship_type, x_stroka, y_stolbec, ship_direct, field):
                    all_correct += 1
                else: print("-ERROR-- Корабль накладывается на зоны других кораблей, выбери другое расположение{}".format(""))


            else:
                print(u"-ERROR-- Не все параметры введены верно, введите снова")

            if ship_direct == 1:
                if y_stolbec  + ship_type <= field.size: all_correct += 1
                else: print(u"-ERROR-- Корабль не помещается в поле, введите заново")

            if ship_direct == 2:
                if x_stroka  + ship_type <= field.size: all_correct += 1
                else: print(u"-ERROR-- Корабль не помещается в поле, введите заново")

            ships_left, ships_left_null = ships_left_to_add(player, field, ships_storage, False)
            if ships_left[str(ship_type)] - 1 >= 0: all_correct += 1
            else: print("-ERROR-- Кораблей типа {} больше нельзя поставить на поле, введи заново".format(ship_type))

            if all_correct == 6: break
        except:
            print(u"-ERROR-- Введено с ошибкой, введите снова")
            continue


    ship_new = Ships(player, ship_type, x_stroka, y_stolbec, ship_direct, ships_storage, field)


    print("-Есть!-- Добавлен корабль: {}".format(ship_new))

    ships_left, ships_left_null = ships_left_to_add(player, field, ships_storage, False)

    return ships_left_null

#________________________________________________________________________________________________________________
def area_free_to_add_or_shot(field, game_stage):
    free_area = []
    for row, i in enumerate(field.field):
        for collum, j in enumerate(i):
            if game_stage == GAME_STAGE_SHIPS_ADDING:

                if j[0] in ([EMPTY_SQUARE]):
                    free_area.append([row, collum])
                else:
                    pass

            elif game_stage == GAME_STAGE_BATTLE:
                if j[0] in [EMPTY_SQUARE, SHIP_AREA, SHIP_HERE]:
                    free_area.append([row, collum])
                else:
                    pass
            else:
                pass

    return free_area

#________________________________________________________________________________________________________________
def ship_area_func(ship_type, x_stroka, y_stolbec, ship_direct):
        area = []
        for i in range(-1, ship_type+1):
            if ship_direct == 1:
                for xi in range(-1,2):
                    if x_stroka + xi in range(0,10) and y_stolbec + i in range(0,10):
                        area.append([x_stroka + xi, y_stolbec +i])


            if ship_direct == 2:
                for yi in range(-1,2):
                    if y_stolbec + yi in range(0,10) and x_stroka + i in range(0,10):
                        area.append([x_stroka + i, y_stolbec +yi])
        return area
#________________________________________________________________________________________________________________
def new_ship_coords(ship_type, x_stroka, y_stolbec, ship_direct):
        area = []
        for i in range(0, ship_type):
            if ship_direct == 1:
                if x_stroka in range(0,10) and y_stolbec + i in range(0,10):
                    area.append([x_stroka, y_stolbec +i])


            if ship_direct == 2:
                if y_stolbec in range(0,10) and x_stroka + i in range(0,10):
                    area.append([x_stroka + i, y_stolbec])
        return area
#________________________________________________________________________________________________________________
def able_to_place_ship(ship_type, x_stroka, y_stolbec, ship_direct, field):
    for i in new_ship_coords(ship_type, x_stroka, y_stolbec, ship_direct):
        if i not in area_free_to_add_or_shot(field, GAME_STAGE_SHIPS_ADDING):
            return False
    return True

#________________________________________________________________________________________________________________

def ships_left_to_add(player, field, ships_storage, print_or_not):

    ships_left = RULES.copy()
    ships_left_null = False

    for ship_type in sorted(RULES):

        n = 0
        for i in ships_storage.box:
            if i.type == int(ship_type) and i.player == player: n += 1
        ships_left.update({ship_type: RULES[ship_type] - n})

        if print_or_not: print(" ------- Корблей типа {}: добавлено {} штук, еще можно добавить {} штук".format(ship_type, n, RULES[ship_type]-n))

    any_left_to_add = 0
    for key in ships_left:
        any_left_to_add += ships_left[key]
    if any_left_to_add ==0: ships_left_null = True

    return ships_left, ships_left_null
#________________________________________________________________________________________________________________
def next_order(order):
    if order == 0:
        order = 1
        enemy = 0
    else:
        order = 0
        enemy = 1

    return order, enemy
#________________________________________________________________________________________________________________
def shot(players, fields, order, enemy, ships_storage):
    hit = False
    victory = False

    coord_correct = False
    while not coord_correct:
        while True:
            if players[order].ai_mode == False:
                x_stroka, y_stolbec, coord_correct = coord_convert(input_func("---->> Игрок {}!, стреляй! (введи координату, например f5):".format(players[order].name)))
            else:
                print("---->>Игрок {}: думаю, куда стрелять ...".format(players[order].name))
                ai_xy = ai_shots(players[enemy],fields[enemy],ships_storage)
                print("---->>Игрок {}: мой выстрел: {}".format(players[order].name, ai_xy))
                x_stroka, y_stolbec, coord_correct = coord_convert(ai_xy)
                time.sleep(SLEEP_BATTLE)

            err_message = u"-Нет!- Так стрелять нельзя, стреляй заново"
            if coord_correct:
                if [x_stroka, y_stolbec] in area_free_to_add_or_shot(fields[enemy], GAME_STAGE_BATTLE):
                    break
                else:
                    print(err_message)
                    continue
            else:
                print(err_message)
                continue

    for i in range(1,5):
        print(" |")
    print(" V")


    if isinstance(fields[enemy].field[x_stroka][y_stolbec][1],Ships):
        fields[enemy].field[x_stroka][y_stolbec][0] = SHOT_SUCCESS
        ship = fields[enemy].field[x_stroka][y_stolbec][1]
        ship.lives -= 1
        hit = True

        if ship.lives == 0:
            print(u"-Да!-- Уррраааа!!! Корабль убит!")
            if ship.d == 1:
                for i in range(0, ship.type):
                    fields[enemy].field[ship.x][ship.y + i][0] = SHIP_KILLED
            if ship.d == 2:
                for i in range(0, ship.type):
                    fields[enemy].field[ship.x + i][ship.y][0] = SHIP_KILLED


            for i in ship.ship_area():

                if fields[enemy].field[i[0]][i[1]][0] == SHIP_AREA:
                    fields[enemy].field[i[0]][i[1]][0] = SHIP_KILLED_AREA
                else:
                    pass



            n = 0
            for sh in ships_storage.box:
                if sh.player == players[enemy]: n = n + sh.lives

            if n == 0:
                print(u"-Да!-- ПОБЕДА!!! Все корабли уничтожены!")

                victory = True
        else:
            print(u"-Да!-- Попадание, снова твой выстрел!")
            players[order].shots_count += 1

    else:
        fields[enemy].field[x_stroka][y_stolbec][0] = SHOT_FAULT
        print(u"-Нет!- Промах! Переход хода!")
        players[order].shots_count += 1

    time.sleep(SLEEP_BATTLE)
    print(SEPARATOR)

    return hit, victory, players[order]
#________________________________________________________________________________________________________________
def ships_alive(players, fields, order, enemy, ships_storage):
    for sh in ships_storage.box:
        if sh.player == players[enemy]:
            print("---------Корабль типа {}:{} - подбито {}, осталось жизней {}".format(sh.type, sh.type_view, sh.type - sh.lives, sh.lives))

#________________________________________________________________________________________________________________
def ai_adding_ships(player, field, ships_storage):

    area_to_place_ships = area_free_to_add_or_shot(field, GAME_STAGE_SHIPS_ADDING)
    random.shuffle(area_to_place_ships)
    #print(area_to_place_ships)
    xy = area_to_place_ships[0]
    #print(xy)
    ships_left, ships_left_null = ships_left_to_add(player, field, ships_storage, False)
    #print(ships_left)


    if ships_left["1"]>0: ship_type = 1
    if ships_left["2"]>0: ship_type = 2
    if ships_left["3"]>0: ship_type = 3
    if ships_left["4"]>0: ship_type = 4

    #print(ship_type)
    direction = random.randint(1,2)
    #print(direction)


    ship_param0 = coord_to_text(xy[0], xy[1])+ " " + str(ship_type) + " " + str(direction)
    #print(ship_param0)
    time.sleep(SLEEP_PLACING)
    return ship_param0

#________________________________________________________________________________________________________________
def ai_shots(player, field, ships_storage):

    def square_is_able_to_shot(x, y):
        if x in range(0,10) and y in range(0,10):
            if field.field[x][y][0] in [EMPTY_SQUARE, SHIP_HERE, SHIP_AREA]: return True
        else: return False

    success_shots_count = []
    area_to_shot = []
    for x, stroka  in enumerate(field.field):
        for y, stolbec in enumerate(stroka):
            if stolbec[0] == SHOT_SUCCESS: success_shots_count.append([x,y])


    if len(success_shots_count)==0:
        area_to_shot = area_free_to_add_or_shot(field, GAME_STAGE_BATTLE)

    elif len(success_shots_count)==1:
        area_to_shot = []
        x = success_shots_count[0][0]
        y = success_shots_count[0][1]

        for ij in [[-1,0],[1,0],[0,-1],[0,1]]:
            if square_is_able_to_shot(x+ij[0], y+ij[1]):
                area_to_shot.append([x+ij[0], y+ij[1]])
            else:
                pass


    else:
        if success_shots_count[0][0] == success_shots_count[1][0]:
            ship_direction = 1
            x = success_shots_count[0][0]

        elif success_shots_count[0][1] == success_shots_count[1][1]:
            ship_direction = 2
            y = success_shots_count[0][1]

        else:print("????")
        if ship_direction == 1:
            min_y = 9

            max_y = 0
            for i in success_shots_count:
                if i[1] < min_y: min_y = i[1]
                if i[1] > max_y: max_y = i[1]
            if min_y - 1 >= 0:
                if square_is_able_to_shot(x, min_y - 1): area_to_shot.append([x, min_y - 1])
            if max_y + 1 <=9:
                if square_is_able_to_shot(x, max_y + 1): area_to_shot.append([x, max_y + 1])

        if ship_direction == 2:
            min_x = 9
            max_x = 0
            for i in success_shots_count:
                if i[0] < min_x: min_x = i[0]
                if i[0] > max_x: max_x = i[0]
            if min_x - 1 >= 0:
                if square_is_able_to_shot(min_x - 1, y): area_to_shot.append([min_x - 1, y])
            if max_x + 1 <=9:
                if square_is_able_to_shot(max_x + 1, y): area_to_shot.append([max_x + 1, y])


    random.shuffle(area_to_shot)
    x = area_to_shot[0][0]
    y = area_to_shot[0][1]
    coord = coord_to_text(x, y)

    time.sleep(SLEEP_BATTLE)
    return coord

#__________________________________________________________________________________________________________
def input_player(n):
    players = []
    ai_mode = False
    for i in range(1,n+1):
        players.append(Player(input_func(">>> Введи имя Ирока{} :".format(i)), ai_mode))
    return players

#__________________________________________________________________________________________________________
def main():
    print(SEPARATOR)
    print(u"            <<<<<  И г р а   М О Р С К О Й   Б О Й  >>>>>")


    print(u"Выбери режим игры:")
    print(u"   1. Игрок1 VS Игрок2")
    print(u"   2. Игрок VS Компьютер")
    print(u"   3. Компьютер VS Компьютер")

    players = []
    while True:
        try:
            game_options = int(input_func(">>> Твой выбор: "))
            if game_options in [1,2,3]:
                if game_options == 1:
                    players = input_player(2)
                elif game_options == 2:
                    players = input_player(1)
                    ai_mode = True
                    players.append(Player(COMP_PLAYER1, ai_mode))
                elif game_options == 3:
                    ai_mode = True
                    players.append(Player(COMP_PLAYER1, ai_mode))
                    players.append(Player(COMP_PLAYER2, ai_mode))
                else:
                    print("game_options ???")
                    continue
            else:
                print("game_options not in [1,2,3]")
                continue
            break
        except:
            print(u"Введи заново")
            continue

    field1 = Field(players[0])
    field2 = Field(players[1])
    fields = [field1, field2]
    #field1.print_field()

    ships_storage = Ships_storage()
    order = 0
    enemy = 1

    #field2.print_field()

    print(SEPARATOR)

    print_2_fields(fields, order, enemy, GAME_STAGE_SHIPS_ADDING)
    print(SEPARATOR)

    for order_i in range(0,2):
        ships_left_null = False
        print("---Добавление кораблей на поле для игрока {}".format(players[order_i].name))

        while not ships_left_null:
            ships_left_null = ship_add_input(players[order_i], fields[order_i], ships_storage)
            print_2_fields(fields, order, enemy, GAME_STAGE_SHIPS_ADDING)
        print("---ВСЕ КОРАБЛИ ДОБАВЛЕНЫ ИГРОКОМ {}".format(players[order_i].name))
        print(SEPARATOR)
    print("")
    print("---Поля укомплектованы кораблями и готовы к битве!!!")
    for i in range(1,20):
        print(" |")
    print(" V")


    order = 0
    enemy = 1
    print_2_fields(fields, order, enemy, GAME_STAGE_BATTLE)

    victory = False
    while not victory:
        hit = False
        hit, victory, winner = shot(players, fields, order, enemy, ships_storage)
        if not hit: order, enemy = next_order(order)
        print_2_fields(fields, order, enemy, GAME_STAGE_BATTLE)
    print("Игра закончена, победитель {}".format(winner.name))
    print ("")
    print("Игрок {} - победитель, сделал {} выстрелов".format(players[order].name, players[order].shots_count))
    print("Игрок {} - проигравший,  сделал {} выстрелов".format(players[enemy].name, players[enemy].shots_count))
    input_func()





#________________________________________________________________________________________________________________
if __name__ == '__main__':
    main()

#-----Вопрос 1: Когда я создаю корабль, я говорю, что это корабль Игрока1. В то же время ранее мною было создано Поле1 (экземпляр класса "Поля"), к которому привязан Игрок1.
# В классе "Корабли" мне нужен новый метод, который будет использовать атрибуды Поля1. Как мне в методе класса Корабли выйти на атрибут экземпляра класса "Поля" через атрибут экземпляра класса Игрок1
#-----Вопрос 2: Какой самый быстрый способ сортировки словаря