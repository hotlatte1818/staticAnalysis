# -*- coding: utf-8 -*-
import sys
import random

if sys.version_info[0] == 3:
    input_func = input
else:
    input_func = raw_input

EMPTY_MARK = '__'


def shuffle_field():
    items = [i for i in range(0,15)]
    items.append(EMPTY_MARK)
    random.shuffle(items)
    return  items

def print_field(field):
    for i in range(0,15,4):
        string =""
        for j in range(i,i+4):
            if field[j]<10:
                p="  "+str(field[j])
            else:
                p=" "+str(field[j])
            string += p+"  |"

        print(string)

def is_game_finished(field):
    pattern_field = [i for i in range(0,15)]
    pattern_field.append(EMPTY_MARK)
    if pattern_field == field:
        return True
    else:
        return False

def perform_move(field, key):
    i = field.index('__')
    if key == "a":
        if (i not in range(0,16,4)):
            field[i],field[i-1]= field[i-1],field[i]
        else:
            raise IndexError()
    elif key == "d":
        if i not in range(3,16,4):
            field[i],field[i+1]= field[i+1],field[i]
        else:
            raise IndexError()
    elif key == "w":
        if i not in range(0,4):
            field[i],field[i-4]= field[i-4],field[i]
        else:
            raise IndexError()
    elif key == "s":
        if i not in range(12,16):
            field[i],field[i+4]= field[i+4],field[i]
        else:
            raise IndexError()
    return field

def handle_user_input():
    key = input_func("Input direction: 'w' - up, 's' - down, 'a' - left, 'd' - right :")
    if key in['w','s','a','d']:
        return str(key)
    else:
        print(u'Incorrect direction')
        return handle_user_input()



def main():
    field = shuffle_field()
    print_field(field)
    while not is_game_finished(field):
        key = handle_user_input()
        perform_move(field, key)
        print_field(field)
    else:
        print(u"The game is over")
if __name__ == '__main__':
    main()