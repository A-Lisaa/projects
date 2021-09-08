print("Preparing for parsing")
from os import getcwd, makedirs
from os.path import exists
from time import time, sleep
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import unquote

class Grabber:
    '''
    line rule:
    <link>; [segment]
    segment can be either x:y(from x to y, x and/or y can be empty) or x,y,z,...
    segment represents position(s) in an album that will be downloaded
    '''
    line = ""
    path = ""
    start = 0
    try_counts = -1
    trying_time = 5
    
    def __init__(self):
        with open("cyberdrop_debug.txt", "w") as dbg:
            pass

    def pic_saver(self, name, href):
        with open(f"{self.path}/{name}", "wb") as code:
            code.write(get(href).content)
        return f"{name} SAVED TO {self.path}"

    def debug(self, string):
        with open("cyberdrop_debug.txt", "a") as dbg:
            dbg.write(string)
            dbg.write("\n")

    def work(self):
        if not exists(self.path):
            makedirs(self.path)
        if self.path == "":
            self.path = getcwd()
        if ";" in self.line:
            segment = self.line.split(";")[1].strip()
            self.line = self.line.split(";")[0].strip()
            if ":" in segment:
                splitted = segment.split(":")
                if splitted[0] == "":
                    splitted[0] = 0
                if splitted[1] == "":
                    soup = BeautifulSoup(get(self.line).content, "html.parser")
                    splitted[1] = int(soup.select("#totalFilesAmount")[0].text)-1
                ranging = range(int(splitted[0]), int(splitted[1])+1)
            elif "," in segment:
                ranging = segment.replace(",", "")
            else:
                ranging = segment
        else:
            soup = BeautifulSoup(get(self.line.strip()).content, "html.parser")
            ranging = range(self.start, int(soup.select("#totalFilesAmount")[0].text))
        for i in ranging:
            print(soup.select("a.image")[int(i)])
            href = soup.select("a.image")[int(i)].attrs['href']
            unquoted = unquote(href.split("/")[-1])
            try:
                string = self.pic_saver(unquoted, href)
                print(string)
                self.debug(string)
            except Exception:
                try_counter = self.try_counts
                while try_counter != 0:
                    try_counter -= 1
                    try:
                        string = self.pic_saver(unquoted, href)
                        print(string)
                        self.debug(string)
                        break
                    except Exception:
                        if self.try_counts > 0:
                            print(f"Downloading error, trying again, left {try_counter} attempt(s)")
                            self.debug(f"Downloading error, trying again, left {try_counter} attempt(s)")
                            start_time = time()
                            if int(time() - start_time) < self.trying_time:
                                sleep(self.trying_time - time() + start_time)
                        elif self.try_counts == 0:
                            print("Downloading error")
                            self.debug("Downloading error")
                        elif self.try_counts < 0:
                            print("Downloading error, trying again")
                            self.debug("Downloading error, trying again")
                            start_time = time()
                            if int(time() - start_time) < self.trying_time:
                                sleep(self.trying_time - time() + start_time)
            

grabber = Grabber()
grabber.path = f"{getcwd()}\Meggii"

with open("E:\Secret Info\Файлы\Альбомы.txt") as file:
    for line in file:
        grabber.line = line
        grabber.work()