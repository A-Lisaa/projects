import os
import sys
import random
from colorama import init, Fore
init(autoreset = True)

string = 0
harmony = 0
count_of_strings = 6
count_of_harmonys = 11
level_of_random = 2
delimiter = "."
notes = {"1.0":"E", "1.1":"F", "1.2":"F♯", "1.3":"G", "1.4":"G♯", "1.5":"A", "1.6":"B", "1.7":"B♯", "1.8":"C", "1.9":"C♯", "1.10":"D", "1.11":"D♯",
         "6.0":"E", "6.1":"F", "6.2":"F♯", "6.3":"G", "6.4":"G♯", "6.5":"A", "6.6":"B", "6.7":"B♯", "6.8":"C", "6.9":"C♯", "6.10":"D", "6.11":"D♯"}

while True:
    already_have = False
    for k in range(count_of_harmonys, -1, -1):
        if k >= 10:
            print(f"     {k}  ", end = "")
        elif 9 >= k >= 0:
            print(f"    {k}   ", end = "")
    print()
    for i in range(count_of_strings, 0, -1):
        print(i, end = " ")
        for j in range(count_of_harmonys, -1, -1):
            if random.randint(1, count_of_strings * count_of_harmonys * level_of_random) == random.randint(1, count_of_strings * count_of_harmonys * level_of_random) and already_have == False:
                already_have = True
                print(Fore.LIGHTCYAN_EX + "|-------", end = "")
                string = i
                harmony = j
            else:
                print("|-------", end = "")
        print("|")
    if already_have == False:
        os.system("cls")
    else:
        while True:
            key = str(string) + delimiter + str(harmony)
            user_choice = input("\nВведите, какая это нота в английской системе: ")
            if user_choice.replace("#", "♯") == notes.get(key):
                print("\nВсе верно\n")
                print("1) Введите 1, чтобы повторить")
                print("2) Введите 2, чтобы выйти\n")
                while True:
                    user_choice_right = input("Введите ваш выбор: ")
                    if user_choice_right == "1":
                        break
                    elif user_choice_right == "2":
                        sys.exit()
                    else:
                        input("Такого варианта ответа нет, нажмите чтобы вернуться к выбору\n")
                os.system("cls")
                break
            else:
                print("\nНеправильный ответ\n")
                print("1) Введите 1, чтобы попытаться еще раз")
                print("2) Введите 2, чтобы обновить ")
                print("3) Введите 3, чтобы выйти\n")
                while True:
                    user_choice_false = input("Введите ваш выбор: ")
                    if user_choice_false == "1":
                        break
                    elif user_choice_false == "2":
                        break
                    elif user_choice_false == "3":
                        sys.exit()
                    else:
                        input("Такого варианта ответа нет, нажмите чтобы вернуться к выбору\n")
                if user_choice_false == "2":
                    os.system("cls")
                    break