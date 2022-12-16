import pygame
import os

WIDTH, HEIGHT = 900, 500
OB_WIDTH, OB_HEIGHT = 90, 90
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
FPS = 60

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CHOCO = (210, 105, 30)
PINK = (255, 192, 203)

mapSize = 11

waterIcon = '~'
shipIcon = 'X'
enemyIcon = 'A'
deathIcon = '#'
obstacleIcon = '!'
bulletIcon = '.'
portalIcon = '@'  # icon game

shipPosX = 6
shipPosY = 9																									# vi tri ban dau cua tau

shipStatus = 1


map = [[0]*50 for i in range(0, 50)]
visited = [[0]*50 for i in range(0, 50)]
global visitedNum

MAP_WIDTH = 6
MAP_HEIGHT = 5

pygame.display.set_caption("The pirate of The Seven Seas")

img1 = pygame.transform.scale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (80, 80))  # Hinh anh va thu nho thanh 80x80px


# Tao mang that bu, moi phan tu la MOT VUNG HINH VUONG de tu do to mau, in hinh,... len
rects = [[0]*50 for i in range(0, 50)]  # Tao mang trong
for y1 in range(MAP_HEIGHT):  # Lap vao mang trong tren cac VUNG HINH VUONG
    for x1 in range(MAP_WIDTH):
        rects[y1][x1] = (pygame.Rect(
            10 + x1 * 90, y1 * 90, OB_WIDTH, OB_HEIGHT))


global hienTaiX, hienTaiY
hienTaiX = 0
hienTaiY = 0
global x, y  # Gia tri can thay doi o truc x, truc y
x = 0
y = 0
global denLuotThuyen
denLuotThuyen = 0


def draw_window():
    WIN.fill((255, 255, 255))  # Lam TRANG nguyen man hinh

    dem = 0
    for y in range(0, 5):
        for x in range(0, 6):

            # To o 0 Bien
            if (map[y][x] == 0):
                pygame.draw.rect(WIN, BLUE, rects[y][x])  # To XANH

            # To o 1 Cuop bien
            if (map[y][x] == 1):
                pygame.draw.rect(WIN, RED, rects[y][x])  # To DO

            # To o 3 Dao
            if (map[y][x] == 3):
                pygame.draw.rect(WIN, GREEN, rects[y][x])  # To XANH LA
            if (map[y][x] == '!'):
                pygame.draw.rect(WIN, CHOCO, rects[y][x])  # To NAU

            # To DO roi them hinh o duoc chon
            if ((x == hienTaiX and y == hienTaiY) and (map[y][x] != 1)):
                toaDoDatHinh = (rects[y][x].x + (100-80)/4,
                                rects[y][x].y + (100-80)/4)
                pygame.draw.rect(WIN, RED, rects[y][x])
                WIN.blit(img1, toaDoDatHinh)

            # To len vien DO o co chuot hover
            if (rects[y][x].collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(WIN, RED, rects[y][x], 4)

            dem += 1

    pygame.display.update()


def getMouseInput(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for y in range(0, 5):
            for x in range(0, 6):

                # Chay qua tat ca VUNG HINH VUONG, tim toa do cua vung ma Chuot click
                if rects[y][x].collidepoint(event.pos) and map[y][x] != 1:
                    global hienTaiX, hienTaiY  # Dung bien global da khai bao o tren
                    hienTaiX = x
                    hienTaiY = y
                    print("Clicked at", hienTaiY, hienTaiX)


def getKeyBoardInput():
    global x, y

    right_pressed = False
    left_pressed = False
    up_pressed = False
    down_pressed = False

    print("Your joystick :")
    print("7 8 9")  # upper left  | up          | upper right
    print("4 5 6")  # left        | fire cannon | right
    print("1 2 3")  # bottom left | bottom      | bottom right
    inputU = input("Nhap so")
    print("Ipnut", type(inputU))

    if int(inputU) == 7:  # TH nhan 7
        x = -1
        y = -1
        print("ban vua chon ", 7)

    elif int(inputU) == 9:  # TH nhan 9
        x = -1
        y = 1
        print("ban vua chon ", 9)

    elif int(inputU) == 3:  # TH nhan 3
        x = 1
        y = 1
        print("ban vua chon ", 3)

    elif int(inputU) == 1:  # TH nhan 1
        x = 1
        y = -1
        print("ban vua chon ", 1)

    elif int(inputU) == 8:  # TH nhan 8
        x = -1
        y = 0
        print("ban vua chon ", 8)

    elif int(inputU) == 6:  # TH nhan 6
        x = 0
        y = 1
        print("ban vua chon ", 6)

    elif int(inputU) == 4:  # TH nhan 4
        x = 0
        y = -1
        print("ban vua chon ", 4)

    elif int(inputU) == 2:  # TH nhan 2
        x = 1
        y = 0
        print("ban vua chon ", 2)

    else:
        x = 100
        print("ban vua chon ", 'none')


def isInMap(x, y):
    return (0 <= x < mapSize and 0 <= y < mapSize)


# Di chuyen <replacementIcon> den vi tri moi trong mang map[][]
def move(hienTaiX, hienTaiY, thayDoiX, thayDoiY, replacementIcon):
    global x, y, denLuotThuyen
    if isInMap(hienTaiX + thayDoiX, hienTaiY + thayDoiY) and map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] != '!' and map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] != 3:
        if map[hienTaiY][hienTaiX] == 0 or map[hienTaiY][hienTaiX] == '🛶':
            map[hienTaiY][hienTaiX] = 0

        # Check co vat can o noi sap den ko
        if map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] != 0:
            if map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] == 1:
                pass
            if replacementIcon == 1:
                pass
            map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] = '!'
        else:
            map[hienTaiY + thayDoiY][hienTaiX + thayDoiX] = replacementIcon
    else:
        x = 0
        y = 0

    if replacementIcon == '🛶' and (x != 0 or y != 0):
        denLuotThuyen = 1


def enemyTurn(hienTaiX, hienTaiY):
    global denLuotThuyen
    print('\n'.join(['\t'.join([str(cell) for cell in row])
                     for row in map]))
    if denLuotThuyen:
        print(len(map), len(map[0]))
        thayDoiX = 0
        thayDoiY = 0
        denLuotThuyen = 0
        for y in range(0, HEIGHT-2):
            for x in range(0, WIDTH-2):
                if map[y][x] == 1:
                    if x < hienTaiX:
                        thayDoiX = 1
                    if x > hienTaiX:
                        thayDoiX = -1

                    if y < hienTaiY:
                        thayDoiY = 1
                    if y > hienTaiY:
                        thayDoiY = -1

                    move(x, y, thayDoiX, thayDoiY, 1)


def initMap(ch):
    for i in range(0, mapSize - 1):
        for j in range(0, mapSize - 1):
            map[i][j] = ch


def updateMap():
    for i in range(0, mapSize):
        for j in range(0, mapSize):
            print(map[i][j], end=" ")
        print()
        print()


def CheckWinCondition():
    if (map[shipPosX][shipPosY] == deathIcon):
        return -1

    for i in range(0, mapSize):
        for j in range(0, mapSize):
            if (map[i][j] == enemyIcon):
                return 0

    return 1


def playerTurn():
    getKeyBoardInput()
    global x, y, shipPosX, shipPosY
    if isInMap(shipPosX + x, shipPosY + y):
        map[shipPosX][shipPosY] = waterIcon
        if (map[shipPosX + x][shipPosY + y] != waterIcon):
            map[shipPosX + x][shipPosY + y] = deathIcon
        else:
            map[shipPosX + x][shipPosY + y] = shipIcon
        shipPosX += x
        shipPosY += y


def enemyTurn():
    global visited
    global x, y
    global visitedNum

    visitedNum = 0

    for i in range(0, mapSize-1):
        for j in range(0, mapSize-1):
            visited[i][j] = False

    while (visitedNum < mapSize * mapSize):
        for i in range(0, mapSize-1):
            for j in range(0, mapSize-1):
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


# Di chuyen tu vi tri (PosX, PosY) sang vi tri (PosX + x, PosY + y)
def enemyMove(posX, posY, x, y):
    global visinum

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
    global map
    initMap(waterIcon)

    global shipPosX, shipPosY
    print(shipPosX, shipPosY)
    print(len(map))
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

    global x, y, hienTaiX, hienTaiY

    chayGame = True
    while chayGame:
        clock.tick(FPS)

        updateMap()

        if (CheckWinCondition() == 1):
            win = True
            break
        elif (CheckWinCondition() == -1):
            win = False
            break

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False
            getMouseInput(event)

        playerTurn()

        # draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
