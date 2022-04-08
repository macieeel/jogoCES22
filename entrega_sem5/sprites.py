import pygame as pg
import pygame.sprite

import random
from settings import *
from tilemap import collide_hit_rect
from os import path
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y =  hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def collide_with_grass(sprite, group):
    #list = pygame.sprite.collide_rect()
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.player_speed = PLAYER_SPEED/2
    else:
        sprite.player_speed = PLAYER_SPEED

def collect_pizza(sprite, group):
    l = pg.sprite.spritecollide(sprite, sprite.game.pizza, False)
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        if l:
            pg.time.wait(1000)
            sprite.qtepizzas += 1
            l[0].kill()
            Pizza(sprite.game)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.player_speed = PLAYER_SPEED
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.qtepizzas = 0

    def get_pizza(self):
        self.qtepizzas += 1

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(self.player_speed, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-self.player_speed / 2, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        image = pg.transform.rotate(self.game.player_img, self.rot)
        self.image = image

        #self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect(center=image.get_rect(topleft=self.pos).center)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        collide_with_grass(self, self.game.grass)

        l = pg.sprite.spritecollide(self, self.game.pizza, False)

        collect_pizza(self, self.game.pizza)



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Grama(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.grass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Pizza(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.pizza
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load('pizza.png').convert_alpha()
        self.rect = self.image.get_rect()
        num = random.randint(0, 6)
        self.rect.center = PIZZA_PLACES[num]
        self.game = game
