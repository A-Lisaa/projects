#-*- coding: utf-8 -*-
import sys
import random
import pygame
from pygame.locals import *

pygame.init()

class Game:
    def __init__(self, fps: int = 60, screen_width: int = 600, screen_height: int = 650, field_columns: int = 4, field_rows: int = 4) -> None:
        self.fps = fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.field_columns = field_columns
        self.field_rows = field_rows
        self.tile_size = min(self.screen_width//self.field_columns, self.screen_height//self.field_rows)
            
        self.colors = {2: (255, 255, 0), 4: (255, 191, 0), 8: (255, 128, 0), 16: (255, 64, 0), 32: (255, 0, 0), 
                       64: (255, 0, 64), 128: (255, 0, 128), 256: (255, 0, 191), 512: (255, 0, 255),
                       1024: (191, 0, 255), 2048: (128, 0, 255), 4096: (64, 0, 255), 8192: (0, 0, 255), 
                       16384: (0, 64, 255), 32768: (0, 128, 255), 65536: (0, 191, 255), 131072: (0, 255, 255), 
                       262144: (0, 255, 191), 524288: (0, 255, 128), 1048576: (0, 255, 64), 2097152: (0, 255, 0), 
                       4194304: (64, 255, 0), 8388608: (128, 255, 0), 16777216: (191, 255, 0)}
        
        self.clock = pygame.time.Clock()
        self.scr = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.chance = lambda x: True if random.random() < x else False
        
    def create_text_box(self, text: str, bg_color, text_color, smooth: int = 1):
        # color = self.colors[number]
        # text_color = (255-color[0], 255-color[1], 255-color[2])
        tile_rect = pygame.Rect(((0, 0), (self.tile_size, self.tile_size)))
        pygame.draw.rect(self.scr, bg_color, tile_rect)
        font_size = int(tile_rect.width // len(text))
        font = pygame.font.SysFont("trebuchet ms", font_size)
        text = font.render(text, smooth, text_color)
        self.scr.blit(text, ((0 + tile_rect.width / 2) - text.get_width() / 2, (0 + tile_rect.height / 2) - text.get_height() / 2))
    
    def run(self):
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
            pygame.display.flip()

game = Game()
game.run()