import pyautogui
import pyperclip
from random import randint, choice
from os.path import exists
from time import sleep

class Spamer:
    amount_of_lines = 200
    amount_of_chars = 200
    pause_in_hotkeys = 0
    enter_sleep = 3
    wait_after_captcha_click = 2
    wait_after_reload = 3
    wait_after_print = 0.3
    duration_of_moving_to_captcha = 0.5
    duration_of_moving_to_some_place = 0.3
    start_randint = 0
    end_randint = 255
    wait_mouse_pos = 100, 200
    doCaptcha = False
    send_isHotkey = False
    send_button = "enter"
    reload_button = "f5"
    where_chars = "self.file_strings()"
    path_to_file_strings = "green_elephant"
    path_to_captcha_image = "check_box.png"
    file_words = []
    send_hotkeys = ["ctrl", "enter"]
    copy_hotkeys = ["ctrl", "v"]

    if where_chars == "self.file_strings()":
        if exists(path_to_file_strings):
            for line in open(path_to_file_strings):
                file_words.append(line)

    def captcha(self):
        captcha_pos = pyautogui.locateCenterOnScreen(self.path_to_captcha_image)
        if captcha_pos != None:
            pyautogui.moveTo(captcha_pos, duration = self.duration_of_moving_to_captcha)
            pyautogui.click(captcha_pos)
            sleep(self.wait_after_captcha_click)
            pyautogui.press(self.reload_button)
            sleep(self.wait_after_reload)
            pyautogui.moveTo(self.wait_mouse_pos, duration = self.duration_of_moving_to_some_place)

    def random_chars(self):
        string = ""
        for j in range(self.amount_of_chars):
            string += chr(randint(self.start_randint, self.end_randint))
        return string

    def file_strings(self):
        return choice(self.file_words)

    def work(self):
        sleep(self.enter_sleep)
        for i in range(self.amount_of_lines):
            if self.doCaptcha:
                self.captcha()
            exec(f"string = {self.where_chars}")
            pyperclip.copy(locals()["string"])
            pyautogui.hotkey(self.copy_hotkeys[0], self.copy_hotkeys[1], interval = self.pause_in_hotkeys)
            if self.send_isHotkey:
                pyautogui.hotkey(self.send_hotkeys[0], self.send_hotkeys[1], interval = self.pause_in_hotkeys)
            elif not self.send_isHotkey:
                pyautogui.press(self.send_button)
            sleep(self.wait_after_print)

spamer = Spamer()
spamer.work()