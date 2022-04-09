from multiprocessing.connection import wait
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


def draw_time_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def load_data(self):
        game_folder = path.dirname(__file__)
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.title_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.map = TiledMap(path.join(map_folder, 'mapav2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(
            path.join(img_folder, 'moto_V2.png')).convert_alpha()
        self.PA_img = pg.image.load(
            path.join(img_folder, 'PA.png')).convert_alpha()
        self.flecha_img = pg.image.load(
            path.join(img_folder, 'flecha.png')).convert_alpha()
        self.pizza_img = pg.image.load(
            path.join(img_folder, 'pizza.png')).convert_alpha()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.time = 0
        self.go_message = ''
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grass = pg.sprite.Group()
        self.pizza = pg.sprite.Group()
        self.PA = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:

            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)

            if tile_object.name == 'PA':
                PA(self, tile_object.x, tile_object.y, PA_BASE_SPEED)

            if tile_object.name == 'obs':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

            if tile_object.name == 'rua':
                Grama(self, tile_object.x, tile_object.y,
                      tile_object.width, tile_object.height)

            if tile_object.name == 'pizza':
                Pizza.pizza_places.append((tile_object.x, tile_object.y))

        Pizza(self)
        self.flecha = Flecha(self)
        self.camera = Camera(self.map.width, self.map.height)

        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.time > MAX_TIME:
                self.go_message = 'Você demorou muito para entregar a pizza'
                self.playing = False
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.time += 1/60
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
            if not sprite == self.player or not self.flecha:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.screen.blit(self.flecha.image, self.flecha.rect)

        # Legendas
        draw_time_bar(self.screen, 10, 10, (MAX_TIME - self.time) / MAX_TIME)

        self.draw_text('Score: {}'.format(self.player.qtepizzas), self.hud_font, 30, RED,
                       WIDTH - 10, 10, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED,
                           WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("3030: Esqueci de Liberar", self.title_font, 80, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        start = self.draw_text("Iniciar", None, 40, WHITE,
                               WIDTH / 3, HEIGHT * 3 / 4, align="center")

        instructions = self.draw_text("Instruções", None, 40, WHITE,
                                      WIDTH * 2 / 3, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_click(start, instructions)

    def como_jogar_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Instruções", None, 70, WHITE,
                       WIDTH / 2, HEIGHT / 6, align="center")
        start = self.draw_text("Iniciar", None, 40, RED,
                               WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_click(start)

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text(self.go_message, None, 60, WHITE,
                       WIDTH / 2, HEIGHT * 2/3, align="center")
        self.draw_text("Precione ESPAÇO para tentar novamente", None, 40, WHITE,
                       WIDTH / 2, HEIGHT * 4 / 5, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def wait_for_click(self, button1, button2=False):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0] and button1.collidepoint(pg.mouse.get_pos()):
                        waiting = False
                    if button2 and pg.mouse.get_pressed()[0]:
                        if button2.collidepoint(pg.mouse.get_pos()):
                            print('hey')
                            waiting = False
                            self.como_jogar_screen()


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
