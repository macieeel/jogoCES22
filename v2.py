import pygame
import sys
import math
from utils import scale_image, blit_rotate_center


GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()


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

        # player.draw(screen)

        self.box_target_camera(player)
        # self.center_target_camera(player)d
        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            blit_rotate_center(self.display_surface, sprite.image,
                               (sprite.x, sprite.y), sprite.angle, offset_pos)
            # self.display_surface.blit(sprite.image, offset_pos)

        # player_vehicle.draw(self.display_surface)


class AbstractVehicle(pygame.sprite.Sprite):
    def __init__(self, max_speed, rotation_speed, group):
        super().__init__(group)
        self.max_speed = max_speed
        self.speed = 0
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05
        self.image = self.IMG
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_speed
        elif right:
            self.angle -= self.rotation_speed

    def draw(self, win):
        blit_rotate_center(win, self.image, (self.x, self.y), self.angle)

    def move_forward(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)
        self.move()

    def move_backward(self):
        self.speed = max(self.speed - self.acceleration, -self.max_speed/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.rect.center -= self.speed * \
            pygame.Vector2(math.sin(radians), math.cos(radians))
        # self.rect.center -= self.speed * math.sin(radians)

    def reduce_speed(self):
        if self.speed > 0:
            self.speed = max(self.speed - self.acceleration/2, 0)
        elif self.speed < 0:
            self.speed = min(self.speed + self.acceleration/2, 0)

        self.move()

    def update(self):
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


class PlayerVehicle(AbstractVehicle):
    IMG = RED_CAR
    START_POS = (180, 200)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("3030: Esqueci de Liberar!")
clock = pygame.time.Clock()

images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
camera_group = CameraGroup()
# player_vehicle = Player((640, 360), camera_group)
player_vehicle = PlayerVehicle(4, 3, camera_group)

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
