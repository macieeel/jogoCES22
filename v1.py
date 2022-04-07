from calendar import c
from email.mime import image
import pygame
import time
import math
from utils import scale_image, blit_rotate_center

pygame.init()
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("3030: Esqueci de Liberar!")


class CameraGroup():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = pygame.image.load(
            'graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def draw(self):
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf, ground_offset)


class AbstractVehicle:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.y -= self.vel * math.cos(radians)
        self.x -= self.vel * math.sin(radians)

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration/2, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration/2, 0)

        self.move()


class PlayerVehicle(AbstractVehicle):
    IMG = RED_CAR.convert_alpha()
    START_POS = (180, 200)


def draw(win, images, player_vehicle):
    for img, pos in images:
        win.blit(img, pos)

    player_vehicle.draw(win)
    pygame.display.update()


def move_player(player_vehicle):
    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_a]:
        player_vehicle.rotate(left=True)
    if keys[pygame.K_d]:
        player_vehicle.rotate(right=True)
    if keys[pygame.K_w]:
        moving = True
        player_vehicle.move_forward()
    if keys[pygame.K_s]:
        moving = True
        player_vehicle.move_backward()

    if not moving:
        player_vehicle.reduce_speed()


FPS = 60
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_vehicle = PlayerVehicle(4, 3)

while run:

    draw(WIN, images, player_vehicle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    WIN.fill('#71ddee')

    move_player(player_vehicle)
    clock.tick(FPS)
