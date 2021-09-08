# -*- coding: utf-8 -*-
import os
import shutil
import requests
from pixivapi import Client, Size
from threading import Thread
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Grabber(Thread):
    def __init__(self, link):
        Thread.__init__(self)
        self.link = link

    def parser(self):
        pass

    def run(self):
        self.parser()

if __name__ == "__main__":
    thread = Grabber("https://www.pixiv.net/en/users/19591509/artworks")
    thread.start()