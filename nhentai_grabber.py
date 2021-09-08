#-*- coding: utf-8 -*-
print("Preparing for parsing")

from os import makedirs
from os.path import exists
from sys import exit
from time import time, sleep
from re import search
from fake_useragent import UserAgent
from requests import get
from bs4 import BeautifulSoup

class Grabber:
    def __init__(self):
        self.page_name = "" # name of the main page with hentai (nhentai.net/g/666666)
        self.root_folder = "" # folder for pics
        self.try_counts = -1 # amount of downloading tries if failed, values below 0 mean infinity
        self.trying_time = 3 # to prevent fast retries, they can not be done more often than this value

    def replace_denied_marks(self, name):
        denied_marks = {"/":"%2F", "\\":"%5C", "*":"%2A", ":":"%3A", "?":"%3F", "\"":"%22", "<":"%3C", ">":"%3E", "|":"%7C"}
        for mark in denied_marks:
             name = name.replace(mark, denied_marks[mark])
        return name

    def page_soup(self, link):
        while True:
            try:
                soup = BeautifulSoup(get(link).content, "html.parser")
                return soup
            except:
                pass
        
    def get_tags(self, link):
        self.tags_dict = {"Name":"", "ID":"", "Parodies":"", "Characters":"", "Tags":"", "Artists":"", "Groups":"", "Languages":"", "Categories":"", "Pages":""}
        self.tags_soup = self.page_soup(link)
        tags = self.tags_soup.select("div.tag-container")
        self.tags_dict["Name"] += self.tags_soup.select("h1.title")[0].text
        self.tags_dict["ID"] += self.tags_soup.select("#gallery_id")[0].text[1:]
        for tag in tags:
            for name in str(tag).split('<span class="name">')[1:]:
                self.tags_dict[str(tag).split(">")[1].split("<")[0].strip()[:-1]] += f'{name.split("</span>")[0]}; '
        return self.tags_dict
                
    def record_in_file(self, link):
        name = self.tags_soup.find('h1', {'class':'title'}).text
        name = self.replace_denied_marks(name)
        if len(name) > 200:
            name = f"{name[:150]}$NEVL"
        path = f"F:\\H\\{name}"
        if not exists(path):
            makedirs(path)
        with open(f"{path}\\{name}.txt", "w", encoding = "utf-8") as f:
            for tag in self.tags_dict:
                f.write(f"{tag}: {self.tags_dict.get(tag)}".strip())
                f.write("\n")
        print(f"{name} tag(s) SAVED TO {path}")

    def valid_checking(self):
        """
        Checks self.page_name for nhentai link validity and self.root_folder for folder validity with regular expressions, 
        replaces \ with /, removes / from ends, tries to convert self.try_counts to int
        """
        self.page_name = self.page_name.replace("\\", "/")
        if self.page_name.endswith("/"):
            self.page_name = self.page_name[0:-1]
        if not search(r"https:\/\/nhentai\.net\/g\/\d+", self.page_name):
            print(f"self.page_name ({self.page_name}) is not valid")
            exit()

        self.root_folder = self.root_folder.replace("\\", "/")
        if self.root_folder.endswith("/"):
            self.root_folder = self.root_folder[0:-1]
        if not search(r"\w:.+", self.root_folder):
            print(f"self.root_folder ({self.root_folder}) is not valid")
            exit()

        try:
            int(self.try_counts)
        except TypeError:
            print(f"self.try_counts is not valid ({self.try_counts}), should be convertable to a number")

        try:
            int(self.trying_time)
        except TypeError:
            print(f"self.trying_time is not valid ({self.trying_time}), should be convertable to a number")

    def work(self):
        '''
        Main method, makes folders, downloads pics
        '''
        self.valid_checking()

        extensions = []
        soup = BeautifulSoup(get(f"{self.page_name}").content, "html.parser")
        name = soup.find('h1', {'class':'title'}).text
        name = self.replace_denied_marks(name)
        name_for_folder = name
        if len(name_for_folder) > 200:
            name_for_folder = f"{name[:200]}$NEVL"
        folder = f"{self.root_folder}/{name_for_folder}"
        if not exists(folder):
            makedirs(folder)
        if len(name) > 200:
            with open(f"{folder}/full_name.txt", "w") as fname:
                fname.write(name)
        images_number = search(r"\d+", soup.find("img", {"class":"lazyload"})["data-src"]).group()

        for ext in soup.findAll("img", {"class":"lazyload"}):
            if search(rf"https:\/\/t\.nhentai\.net\/galleries\/{images_number}\/\d+t\..+", ext["data-src"]):
                extensions.append(ext["data-src"].split(".")[-1])

        for page in range(1, int(soup.findAll("span", {"class":"name"})[-1].text)+1):
            extension = extensions[page-1]
            link = f"https://i.nhentai.net/galleries/{images_number}/{page}.{extension}"
            try:
                with open(f"{folder}/{page}.{extension}", "wb") as code:
                    code.write(get(link).content)
                with open(f"{folder}/{page}.{extension}", "a") as code:
                    code.write(f"\nID:{self.tags_dict['ID']}")
                print(f"{link} SAVED TO {folder}")
            except Exception:
                try_counter = self.try_counts
                while try_counter != 0:
                    try_counter -= 1
                    try:
                        with open(f"{folder}/{page}.{extension}", "wb") as code:
                            code.write(get(link).content)
                        with open(f"{folder}/{page}.{extension}", "a") as code:
                            code.write(f"\nID:{self.tags_dict['ID']}")
                        print(f"{link} SAVED TO {folder}")
                        break
                    except Exception:
                        if self.try_counts > 0:
                            print(f"Downloading error, trying again, left {try_counter} attempt(s)")
                            start_time = time()
                            if int(time() - start_time) < self.trying_time:
                                sleep(self.trying_time - time() + start_time)
                        elif self.try_counts == 0:
                            print("Downloading error")
                        elif self.try_counts < 0:
                            print("Downloading error, trying again")
                            start_time = time()
                            if int(time() - start_time) < self.trying_time:
                                sleep(self.trying_time - time() + start_time)

grabber = Grabber()
grabber.root_folder = "F:\\H"

with open("E:\\Secret Info\\Файлы\\Циферки.txt") as file:
    for line in file:
        grabber.get_tags(line)
        grabber.record_in_file(line)
        grabber.page_name = line
        grabber.work()