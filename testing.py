import time
import random
import numpy
import pygame
from os import system
import os

MAX = 100
mapSize = 11

# CONST for the pygame
OBJ_WIDTH, OBJ_HEIGHT = 50, 50
WIN = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
FPS = 60

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CHOCO = (210, 105, 30)
PINK = (255, 192, 203)

pygame.display.set_caption("The pirate of The Seven Seas")

pygame.font.init()

img1 = pygame.transform.scale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (OBJ_HEIGHT, OBJ_HEIGHT))  # Hinh anh va thu nho thanh 80x80px
bullet = pygame.transform.scale(pygame.image.load(
    os.path.join("bullet.png")), (OBJ_HEIGHT, OBJ_HEIGHT))  # Hinh anh va thu nho thanh 80x80px
votex = pygame.transform.scale(pygame.image.load(
    "images/votex/01.gif"), (60, 60))
obstacle = pygame.transform.scale(pygame.image.load(
    "images/obstacle/neutron.gif"), (92, 92))

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

shipStatus = 1
# 1, 9 = / -> 1
# 2, 8 = _  -> 2
# 3, 7 = \  -> 3
# 4, 6 = |  -> 4


map = [['0']*MAX for i in range(0, MAX)]
visited = [['0']*MAX for i in range(0, MAX)]
visitedNum = 0


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


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join("pikachuOnDeskSqr.png")), (OBJ_HEIGHT, OBJ_HEIGHT))
        self.rect = self.image.get_rect()

    def update(self, pos=(600, 300)):
        self.rect.topleft = pos


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


def write(content, color="black", pos=(300, 200), size=20, font="fonts/PressStart2P-Regular.ttf"):
    text = pygame.font.Font(font, size)
    text_sur = text.render(content, False, color)
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


def draw_window():
    WIN.fill('#01051f')  # Lam DEN nguyen man hinh
    global movingBgGroup, img1, movingCelesGroup, vot

    movingBgGroup.draw(WIN)

    movingBgGroup.update()

    vot.animate()

    for i in range(0, mapSize):
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
                pygame.draw.rect(WIN, RED, rects[x][y])  # To DO

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
                pygame.draw.rect(WIN, CHOCO, rects[x][y])  # To NAU

            if (map[x][y] == monsterIcon):
                pygame.draw.rect(WIN, "cornflowerblue", rects[x][y])  # To NAU

            if (map[x][y] == bulletIcon):
                ptoaDoDatHinh = (rects[x][y].x + (100-80)/4,
                                 rects[x][y].y + (100-80)/4)
                pygame.draw.rect(WIN, BLUE, rects[x][y])
                bullet_rect = bullet.get_rect(center=rects[x][y].center)
                WIN.blit(bullet, bullet_rect)

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

            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                x = 1
                y = 0
                shipStatus = 2
                print("ban vua chon ", 2)

            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                x = 1
                y = 1
                shipStatus = 3
                print("ban vua chon ", 3)

            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                x = 0
                y = -1
                shipStatus = 4
                print("ban vua chon ", 4)

            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                x = 100
                print("ban vua chon ", 'none')

            elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                x = 0
                y = 1
                shipStatus = 4
                print("ban vua chon ", 6)

            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                x = -1
                y = -1
                shipStatus = 3
                print("ban vua chon ", 7)

            elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
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
            while (True):
                tempx = random.randint(0, 10)
                tempy = random.randint(0, 10)
                if (map[tempx][tempy] == waterIcon):
                    break
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
                if (map[bullet1X + x][bullet1Y + y] == monsterIcon):
                    bullet1Stop = True
                else:
                    map[bullet1X + x][bullet1Y + y] = deathIcon
            else:
                map[bullet1X + x][bullet1Y + y] = bulletIcon
            bullet1X += x
            bullet1Y += y

        if (bullet2Stop == False and isInMap(bullet2X - x, bullet2Y - y)):
            if (map[bullet2X - x][bullet2Y - y] != waterIcon):
                if (map[bullet2X - x][bullet2Y - y] == monsterIcon):
                    bullet2Stop = True
                else:
                    map[bullet2X - x][bullet2Y - y] = deathIcon
            else:
                map[bullet2X - x][bullet2Y - y] = bulletIcon
            bullet2X -= x
            bullet2Y -= y

        # system('cls')
        print("ban vien dan thu:", i, " tai: ",
              bullet1X, bullet1Y, bullet2X, bullet2Y)
        # updateMap()
        draw_window()
        time.sleep(1)

        # clear the last bullet
        if (map[bullet1X][bullet1Y] != shipIcon and map[bullet1X][bullet1Y] != deathIcon):
            map[bullet1X][bullet1Y] = waterIcon
        if (map[bullet2X][bullet2Y] != shipIcon and map[bullet2X][bullet2Y] != deathIcon):
            map[bullet2X][bullet2Y] = waterIcon


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

                while (not isInMap(i + tempx, j + tempy)) and map[i + tempx][j + tempy] != obstacleIcon and map[i + tempx][j + tempy] != portalIcon and map[i + tempx][j + tempy] != deathIcon:
                    tempx = random.randint(-1, 1)
                    tempy = random.randint(-1, 1)

                map[i][j] = waterIcon
                map[i + tempx][j + tempy] = monsterIcon
                visited[i + tempx][j + tempy] = True

            visited[i][j] = True


def playerMoving():
    ship_rect = img1.get_rect()
    # WIN.blit(img1, ship_rect)

    global ship, shipGroup
    xOnMap = yOnMap = -1
    for y in range(0, mapSize):
        for x in range(0, mapSize):
            if (map[y][x] == shipIcon):
                xOnMap = 10 + x*OBJ_WIDTH
                yOnMap = 10 + y*OBJ_WIDTH

    if xOnMap == ship.rect.x and yOnMap == ship.rect.y:
        return False

    x = y = 0
    if xOnMap > ship.rect.x:
        x = 1
    elif xOnMap < ship.rect.x:
        x = -1

    if yOnMap > ship.rect.y:
        y = 1
    elif yOnMap < ship.rect.y:
        y = -1

    shipGroup.update((int(ship.rect.x) + x, int(ship.rect.y) + y))

    return True


def endSreen(events):
    global win, screen, game_restart
    if win:
        write("You Win!!", "white")
        print("You Win!!")

    else:
        write("You dumbass, you lost", "white")
        print("Game over")

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen = 1
                game_restart = True


game_restart = True


def startScreen(events):
    global screen

    WIN.fill('#01051f')
    write("Press any key to start the game!", "white", (150, 300))
    for event in events:
        if event.type == pygame.KEYDOWN:
            screen = 1


level = 0


def playScreen(events):
    global game_restart, map, shipPosX, shipPosY
    if game_restart:
        game_restart = False

        match level:
            case 0:
                map = [
                    ['@', '+', '~', '~', '~', '~', '~',
                        '~', '~', '~', '@', '~', '~', '~'],
                    ['~', '~', 'A', '~', '~', '~', '~',
                        '~', '~', '!', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', 'A', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '!', '~', '~',
                        '~', '~', '!', '~', '~', '~', '~'],
                    ['~', 'A', 'A', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                    ['@', '~', '~', '~', '~', '~', '~',
                        '~', '~', 'A', '@', '~', '~', '~'],
                    ['@', '~', '~', '~', '~', '~', '~',
                        '~', '~', 'A', '@', '~', '~', '~'],
                    ['@', '~', '~', '~', '~', '~', '~', '~', '~', 'A', '@', '~', '~', '~'], ]
                shipPosX = 6
                shipPosY = 9
                map[shipPosX][shipPosY] = shipIcon
            case 1:
                map = [['~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                           '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                           'A', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                        '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                           '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                           '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~',
                           '~', '~', '~', '~', '~', '~', '~'],
                       ['~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~']]
                shipPosX = 5
                shipPosY = 9
                map[shipPosX][shipPosY] = shipIcon

    global screen, win, hasMoved

    updateMap()
    draw_window()

    if CheckWinCondition() == 1:
        win = True
        screen = 2
        return
    elif CheckWinCondition() == -1:
        win = False
        screen = 2
        return

    for event in events:
        if event.type == pygame.QUIT:
            chayGame = False

    if playerMoving() == False:
        if playerTurn(events):
            hasMoved = True

    if playerMoving():
        print("Animation in progress")
        return

    print(f'{hasMoved = }')
    if hasMoved:
        print("ENEMY TURN")
        enemyTurn()

        monsterTurn()
        hasMoved = False


# Screen dau tien luon la screen game
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
shipGroup.add(ship)


def main():
    initMap(waterIcon)
    """ # manual set up
    map[shipPosX][shipPosY] = shipIcon

    map[0][0] = portalIcon
    map[0][10] = portalIcon
    map[10][0] = portalIcon
    map[10][10] = portalIcon

    map[0][1] = monsterIcon

    map[6][1] = enemyIcon
    map[6][2] = enemyIcon
    map[2][5] = enemyIcon
    map[10][9] = enemyIcon
    map[1][2] = enemyIcon

    map[5][9] = obstacleIcon
    map[1][9] = obstacleIcon
    map[5][4] = obstacleIcon """

    clock = pygame.time.Clock()
    chayGame = True
    global hasMoved
    hasMoved = False
    while chayGame:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False

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
