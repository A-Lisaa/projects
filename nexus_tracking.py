# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.headers = {"apikey":"UzJmYW05SlIrY040bkZHdjY4UE1lQ2p3Q2FHOURldkY5NkpFY0JzdVdWSW5reldhSzczcDNobnNGUkdjeDhNMS0tNHl5K29HNTIzYzY1R0xJVzdKalJjUT09--2b9ecb816d9d0f5348f9db528505111d1deeb25f",
                        "user-agent":"nexus_tracking/0"}

    def run(self):
        page = requests.get("https://api.nexusmods.com/v1/user/tracked_mods.json", headers=self.headers)
        #print(page.headers)
        soup = str(BeautifulSoup(page.content, "html.parser"))
        for mod in json.loads(soup):
            print(mod["mod_id"], mod["domain_name"])

if __name__ == "__main__":
    thread = Parser()
    thread.run()