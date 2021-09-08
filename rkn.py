import sys
from torpy.http.requests import TorRequests
from fake_useragent import UserAgent

headers = {"user-agent":UserAgent().firefox, "referer": "https://..."}

with TorRequests() as tor_requests:
    print("build circuit")
    with tor_requests.get_session() as sess:
        with sess.get("http://httpbin.org/ip") as resp:
            print(resp.json())
        #with sess.get("https://reestr.rublacklist.net/api/v2/domains/json/") as resp:
        #    print(resp.json())
        with sess.get("https://img3.gelbooru.com/images/95/e3/95e37f8e9d303f5d4d579aec99689bbe.jpg", headers=headers, stream = True) as resp:
            print(sys.getsizeof(resp.text))