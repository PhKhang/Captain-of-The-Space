import pygame
import os

WIDTH, HEIGHT = 900, 500
OB_WIDTH, OB_HEIGHT = 90, 90
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
FPS = 60

RED = (255, 0,  0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

level = [
    0, 0, 0, 0, 1, 0,
    0, 0, 1, 0, 0, 0,
    0, 0, 0, 3, 1, 0,
    0, 3, 0, 0, 0, 0,
    1, 0, 1, 0, 0, 0
]

pygame.display.set_caption("The pirate of The Seven Seas")

img1 = pygame.transform.scale(pygame.image.load(
    os.path.join("pikachuOnDeskSqr.png")), (80, 80))  # Hinh anh va thu nho thanh 80x80px
img2 = pygame.image.load(os.path.join("Group 1.png"))  # Hinh anh


global vtToix, vtToiy
vtToix = 0
vtToiy = 0


rects = []
for x in range(5):
    for y in range(6):
        rects.append(pygame.Rect(10 + y * 90, x *
                     90, OB_WIDTH, OB_HEIGHT))

[rects[i:i+6] for i in range(0, len(rects), 6)]


def draw_win(ob1, ob2, a=(0, 0)):
    WIN.fill((255, 255, 255))

    WIN.blit(img2, (ob2.x, ob2.y))
    # pygame.draw.rect(WIN, RED, sss)

    # sss.x += 1

    dem = 0

    for i in rects:
        print(dem)
        if (level[dem] == 0):
            pygame.draw.rect(WIN, BLUE, i)
        if (level[dem] == 1):
            pygame.draw.rect(WIN, RED, i)
        if (level[dem] == 3):
            pygame.draw.rect(WIN, GREEN, i)
        if (dem == select):
            print("click")
            cord = (i.x + (100-80)/4, i.y + (100-80)/4)
            # pygame.draw.rect(WIN, GREEN, i)
            pygame.draw.rect(WIN, RED, i)
            WIN.blit(img1, cord)

        if (i.collidepoint(pygame.mouse.get_pos())):
            cord = (i.x + (100-80)/4, i.y + (100-80)/4)
            # pygame.draw.rect(WIN, GREEN, i)
            pygame.draw.rect(WIN, RED, i, 4)

        dem += 1

    # WIN.blit(img1, (a.x, a.y))

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
                    global vtToix, vtToiy
                    vtToix, vtToiy = event.pos
                    vt = event.pos
                    # print(vt)

                    select = -1
                    dem = 0
                    for i in rects:
                        if i.collidepoint(vt):
                            print("clicked aaa at", dem)
                            select = dem
                        dem += 1

        vec = pygame.math.Vector2
        a = vec(1, 1)
        b = vec(vtToix, vtToiy)

        a = FollowMe(b, a)

        draw_win(object1, object2, a)

    pygame.quit()


if __name__ == "__main__":
    main()
