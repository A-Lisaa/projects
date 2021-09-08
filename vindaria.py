from urllib.parse import unquote
from requests import get
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Parser:
    start_page = int(BeautifulSoup(get(f"{self.site_name}/user/{self.username}/comments/1").content, "html.parser").select("div.pagination_expanded a")[-1].text)
    stop_page = 0

    def __init__(self):
        self.username = ""
        self.site_name = ""
        self.path = ""

    def empty_file(self):
        with open(self.path, "w") as f:
            pass

    def work(self):
        for page in range(self.start_page, self.stop_page, -1):
            print(f"now is being parsed page {page} of {self.site_name}/user/{self.username}/comments")
            full_page = get(f"{self.site_name}/user/{self.username}/comments/{page}")
            soup = BeautifulSoup(full_page.content, "html.parser")
            for each_comment in soup.select("div.comment")[::-1]:
                comment = each_comment.select("div")[1].text.strip()
                date = each_comment.select("span.date")[0].text.strip()
                time = each_comment.select("span.time")[0].text.strip()
                link = f"{self.site_name}{each_comment.select('a.comment_link')[0].attrs['href']}"

                full_image_select = each_comment.select("div.image a.prettyPhotoLink")
                image_select = each_comment.select("div.image img")
                if full_image_select:
                    image_ref = full_image_select[0].attrs['href']
                elif each_comment.select("div.image") and not full_image_select:
                    if image_select:
                        image_ref = image_select[0].attrs['src']
                else:
                    image_ref = "no image"

                with open(self.path, "a", encoding = "utf-8") as f:
                    f.write(f"{comment} (image link: {unquote(image_ref)}) (date: {date} time: {time}) (comment link: {link}) (page: {page})".strip())
                    f.write("\n\n")

parser = Parser()
parser.username = "vindaria"
parser.path = "vindaria.txt"
parser.empty_file()
parser.site_name = "http://joyreactor.cc"
parser.work()
parser.site_name = "http://pornreactor.cc"
parser.work()