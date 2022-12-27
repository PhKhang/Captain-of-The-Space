import time
import random
import numpy
from copy import deepcopy
import pygame
from os import system
import os

MAX = 100
mapSize = 11

# CONST for the pygame
OBJ_WIDTH, OBJ_HEIGHT = 50, 50
WIN = pygame.display.set_mode((900, 600))
FPS = 60

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CHOCO = (210, 105, 30)
PINK = (255, 192, 203)

pygame.display.set_caption("The pirate of The Seven Seas")

pygame.font.init()


img1 = pygame.transform.smoothscale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (OBJ_HEIGHT, OBJ_HEIGHT))  # Hinh anh va thu nho thanh 80x80px
bullet = pygame.transform.smoothscale(pygame.image.load(
    "images/laser/laserRed01.png"), (9, 54))  # Hinh anh va thu nho thanh 80x80px
obstacle = pygame.transform.scale(pygame.image.load(
    "images/obstacle/neutron.gif"), (92, 92))
death = pygame.transform.smoothscale(pygame.image.load(
    "images/laser/laserRed11.png"), (50, 50))

# Tao mang that bu, moi phan tu la MOT VUNG HINH VUONG de tu do to mau, in hinh,... len
rects = [[0]*50 for i in range(0, 50)]  # Tao mang trong
for y in range(0, mapSize):  # Lap vao mang trong tren cac VUNG HINH VUONG
    for x in range(0, mapSize):
        rects[y][x] = (pygame.Rect(
            10 + x * OBJ_HEIGHT, 10 + y * OBJ_HEIGHT, OBJ_WIDTH, OBJ_HEIGHT))


# Variables for the game algo

# icon game
waterIcon = '~'
shipIcon = 'X'
enemyIcon = 'A'
deathIcon = '#'
obstacleIcon = '!'
bulletIcon = '.'
portalIcon = '@'
monsterIcon = '+'

shipPosX = 6
shipPosY = 9

shipStatus = 2
# 1, 9 = / -> 1
# 2, 8 = _  -> 2
# 3, 7 = \  -> 3
# 4, 6 = |  -> 4


mapList = [
    [
        ["@", "~", "~", "~", "~", "~", "~", "~", "~", "~", "@"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "!", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "!", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "A", "~", "~", "~", "~", "~", "~", "!"],
        ["!", "A", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["@", "~", "~", "~", "~", "~", "~", "~", "~", "~", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "A", "~", "~", "~", "~", "@"],
        ["~", "A", "~", "~", "!", "~", "!", "~", "~", "~", "~"],
        ["~", "~", "~", "!", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "!"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "!", "~", "A", "~", "~"],
        ["!", "!", "~", "~", "~", "~", "~", "~", "~", "!", "~"],
        ["@", "~", "~", "~", "~", "~", "~", "~", "~", "~", "@"],
    ],
    [
        ["@", "!", "~", "~", "~", "~", "~", "~", "~", "~", "@"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "A"],
        ["~", "!", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "!", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "!", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "!", "!", "~", "~", "~", "~", "~", "~", "~", "!"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "!", "~", "~", "~", "!", "~", "~", "~", "!"],
        ["~", "~", "A", "~", "~", "~", "~", "~", "~", "A", "~"],
        ["@", "~", "~", "!", "~", "~", "~", "~", "~", "!", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "A", "!", "~", "~", "~", "@"],
        ["~", "~", "~", "~", "~", "A", "~", "~", "~", "~", "~"],
        ["!", "~", "~", "A", "~", "~", "~", "~", "!", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "!", "~", "A", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["@", "~", "~", "~", "~", "~", "~", "~", "~", "A", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "A", "~", "~", "~", "~", "@"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "A", "~", "A", "~", "~", "~", "~", "~"],
        ["~", "~", "A", "~", "~", "~", "~", "~", "~", "!", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "A", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "!", "~", "~", "~", "~"],
        ["!", "~", "~", "~", "A", "!", "~", "~", "~", "~", "~"],
        ["@", "~", "!", "~", "~", "~", "~", "~", "A", "~", "@"],
    ],
    [
        ["@", "~", "!", "~", "!", "~", "~", "~", "A", "~", "@"],
        ["~", "~", "~", "~", "~", "!", "~", "~", "~", "~", "A"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "A", "!", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["A", "~", "A", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "A", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "A", "~", "~", "~", "~", "!", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["@", "~", "A", "~", "~", "~", "~", "!", "~", "~", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "~", "~", "~", "~", "~", "@"],
        ["~", "~", "~", "~", "!", "~", "~", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "!", "~", "~", "~", "~"],
        ["A", "~", "A", "~", "~", "~", "~", "~", "~", "A", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "!", "~"],
        ["~", "A", "~", "~", "~", "~", "~", "~", "~", "~", "!"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "!", "~", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "A", "~", "~"],
        ["@", "~", "~", "~", "~", "~", "A", "~", "!", "~", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "!", "~", "A", "~", "~", "@"],
        ["~", "!", "~", "~", "~", "A", "A", "~", "~", "~", "~"],
        ["~", "~", "!", "!", "~", "~", "~", "~", "A", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "!", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "A", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "A"],
        ["@", "~", "~", "A", "~", "!", "!", "~", "~", "~", "@"],
    ],
    [
        ["@", "!", "~", "~", "~", "~", "A", "~", "~", "~", "@"],
        ["~", "~", "A", "~", "~", "~", "A", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "A", "~", "~", "~", "~"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "~", "~", "A"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "A", "~", "~"],
        ["~", "A", "~", "A", "~", "~", "~", "~", "~", "A", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["@", "~", "~", "~", "~", "~", "~", "~", "!", "~", "@"],
    ],
    [
        ["@", "~", "~", "~", "~", "A", "~", "~", "~", "~", "@"],
        ["A", "~", "~", "~", "!", "A", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "!", "~", "~", "~", "~", "~", "!"],
        ["A", "~", "~", "~", "~", "~", "~", "~", "A", "~", "!"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "A"],
        ["~", "A", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["!", "~", "~", "~", "~", "~", "~", "~", "!", "A", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ["~", "!", "~", "~", "~", "A", "~", "~", "~", "~", "~"],
        ["~", "~", "~", "~", "~", "~", "~", "~", "~", "A", "A"],
        ["@", "!", "~", "~", "~", "~", "~", "~", "!", "~", "@"],
    ],
]


map = [['0']*MAX for i in range(0, MAX)]
visited = [['0']*MAX for i in range(0, MAX)]
visitedNum = 0

encouragement = ["Wow, you actually accomplished something for once.",
                 "Gamer Moment", "Great job, now you can beat my cat", ""]


class Bg(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            "images/background/frame_0_delay-0.5s.gif"), (550, 550)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            "images/background/frame_1_delay-0.5s.gif"), (550, 550)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            "images/background/frame_2_delay-0.5s.gif"), (550, 550)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            "images/background/frame_3_delay-0.5s.gif"), (550, 550)))

        self.index = 0

        self.image = self.sprites[self.index]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self):
        self.index += .06

        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[int(self.index)]


def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


class Ship(pygame.sprite.Sprite):
    def __init__(self, path="images/player/playerShip1_blue.png", size=(50, 50)):
        super().__init__()
        self.path = path
        self.size = size
        self.image = pygame.transform.smoothscale(
            pygame.image.load(self.path), size)
        self.rect = self.image.get_rect()
        self.rect.center = (285, 285)
        self.rot = 0

    def rotate(self, value=0):
        self.rot = value

    def update(self, pos=(100, 100)):
        self.rect.center = (pos[0], pos[1])
        self.image, self.rect = rot_center(pygame.transform.scale(pygame.image.load(
            self.path), self.size), self.rot, self.rect.centerx, self.rect.centery)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            "images/enemy/enemyBlack2.png"), (OBJ_HEIGHT, OBJ_HEIGHT))
        self.rect = self.image.get_rect()
        self.rot = 0

    def rotate(self, value=0):
        self.rot = value

    def update(self, pos=(100, 100)):
        self.rect.center = (pos[0], pos[1])
        self.image, self.rect = rot_center(pygame.transform.scale(pygame.image.load(
            "images/enemy/enemyBlack2.png"), (OBJ_HEIGHT, OBJ_HEIGHT)), self.rot, self.rect.centerx, self.rect.centery)


class Stuff(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprites = []

        for i in range(0, 60):
            path_name = "images/votex/" + str(i).zfill(2) + ".gif"
            image = pygame.image.load(path_name)
            self.sprites.append(pygame.transform.scale(image, (86, 86)))

        self.index = 0

        self.image = self.sprites[self.index]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def animate(self):
        self.index += .5

        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[int(self.index)]

    def update(self, x, y):
        self.rect.center = [x, y]


def write(content, color="black", pos=(900/2, 600/2), size=20, font="fonts/PressStart2P-Regular.ttf", background=0):
    text = pygame.font.Font(font, size)
    if background == 0:
        text_sur = text.render(content, False, color)
    else:
        text_sur = text.render(content, False, color, "#01051f")

    text_rec = text_sur.get_rect(center=pos)
    WIN.blit(text_sur, text_rec)


def writeLeft(content, color="black", pos=(900/2, 600/2), size=20, font="fonts/PressStart2P-Regular.ttf", background=0):
    text = pygame.font.Font(font, size)
    if background == 0:
        text_sur = text.render(content, False, color)
    else:
        text_sur = text.render(content, False, color, "#01051f")

    WIN.blit(text_sur, pos)


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(numpy.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)


def draw_window(laser=(-1, -1)):
    WIN.fill('#01051f')  # Lam DEN nguyen man hinh

    global movingBgGroup, movingCelesGroup, vot, ship

    movingBgGroup.draw(WIN)

    movingBgGroup.update()

    vot.animate()

    if laser[0] != -1:
        laserGroup.update(laser)
        laserGroup.draw(WIN)

    for i in range(0, mapSize + 1):
        draw_dashed_line(WIN, "#1C10AE", (10 + OBJ_WIDTH*i, 10),
                         (10 + OBJ_WIDTH*i, 10 + mapSize*OBJ_WIDTH), dash_length=5)
        draw_dashed_line(WIN, "#1C10AE", (10, 10 + OBJ_WIDTH*i),
                         (10 + mapSize*OBJ_WIDTH,  10 + OBJ_WIDTH*i), dash_length=5)

    dem = 0
    for y in range(0, mapSize):
        for x in range(0, mapSize):
            # pygame.draw.rect(WIN, "black", rects[y][x], 1)

            # To o 1 Cuop bien
            if (map[x][y] == enemyIcon):
                # pygame.draw.rect(WIN, RED, rects[x][y])  # To DO
                enemyGroup.update(rects[x][y].center)
                enemyGroup.draw(WIN)

            # To o 3 Dao
            if (map[x][y] == obstacleIcon):

                toaDoDatHinh = (rects[x][y].x - 20,
                                rects[x][y].y - 20)
                WIN.blit(obstacle, toaDoDatHinh)

            if (map[x][y] == portalIcon):
                # pygame.draw.rect(WIN, PINK, rects[x][y])  # To HONG
                movingCelesGroup.update(
                    rects[x][y].centerx, rects[x][y].centery)
                movingCelesGroup.draw(WIN)

            if (map[x][y] == deathIcon):
                death_rect = death.get_rect(center=rects[x][y].center)
                WIN.blit(death, death_rect)

            if (map[x][y] == monsterIcon):
                pygame.draw.rect(WIN, "cornflowerblue", rects[x][y])  # To NAU

            if (map[x][y] == bulletIcon):
                bullet_rect = bullet.get_rect(center=rects[x][y].center)
                # WIN.blit(bullet, bullet_rect)

                laserGroup.update(bullet_rect.center)
                laserGroup.draw(WIN)

            # To DO roi them hinh o duoc chon
            """ if ((x == shipPosX and y == shipPosY) and (map[x][y] != enemyIcon)):
                toaDoDatHinh = (rects[x][y].x + (100-80)/4,
                                rects[x][y].y + (100-80)/4)
                pygame.draw.rect(WIN, RED, rects[x][y])
                ship_rect = img1.get_rect(center=rects[x][y].center)
                WIN.blit(img1, ship_rect)

                shipGroup.update(rects[x][y].center) """

            # To len vien DO o co chuot hover
            if (rects[y][x].collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(WIN, RED, rects[y][x], 4)

            dem += 1

    shipGroup.draw(WIN)
    message = "LEVEL " + str(level)
    writeLeft(message, "white", (570, 50), size=40)
    message = "Bonus point: " + str(bonusTurn_score)
    writeLeft(message, "white", (570, 110))

    instruct = pygame.image.load("images/screen/instruct.png")
    WIN.blit(instruct, (560, 300))

    pygame.display.update()


def updateMap():
    for i in range(0, mapSize):
        for j in range(0, mapSize):
            print(map[i][j], end='')
        print()


def initMap(ch):
    for i in range(0, mapSize):
        for j in range(0, mapSize):
            map[i][j] = ch


def isInMap(x, y):
    return (0 <= x < mapSize and 0 <= y < mapSize)


def CheckWinCondition():
    if (map[shipPosX][shipPosY] == deathIcon):
        print(f'{map[shipPosX][ shipPosY]}')
        return -1

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            if (map[i][j] == enemyIcon):
                return 0

    return 1


def getKeyBoardInput(events):
    x = y = 0

    """ print("Your joystick :")
    print("7 8 9")  # upper left  | up          | upper right
    print("4 5 6")  # left        | fire cannon | right
    print("1 2 3")  # bottom left | bottom      | bottom right """

    global shipStatus

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                x = 1
                y = -1
                shipStatus = 1
                print("ban vua chon ", 1)

            elif event.key == pygame.K_2 or event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
                x = 1
                y = 0
                shipStatus = 2
                print("ban vua chon ", 2)

            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                x = 1
                y = 1
                shipStatus = 3
                print("ban vua chon ", 3)

            elif event.key == pygame.K_4 or event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
                x = 0
                y = -1
                shipStatus = 4
                print("ban vua chon ", 4)

            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                x = 100
                print("ban vua chon ", 'none')

            elif event.key == pygame.K_6 or event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
                x = 0
                y = 1
                shipStatus = 4
                print("ban vua chon ", 6)

            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                x = -1
                y = -1
                shipStatus = 3
                print("ban vua chon ", 7)

            elif event.key == pygame.K_8 or event.key == pygame.K_KP8 or event.key == pygame.K_UP:
                x = -1
                y = 0
                shipStatus = 2
                print("ban vua chon ", 8)

            elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                x = -1
                y = 1
                shipStatus = 1
                print("ban vua chon ", 9)

    return x, y


def playerTurn(events):
    x = y = 0
    x, y = getKeyBoardInput(events)
    global shipPosX, shipPosY

    print(f'{x = }, {y = }, {shipStatus = }, {shipPosX = } , {shipPosY = }')
    if x == 0 and y == 0:
        print("No input")
        return 0

    if x == 100:
        fireCannon()
    elif isInMap(shipPosX + x, shipPosY + y):
        map[shipPosX][shipPosY] = waterIcon
        if (map[shipPosX + x][shipPosY + y] != portalIcon):
            if (map[shipPosX + x][shipPosY + y] != waterIcon):
                map[shipPosX + x][shipPosY + y] = deathIcon
            else:
                map[shipPosX + x][shipPosY + y] = shipIcon
            shipPosX += x
            shipPosY += y

        else:
            random.seed(time.time())
            tempx = tempy = None
            dx = [-1, -1, -1,  0, 0,  1, 1, 1]
            dy = [-1,  0,  1, -1, 1, -1, 0, 1]
            badPos = True
            while (badPos):
                tempx = random.randint(0, 10)
                tempy = random.randint(0, 10)
                if (map[tempx][tempy] == waterIcon):
                    badPos = False
                    for i in range(0, 8):
                        if (isInMap(tempx + dx[i], tempy + dy[i]) and map[tempx + dx[i]][tempy + dy[i]] == enemyIcon):
                            badPos = True
            shipPosX = tempx
            shipPosY = tempy
            map[shipPosX][shipPosY] = shipIcon

    print("-------------------------------------------Co input: ", events)
    return 1


def fireCannon():
    x = y = 0
    global shipStatus
    match shipStatus:
        case 1:
            x = -1
            y = -1

        case 2:
            x = 0
            y = 1

        case 3:
            x = 1
            y = -1

        case 4:
            x = -1
            y = 0

    bulletMove(x, y)


def bulletMoving():

    global ship, laserGroup, map
    xTarget = xOnMap = ship.rect.centerx
    yTarget = yOnMap = ship.rect.centery

    if shipStatus == 2:
        xTarget += OBJ_WIDTH*3

        xOnMap += OBJ_WIDTH

    elif shipStatus == 1:
        xTarget += OBJ_WIDTH*3
        yTarget += OBJ_WIDTH*3

        xOnMap += OBJ_WIDTH
        yOnMap += OBJ_WIDTH

    elif shipStatus == 4:
        yTarget += OBJ_WIDTH*3
        yOnMap += OBJ_WIDTH

    elif shipStatus == 3:
        xTarget -= OBJ_WIDTH*3
        yTarget -= OBJ_WIDTH*3

        xOnMap -= OBJ_WIDTH
        yOnMap -= OBJ_WIDTH

    print(shipStatus)
    print("fire at: ", ship.rect.center, (xTarget, yTarget), (xOnMap, yOnMap))

    global clock, chayGame
    while xOnMap != xTarget or yOnMap != yTarget:

        xWidth = int((xOnMap - 35)/OBJ_WIDTH)
        yWidth = int((yOnMap - 35)/OBJ_WIDTH)

        if yWidth < 11 and xWidth < 11:
            map[yWidth][xWidth] = bulletIcon

        print(f'{xOnMap = }, {yOnMap = }')

        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False
            if event.type == bonusReduce:
                global bonusTurn_score
                if bonusTurn_score > 0:
                    bonusTurn_score -= 10

        draw_window(laser=(xOnMap, yOnMap))

        if xOnMap != xTarget:
            if xOnMap < xTarget:
                xOnMap += 1
            else:
                xOnMap -= 1
        if yOnMap != yTarget:
            if yOnMap < yTarget:
                yOnMap += 1
            else:
                yOnMap -= 1


def bulletMove(x, y):
    temp = None
    global shipPosX, shipPosY, map

    bullet1Stop = bullet2Stop = False

    bullet1X = shipPosX
    bullet2X = shipPosX
    bullet1Y = shipPosY
    bullet2Y = shipPosY

    for i in range(0, 3):

        if bullet1Stop == False and isInMap(bullet1X + x, bullet1Y + y):
            if (map[bullet1X + x][bullet1Y + y] != waterIcon):
                if (map[bullet1X + x][bullet1Y + y] == monsterIcon or map[bullet1X + x][bullet1Y + y] == obstacleIcon):
                    bullet1Stop = True
                else:
                    map[bullet1X + x][bullet1Y + y] = obstacleIcon if (
                        map[bullet1X - x][bullet1Y - y] == obstacleIcon) else deathIcon
            else:
                map[bullet1X + x][bullet1Y + y] = bulletIcon
            bullet1X += x
            bullet1Y += y

        if (bullet2Stop == False and isInMap(bullet2X - x, bullet2Y - y)):
            if (map[bullet2X - x][bullet2Y - y] != waterIcon):
                if (map[bullet2X - x][bullet2Y - y] == monsterIcon or map[bullet2X - x][bullet2Y - y] == obstacleIcon):
                    bullet2Stop = True
                else:
                    map[bullet2X - x][bullet2Y - y] = obstacleIcon if (
                        map[bullet2X - x][bullet2Y - y] == obstacleIcon) else deathIcon
            else:
                map[bullet2X - x][bullet2Y - y] = bulletIcon
            bullet2X -= x
            bullet2Y -= y

        # system('cls')
        print(f'{bullet1Stop = }, {bullet2Stop = }')
        print("ban vien dan thu:", i, " tai: ",
              bullet1X, bullet1Y, bullet2X, bullet2Y)
        updateMap()

        endTime = pygame.time.get_ticks() + 1000
        while pygame.time.get_ticks() < endTime:
            gameCore()

        # clear the last bullet
        if (map[bullet1X][bullet1Y] != shipIcon and map[bullet1X][bullet1Y] != deathIcon):
            map[bullet1X][bullet1Y] = obstacleIcon if map[bullet1X][bullet1Y] == obstacleIcon else waterIcon
        if (map[bullet2X][bullet2Y] != shipIcon and map[bullet2X][bullet2Y] != deathIcon):
            map[bullet2X][bullet2Y] = obstacleIcon if map[bullet2X][bullet2Y] == obstacleIcon else waterIcon


def enemyTurn():

    x = y = None
    global visitedNum, visited
    visitedNum = 0

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            visited[i][j] = False

    while (visitedNum < mapSize * mapSize):
        for i in range(0, mapSize):
            for j in range(0, mapSize):
                if (visited[i][j] == False):
                    visited[i][j] = True
                    visitedNum += 1
                    if (map[i][j] == enemyIcon):
                        # so sanh vi tri dich tai(i, j) so voi tau cua minh de co huong di toi uu nhat
                        if (i == shipPosX):
                            x = 0
                        elif (i < shipPosX):
                            x = 1
                        else:
                            x = -1

                        if (j == shipPosY):
                            y = 0
                        elif (j < shipPosY):
                            y = 1
                        else:
                            y = -1

                        enemyMove(i, j, x, y)


def enemyMove(posX, posY, x, y):
    global visited, visitedNum, map

    # print(f'{posX} to {posX + x}, {posY} to {posY + y}')

    # check xem vi tri di chuyen toi co vat can gi khong
    if (map[posX + x][posY + y] != waterIcon):
        if (map[posX + x][posY + y] == enemyIcon):
            if (visited[posX + x][posY + y] == True):
                map[posX][posY] = waterIcon
                map[posX + x][posY + y] = deathIcon
            else:
                visited[posX][posY] = False
                visitedNum -= 1
        elif map[posX + x][posY + y] == monsterIcon:
            map[posX][posY] = waterIcon
        else:
            map[posX][posY] = waterIcon
            map[posX + x][posY + y] = deathIcon
    else:
        map[posX][posY] = waterIcon
        map[posX + x][posY + y] = enemyIcon
        if (visited[posX + x][posY + y] != True):
            visited[posX + x][posY + y] = True
            visitedNum += 1


def monsterTurn():
    x = y = None
    global visitedNum, visited
    visitedNum = 0

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            visited[i][j] = False

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            if visited[i][j] == False and map[i][j] == monsterIcon:
                random.seed(time.time())
                tempx = random.randint(-1, 1)
                tempy = random.randint(-1, 1)

                while (not isInMap(i + tempx, j + tempy)) and map[i + tempx][j + tempy] != obstacleIcon and map[i + tempx][j + tempy] != portalIcon and map[i + tempx][j + tempy] != deathIcon and map[i + tempx][j + tempy] != shipIcon:
                    tempx = random.randint(-1, 1)
                    tempy = random.randint(-1, 1)

                map[i][j] = waterIcon
                map[i + tempx][j + tempy] = monsterIcon
                visited[i + tempx][j + tempy] = True

            visited[i][j] = True


def playerMoving():

    global ship, shipGroup
    xOnMap = yOnMap = -1
    for y in range(0, mapSize):
        for x in range(0, mapSize):
            if (map[y][x] == shipIcon):
                xOnMap = 10 + x*OBJ_WIDTH + OBJ_WIDTH/2
                yOnMap = 10 + y*OBJ_WIDTH + OBJ_WIDTH/2

    if xOnMap == ship.rect.centerx and yOnMap == ship.rect.centery:
        return False

    x = y = 0
    rotate = 0

    if abs(xOnMap - ship.rect.centerx) <= 71 and abs(yOnMap - ship.rect.centery) <= 71:
        if xOnMap > ship.rect.centerx:
            x = 1
            rotate = -90
        elif xOnMap < ship.rect.centerx:
            x = -1
            rotate = 90

        if yOnMap > ship.rect.centery:
            y = 1
            if rotate == 0:
                rotate = 180
            elif rotate == 90:
                rotate = 135
            else:
                rotate = -135
        elif yOnMap < ship.rect.centery:
            y = -1
            if rotate == 0:
                rotate = 0
            elif rotate == 90:
                rotate = 45
            else:
                rotate = -45
    else:
        x = xOnMap - ship.rect.x
        y = yOnMap - ship.rect.y

    ship.rotate(rotate)
    shipGroup.update((int(ship.rect.centerx) + x, int(ship.rect.centery) + y))

    return True


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


imgAlpha = 0


def endSreen(events):
    global win, screen, game_restart, display_score, imgAlpha, level

    if display_score + 5 < lvl_score + bonusTurn_score:
        display_score += 5
    else:
        display_score = lvl_score + bonusTurn_score

    if win:
        endscreen = pygame.image.load("images/screen/endscreenWin.png")
        WIN.blit(endscreen, (0, 0))

        """ if display_score >= 400:
            グラ = pygame.image.load("images/.config/グラ.png")
            if imgAlpha < 225:
                imgAlpha += 10
            blit_alpha(WIN, グラ, (0, 150), imgAlpha) """

        pygame.time.set_timer(bonusReduce, 0)

        message = "Your score " + \
            str(display_score)
        write(message, "#f8f239", (460, 450), 35)
        message = "Right arrow for level " + str(level+1)
        write(message, "#f8f239", (450, 490))
        print(message)

    else:
        endscreen = pygame.image.load("images/screen/endscreen.png")
        WIN.blit(endscreen, (0, 0))
        pygame.time.set_timer(bonusReduce, 0)

        write("Oh no! You lost", "white", (450, 450))
        write("Better luck next time", "white", (450, 480))
        write("Space to retry", "white", (450, 540))
        print("Game over")

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and win and level < 9:
                screen = 1
                game_restart = True
                level += 1
                imgAlpha = 0

            if event.key == pygame.K_RIGHT and win and level >= 9:
                screen = 3
                game_restart = True
                level += 1
                imgAlpha = 0

            if event.key == pygame.K_SPACE:
                screen = 1
                game_restart = True
                imgAlpha = 0


game_restart = True


def startScreen(events):
    global screen

    winscreen = pygame.image.load("images/screen/startscreen.png")
    WIN.blit(winscreen, (0, 0))
    write("Press any key to start the game!", "white", (900/2, 400))
    for event in events:
        if event.type == pygame.KEYDOWN:
            screen = 1


level = 0


def playScreen(events):
    global game_restart, map, shipPosX, shipPosY, shipStatus, hasMoved
    if game_restart:
        game_restart = False

        ship.rotate(0)
        ship.update((285, 285))
        shipStatus = 2
        hasMoved = False

        global bonusTurn_score, display_score

        bonusTurn_score = 400
        display_score = 0
        pygame.time.set_timer(bonusReduce, 1000)

        map = deepcopy(mapList[level])

        shipPosX = 5
        shipPosY = 5
        map[shipPosX][shipPosY] = shipIcon

    global screen, win

    updateMap()
    draw_window()

    if CheckWinCondition() == 1:
        win = True
        screen = 2
        pygame.time.delay(1000)
        return
    elif CheckWinCondition() == -1:
        win = False
        screen = 2
        pygame.time.delay(1000)
        return

    for event in events:
        if event.type == pygame.QUIT:
            chayGame = False

    playerMoving()
    animationInProgress = playerMoving()

    if animationInProgress == False:
        if playerTurn(events):
            hasMoved = True

    if animationInProgress:
        print("Animation in progress")
        return

    print(f'{hasMoved = }')
    if hasMoved:
        print("ENEMY TURN")
        enemyTurn()

        monsterTurn()
        hasMoved = False
        draw_window()


# Screen dau tien luon la screen start
screen = 3

win = False


# Making moving gif group
movingBgGroup = pygame.sprite.Group()
bg = Bg(10, 10)
movingBgGroup.add(bg)

movingCelesGroup = pygame.sprite.Group()
vot = Stuff(0, 0)
movingCelesGroup.add(vot)


shipGroup = pygame.sprite.Group()
ship = Ship()
ship.update
shipGroup.add(ship)

laserGroup = pygame.sprite.Group()
laser = Ship(path="images/laser/laserRed01.png", size=(9, 54))
laser.update
laserGroup.add(laser)

enemyGroup = pygame.sprite.Group()
enemy = Enemy()
enemy.update
enemyGroup.add(enemy)


lvl_score = 200
bonusTurn_score = 400
total_score = 0
display_score = 0

bonusReduce = pygame.USEREVENT + 1


clock = pygame.time.Clock()
chayGame = True


def gameCore(laser=(-1, -1)):

    global clock, chayGame

    clock.tick(FPS)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            chayGame = False

        if event.type == bonusReduce:
            global bonusTurn_score
            if bonusTurn_score > 0:
                bonusTurn_score -= 10

    draw_window(laser)


def main():

    global hasMoved, clock, chayGame

    hasMoved = False
    while chayGame:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False

            if event.type == bonusReduce:
                global bonusTurn_score
                if bonusTurn_score > 0:
                    bonusTurn_score -= 10

        if screen == 1:
            playScreen(events)
        elif screen == 2:
            endSreen(events)
        elif screen == 3:
            startScreen(events)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
