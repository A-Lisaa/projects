print("PREPARING FOR PARSING")

import os
import shutil
import requests
import winsound
import time
from colorama import init as colorama_init, Fore
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
colorama_init()

class Parser():
    '''
    Required: username, start path, end path\nPossible: start page, end page
    '''
    start_page = None
    stop_page = None

    def __init__(self, username, start_path, end_path):
        self.username = username
        self.start_path = start_path
        self.end_path = end_path

        self.program_name = "".join(__file__.split('\\')[-1].split(".")[:-1])
        with open(f"{self.program_name}_debug.txt", "w") as dbg:
            pass

    def debug(self, string):
        with open(f"{self.program_name}_debug.txt", "a", encoding = "utf-8") as dbg:
            dbg.write(string)
            dbg.write("\n")

    def alphing(self, string):
        alphed_word = ""

        for word in string:
            for letter in word:
                if word.isalpha() or word.isdigit():
                    alphed_word += letter

        return alphed_word

    def comparison(self, first_string, second_string, comparison_number = 0.9):
        comparison_value = 0
        first_string_length = len(first_string)
        second_string_length = len(second_string)

        if first_string_length <= second_string_length:
            stop = first_string_length
            comparison_length = second_string_length
        else:
            stop = second_string_length
            comparison_length = first_string_length

        for i in range(stop):
            if first_string[i] == second_string[i]:
                comparison_value += 1

        if comparison_value/comparison_length >= comparison_number:
            return True

    def get_songs(self):
        songs = {}

        if not self.start_page:
            self.start_page = 1
        if not self.stop_page:
            self.stop_page = int(BeautifulSoup(requests.get(f"https://www.last.fm/user/{self.username}/loved", headers = {"user-agent": UserAgent().random}).content, "html.parser").select("li.pagination-page")[-1].text.strip())

        print(Fore.LIGHTCYAN_EX)
        for page in range(self.start_page, self.stop_page + 1):
            print(f"NOW IS BEING PARSED PAGE {page}")
            full_page = requests.get(f"https://www.last.fm/user/{self.username}/loved?page={page}", headers = {"user-agent": UserAgent().random})
            soup = BeautifulSoup(full_page.content, "html.parser")
            for song in soup.select("tr.chartlist-row"):
                artist = song.select('td.chartlist-artist')[0].text.strip()
                name = song.select('td.chartlist-name')[0].text.strip()
                if artist.strip() == "" or name.strip() == "":
                    songs[self.alphing(f"{artist} {name}").lower()] = "EMPTY ARTIST OR NAME"
                if name.endswith("."):
                    name = name[:-1]
                songs[self.alphing(f"{artist} {name}").lower()] = f"{artist} - {name}"

        return songs

    def get_music_files(self):
        music_files = {}

        for path, subdirs, files in os.walk(self.start_path):
            for name in files:
                music_files[self.alphing("".join(name.split('\\')[-1].split(".")[:-1]).strip()).lower()] = os.path.join(path, name)

        return music_files

    def copy_music_files(self):
        problems = {}
        songs = self.get_songs()
        music_files = self.get_music_files()

        if not os.path.exists(self.end_path):
            os.makedirs(self.end_path)

        print(Fore.LIGHTGREEN_EX)
        for song in songs:
            if song in music_files:
                if not os.path.exists("%s\\%s" %(self.end_path, music_files[song].split('\\')[-1])):
                    shutil.copy2(music_files[song], self.end_path)
                    print(f"COPIED {songs[song]}")
            elif songs[song] == "EMPTY ARTIST OR NAME":
                problems[song] = songs[song]
            else:
                copied = False
                for music_file in music_files:
                    if self.comparison(song, music_file):
                        if song in music_files:
                            if not os.path.exists("%s\\%s" %(self.end_path, music_files[song].split('\\')[-1])):
                                shutil.copy2(music_files[music_file], self.end_path)
                                print(f"COPIED {songs[song]}")
                            copied = True
                if not copied:
                    problems[song] = songs[song]

        if problems:
            print(Fore.LIGHTRED_EX)
            for key, value in {k: v for k, v in sorted(problems.items(), key=lambda item: item[1])}.items():
                self.debug(f"{value} ({key}) IS NOT COPIED")
                print(f"{value} ({key}) IS NOT COPIED")

parser = Parser("DvaChe59", "E:\\Матерный блатняк", "E:\\Матерный блатняк\\Loved Tracks")
#parser.stop_page = 1

parser.copy_music_files()

winsound.MessageBeep()
input("Press any key")