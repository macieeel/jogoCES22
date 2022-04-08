# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 4
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        #self.map = Map(path.join(game_folder, 'map2.txt'))
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        self.map = TiledMap(path.join(map_folder, 'MapV1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, 'moto_V2.png')).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grass = pg.sprite.Group()
        self.pizza = pg.sprite.Group()
        my_pizza = Pizza(self)
        #self.player = Player(self, 300, 300)
        #Obstacle(self, 10,20,
         #        50,50)
        for tile_object in self.map.tmxdata.objects:
            #if tile_object.name == 'casa':
            #   pass
            #self.player = Player(self, 400, 300)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)

            if tile_object.name == 'casa':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

            if tile_object.name == 'grama':
                Grama(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)


        self.camera = Camera(self.map.width+20, self.map.height+20)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.pizza.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
