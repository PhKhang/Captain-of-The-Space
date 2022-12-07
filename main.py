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
img2 = pygame.image.load(os.path.join("Group 1.png"))  # Hinh anh


rects = [[0]*50 for i in range(0, 50)]
for y in range(5):
    for x in range(6):
        rects[y][x] = (pygame.Rect(10 + x * 90, y * 90, OB_WIDTH, OB_HEIGHT))


def draw_win(ob1, ob2, a=(0, 0)):
    WIN.fill((255, 255, 255))  # Lam trang nguyen man hinh

    dem = 0
    for y in range(0, 5):
        for x in range(0, 6):
            if (map[y][x] == 0):  # To o 0 Bien
                pygame.draw.rect(WIN, BLUE, rects[y][x])

            if (map[y][x] == 1):  # To o 1 Cuop bien
                pygame.draw.rect(WIN, RED, rects[y][x])

            if (map[y][x] == 3):  # To o 3 Dao
                pygame.draw.rect(WIN, GREEN, rects[y][x])

            # To DO roi them hinh o duoc chon
            if (dem == select and map[y][x] != 1):
                cord = (rects[y][x].x + (100-80)/4, rects[y][x].y + (100-80)/4)
                pygame.draw.rect(WIN, RED, rects[y][x])
                WIN.blit(img1, rects[y][x])

            # To len vien DO o co chuot hover
            if (rects[y][x].collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(WIN, RED, rects[y][x], 4)

            dem += 1

    pygame.display.update()


def FollowMe(pops, fpos):
    LERP_FACTOR = 0.05
    minimum_distance = 25
    maximum_distance = 100

    target_vector = pygame.math.Vector2(*pops)
    follower_vector = pygame.math.Vector2(*fpos)
    new_follower_vector = pygame.math.Vector2(*fpos)

    distance = follower_vector.distance_to(target_vector)
    if distance > minimum_distance:
        direction_vector = (target_vector - follower_vector) / distance
        min_step = max(0, distance - maximum_distance)
        max_step = distance - minimum_distance
        step_distance = min_step + (max_step - min_step) * LERP_FACTOR
        new_follower_vector = follower_vector + direction_vector * step_distance

    return (new_follower_vector)


def main():
    global select
    select = 0

    clock = pygame.time.Clock()

    object1 = pygame.Rect(700, 300, OB_WIDTH, OB_HEIGHT)
    object2 = pygame.Rect(100, 300, OB_WIDTH, OB_HEIGHT)

    chayGame = True
    while chayGame:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chayGame = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    vt = event.pos

                    dem = 0
                    for y in range(0, 5):
                        for x in range(0, 6):

                            if rects[y][x].collidepoint(vt) and map[y][x] != 1:
                                print("clicked aaa at", dem)
                                select = dem

                            dem += 1

        draw_win(object1, object2)

    pygame.quit()


if __name__ == "__main__":
    main()
