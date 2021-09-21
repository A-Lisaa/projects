import os
import hashlib
import shutil
import statistics
import time
import sqlite3
from PIL import Image, UnidentifiedImageError
from threading import Thread
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class StartThread(Thread):
    files = []
    counter = 1
    
    def __init__(self, name, db_name, pixel_group = 1, check_value = 25):
        Thread.__init__(self)
        self.name = name
        self.pixel_group = pixel_group
        self.check_value = check_value

        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        
    def get_file_md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def comparison(self, img, mode_lab_color, pixel_width):
        compared_pixels = 0
        for pixel_height in range(0, img.height-1, self.pixel_group):
            r, g, b, _ = img.getpixel((pixel_width, pixel_height))
            lab_pixel_color = convert_color(sRGBColor(r, g, b), LabColor)
            if delta_e_cie2000(lab_pixel_color, mode_lab_color) <= self.check_value:
                compared_pixels += 1
        return compared_pixels

    def edges_mono_check(self, img):
        colors = []
        img = img.crop((0, img.height*0.1, img.width, img.height*0.9))

        for pixel_height in range(0, img.height-1, self.pixel_group):
            colors.append(img.getpixel((0, pixel_height)))
            colors.append(img.getpixel((img.width-1, pixel_height)))
                
        modes = statistics.multimode(colors)
        modes_length = len(modes)
        red, green, blue = 0, 0, 0
        for mode in modes:
            red += mode[0]
            green += mode[1]
            blue += mode[2]
        red /= modes_length
        green /= modes_length
        blue /= modes_length
        mode_lab_color = convert_color(sRGBColor(red, green, blue), LabColor)

        compared_pixels = self.comparison(img, mode_lab_color, 0)
        compared_pixels += self.comparison(img, mode_lab_color, img.width-1)
        percentage = compared_pixels/(img.height*2/self.pixel_group)

        return percentage

    def run(self):
        print(f"{self.name} has been launched\n", end="")
        while len(StartThread.files) > 0:
            file = StartThread.files.pop(0)
            
            try:
                img = Image.open(file)
            except UnidentifiedImageError:
                continue
            
            try:
                monochrome = self.edges_mono_check(img.convert("RGBA"))
            except Exception:
                monochrome = -1

            md5 = self.get_file_md5(file)
            resolution = img.width/img.height
            current_time = time.localtime()
            addition_date = time.strftime("%d.%m.%Y", current_time)
            addition_time = time.strftime("%H:%M:%S", current_time)

            values = (md5, file, img.width, img.height, resolution, monochrome, self.check_value, addition_date, addition_time)
            self.cur.execute("INSERT INTO files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", values)
            self.conn.commit()
            print(f"{self.name} CHECKED {file} ({StartThread.counter}/{len(StartThread.files)})\n", end="")
            StartThread.counter += 1

class Main():
    def __init__(self, db_name = "wallpaper.db"):
        self.db_name = db_name

        if not os.path.exists(self.db_name):  
            with open(self.db_name, "w"):
                pass
        self.mkdbcopy()

    def mkdbcopy(self):
        appdata = os.getenv("appdata")
        copy_db_name = f"{os.path.splitext(self.db_name)[0]}_copy{os.path.splitext(self.db_name)[1]}"

        shutil.copy2(self.db_name, appdata)
        try:
            os.rename(f"{appdata}\\{self.db_name}", f"{appdata}\\{copy_db_name}")
        except FileExistsError:
            os.remove(f"{appdata}\\{copy_db_name}")
            os.rename(f"{appdata}\\{self.db_name}", f"{appdata}\\{copy_db_name}")
        shutil.copy2(f"{appdata}\\{copy_db_name}", os.getcwd())
        os.remove(f"{appdata}\\{copy_db_name}")
        
    def mkdb(self, start_folder, threads_amount = 24):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cur = conn.cursor()

        # TODO: md5 instead of path as key, path is needed but not as key
        cur.execute("""CREATE TABLE IF NOT EXISTS files(
            md5 TEXT PRIMARY KEY,
            path TEXT,
            width INT,
            height INT,
            resolution INT,
            monochrome INT,
            max_deviation INT,
            addition_date TEXT,
            addition_time TEXT
            );
        """)
        conn.commit()

        cur.execute("SELECT * FROM files;")
        db_files = (file[0] for file in cur.fetchall())
        conn.close()

        all_files = []
        for path, _, files in os.walk(start_folder):
            for name in files:
                fpath = os.path.join(path, name)
                if fpath not in db_files:
                    all_files.append(fpath)
        files_length = len(all_files)

        StartThread.files = all_files

        if files_length < threads_amount:
            threads_amount = files_length

        for i in range(threads_amount):
            thread = StartThread(f"Thread {i}", self.db_name)
            thread.start()

    def copy(self, condition, end_folder):
        if not os.path.exists(end_folder):
            os.makedirs(end_folder)
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cur = conn.cursor()

        cur.execute("PRAGMA table_info(files);")
        columns_data = cur.fetchall()
        columns_names = [item[1] for item in columns_data]
        columns_types = []
        for item in columns_data:
            convert_types_dict = {"TEXT":"str", "NUMERIC":"int", "INTEGER":"int", "INT":"int", "REAL":"float"}
            columns_types.append(convert_types_dict[item[2].upper()])

        cur.execute("SELECT * FROM files ORDER BY path ASC;")
        for file in cur.fetchall(): # TODO: md5 implementation
            file = list(file)
            file[0] = file[0].replace("\\", "/")
            for i, cell in enumerate(file):
                exec(f"{columns_names[i]} = {columns_types[i]}(\"{cell}\")")
            if eval(condition):
                eval("shutil.copy2(path, end_folder)")

if __name__ == "__main__":
    main = Main(db_name = "test.db")
    main.mkdb("E:\\Эротические фотокарточки\\Хентай (полноразмерный)")
    # main.copy("0.95 < monochrome <= 0.98", "E:\\Эротические фотокарточки\\На обои (по цветам краев)")