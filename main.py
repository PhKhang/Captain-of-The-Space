import pygame
import os

WIDTH, HEIGHT = 900, 500
OB_WIDTH, OB_HEIGHT = 90, 90
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
FPS = 60

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

map = [
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 3, 1, 0],
    [0, 3, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0]
]

pygame.display.set_caption("The pirate of The Seven Seas")

img1 = pygame.transform.scale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (80, 80))  # Hinh anh va thu nho thanh 80x80px


# Tao mang that bu, moi phan tu la MOT VUNG HINH VUONG de tu do to mau, in hinh,... len
rects = [[0]*50 for i in range(0, 50)]
for y in range(5):
    for x in range(6):
        rects[y][x] = (pygame.Rect(10 + x * 90, y * 90, OB_WIDTH, OB_HEIGHT))


global diToiX, diToiY
diToiX = 0
diToiY = 0


def draw_win():
    WIN.fill((255, 255, 255))  # Lam trang nguyen man hinh

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

            # To DO roi them hinh o duoc chon
            if ((x == diToiX and y == diToiY) and (map[y][x] != 1)):
                toaDoDatHinh = (rects[y][x].x + (100-80)/4,
                                rects[y][x].y + (100-80)/4)
                pygame.draw.rect(WIN, RED, rects[y][x])
                WIN.blit(img1, rects[y][x])

            # To len vien DO o co chuot hover
            if (rects[y][x].collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(WIN, RED, rects[y][x], 4)

            dem += 1

    pygame.display.update()


def main():
    global select
    select = 0

    clock = pygame.time.Clock()

    chayGame = True
    while chayGame:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chayGame = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                dem = 0
                for y in range(0, 5):
                    for x in range(0, 6):

                        if rects[y][x].collidepoint(event.pos) and map[y][x] != 1:
                            print("clicked aaa at", dem)
                            select = dem
                            global diToiX, diToiY  # Dung bien global da khai bao o tren
                            diToiX = x
                            diToiY = y
                            print(diToiX, diToiY)

                        dem += 1

        draw_win()

    pygame.quit()


if __name__ == "__main__":
    main()
