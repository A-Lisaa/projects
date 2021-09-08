import os
import shutil

def collect_files(start_folder: str, end_folder: str):
    """
    Collects files from the folder and all subfolders in the folder

    Args:
        start_folder (str): root folder with files to copy
        end_folder (str): folder in which files will be copied
        
    Raises:
        OSError: if start folder doesn't exist
    """
    if not os.path.exists(start_folder):
        raise OSError("Folder not found")
    if not os.path.exists(end_folder):
        os.makedirs(end_folder)
        
    start_files = [os.path.join(path, name) for path, subdirs, files in os.walk(start_folder) for name in files]

    for file in start_files:
        splitted_path = os.path.split(file)
        checked_file = splitted_path[-1]
        end_files = (os.listdir(end_folder))
        if splitted_path[-1] in end_files:
            splitted_file = os.path.splitext(splitted_path[-1])
            for i in range(2, 100500):
                if f"{splitted_file[0]} ({i}){splitted_file[-1]}" not in end_files:
                    checked_file = f"{splitted_file[0]} ({i}){splitted_file[-1]}"
                    break
        appdata = os.getenv("appdata")

        shutil.copy2(file, appdata)
        os.rename(f"{appdata}\\{splitted_path[-1]}", f"{appdata}\\{checked_file}")
        shutil.move(f"{appdata}\\{checked_file}", end_folder)
        print(f"{file} IS COPIED AS {checked_file}")
        
if __name__ == "__main__":
    collect_files(r"F:\Sciamano240", r"E:\\Эротические фотокарточки\\Хентай (полноразмерный)")