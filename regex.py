from re import search

with open("Feguimel.txt", encoding = "utf-8") as f:
    for line in f:
        if search(r"https:\/\/.+|http:\/\/.+&(^http:\/\/*.reactor.cc\/.+|https:\/\/*.reactor.cc\/.+)", line):
            print(line)