print("PREPARING FOR PARSING")

import os
import shutil
import requests
import xml.etree.ElementTree as ET
from colorama import init as colorama_init, Fore
colorama_init()
api_key = "5b786ecb2cbb8a330422ab32b84be32e"

class Parser():
    """
    Parses Loved Tracks of last.fm and copies those tracks from a folder and its subfolders to another
    """
    def __init__(self, username: str, start_path: str, end_path: str, start_page: int = 1, stop_page: int = None, comparison_number: float = 0.9):
        """
        Args:
            username (str): name of user whose Loved Tracks will be copied
            start_path (str): path to a folder containing music files, subfolders will also be scanned
            end_path (str): path to put copied files
            start_page (int, optional): first page to start parsing (counts from page containing most recent added tracks). Defaults to 1.
            stop_page (int, optional): last page to parse. Defaults to None.
            comparison_number (float, optional): level of identity of two strings to pass comparison check. Defaults to 0.9

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
            page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getLovedTracks&user={username}&api_key={api_key}", headers = {"user-agent":"loved_tracks_copier"})
            root = ET.fromstring(page.text)
            self.stop_page = int(root.find("lovedtracks").attrib["totalPages"])
        self.comparison_number = comparison_number

    def alphing(self, string: str) -> str:
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
                if word.isalpha() or word.isdigit():
                    alphed_word += letter

        return alphed_word

    def comparison(self, first_string: str, second_string: str) -> float:
        """
        Compares two string for their identity letter be letter

        Args:
            first_string (str): first string to compare
            second_string (str): second string to compare

        Returns:
            float: strings identity, 0.9 should be good enough
        """
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

        return comparison_value/comparison_length

    def get_songs(self) -> dict:
        """
        Gets Loved Tracks from last.fm

        Returns:
            dict: dictionary done by template: [self.alphing(f"{artist} {name}").lower()] = f"{artist} - {name}"
        """
        songs = {}
        print(Fore.LIGHTCYAN_EX, end = "")
        
        for page in range(self.start_page, self.stop_page):
            print(f"PAGE {page} IS BEING PARSED")
            page = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={self.username}&page={page}&api_key={api_key}", headers = {"user-agent": "loved_tracks_copier"})
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

    def get_music_files(self) -> dict:
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
        Tries to copy Loved Tracks from start_path
        """
        problems = {}
        songs = self.get_songs()
        music_files = self.get_music_files()

        if not os.path.exists(self.end_path):
            os.makedirs(self.end_path)

        print(Fore.LIGHTGREEN_EX)
        for song in songs:
            if song in music_files:
                if not os.path.exists(f"{self.end_path}\\{os.path.split(music_files[song])[-1]}"):
                    shutil.copy2(music_files[song], self.end_path)
                    print(f"COPIED {songs[song]}")
            elif songs[song] == "EMPTY ARTIST OR NAME":
                problems[song] = songs[song]
            else:
                copied = False
                for music_file in music_files:
                    if self.comparison(song, music_file) >= self.comparison_number and song in music_files:
                        if not os.path.exists(f"{self.end_path}\\{os.path.split(music_files[song])[-1]}"):
                            shutil.copy2(music_files[music_file], self.end_path)
                            print(f"COPIED {songs[song]}")
                        copied = True
                if not copied:
                    problems[song] = songs[song]

        if problems:
            print(Fore.LIGHTRED_EX)
            for key, value in {k: v for k, v in sorted(problems.items(), key=lambda item: item[1])}.items():
                print(f"{value} ({key}) IS NOT COPIED")
                
    def start(self):
        """
        Method to start program
        """
        self.copy_music_files()
        
if __name__ == "__main__":
    parser = Parser("DvaChe59", "E:\\Матерный блатняк", "E:\\Матерный блатняк\\Loved Tracks")
    parser.start()