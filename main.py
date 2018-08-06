import pygame
import sys
import time
import math

from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 400), 0, 0)
pygame.display.set_caption('what The Duck')

# color palette
black = (35, 50, 80)
blue = (50, 150, 255)
yellow = (255, 255, 0)

# mommaDuck and babyDuck start Coordinates
mx = 50
my = 50
mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mx, my), 8, 0)

bx = 10
by = 10
babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (bx, by), 5, 0)

# food coordinates and score start
foodx = 200
foody = 200
score = 0


# create display surface grid imitation(400x400) to create colliders
# should find a way to draw obstacles vs. manual input to each coordinate
# could pull from file ex:
# 000000000
# 000110000
# 000111100
# 000000000
m = 400
n = 400
a = [0] * n
for i in range(n):
    a[i] = [0] * m
    print(a[i])


def ck_neighbors(x1, y1, x2, y2):

    # format = [distance, x1, y1]

    up = [ck_distance(x1, y1 + 1, x2, y2), x1, y1 + 1]
    down = [ck_distance(x1, y1 - 1, x2, y2), x1, y1 - 1]

    right = [ck_distance(x1 + 1, y1, x2, y2), x1 + 1, y1]
    right_up = [ck_distance(x1 + 1, y1 + 1, x2, y2), x1 + 1, y1 + 1]
    right_down = [ck_distance(x1 + 1, y1 - 1, x2, y2), x1 + 1, y1 - 1]

    left = [ck_distance(x1 - 1, y1, x2, y2), x1 - 1, y1]
    left_up = [ck_distance(x1 - 1, y1 + 1, x2, y2), x1 - 1, y1 + 1]
    left_down = [ck_distance(x1 - 1, y1 - 1, x2, y2), x1 - 1, y1 - 1]

    best_distance = 400

    if up[0] < best_distance:
        best_distance = up[0]
        x1 = up[1]
        y1 = up[2]

    if down[0] < best_distance:
        best_distance = down[0]
        x1 = down[1]
        y1 = down[2]

    if right_down[0] < best_distance:
        best_distance = right_down[0]
        x1 = right_down[1]
        y1 = right_down[2]

    if right[0] < best_distance:
        best_distance = right[0]
        x1 = right[1]
        y1 = right[2]

    if right_up[0] < best_distance:
        best_distance = right_up[0]
        x1 = right_up[1]
        y1 = right_up[2]

    if left[0] < best_distance:
        best_distance = left[0]
        x1 = left[1]
        y1 = left[2]

    if left_up[0] < best_distance:
        best_distance = left_up[0]
        x1 = right_up[1]
        y1 = right_up[2]

    if left_down[0] < best_distance:
        x1 = right_up[1]
        y1 = right_up[2]

    return x1, y1

# moves given item based on given info
def move_to(item, x, y):
    if item == 'food':
        food = pygame.draw.circle(DISPLAYSURF, blue, (x, y), 5, 0)
    if item == 'mommaDuck':
        mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 8, 0)
    if item == 'babyDuck':
        babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 5, 0)


# finds direct distance using coordinates
def ck_distance(x1, y1, x2, y2):
    print("checking distance")
    distance1 = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    if x2 - x1 == 0:
        return distance1
    else:
        slope1 = (y2-y1)/(x2-x1)
        print("Distance is: ", distance1, slope1)
        return distance1


# main game loop
while True:

    # manipulating display surface
    DISPLAYSURF.fill(black)
    food = pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 5, 0)

    mx, my = ck_neighbors(mx, my, foodx, foody)
    mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mx, my), 8, 0)

    bx, by = ck_neighbors(bx, by, mx, my)
    babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (bx, by), 5, 0)

    ################################################################
    # ducks movement with changing (x,y) coordinates
    #
    # need to be A* algorithm needs to avoid obstacles
    #
    # baby duck needs to be linked to same pathfinder independently
    # but gains and loses attraction to mommaDuck's previous position to imitate following
    ################################################################

    # take start coordinate, check distance from neighboring coordinates, move duck to coordinate that
    # returns the smallest distance from food









    dis = ck_distance(foodx, mx, foody, my)

    # mission complete, reset food location randomly
    if mx == foodx and my == foody:
        import random
        score += 1
        foodx = random.randint(0, 400)
        foody = random.randint(0, 400)
        print("Food coordinates: ", foodx, foody)
        print(score)

        # send to function that changes food coordinates


    # need a better way to manipulate speed
    time.sleep(.02)

    # exit window button
    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)