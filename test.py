import os

music_files = {}

def alphing(string):
    alphed_word = ""

    for word in string:
        for letter in word:
            if word.isalpha() or word.isdigit():
                alphed_word += letter

    return alphed_word

for path, subdirs, files in os.walk("E:\\Матерный блатняк"):
    for name in files:
        music_files[alphing("".join(name.split('\\')[-1].split(".")[:-1]).strip()).lower()] = os.path.join(path, name)

string = "dreamtheaterehindtheevil"

for elem in music_files:
    c = 0
    start = 0
    do = True
    if elem != "dreamtheaterbehindtheevil":
        continue

    if len(elem) <= len(string):
        stop = len(elem)
        comp = len(string)
    else:
        stop = len(string)
        comp = len(elem)

    while do:
        for i in range(start, stop):
            print(start, i)
            print(elem[start:i+1], string[start:i+1])
            if elem[start:i+1] != string[start:i+1]:
                print(elem[i+1:stop+1], string[i+1:stop])
                if elem[i+1:stop] == string[i+1:stop]:
                    string = " ".join((string[start:i], string[i:]))
                print(string)
                c += 1
                start = i + 1
                break
            if i+1 == stop:
                do = False

    if c/comp < 0.15:
        print(c)
        print(elem)