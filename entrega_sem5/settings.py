
import pygame as pg
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 72
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 500
PA_SPEED = 250

PLAYER_ROT_SPEED = 200

PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 83)
PA_HIT_RECT = pg.Rect(0, 0, 50, 100)

PIZZA_PLACES = [(400, 300), (800, 500), (1000, 100),
                (3100, 900), (1450, 1000), (3700, 1100), (1900, 900)]
