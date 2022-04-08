
import pygame
import sys
from random import randint
import math
from utils import scale_image


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, max_vel, rotation_vel, group):
        super().__init__(group)
        self.image = self.IMG
        self.rect = self.image.get_rect(center=self.START_POS)
        self.x, self.y = self.START_POS
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = 0.05
        self.screen = pygame.display.get_surface()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center)
        # self.image = rotated_image
        win.blit(rotated_image, new_rect.topleft)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.rect.center -= self.vel * \
            pygame.Vector2(math.sin(radians), math.cos(radians))

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration/2, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration/2, 0)

        self.move()

    def input(self):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            moving = True
            self.move_forward()
        if keys[pygame.K_s]:
            moving = True
            self.move_backward()

        if not moving:
            self.reduce_speed()

    def update(self):
        self.input()

        # self.rect.center += (self.x, self.y)
        # screen.blit(rotated_image, self.rect.topleft)


class PlayerVehicle(Vehicle):
    IMG = scale_image(pygame.image.load(
        "imgs/red-car.png"), 0.55)
    START_POS = (570, 280)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 200,
                               'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size(
        )[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size(
        )[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # ground
        self.ground_surf = pygame.image.load(
            'graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player):

        self.center_target_camera(player)
        # self.box_target_camera(player)

        # self.internal_surf.fill('#71ddee')

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        # for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     self.display_surface.blit(sprite.image, offset_pos)

        # rotated_image = pygame.transform.rotate(player.image, player.angle)
        # player.rect = rotated_image.get_rect(
        #     center=player.image.get_rect(topleft=(player.x, player.y)).center)
        # player.image = rotated_image
        # self.display_surface.blit(rotated_image, player.rect.topleft)
        player_vehicle.draw(self.display_surface)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("3030: Esqueci de Liberar!")
clock = pygame.time.Clock()


# setup
camera_group = CameraGroup()
player_vehicle = PlayerVehicle(14, 3, camera_group)

for i in range(20):
    random_x = randint(1000, 2000)
    random_y = randint(1000, 2000)
    Tree((random_x, random_y), camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('#71ddee')
    camera_group.update()
    camera_group.custom_draw(player_vehicle)

    pygame.display.update()
    clock.tick(60)
