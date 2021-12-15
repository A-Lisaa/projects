from urllib.parse import unquote
from requests import get
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.page_name = ""
        self.path = ""
        self.start_page = False
        self.stop_page = 0

    def empty_file(self):
        with open(self.path, "w") as f:
            pass

    def work(self):
        if not self.start_page:
            self.start_page = int(BeautifulSoup(get(f"{self.page_name}/1").content, "html.parser").select("div.pagination_expanded a")[0].text)
        for page in range(self.start_page, self.stop_page, -1):
            print(f"now is being parsed page {page} of {self.page_name}")
            full_page = get(f"{self.page_name}/{page}")
            soup = BeautifulSoup(full_page.content, "html.parser")
            for elem in soup.select("span.comments a"):
                if int(elem.text[-1]) > 0:
                    full_page = get(f"{self.page_name[:self.page_name.find('/', 9)]}{elem.attrs['href']}")
                    soup = BeautifulSoup(full_page.content, "html.parser")
                    for each_comment in soup.select("div.comment")[::-1]:
                        if each_comment.select("a.comment_show"):
                            continue
                        comment = each_comment.select("div")[1].text.strip()
                        date = each_comment.select("span.date")[0].text.strip()
                        time = each_comment.select("span.time")[0].text.strip()
                        link = f"{self.page_name[:self.page_name.find('/', 9)]}{each_comment.select('a.comment_link')[0].attrs['href']}"

                        full_image_select = each_comment.select("div.image a.prettyPhotoLink")
                        image_select = each_comment.select("div.image img")
                        if full_image_select:
                            image_ref = full_image_select[0].attrs['href']
                        elif each_comment.select("div.image") and not full_image_select:
                            if image_select:
                                image_ref = image_select[0].attrs['src']
                            else:
                                image_ref = "no image or image blocked"
                        else:
                            image_ref = "no image or image blocked"

                        with open(self.path, "a", encoding = "utf-8") as f:
                            f.write(f"{comment} (image link: {unquote(image_ref)}) (date: {date} time: {time}) (comment link: {link})".strip())
                            f.write("\n\n")

parser = Parser()
parser.page_name = "http://joyreactor.cc/tag/Feguimel/all"
parser.path = "Feguimel.txt"
parser.empty_file()
parser.work()