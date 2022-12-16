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

map[MAX][MAX]
print(f'map = ')