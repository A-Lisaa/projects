#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import shutil
import hashlib
import time

start_time = time.time()

class Main:
    start_included = []
    end_included = []

    def __init__(self, start_folder, end_folder, what_to_do, copy_destination):
        self.start_folder = start_folder
        self.end_folder = end_folder
        self.what_to_do = what_to_do
        self.copy_destination = copy_destination
        if what_to_do == 'replace':
            if not os.path.exists(copy_destination):
                os.makedirs(copy_destination)

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_folder_files_md5(self, included, folder):
        hashsums = {}

        for file in [os.path.join(path, name) for path, subdirs, files in os.walk(folder) for name in files]:
            if included:
                for inclusion in included:
                    if "\\".join(file.split("\\")[len(folder.split('\\')):len(folder.split('\\'))+len(inclusion.split("\\"))]) == inclusion:
                        hashsums[self.md5(file)] = file
            else:
                hashsums[self.md5(file)] = file

        return hashsums

    def do_magic(self):
        start_hashsums = self.get_folder_files_md5(self.start_included, self.start_folder)
        end_hashsums = self.get_folder_files_md5(self.end_included, self.end_folder)
        print(start_hashsums)
        for start_hashsum in start_hashsums:
            end_file = end_hashsums.get(start_hashsum)
            if end_file:
                if self.what_to_do == 'delete':
                    os.remove(end_file)
                elif self.what_to_do == 'replace':
                    shutil.copy2(end_file, self.copy_destination)
                    os.remove(end_file)

main = Main("F:\\Временный лагерь сталкеров\\1.6.7_Groks_Body_Health_System_Redux\\PATCH Grok's Mask", "D:\\S.T.A.L.K.E.R. Anomaly 1.5.1 build F.E.A.R\\mods\\mods\\S.T.A.L.K.E.R. Anomaly build F.E.A.R. (Сборка всегда должна быть первая в приоритете .)\\gamedata", "replace", "D:\\S.T.A.L.K.E.R. Anomaly 1.5.1 build F.E.A.R\\mods\\mods\\S.T.A.L.K.E.R. Anomaly build F.E.A.R. (Сборка всегда должна быть первая в приоритете .)\\gamedata\\copied")
main.end_included = ["configs"]
main.do_magic()

print(time.time() - start_time)