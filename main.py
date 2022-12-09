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

map = [
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 3, 1, 0],
    [0, 3, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0]
]

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
                WIN.blit(img1, rects[y][x])

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


def getKeyBoardInput(events):
    global x, y

    right_pressed = False
    left_pressed = False
    up_pressed = False
    down_pressed = False

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right_pressed = True
            if event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_UP:
                up_pressed = True
            if event.key == pygame.K_DOWN:
                down_pressed = True

    if left_pressed and up_pressed:  # TH nhan 7
        x = -1
        y = -1
        # print(7)

    elif right_pressed and up_pressed:  # TH nhan 9
        x = 1
        y = 1
        # print(9)

    elif right_pressed and down_pressed:  # TH nhan 3
        x = 1
        y = 1
        # print(3)

    elif left_pressed and down_pressed:  # TH nhan 1
        x = -1
        y = 1
        # print(1)

    elif up_pressed:  # TH nhan 8
        x = 0
        y = -1
        # print(8)

    elif right_pressed:  # TH nhan 6
        x = 1
        y = 0
        # print(6)

    elif left_pressed:  # TH nhan 4
        x = -1
        y = 0
        # print(4)

    elif down_pressed:  # TH nhan 2
        x = 0
        y = 1
        # print(2)

    else:
        x = 0
        y = 0
        # print('none')


def isInMap(x, y):
    print(y, x, (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT))
    return (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT)


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


def main():
    clock = pygame.time.Clock()

    global x, y, hienTaiX, hienTaiY

    chayGame = True
    while chayGame:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                chayGame = False
            getMouseInput(event)

        getKeyBoardInput(events)
        move(hienTaiX, hienTaiY, x, y, '🛶')
        hienTaiX += x
        hienTaiY += y

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
