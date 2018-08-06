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
dark_blue = (35, 50, 80)
blue = (50, 150, 255)
yellow = (255, 255, 0)

# mommaDuck and babyDuck start Coordinates
mx = 20
my = 20

bx1 = 10
by1 = 10

bx2 = 0
by2 = 0


# food coordinates and score start
foodx = 200
foody = 200
score = 0


# create display surface grid imitation(400x400) to create colliders
# should find a way to draw obstacles vs. manual input to each coordinate
# could pull from file ex:
# 11111111111
# 10000000001
# 10001100001
# 10001111001
# 10000000001
# 11111111111
m = 400
n = 400
a = [0] * n
for i in range(n):
    a[i] = [0] * m
    print(a[i])


# checks node if distance to food is shorter than changes coordinates to best node
# very VERY slow and inefficient
# intention^ but not working properly, need to fix order/priority
def ck_node(x1, y1, x2, y2):

    # format = [distance from node to target, node x1, node y1]
    up = [(ck_distance(x1, y1 + 1, x2, y2)), x1, y1 + 1]
    down = [(ck_distance(x1, y1 - 1, x2, y2)), x1, y1 - 1]

    right = [(ck_distance(x1 + 1, y1, x2, y2)), x1 + 1, y1]
    right_up = [(ck_distance(x1 + 1, y1 + 1, x2, y2)), x1 + 1, y1 + 1]
    right_down = [(ck_distance(x1 + 1, y1 - 1, x2, y2)), x1 + 1, y1 - 1]

    left = [(ck_distance(x1 - 1, y1, x2, y2)), x1 - 1, y1]
    left_up = [(ck_distance(x1 - 1, y1 + 1, x2, y2)), x1 - 1, y1 + 1]
    left_down = [(ck_distance(x1 - 1, y1 - 1, x2, y2)), x1 - 1, y1 - 1]

    best_distance = 800

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
        x1 = left_up[1]
        y1 = left_up[2]

    if left_down[0] < best_distance:
        x1 = left_down[1]
        y1 = left_down[2]

    return x1, y1


# moves given item based on given info
def move_to(item, x, y):
    if item == 'food':
        pygame.draw.circle(DISPLAYSURF, blue, (x, y), 2, 0)
    if item == 'mommaDuck':
        pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 5, 0)
    if item == 'babyDuck':
        pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 2, 0)


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


# randomizes location of food each time it gets eaten by mommaDuck
def rand_food():
    import random
    new_x = random.randint(0, 400)
    new_y = random.randint(0, 400)
    print("Food coordinates: ", new_x, new_y)
    return new_x, new_y


# main game loop
while True:

    # manipulating display surface
    DISPLAYSURF.fill(dark_blue)
    pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 3, 0)

    # take start coordinate, check distance from neighboring coordinates, move designated duck to coordinate that
    # returns the closer coordinates to food

    mx, my = ck_node(mx, my, foodx, foody)

    # same as mommaDuck pathfinder but keeps ducks 10 away from target, each one follows the duck in front of it
    if ck_distance(bx1, by1, mx, my) > 20:
        bx1, by1 = ck_node(bx1, by1, mx, my)

    if ck_distance(bx2, by2, bx1, by1) >= 17:
        bx2, by2 = ck_node(bx2, by2, bx1, by1)

    # print all ducks
    pygame.draw.circle(DISPLAYSURF, yellow, (mx, my), 8, 0)
    pygame.draw.circle(DISPLAYSURF, yellow, (bx1, by1), 5, 0)
    pygame.draw.circle(DISPLAYSURF, yellow, (bx2, by2), 5, 0)

    # I want baby duck to search for and find mommaDucks PREVIOUS position to imitate following.
    # right now it just stays at least 10 pixels away at all times

    ##################################################################################
    # ducks movement with changing (x,y) coordinates                                 #
    # need to be A* algorithm needs to avoid obstacles                               #
    #                                                                                #
    # baby duck needs to use same pathfinder independently but gains and loses       #
    # attraction to mommaDuck's previous position to imitate following               #
    # and lack of following, kind of a lose focus and wander trait                   #
    ##################################################################################

    # mission complete, reset food location randomly
    if mx == foodx and my == foody:
        # send to function that changes food coordinates
        foodx, foody = rand_food()
        score += 1
        print(score)

    # need a better way to manipulate speed
    time.sleep(.02)

    # exit window button
    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)
