# -*- coding: utf-8 -*-
# pylint: disable = line-too-long, fixme, too-many-arguments, too-few-public-methods
import os
import time

import requests
from bs4 import BeautifulSoup

__python_version__ = 3.10
__doc__ = """
! Minimum python version is 3.10

Downloads manga and doujinsi from nhentai.net.
Gets and downloads tags of a manga.

Usage:
1) Make an instance of Grabber
2) Call method 'run'
"""
# TODO: Problems may occur when manga name is too long

print("Preparing for parsing")
class Grabber:
    """
    Main class, see file docstring
    """

    class Decorators:
        """
        Class for decorators
        """
        @classmethod
        def connecter(cls, func):
            """
            Tries to connect ot website

            Args:
                func (Callable): function to retry
            """
            def inner(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                except requests.RequestException:
                    try_counter = self.try_counts
                    while try_counter != 0:
                        try_counter -= 1
                        try:
                            result = func(self, *args, **kwargs)
                            break
                        except requests.RequestException:
                            if self.try_counts > 0:
                                print(f"Error, trying again, left {try_counter} attempt(s)")

                                start_time = time.time()
                                if int(time.time() - start_time) < self.trying_time:
                                    time.sleep(self.trying_time - time.time() + start_time)
                            elif self.try_counts == 0:
                                print("Error")

                                result = None
                            elif self.try_counts < 0:
                                print("Error, trying again")

                                start_time = time.time()
                                if int(time.time() - start_time) < self.trying_time:
                                    time.sleep(self.trying_time - time.time() + start_time)
                return result
            return inner

    def __init__(self, folder: str,
                 try_counts: int = -1, trying_time: int = 3,
                 tags_delimiter: str = "; ", tags_file: str = "tags.txt"):
        """
        Downloads doujinsis from nhentai.net

        Args:
            folder (str): folder to save doujinsi
            try_counts (int, optional): amount of downloading tries if failed, values below 0 mean infinity. Defaults to -1.
            trying_time (int, optional): to prevent fast retries, they can not be done more often than this value. Defaults to 3.
            tags_delimiter (str, optional): delimiter to split tags in one group. Defaults to "; "
            tags_file (str, optional): name of a file with tags. Defaults to "tags.txt"
        """
        self.folder = folder
        self.try_counts = try_counts
        self.trying_time = trying_time
        self.tags_delimiter = tags_delimiter
        self.tags_file = tags_file

    @staticmethod
    def replace_denied_marks(string: str) -> str:
        """
        Replaces characters denied by windows with their % analog

        Args:
            string (str): string with denied marks

        Returns:
            str: string with replaced denied marks
        """
        denied_marks = {"/":"%2F", "\\":"%5C", "*":"%2A", ":":"%3A",
                        "?":"%3F", "\"":"%22", "<":"%3C", ">":"%3E", "|":"%7C"}

        for mark, code in denied_marks.items():
            string = string.replace(mark, code)

        return string

    @staticmethod
    @Decorators.connecter
    def get_soup(link: str) -> BeautifulSoup | None:
        """
        Gets BeautifulSoup of a page

        Args:
            link (str): link to the webpage

        Returns:
            Union[BeautifulSoup, None]: BeautifulSoup if connecting is succesful, else None
        """
        return BeautifulSoup(requests.get(link).content, "html.parser")

    def get_tags(self, soup: BeautifulSoup) -> dict:
        """
        Gets tags of a doujinsi

        Args:
            soup (BeautifulSoup): BeautifulSoup of the doujinsi page

        Returns:
            dict: dictionary with tags in format "Name":"%name%", "ID":"%id%", etc.
        """
        tags = {"ID":"", "Name":"", "Parodies":"", "Characters":"", "Tags":"",
                "Artists":"", "Groups":"", "Languages":"", "Categories":"", "Pages":""}

        tags["Name"] += soup.select("h1.title")[0].text
        tags["ID"] += soup.select("#gallery_id")[0].text[1:] # From 1 because the first char is # (#123456)
        for tag_container in soup.select("div.tag-container")[:-1]: # To -1 because the last tag is Uploaded
            for name in tag_container.select("span.name"):
                tags[tag_container.contents[0].strip()[:-1]] += name.text.strip() + self.tags_delimiter # To -1 because the last char is : (Pages:)

        return tags

    @staticmethod
    @Decorators.connecter
    def download_page(link: str, manga_folder: str):
        """
        Downloads one page of manga

        Args:
            link (str): link to a page
            manga_folder (str): folder in which the page will be downloaded
        """
        with open(f"{manga_folder}\\{link.split('/')[-1]}", "wb") as file:
            file.write(requests.get(link).content)

    def manga_page_parser(self, link: str, first_page: int = 1, last_page: int = None):
        """
        Parses manga page and downloads pics and tags

        Args:
            link (str): link to a manga page
            first_page (int, optional): first page of a manga to download. Defaults to 1.
            last_page (int, optional): last page of manga to download. Defaults to None.
        """
        soup = self.get_soup(link)
        tags = self.get_tags(soup)
        if last_page is None:
            last_page = int(tags["Pages"].strip("; ")) + 1
        manga_folder = f"{self.folder}\\{self.replace_denied_marks(tags['Name'])}"
        if not os.path.exists(manga_folder):
            os.makedirs(manga_folder)

        # Downloads pages from first_page to last_page
        for img in soup.select("img.lazyload")[first_page:last_page+1]: # From 1 because of cover, to Pages+1 because of Thumbs
            data_src = img.attrs['data-src'].split('/')
            page, extension = os.path.splitext(data_src[-1])
            img_link = f"https://i.nhentai.net/galleries/{data_src[-2]}/{page[:-1]}{extension}"

            self.download_page(img_link, manga_folder)

            # Adds manga ID to the end of each picture code
            with open(f"{manga_folder}\\{page[:-1]}{extension}", "a", encoding = "utf-8") as file:
                file.write(f"\nID:{tags['ID']}")

            print(f"{img_link} SAVED TO {manga_folder}")

        # Writes tags to a file
        with open(f"{manga_folder}\\{self.tags_file}", "w", encoding = "utf-8") as file:
            for tag, value in tags.items():
                file.write(f"{tag}: {value.strip()}\n")

    def run(self, link: str):
        """
        Main method, call this with manga link as an argument.

        Args:
            link (str): link to a manga page
        """
        self.manga_page_parser(link)

if __name__ == "__main__":
    grabber = Grabber("F:\\H")
    with open("E:\\Secret Info\\Файлы\\Циферки.txt", encoding = "utf-8") as manga_file:
        for manga in manga_file:
            grabber.run(manga.strip())
