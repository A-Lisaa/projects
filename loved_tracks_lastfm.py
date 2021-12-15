# -*- coding: utf-8 -*-
# pylint: disable = line-too-long, fixme, too-many-arguments

"""
"""

import os
import shutil
import xml.etree.ElementTree as ET

import colorama
import Levenshtein
import requests

colorama.init()

API_KEY = "5b786ecb2cbb8a330422ab32b84be32e"

print("PREPARING FOR PARSING")
class Parser:
    """
    Parses Loved Tracks of last.fm and copies those tracks from a folder and its subfolders to another
    """
    def __init__(self, username: str,
                 start_path: str, end_path: str,
                 start_page: int = 1, stop_page: int | None = None,
                 levenstein_minimum_ratio: float = 0.9):
        """
        Args:
            username (str): name of user whose Loved Tracks will be copied
            start_path (str): path to a folder containing music files, subfolders will also be scanned
            end_path (str): path to put copied files
            start_page (int, optional): first page to start parsing (counts from page containing most recent added tracks). Defaults to 1.
            stop_page (int, optional): last page to parse. Defaults to None.
            levenstein_minimum_ratio (float, optional): level of identity of two strings to pass comparison check. Defaults to 0.9

        Raises:
            OSError: raised if start_path does not exist
        """
        self.username = username
        self.start_path = start_path
        if not os.path.exists(start_path):
            raise OSError("start_path does not exist")
        self.end_path = end_path
        self.start_page = start_page
        if stop_page is None:
            page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getLovedTracks&user={username}&api_key={API_KEY}", headers = {"user-agent": "loved_tracks_copier"})
            root = ET.fromstring(page.text)
            self.stop_page = int(root.find("lovedtracks").attrib["totalPages"])
        else:
            self.stop_page = stop_page
        self.levenstein_minimum_ratio = levenstein_minimum_ratio

    def alphing(self, string: str, change_symbol: str = "") -> str:
        """
        Removes non-alphabet characters and non-digits from a string

        Args:
            string (str): string to be made alphabetic

        Returns:
            str: alphabetic string
        """
        alphed_word = ""

        for word in string:
            for letter in word:
                if not word.isalpha() and not word.isdigit():
                    letter = change_symbol
                alphed_word += letter

        return alphed_word

    def get_songs(self) -> dict[str, str]:
        """
        Gets Loved Tracks from last.fm

        Returns:
            dict: dictionary done by template: [self.alphing(f"{artist} {name}").lower()] = f"{artist} - {name}"
        """
        songs = {}
        print(colorama.Fore.LIGHTCYAN_EX, end = "")

        for page in range(self.start_page, self.stop_page):
            print(f"PAGE {page} IS BEING PARSED")
            page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={self.username}&page={page}&api_key={API_KEY}", headers = {"user-agent": "loved_tracks_copier"})
            root = ET.fromstring(page.text)

            for song in root.find("lovedtracks").findall("track"):
                name = song.find("name").text
                artist = song.find("artist").find("name").text

                if artist.strip() == "" or name.strip() == "":
                    songs[self.alphing(f"{artist} {name}").lower()] = "EMPTY ARTIST OR NAME"
                    continue

                if name.endswith("."):
                    name = name[:-1]

                songs[self.alphing(f"{artist} {name}").lower()] = f"{artist} - {name}"

        return songs

    def get_music_files(self) -> dict[str, str]:
        """
        Gets all music files from start_path

        Returns:
            dict: dictionary done by template: [self.alphing("".join(name.split('\\')[-1].split(".")[:-1]).strip()).lower()] = os.path.join(path, name)
        """
        music_files = {}
        for path, _, files in os.walk(self.start_path):
            for name in files:
                music_files[self.alphing("".join(name.split('\\')[-1].split(".")[:-1]).strip()).lower()] = os.path.join(path, name)
        return music_files

    def copy_music_files(self):
        """
        Copies Loved Tracks from start_path
        """
        problems = {}
        songs = self.get_songs()
        music_files = self.get_music_files()

        if not os.path.exists(self.end_path):
            os.makedirs(self.end_path)

        print(colorama.Fore.LIGHTGREEN_EX)
        for song, song_path in songs.items():
            if song in music_files:
                if not os.path.exists(f"{self.end_path}\\{os.path.split(song_path)[-1]}"):
                    shutil.copy2(music_files[song], self.end_path)
                    print(f"COPIED {song_path}")
            elif song_path == "EMPTY ARTIST OR NAME":
                problems[song] = song_path
            else:
                copied = False
                for music_file, music_file_path in music_files.items():
                    if Levenshtein.ratio(song, music_file) >= self.levenstein_minimum_ratio and song in music_files:
                        if not os.path.exists(f"{self.end_path}\\{os.path.split(song_path)[-1]}"):
                            shutil.copy2(music_file_path, self.end_path)
                            print(f"COPIED {song_path}")
                        copied = True
                if not copied:
                    problems[song] = song_path

        if problems:
            print(colorama.Fore.LIGHTRED_EX)
            for key, value in dict(sorted(problems.items(), key=lambda item: item[1])):
                print(f"{value} ({key}) IS NOT COPIED")

    def start(self):
        """
        Method to start program
        """
        self.copy_music_files()

if __name__ == "__main__":
    parser = Parser("DvaChe59", "E:\\Матерный блатняк", "E:\\Матерный блатняк\\Loved Tracks", stop_page=2)
    parser.start()
