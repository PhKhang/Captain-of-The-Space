import time
import random
import pygame
from os import system
import os

MAX = 100
mapSize = 11

# CONST for the pygame
OBJ_WIDTH, OBJ_HEIGHT = 40, 40
WIN = pygame.display.set_mode((900, 500), pygame.RESIZABLE)
FPS = 5

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CHOCO = (210, 105, 30)
PINK = (255, 192, 203)

pygame.display.set_caption("The pirate of The Seven Seas")

img1 = pygame.transform.scale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (OBJ_HEIGHT, OBJ_HEIGHT))  # Hinh anh va thu nho thanh 80x80px
bullet = pygame.transform.scale(pygame.image.load(
    os.path.join("bullet.png")), (OBJ_HEIGHT, OBJ_HEIGHT))  # Hinh anh va thu nho thanh 80x80px

# Tao mang that bu, moi phan tu la MOT VUNG HINH VUONG de tu do to mau, in hinh,... len
rects = [[0]*50 for i in range(0, 50)]  # Tao mang trong
for y in range(0, mapSize):  # Lap vao mang trong tren cac VUNG HINH VUONG
    for x in range(0, mapSize):
        rects[y][x] = (pygame.Rect(
            10 + x * OBJ_HEIGHT, y * OBJ_HEIGHT, OBJ_WIDTH, OBJ_HEIGHT))


# Variables for the game algo
waterIcon = '~'
shipIcon = 'X'
enemyIcon = 'A'
deathIcon = '#'
obstacleIcon = '!'
bulletIcon = '.'
portalIcon = '@'  # icon game

shipPosX = 6
shipPosY = 9

shipStatus = 1																												# 1, 9 = / -> 1
# 2, 8 = _  -> 2
# 3, 7 = \  -> 3
# 4, 6 = |  -> 4


map = [['0']*MAX for i in range(0, MAX)]
visited = [['0']*MAX for i in range(0, MAX)]
visitedNum = 0


def draw_window():
    WIN.fill((255, 255, 255))  # Lam TRANG nguyen man hinh

    dem = 0
    for y in range(0, mapSize):
        for x in range(0, mapSize):

            # To o 0 Bien
            if (map[x][y] == waterIcon):
                pygame.draw.rect(WIN, BLUE, rects[x][y])  # To XANH

            # To o 1 Cuop bien
            if (map[x][y] == enemyIcon):
                pygame.draw.rect(WIN, RED, rects[x][y])  # To DO

            # To o 3 Dao
            if (map[x][y] == obstacleIcon):
                pygame.draw.rect(WIN, GREEN, rects[x][y])  # To XANH LA

            if (map[x][y] == portalIcon):
                pygame.draw.rect(WIN, PINK, rects[x][y])  # To HONG

            if (map[x][y] == deathIcon):
                pygame.draw.rect(WIN, CHOCO, rects[x][y])  # To NAU

            if (map[x][y] == bulletIcon):
                ptoaDoDatHinh = (rects[x][y].x + (100-80)/4,
                                 rects[x][y].y + (100-80)/4)
                pygame.draw.rect(WIN, BLUE, rects[x][y])
                WIN.blit(bullet, rects[x][y])

            # To DO roi them hinh o duoc chon
            if ((x == shipPosX and y == shipPosY) and (map[x][y] != enemyIcon)):
                toaDoDatHinh = (rects[x][y].x + (100-80)/4,
                                rects[x][y].y + (100-80)/4)
                pygame.draw.rect(WIN, RED, rects[x][y])
                WIN.blit(img1, rects[x][y])

            # To len vien DO o co chuot hover
            if (rects[y][x].collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(WIN, RED, rects[y][x], 4)

            dem += 1

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
        return -1

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            if (map[i][j] == enemyIcon):
                return 0

    return 1


def getKeyBoardInput(events):
    x = y = 0

    print("Your joystick :")
    print("7 8 9")  # upper left  | up          | upper right
    print("4 5 6")  # left        | fire cannon | right
    print("1 2 3")  # bottom left | bottom      | bottom right

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
    global shipPosX, shipPosY
    bullet1X = shipPosX
    bullet2X = shipPosX
    bullet1Y = shipPosY
    bullet2Y = shipPosY
    for i in range(0, 3):
        if (map[bullet1X][bullet1Y] != shipIcon and map[bullet1X][bullet1Y] != deathIcon):
            map[bullet1X][bullet1Y] = waterIcon
        if (map[bullet1X + x][bullet1Y + y] != waterIcon):
            map[bullet1X + x][bullet1Y + y] = deathIcon
        else:
            map[bullet1X + x][bullet1Y + y] = bulletIcon
        bullet1X += x
        bullet1Y += y

        if (map[bullet2X][bullet2Y] != shipIcon and map[bullet2X][bullet2Y] != deathIcon):
            map[bullet2X][bullet2Y] = waterIcon
        if (map[bullet2X - x][bullet2Y - y] != waterIcon):
            map[bullet2X - x][bullet2Y - y] = deathIcon
        else:
            map[bullet2X - x][bullet2Y - y] = bulletIcon
        bullet2X -= x
        bullet2Y -= y
        # system('cls')
        print("ban vien dan thu:", i, " tai: ",
              bullet1X, bullet1Y, bullet2X, bullet2Y)
        updateMap()
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


def main():
    initMap(waterIcon)
    # manual set up
    map[shipPosX][shipPosY] = shipIcon

    map[0][0] = portalIcon
    map[0][10] = portalIcon
    map[10][0] = portalIcon
    map[10][10] = portalIcon

    map[6][1] = enemyIcon
    map[6][2] = enemyIcon
    map[2][5] = enemyIcon
    map[10][9] = enemyIcon
    map[1][2] = enemyIcon

    map[5][9] = obstacleIcon
    map[1][9] = obstacleIcon
    map[5][4] = obstacleIcon

    win = False

    clock = pygame.time.Clock()
    chayGame = True
    while chayGame:
        clock.tick(FPS)

        # system('cls')
        updateMap()
        draw_window()

        if CheckWinCondition() == 1:
            win = True
            break
        elif CheckWinCondition() == -1:
            win = False
            break

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False

        bao = playerTurn(events)

        # system('cls')
        updateMap()
        draw_window()
        # time.sleep(1)

        if bao != 0:
            print("ENEMY TURN")
            enemyTurn()

    if win:
        print("You Win!!")
    else:
        print("ゲームオーバー")

    pygame.quit()


if __name__ == "__main__":
    main()
