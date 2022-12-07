import os
import pygame as pg
import math
import time
import copy

# SCREEN INFO
screen_width = 800
screen_height = 700
Title = 'FARE'
FPS = 100

# screen is 40*30 grid wise
TILESIZE = 20
GRIDWIDTH = screen_width / TILESIZE
GRIDHEIGHT = screen_height / TILESIZE

# COLORS
darkmagenta = (139,0,139)
black = (0,0,0)
red = (255,0,0)
light_grey = (100, 100, 100)
grey = (50,50,50)
dark_grey = (20, 20, 20)
blue = (0,0,255)
light_blue = (100, 100, 255)
white = (255, 255, 255)
less_white = (160, 160, 160)
green = (0, 255, 0)

# list of alphabet
alphabet_list = []
for i in range(97, 123):
    alphabet_list.append(chr(i))


# FILES
FA_folder = os.path.join(os.path.dirname(__file__), "FA")



img_folder = os.path.join(os.path.dirname(__file__), "img_folder")
Main_menubg = pg.image.load(os.path.join(img_folder, "background.jpeg"))


