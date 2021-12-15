#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import sys
import random
import pygame
from pygame.locals import *
from configparser import ConfigParser
pygame.init()

class Settings:
    SETTINGS_PATH = "minesweeper.ini"

    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w"):
            pass

    def get_config(self):
        """
        Возвращает объект с файлом конфига
        """
        config = ConfigParser()
        config.read(self.SETTINGS_PATH)

        return config

    def get_setting(self, section, setting):
        """
        Возвращает значение из конфига
        """
        config = self.get_config()

        value = config.get(section, setting)

        return value

    def update_setting(self, section, setting, value):
        """
        Обновляет значение из конфига
        """
        config = self.get_config()

        if not config.has_section(section):
            config.add_section(section)
        config.set(section, setting, str(value))

        with open(self.SETTINGS_PATH, "w") as config_file:
            config.write(config_file)

class Game(Settings):
    def __init__(self):
        try:
            # [Graphics]
            self.fps = int(Settings.get_setting(self, "Graphics", "fps"))
            self.screen_width = int(Settings.get_setting(self, "Graphics", "screen_width"))
            self.screen_height = int(Settings.get_setting(self, "Graphics", "screen_height"))
            self.tile_size = int(Settings.get_setting(self, "Graphics", "tile_size"))
            self.font = Settings.get_setting(self, "Graphics", "font")

            # [Files]
            self.tiles_file = Settings.get_setting(self, "Files", "tiles_file")

            # [In-game]
            self.mines_amount = int(Settings.get_setting(self, "In-game", "mines_amount"))
            self.do_show_closed_tiles = bool(eval(Settings.get_setting(self, "In-game", "do_show_closed_tiles")))
            self.showable_tiles = list(eval(Settings.get_setting(self, "In-game", "showable_tiles")))
            self.do_show_everything = bool(eval(Settings.get_setting(self, "In-game", "do_show_everything")))
        except Exception:
            self.default_settings()
            self.__init__()

        self.screen_width -= self.screen_width % self.tile_size
        self.screen_height -= self.screen_height % self.tile_size

        if self.do_show_everything:
            self.showable_tiles = ["tile_0", "tile_1", "tile_2", "tile_3", "tile_4", "tile_5", "tile_6", "tile_7", "tile_8", "tile_mine"]

        self.chords = {}
        self.tile_positions = {"tile_0": (self.tile_size * 0, 0), "tile_1": (self.tile_size * 1, 0),
                               "tile_2": (self.tile_size * 2, 0), "tile_3": (self.tile_size * 3, 0),
                               "tile_4": (self.tile_size * 4, 0), "tile_5": (self.tile_size * 5, 0),
                               "tile_6": (self.tile_size * 6, 0), "tile_7": (self.tile_size * 7, 0),
                               "tile_8": (self.tile_size * 8, 0), "tile_closed": (self.tile_size * 9, 0),
                               "tile_mine": (self.tile_size * 10, 0), "tile_flag": (self.tile_size * 11, 0)}

        self.tiles_places = [(x, y) for x in range(0, self.screen_width, self.tile_size) for y in range(0, self.screen_height, self.tile_size)]

        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID()
        pygame.display.set_caption("Minesweeper")
        #pygame.display.set_icon(pygame.image.load("images/icon.ico"))

        self.clock = pygame.time.Clock()
        self.scr = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.cover = pygame.Surface((self.screen_width, self.screen_height))
        self.tiles = pygame.transform.scale(pygame.image.load(self.tiles_file), (self.tile_size * 12, self.tile_size))

    def default_settings(self):
        # [Graphics]
        Settings.update_setting(self, "Graphics", "fps", "60")
        Settings.update_setting(self, "Graphics", "screen_width", "960")#ctypes.windll.user32.GetSystemMetrics(0)
        Settings.update_setting(self, "Graphics", "screen_height", "640")#ctypes.windll.user32.GetSystemMetrics(1)
        Settings.update_setting(self, "Graphics", "tile_size", "32")
        Settings.update_setting(self, "Graphics", "font", "trebuchet ms")

        # [Files]
        Settings.update_setting(self, "Files", "tiles_file", "minesweeper_tiles.png")

        # [In-game]
        Settings.update_setting(self, "In-game", "mines_amount", "100")
        Settings.update_setting(self, "In-game", "do_show_closed_tiles", "False")
        Settings.update_setting(self, "In-game", "showable_tiles", "[]")
        Settings.update_setting(self, "In-game", "do_show_everything", "False")

    def button_pressed(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN or event.type == QUIT:
                    return True

    def write_text(self, text, x, y, length, text_color = (255, 165, 0), smooth = 1):
        font_size = int(length // (len(text)//1.75))
        font = pygame.font.SysFont(self.font, font_size)
        text = font.render(text, smooth, text_color)
        self.scr.blit(text, (x  - text.get_width() / 2, y - text.get_height() / 2))

    def place_mines(self):
        for i in range(self.mines_amount):
            xy = random.choice(self.tiles_places)
            self.tiles_places.remove(xy)
            self.chords[xy] = "tile_mine"

    def get_danger_levels(self):
        for xy in self.tiles_places:
            x, y = xy
            danger_level = 0
            danger_level_positions = [(x + self.tile_size, y),
                                      (x - self.tile_size, y),
                                      (x, y + self.tile_size),
                                      (x, y - self.tile_size),
                                      (x + self.tile_size, y + self.tile_size),
                                      (x + self.tile_size, y - self.tile_size),
                                      (x - self.tile_size, y - self.tile_size),
                                      (x - self.tile_size, y + self.tile_size)
                                      ]

            for danger_level_position in danger_level_positions:
                if danger_level_position in self.chords:
                    if self.chords[danger_level_position] == "tile_mine":
                        danger_level += 1

            self.chords[xy] = f"tile_{danger_level}"

    def show_tiles(self):
        for chord in self.chords:
            self.scr.blit(self.tiles, chord, (self.tile_positions["tile_closed"][0], self.tile_positions["tile_closed"][1], self.tile_size, self.tile_size))

    def show_closed_tiles(self):
        for chord in self.chords:
            if self.chords[chord] in self.showable_tiles:
                self.scr.blit(self.tiles, chord, (self.tile_positions[self.chords[chord]][0], self.tile_positions[self.chords[chord]][1], self.tile_size, self.tile_size))

    def run(self):
        self.place_mines()
        self.get_danger_levels()
        self.show_tiles()
        if self.do_show_closed_tiles:
            self.show_closed_tiles()

        flags = []
        shown = []

        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    mouse = (mouse[0] - mouse[0] % self.tile_size, mouse[1] - mouse[1] % self.tile_size)
                    if event.button == 1 and mouse not in flags and mouse not in shown:
                        if self.chords[mouse] == "tile_mine":
                            self.write_text("Мина взорвалась", self.screen_width//2, self.screen_height//2 - int(self.screen_width//2 // (len("Мина взорвалась")//1.75)) - self.screen_height*0.05, self.screen_width*0.9)
                            self.write_text("Нажмите любую кнопку для выхода", self.screen_width//2, self.screen_height//2 - int(self.screen_width//2 // (len("Нажмите любую кнопку для выхода")//1.75)) + self.screen_height*0.05, self.screen_width*0.9)
                            pygame.display.update()
                            if self.button_pressed():
                                pygame.quit()
                                sys.exit()
                        if self.chords[mouse] == "tile_0":
                            possible_positions = [(mouse[0] + self.tile_size, mouse[1]),
                                                  (mouse[0] - self.tile_size, mouse[1]),
                                                  (mouse[0], mouse[1] + self.tile_size),
                                                  (mouse[0], mouse[1] - self.tile_size),
                                                  (mouse[0] + self.tile_size, mouse[1] + self.tile_size),
                                                  (mouse[0] + self.tile_size, mouse[1] - self.tile_size),
                                                  (mouse[0] - self.tile_size, mouse[1] - self.tile_size),
                                                  (mouse[0] - self.tile_size, mouse[1] + self.tile_size)
                                                  ]
                            self.scr.blit(self.tiles, mouse, (self.tile_positions[self.chords[mouse]][0], self.tile_positions[self.chords[mouse]][1], self.tile_size, self.tile_size))
                            shown.append(mouse)
                            
                            for position in possible_positions:
                                if position in ("tile_0", "tile_1", "tile_2", "tile_3", "tile_4", "tile_5", "tile_6", "tile_7", "tile_8"):
                                    self.scr.blit(self.tiles, position, (self.tile_positions[self.chords[position]][0], self.tile_positions[self.chords[position]][1], self.tile_size, self.tile_size))
                                    shown.append(position)
                        else:
                            self.scr.blit(self.tiles, mouse, (self.tile_positions[self.chords[mouse]][0], self.tile_positions[self.chords[mouse]][1], self.tile_size, self.tile_size))
                            shown.append(mouse)
                    elif event.button == 3 and mouse not in shown:
                        if mouse not in flags:
                            self.scr.blit(self.tiles, mouse, (self.tile_positions["tile_flag"][0], self.tile_positions["tile_flag"][1], self.tile_size, self.tile_size))
                            flags.append(mouse)
                        elif mouse in flags:
                            self.scr.blit(self.tiles, mouse, (self.tile_positions["tile_closed"][0], self.tile_positions["tile_closed"][1], self.tile_size, self.tile_size))
                            flags.remove(mouse)

            if len(shown) == int(self.screen_width/self.tile_size * self.screen_height/self.tile_size - self.mines_amount):
                self.write_text("Мины обезврежены", self.screen_width//2, self.screen_height//2 - int(self.screen_width//2 // (len("Мины обезврежены")//1.75)) - self.screen_height*0.05, self.screen_width*0.9)
                self.write_text("Нажмите любую кнопку для выхода", self.screen_width//2, self.screen_height//2 - int(self.screen_width//2 // (len("Нажмите любую кнопку для выхода")//1.75)) + self.screen_height*0.05, self.screen_width*0.9)
                pygame.display.update()
                if self.button_pressed():
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            pygame.display.flip()

game = Game()
game.run()