import os
import math
import imghdr
from PIL import Image
from threading import Thread

class StartThread(Thread):
    end_folder = "E:\Эротические фотокарточки\На обои (по цветам краев)\Увеличенные"
    height_folder = "E:\Эротические фотокарточки\На обои (по цветам краев)\Малый размер"

    def __init__(self, name, files):
        Thread.__init__(self)
        self.name = name
        self.files = files

    def run(self):
        for file in self.files:
            if imghdr.what(f"E:\Эротические фотокарточки\На обои (по цветам краев)\{file}") in ("png", "jpeg", "bmp"):
                im = Image.open(f"E:\Эротические фотокарточки\На обои (по цветам краев)\{file}")
                with open("enlargement_existing_files.txt", "a", encoding = "utf-8") as f:
                    f.write(file)
                    f.write("\n")
                if im.height < 1000:
                    im.save("{}\\{}".format(self.height_folder, file))
                    continue
                left_strip = im.crop((0, 0, 1, im.height))
                right_strip = im.crop((im.width-1, 0, im.width, im.height))

                enl_im = Image.new(im.mode, (int(im.height*1.77), im.height))
                enl_im.paste(im, (int(enl_im.width/2-im.width/2), 0))
                for width in range(int(enl_im.width/2-im.width/2)+3):
                    enl_im.paste(left_strip, (width, 0))
                    enl_im.paste(right_strip, (enl_im.width-width, 0))
                enl_im.save("{}\\{}".format(self.end_folder, file))

                print(f"{self.name} ENLARGED {file}")

threads_amount = 24

existing_files = []

if not os.path.exists("enlargement_existing_files.txt"):
    with open("enlargement_existing_files.txt", "w"):
        pass

with open("enlargement_existing_files.txt", encoding = 'utf-8') as f:
    for line in f:
        existing_files.append(line.strip())

files = os.listdir("E:\Эротические фотокарточки\На обои (по цветам краев)")

for existing_file in existing_files:
    if existing_file in files:
        files.remove(existing_file)

files_length = len(files)

if files_length<threads_amount:
    threads_amount = files_length

for i in range(threads_amount):
    thread_files = files[math.ceil(files_length*(i/threads_amount)):math.floor(files_length*((i+1)/threads_amount)+1)]
    thread = StartThread(f"Thread {i}", thread_files)
    thread.start()