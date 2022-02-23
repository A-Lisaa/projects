"""
Parses Loved Tracks of last.fm and copies these tracks from a folder and its subfolders to another
"""
import os
import shutil
import xml.etree.ElementTree as ET

import Levenshtein
from bs4 import BeautifulSoup
import requests
from colorama import Fore, init as colorama_init

colorama_init()


API_KEY = "5b786ecb2cbb8a330422ab32b84be32e"


def alphing(string: str, change_symbol: str = "") -> str:
    alphed_word = str()

    for word in string:
        for letter in word:
            if not word.isalpha() and not word.isdigit():
                letter = change_symbol
            alphed_word += letter

    return alphed_word



def get_songs(username: str, start_page: int = 1, stop_page: int | None = None) -> dict[str, str]:
    songs = {}
    if stop_page is None:
        page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getLovedTracks&user={username}&api_key={API_KEY}", headers = {"user-agent": "loved_tracks_copier"})
        root = BeautifulSoup(page.content, features="html.parser")
        pages_amount = root.select("lovedtracks")[0]["totalpages"]
        if isinstance(pages_amount, str):
            stop_page = int(pages_amount)
        else:
            raise ValueError("Pages amount error")

    print(Fore.LIGHTCYAN_EX, end = "")
    for page in range(start_page, stop_page):
        print(f"СЕЙЧАС ПАРСИТСЯ СТРАНИЦА №{page}")
        page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&page={page}&api_key={API_KEY}", headers = {"user-agent": "loved_tracks_copier"})
        root = BeautifulSoup(page.content, features="html.parser")
        print(root.select("lovedtracks")[0].findall("track"))

        for song in root.select("lovedtracks.track"):
            name = song.find("name").text
            artist = song.find("artist").find("name").text

            if artist.strip() == "" or name.strip() == "":
                songs[alphing(f"{artist} {name}").lower()] = "EMPTY ARTIST OR NAME"
                continue

            if name.endswith("."):
                name = name[:-1]

            songs[alphing(f"{artist} {name}").lower()] = f"{artist} - {name}"

    return songs


def get_music_files(start_path: str) -> dict[str, str]:
    music_files = {}
    if not os.path.exists(start_path):
        raise OSError("start_path does not exist")

    for path, _, files in os.walk(start_path):
        for name in files:
            music_files[alphing("".join(name.split('\\')[-1].split(".")[:-1]).strip()).lower()] = os.path.join(path, name)

    return music_files


def copy_music_files():
    problems = {}
    songs = get_songs()
    music_files = get_music_files()

    if not os.path.exists(end_path):
        os.makedirs(end_path)

    print(colorama.Fore.LIGHTGREEN_EX)
    for song, song_path in songs.items():
        if song in music_files:
            if not os.path.exists(f"{end_path}\\{os.path.split(song_path)[-1]}"):
                shutil.copy2(music_files[song], end_path)
                print(f"COPIED {song_path}")
        elif song_path == "EMPTY ARTIST OR NAME":
            problems[song] = song_path
        else:
            copied = False
            for music_file, music_file_path in music_files.items():
                if Levenshtein.ratio(song, music_file) >= levenstein_minimum_ratio and song in music_files:
                    if not os.path.exists(f"{end_path}\\{os.path.split(song_path)[-1]}"):
                        shutil.copy2(music_file_path, end_path)
                        print(f"COPIED {song_path}")
                    copied = True
            if not copied:
                problems[song] = song_path

    if problems:
        print(colorama.Fore.LIGHTRED_EX)
        for key, value in dict(sorted(problems.items(), key=lambda item: item[1])):
            print(f"{value} ({key}) IS NOT COPIED")


if __name__ == "__main__":
    get_songs("DvaChe59")
