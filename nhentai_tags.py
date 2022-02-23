print("Preparing for parsing")
from os import listdir, makedirs, system
from os.path import exists
from re import match
from sys import argv
from urllib.parse import quote_plus, unquote

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import get


class Parser:
    language = ""
    use_name_language_definition = True
    check_for_pages = True
    check_images = True

    def __init__(self):
        self.program_name = argv[0].split('\\')[-1]
        with open(f"{self.program_name}_debug.txt", "w"):
            pass

    def debug(self, string):
        with open(f"{self.program_name}_debug.txt", "a", encoding = "utf-8") as dbg:
            dbg.write(string)
            dbg.write("\n")

    def replace_denied_marks(self, name):
        denied_marks = {"/":"%2F", "\\":"%5C", "*":"%2A", ":":"%3A", "?":"%3F", "\"":"%22", "<":"%3C", ">":"%3E", "|":"%7C"}
        for mark in denied_marks:
             name = name.replace(mark, denied_marks[mark])
        return name

    def get_manga_language(self, name):
        if "[English]" in name or "(English)" in name:
            return "en"
        if "[Chinese]" in name or "(Chinese)" in name:
            return "ch"
        if "[Japanese]" in name or "(Japanese)" in name:
            return "jp"

    def create_soup(self, link):
        while True:
            soup = BeautifulSoup(get(link).content, "html.parser")
            return soup

    def find_manga_search(self, search_link):
        while True:
            try:
                manga_soup = BeautifulSoup(get(search_link).content, "html.parser")
                return manga_soup
            except:
                pass

    def find_manga(self, name, path):
        if name.endswith("$NEVL"):
            with open(f"{path}\\full_name.txt") as fname:
                name = fname.read().strip()
        if name[0] == "!" or name[0] == "~":
            name = name[1:]
        while True:
            search_link = f"https://nhentai.net/search/?q={quote_plus(unquote(name).replace('_', ' '))}"
            manga_soup = self.find_manga_search(search_link)
            amount_of_manga = len(manga_soup.select("div.gallery a"))
            if amount_of_manga == 0:
                return []

            if amount_of_manga == 1:
                return f"https://nhentai.net{manga_soup.select('div.gallery a')[0].attrs['href']}"
            elif amount_of_manga > 1:
                links = []
                pages_amount = 0
                language = ""
                manga_files = listdir(path)
                if self.use_name_language_definition:
                    language = self.get_manga_language(name)
                if not language and self.language:
                    language = self.language

                if language:
                    for manga_name in manga_soup.select("a.cover"):
                        if self.get_manga_language(manga_name) == language:
                            links.append(f"https://nhentai.net{manga_name.attrs['href']}")
                    if len(links) == 1:
                        return links[0]
                if self.check_for_pages:
                    for file in manga_files:
                        if file.split(".")[0].isnumeric():
                            pages_amount += 1
                    for manga_name in manga_soup.select("a.cover"):
                        manga_link = f"https://nhentai.net{manga_name.attrs['href']}"
                        if manga_link in links:
                            self.get_tags(manga_link)
                            if not self.tags_dict["Pages"][:-2] == str(pages_amount):
                                links.remove(manga_link)
                    if len(links) == 1:
                        return links[0]
                if self.check_images:
                    soup = ""
                    for manga_name in manga_soup.select("a.cover"):
                        isIdenticImageFiles = True
                        manga_link = f"https://nhentai.net{manga_name.attrs['href']}"
                        if not soup:
                            soup = self.create_soup(manga_link)
                        for image in soup.select("img.lazyload"):
                            image_src = image.attrs['data-src']
                            if match(r"https:\/\/t\.nhentai\.net\/galleries\/.+\/*\dt\..+", image_src):
                                if image_src.split("/")[-1].replace("t", "") not in manga_files:
                                    isIdenticImageFiles = False
                        if not isIdenticImageFiles:
                            links.remove(manga_link)
                    if len(links) == 1:
                        return links[0]
                if not links:
                    for i in range(len(manga_soup.select("div.gallery a"))):
                        links.append(f"https://nhentai.net{manga_soup.select('div.gallery a')[i].attrs['href']}")
                    return links

    def get_tags(self, link):
        self.tags_dict = {"Name":"", "ID":"", "Parodies":"", "Characters":"", "Tags":"", "Artists":"", "Groups":"", "Languages":"", "Categories":"", "Pages":""}
        self.tags_soup = self.create_soup(link)
        tags = self.tags_soup.select("div.tag-container")
        self.tags_dict["Name"] += self.tags_soup.select("h1.title")[0].text
        self.tags_dict["ID"] += self.tags_soup.select("#gallery_id")[0].text[1:]
        for tag in tags[1:]:
            for name in str(tag).split('<span class="name">')[1:]:
                self.tags_dict[str(tag).split(">")[1].split("<")[0].strip()[:-1]] += f'{name.split("</span>")[0]}; '

    def record_in_file(self, path = "."):
        if not exists(path):
            makedirs(path)
        path = path.replace("\\", "/")
        path = f"{'/'.join(path.split('/')[:-1])}/{self.replace_denied_marks(path.split('/')[-1])}"
        with open(f"{path}/tags.txt", "w", encoding = "utf-8") as f:
            for tag in self.tags_dict:
                f.write(f"{tag}: {self.tags_dict[tag]}".strip())
                f.write("\n")
        

parser = Parser()
parser.language = "en"
for manga_name in listdir("X:\\H\\Додзинси"):
    txt_exists = False
    manga_folder_filelist = listdir(f"X:\\H\\Додзинси\\{manga_name}")
    if exists(f"X:\\H\\Додзинси\\{manga_name}\\full_name.txt"):
        manga_folder_filelist.remove("full_name.txt")
    for elem in manga_folder_filelist:
        if match(r".+\.txt", elem):
            txt_exists = True
    if not txt_exists:
        found_link = parser.find_manga(manga_name, f"X:\\H\\Додзинси\\{manga_name}")
        if type(found_link) == str:
            parser.get_tags(found_link)
            parser.record_in_file(f"X:\\H\\Додзинси\\{manga_name}")
            print(f"{manga_name} tag(s) SAVED TO X:\\H\\Додзинси\\{manga_name}")
        elif type(found_link) == list and len(found_link) == 0:
            print(f"FOR {manga_name} LINKS WERE NOT FOUND")
            parser.debug(f"FOR {manga_name} LINKS WERE NOT FOUND")
        elif type(found_link) == list:
            print(f"FOR {manga_name} FOUND MULTIPLE LINKS: {str(['; '.join(found_link[:])][0])}")
            parser.debug(f"FOR {manga_name} FOUND MULTIPLE LINKS: {str(['; '.join(found_link[:])][0])}")

system(f"start E:/Projects/Python/source/{parser.program_name}_debug.txt")
