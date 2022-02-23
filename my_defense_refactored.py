import json
import os
import random
from enum import Enum
from typing import Any, Callable


class MyDefense:
    class Words(Enum):
        FIRST = "first_word"
        SECOND = "second_word"
        THIRD = "third_word"
        FOURTH = "fourth_word"

    def __init__(self):
        # Слова для припева
        self.words: dict[str, list[str]] = {
            "first_word": [
                "Солнечный", "Траурный", "Плюшевый", "Бешеный", "Памятный",
                "Трепетный", "Базовый", "Скошенный", "Преданный", "Ласковый",
                "Пойманный", "Радужный", "Огненный", "Радостный", "Тензорный",
                "Шёлковый", "Пепельный", "Ламповый", "Жареный", "Загнанный"
            ],
            "second_word": [
                "зайчик", "Верник", "глобус", "ветер", "щавель", "пёсик",
                "копчик", "ландыш", "стольник", "мальчик", "дольщик", "Игорь",
                "невод", "егерь", "пончик", "лобстер", "жемчуг", "кольщик",
                "йогурт", "овод"
            ],
            "third_word": [
                "стеклянного", "ванильного", "резонного", "широкого", "дешёвого",
                "горбатого", "собачьего", "исконного", "волшебного", "картонного",
                "лохматого", "арбузного", "огромного", "запойного", "великого",
                "бараньего", "вандального", "едрёного", "парадного", "укромного"
            ],
            "fourth_word": [
                "глаза", "плова", "Пельша", "мира", "деда", "жира", "мема",
                "ада", "бура", "жала", "нёба", "гунна", "хлама", "шума",
                "воза", "сала", "фена", "зала", "рака", "макдака"
            ]
        }

        # Захардкоденное кол-во слов в каждом списке
        self.initial_words_amount: dict[str, int] = {
            "first_word": len(self.words["first_word"]),
            "second_word": len(self.words["second_word"]),
            "third_word": len(self.words["third_word"]),
            "fourth_word": len(self.words["fourth_word"])
        }

        self.delete_word_choices = {
            "Удалить первое слово": (
                self.delete_word,
                ["first_word"],
                {}
            ),
            "Удалить второе слово": (
                self.delete_word,
                ["second_word"],
                {}
            ),
            "Удалить третье слово": (
                self.delete_word,
                ["third_word"],
                {}
            ),
            "Удалить четвертое слово": (
                self.delete_word,
                ["fourth_word"],
                {}
            ),
            "Вернуться в меню": (
                lambda: None,
                [],
                {}
            )
        }

        self.add_words_choices = {
            "Добавить первое слово": (
                self.add_word,
                ["first_word"],
                {}
            ),
            "Добавить второе слово": (
                self.add_word,
                ["second_word"],
                {}
            ),
            "Добавить третье слово": (
                self.add_word,
                ["third_word"],
                {}
            ),
            "Добавить четвертое слово": (
                self.add_word,
                ["fourth_word"],
                {}
            ),
            "Вернуться в меню": (
                lambda: None,
                [],
                {}
            )
        }

        self.main_menu_choices = {
            "Создать припев": (
                self.create_chorus,
                [
                    self.words["first_word"],
                    self.words["second_word"],
                    self.words["third_word"],
                    self.words["fourth_word"]
                ],
                {}
            ),
            "Добавить слово": (
                self.menu,
                [self.add_words_choices],
                {}
            ),
            "Удалить слово": (
                self.menu,
                [self.delete_word_choices],
                {}
            ),
            "Сбросить слова к исходному состоянию": (
                self.reset_all_words,
                [],
                {}
            ),
            "Показать возможные слова": (
                self.show_words,
                [],
                {}
            ),
            "Выход": (
                self.quit,
                [],
                {}
            )
        }

        self.active = True
        self.words = self.read_json()

    def read_json(self, filename: str = "words.json") -> dict[Any, Any]:
        if not os.path.exists(filename):
            self.write_json(self.words)
        with open(filename, "r", encoding = "utf-8") as json_file:
            return json.load(json_file)

    def write_json(self, data: dict[Any, Any], filename: str = "words.json"):
        with open(filename, "w", encoding = "utf-8") as json_file:
            json.dump(data, json_file)

    def menu(self, actions: dict[str, tuple[Callable[..., Any], list[Any], dict[str, Any]]], start_number: int = 1):
        print()
        for position, action in enumerate(actions, start=start_number):
            print(f"{position}) {action}")

        actions = {str(k): v for k, v in enumerate(actions.values(), start=start_number)}
        while True:
            answer = input("\nВведите ваш выбор: ")
            if answer in actions:
                break
            print("Неверный ввод")

        actions[answer][0](*actions[answer][1], **actions[answer][2])

    def create_chorus(self,
        first_words: list[Any],
        second_words: list[Any],
        third_words: list[Any],
        fourth_words: list[Any]
        ):
        # Проверка всех списков на пустоту
        if not all(map(lambda x: len(x) > 0, (first_words, second_words, third_words, fourth_words))):
            raise ValueError("Хотя бы один из списков слов пуст")

        first_line = f"\nОооо, моя оборона\n{random.choice(first_words)} {random.choice(second_words)} {random.choice(third_words)} {random.choice(fourth_words)}"
        second_line = f"\nОооо, моя оборона\n{random.choice(first_words)} {random.choice(second_words)} {random.choice(third_words)} {random.choice(fourth_words)}\n"

        print(first_line + second_line)
        input("Нажмите любую кнопку для продолжения")

    def add_word(self, word_list_name: str):
        word = input("\nВведите слово для добавления: ")
        if word not in self.words[word_list_name]:
            self.words[word_list_name].append(word)
            self.write_json(self.words)
            print(f"{word} добавлено в список слов")
        else:
            print(f"{word} уже в списке слов")

    def delete_word(self, word_list_name: str):
        word_list = self.words[word_list_name]
        print("Список выбранного слова:\n", *word_list)
        word = input("\nВведите слово для удаления: ")
        if word in word_list:
            self.words[word_list_name].remove(word)
            self.write_json(self.words)
            print(f"{word} удалено из списка слов")
        else:
            print(f"Нет слова {word} в списке")

    def reset_word(self, word_list_name: str):
        self.words[word_list_name] = self.words[word_list_name][:self.initial_words_amount[word_list_name]]

    def reset_all_words(self):
        for word in self.Words:
            self.reset_word(word.value)

    def show_words(self):
        for value in self.words.values():
            print(*value, "\n")

    def quit(self):
        self.active = False

    def main(self):
        while self.active:
            self.menu(self.main_menu_choices)


if __name__ == "__main__":
    my_defense = MyDefense()
    my_defense.main()
