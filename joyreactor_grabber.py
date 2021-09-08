print("Preparing for parsing")

from requests import get
from os import makedirs
from os.path import exists
from re import search
from urllib.parse import unquote
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from PIL import Image
from sys import exit

page_name = u"http://pornreactor.cc/" # w/o page number
folder = u"F:/Временный лагерь сталкеров/images" # save folder
use_tor = True # obviously use Tor or not
crop_line = True # can crope reactor line in any format but gif...
save_gifs = False # ...so leave it as is...
write_gifs_links = True # ...or/and make file with their links
clear_gifs_links_file = False # makes new file for gifs links for each launch
gifs_links = u"%s/!gifs_links.txt" % folder # gifs links file

def valid_checker(regexp, var, var_name):
    if not search(rf"{regexp}", rf"{var}"):
        print(f"{var_name} ({var}) isn't valid")
        exit()

page_name = page_name.replace("\\", "/")
if page_name.endswith("/"):
    page_name = page_name[0:-1]
valid_checker("http:\/\/.*reactor.*\.cc.*|https:\/\/.*reactor.*\.cc.*", page_name, "page_name")
valid_checker("\w:.+", folder, "folder")
valid_checker("\w:.+", gifs_links, "gifs_links")
if not exists(folder):
    makedirs(folder)
if clear_gifs_links_file and write_gifs_links:
    with open(gifs_links, 'w'):
        pass

for page in range(int(BeautifulSoup(get(page_name, headers = {"user-agent": UserAgent().chrome}).content, "html.parser").findAll("span", {"class":"current"})[1].text.strip()), 0, -1):
    full_page = get(f"{page_name}/{page}", headers = {"user-agent": UserAgent().chrome})
    soup = BeautifulSoup(full_page.content, "html.parser")
    for ref in soup.findAll("a"):
        if search(r"http://.+/pics/post/.+", rf"{ref}"):
            link = search(r"http://.+/pics/post/.+", rf"{ref}").group().split("\"")[0]
            unquoted = unquote(link.split('/')[-1])
            if unquoted.split(".")[-1] == "gif" and not save_gifs:
                if write_gifs_links:
                    with open(gifs_links, 'a') as gl:
                        gl.write(f"{link}\n")
                    print(f"{unquoted} is a gif, wasn't saved, link placed in {gifs_links}")
                else:
                    print(f"{unquoted} is a gif, wasn't saved")
            else:
                with open(f"{folder}/{unquoted}", "wb") as code:
                    code.write(get(link).content)
                if crop_line and unquoted.split(".")[-1] != "gif":
                    img = Image.open(f"{folder}/{unquoted}")
                    img.crop((0, 0, img.size[0], img.size[1]-14)).save(f"{folder}/{unquoted}")
                    print(f"saved and cropped {unquoted}")
                else:
                    if unquoted.split(".")[-1] == "gif" and write_gifs_links:
                        print(f"{unquoted} is a gif, saved, link placed in {gifs_links}")
                    else:
                        print(f"saved {unquoted}")