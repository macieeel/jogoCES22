import pygame as pg

import random
from settings import *
from tilemap import collide_hit_rect
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
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def collide_between_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if len(hits) > 1:
            if hits[1].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[1].rect.left - sprite.hit_rect.width / 8
            if hits[1].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[1].rect.right + sprite.hit_rect.width / 8
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if len(hits) > 1:
            if hits[1].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[1].rect.top - sprite.hit_rect.height / 8
            if hits[1].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[1].rect.bottom + sprite.hit_rect.height / 8
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def collide_with_grass(sprite, group, default_speed):
    # list = pygame.sprite.collide_rect()
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.player_speed = default_speed
    else:
        sprite.player_speed = default_speed/2


def collect_pizza(sprite):

    l = pg.sprite.spritecollide(sprite, sprite.game.pizza, False)
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE] and l:
        sprite.game.pizza.sprites()[0].time += 1/60

    if sprite.game.pizza.sprites()[0].time > 0.8:
        sprite.qtepizzas += 1
        sprite.game.pizza.sprites()[0].time = 0
        l[0].kill()
        Pizza(sprite.game)
        sprite.game.time = 0
        pg.mixer.pause()
        sprite.game.effects_sounds['pick_pizza'].play()
        if sprite.qtepizzas % 3 == 0:
            PA(sprite.game, 6018, 5285, PA_BASE_SPEED + sprite.qtepizzas * 10)


def collide_with_PA(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

    if hits:
        sprite.game.playing = False
        if group == sprite.game.PA:
            sprite.game.go_message = "A PA te pegou"
        else:
            sprite.game.go_message = "Você não pode dirigir na água"


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

        # self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect(
            center=image.get_rect(topleft=self.pos).center)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        collide_with_grass(self, self.game.grass, PLAYER_SPEED)

        l = pg.sprite.spritecollide(self, self.game.pizza, False)

        collect_pizza(self)
        collide_with_PA(self, self.game.PA)
        collide_with_PA(self, self.game.agua)


class PA(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites, game.PA
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.PA_img
        self.rect = self.image.get_rect()
        self.hit_rect = PA_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.speed = speed
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.PA_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.agua, 'x')
        # collide_between_walls(self, self.game.PA, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.agua, 'y')
        # collide_between_walls(self, self.game.PA, 'y')
        collide_with_grass(self, self.game.grass, self.speed)
        self.rect.center = self.hit_rect.center


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
    pizza_places = []

    def __init__(self, game):
        self.groups = game.all_sprites, game.pizza
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.pizza_img
        self.rect = self.image.get_rect()
        num = random.randint(0, len(Pizza.pizza_places)-1)
        self.rect.center = Pizza.pizza_places[num]
        self.game = game

        self.time = 0
        self.reference = 0


class Flecha(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.flecha_img
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

    def update(self):
        rot = (vec(self.game.pizza.sprites()[
               0].rect.center) - self.game.player.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.flecha_img, rot)


class Agua(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.agua
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
