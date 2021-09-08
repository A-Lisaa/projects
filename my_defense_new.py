#!/usr/bin/python3

import random
import sys
import os
import shutil

#############################################################################
# Ванильные слова
#############################################################################

word_1 = ["Солнечный", "Траурный", "Плюшевый", "Бешеный", "Памятный",
          "Трепетный", "Базовый", "Скошенный", "Преданный", "Ласковый",
          "Пойманный", "Радужный", "Огненный", "Радостный", "Тензорный",
          "Шёлковый", "Пепельный", "Ламповый", "Жареный", "Загнанный"] 

word_2 = ["зайчик", "Верник", "глобус", "ветер", "щавель", "пёсик",
          "копчик", "ландыш", "стольник", "мальчик", "дольщик", "Игорь",
          "невод", "егерь", "пончик", "лобстер", "жемчуг", "кольщик",
          "йогурт", "овод"] 

word_3 = ["стеклянного", "ванильного", "резонного", "широкого", "дешёвого",
          "горбатого", "собачьего", "исконного", "волшебного", "картонного",
          "лохматого", "арбузного", "огромного", "запойного", "великого",
          "бараньего", "вандального", "едрёного", "парадного", "укромного"]

word_4 = ["глаза", "плова", "Пельша", "мира", "деда", "жира", "мема",
          "ада", "бура", "жала", "нёба", "гунна", "хлама", "шума",
          "воза", "сала", "фена", "зала", "рака", "макдака"]

def check_file(file): 
    if not os.path.exists(file): 
        with open(file, "w"): 
            pass

wrong_choice = lambda: input("\nТакого варианта ответа нет, нажмите, чтобы вернуться к выбору\n")

def menu():
    choices = {"1":"my_defense()",
               "2":"add_word()",
               "3":"delete_word()",
               "4":"reset_all()",
               "0":"sys.exit()",
               "sosi hui":"print('sam sosi')"
               }

    print("Для создания припева, введите 1")
    print("Для добавления своих слов, введите 2")
    print("Для удаления слов, введите 3")
    print("Для сброса слов к исходному состоянию, введите 4")
    print("Для выхода, введите 0")

    choice = input("\nВведите пункт меню: ")

    exec(choices.get(choice, "wrong_choice()"))
    menu()

def my_defense(word_1 = word_1, word_2 = word_2, word_3 = word_3, word_4 = word_4):
    print(f"""
    Оооо, моя оборона
    {random.choice(word_1)} {random.choice(word_2)} {random.choice(word_3)} {random.choice(word_4)}
    Оооо, моя оборона
    {random.choice(word_1)} {random.choice(word_2)} {random.choice(word_3)} {random.choice(word_4)}
    """.replace("  ", ""))

def add_word():
    print("\nДля добавления первого слова припева, введите 1")
    print("Для добавления второго слова припева, введите 2")
    print("Для добавления третьего слова припева, введите 3")
    print("Для добавления четвертого слова припева, введите 4")
    print("Чтобы вернуться в главное меню, введите 0")

    choice = input("\nВыберите пункт меню: ")

    if choice == "0":
        return 0
    elif choice not in ("1", "2", "3", "4"):
        wrong_choice()
        add_words()

    word = input("\nВведите слово: ")

    check_file(f"files/word_{choice}")

    with open(f"files/word_{choice}", "a") as f:
        f.write(word)
        f.write("\n")

    print(f"{word} записано в список вариантов {choice}-го слова")


def del_words_func(path, num_of_list, choice_del_words):
    try:
        num_of_list.remove(del_var)
        with open(path, "a") as f:
            f.write(del_var)
            f.write("\n")
        del_words()
    except ValueError:
        print("\nТакого слова нет, проверьте правильность введенного слова\n")
        del_words()

def delete_word_func(choice):
    print(f"\nСписок слов для {choice}-го слова припева: ")
    for word in eval(f"word_{choice}"):
        print(word, end = "; ")
    print("\nСлова надо вводить так же, как они написаны в списке, регистр важен, точка и пробел с запятой не нужны\n")

    word = input("Введите слово: ")

    try:
        num_of_list.remove(del_var)
        with open(path, "a") as f:
            f.write(del_var)
            f.write("\n")
        del_words()
    except ValueError:
        print("\nТакого слова нет, проверьте правильность введенного слова\n")
        del_words()

def delete_word():
    print("\nДля удаления первого слова припева, введите 1")
    print("Для удаления второго слова припева, введите 2")
    print("Для удаления третьего слова припева, введите 3")
    print("Для удаления четвертого слова припева, введите 4")
    print("Чтобы вернуться в главное меню, введите 0")

    choice = input("\nВыберите пункт меню: ")

    if choice == "0":
        return 0
    elif choice not in ("1", "2", "3", "4"):
        wrong_choice()
        add_words()

    



## Сброс всех слов к исходному состоянию

def reset_all():
    if os.path.exists("files"):
        shutil.rmtree("files")
        if not os.path.exists("files"):
            print("Очистка слов выполнена успешно")
        elif os.path.exists("files"):
            print("Ошибка очистки слов")
   
    else:
        print("Слова уже в исходном состоянии")
        input("\nНажмите любую кнопку, чтобы перейти в меню")
   

#############################################################################
# init часть, инициализируются пользовательские слова, проводятся проверки # 
#############################################################################

## Считываем пользовательские слова из файлов и добавляем их в списки

def check_for_files(add_path = "", del_path = ""):
    if not os.path.exists("files"):
        os.mkdir("files")
    if not os.path.exists(add_path) and add_path != "":
        with open(add_path, "w") as f:
            pass
    if not os.path.exists(del_path) and del_path != "":
        with open(del_path, "w") as f:
            pass

def init_user_words(add_path, del_path, num_of_list):
    if os.path.exists(add_path):
        with open(add_path) as f: # Открываем файл с пользовательскими словами на чтение
            for line in f: # Идем построчно по файлу с пользовательскими словами
                num_of_list.append(line.rstrip()) # Добавляем слова в списки слов припева
    if os.path.exists(del_path):
        with open(del_path) as f: # Открываем файл с пользовательскими словами на чтение
            for line in f: # Идем построчно по файлу с пользовательскими словами
                num_of_list.remove(line.rstrip()) # Удаляем слова из списков слов припева с удалением пустых строк

#for i in range (1, 5):
#    init_user_words(f"files/add_word_{i}", f"files/del_word_{i}", list_of_lists[i])
#    print(list_of_lists[i])

# TODO: отмена удаления и добавления слов

#############################################################################
# Вызываем пользовательский интерфейс #
#############################################################################

menu()