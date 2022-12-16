import time
from os import system
import random

map = [[1, 34, 54, 64, 434, 34],
       [1, 78, 48, 13, 0, 2]]

a = 1112

MAX = 100

mapSize = 11
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


def getKeyBoardInput():
    x = y = None

    print("Your joystick :")
    print("7 8 9")  # upper left  | up          | upper right
    print("4 5 6")  # left        | fire cannon | right
    print("1 2 3")  # bottom left | bottom      | bottom right
    inputU = input("Nhap so: ")

    global shipStatus

    if int(inputU) == 7:  # TH nhan 7
        x = -1
        y = -1
        shipStatus = 7
        print("ban vua chon ", 7)

    elif int(inputU) == 9:  # TH nhan 9
        x = -1
        y = 1
        shipStatus = 9
        print("ban vua chon ", 9)

    elif int(inputU) == 3:  # TH nhan 3
        x = 1
        y = 1
        shipStatus = 3
        print("ban vua chon ", 3)

    elif int(inputU) == 1:  # TH nhan 1
        x = 1
        y = -1
        shipStatus = 1
        print("ban vua chon ", 1)

    elif int(inputU) == 8:  # TH nhan 8
        x = -1
        y = 0
        shipStatus = 8
        print("ban vua chon ", 8)

    elif int(inputU) == 6:  # TH nhan 6
        x = 0
        y = 1
        shipStatus = 6
        print("ban vua chon ", 6)

    elif int(inputU) == 4:  # TH nhan 4
        x = 0
        y = -1
        shipStatus = 4
        print("ban vua chon ", 4)

    elif int(inputU) == 2:  # TH nhan 2
        x = 1
        y = 0
        shipStatus = 2
        print("ban vua chon ", 2)

    else:
        x = 100
        print("ban vua chon ", 'none')

    return x, y


def playerTurn():
    x = y = None
    x, y = getKeyBoardInput()
    global shipPosX, shipPosY

    print(f'{x = }, {y = }, {shipStatus = }, {shipPosX = } , {shipPosY = }')

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


def fireCannon():
    x = y = None
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
        system('cls')
        updateMap()
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

    while True:
        system('cls')
        updateMap()

        if CheckWinCondition() == 1:
            win = True
            break
        elif CheckWinCondition() == -1:
            win = False
            break

        playerTurn()

        system('cls')
        updateMap()
        time.sleep(1)

        enemyTurn()

    if win:
        print("You Win!!")
    else:
        print("ゲームオーバー")


if __name__ == "__main__":
    main()
