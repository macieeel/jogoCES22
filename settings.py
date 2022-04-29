import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1920   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "3030: Esqueci de Liberar"
BGCOLOR = DARKGREY

TILESIZE = 72
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 200
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 72)
MAX_TIME = 100

# PA seetings
PA_BASE_SPEED = 300
PA_HIT_RECT = pg.Rect(0, 0, 50, 50)

BG_MUSIC = 'jogo.mp3'
EFFECTS_SOUNDS = {'pick_pizza': 'pick_pizza.mp3',
                  'clock': 'ticking_clock.wav',
                  'game_over': 'game_over.mp3',
                  'menu': 'tela_inicial.mp3'
                  }
