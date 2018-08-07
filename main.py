# I want baby duck to search for and find mommaDucks PREVIOUS position to imitate following.
# right now it just stays at least 10 pixels away at all times
# might be able to store this location with a*
#
# ducks movement with changing (x,y) coordinates
# need to be a* algorithm needs to avoid obstacles
#
# baby duck needs to use same pathfinder independently but gains and loses
# attraction to mommaDuck's PREVIOUS position to imitate following
# and lack of following, kind of a lose focus and wander trait
#
# with a*, path needs to loop new coordinates through my move_to function.
# should be able to reuse target information. might have to rebuild babyduck following.

import pygame
import sys
import time
import math
import random

from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 400), 0, 0)
pygame.display.set_caption('What_The_Duck')

# color palette
dark_blue = (35, 50, 80)
blue = (50, 150, 255)
yellow = (255, 255, 0)

# starting variables and targets
target = 0

# food = [food_x, food_y]
food_x = 200
food_y = 200
food = [food_x, food_y]
score = 0

#               0       1       2        3       4(t/f) 5(t/f)
# mommaDuck = [mom_x, mom_y, target_x, target_y, lost1, lost2]
mDuck = [20, 20, food_x, food_y, False, False]

#                 0        1       2      3      4(t/f)
# babyDuck1 = [baby_x1, baby_x2, mom_x, mom_y, wander]
bDuck1 = [10, 10, mDuck[0], mDuck[1], False]

#               0         1        2         3      4(t/f)
# babyDuck2 = [baby_x2, baby_y2, baby_x1, baby_y2, wander]
bDuck2 = [0, 0, bDuck1[2], bDuck1[3], False]

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

    if item == 'mDuck':
        pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 5, 0)
    if item == 'bDuck1':
        pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 2, 0)
    if item == 'bDuck2':
        pygame.draw.circle(DISPLAYSURF, yellow, (x, y), 2, 0)
    if item == 'food':
        pygame.draw.circle(DISPLAYSURF, blue, (x, y), 2, 0)


# finds direct distance using coordinates
def ck_distance(x1, y1, x2, y2):
    print("checking distance")
    distance1 = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    if x2 - x1 == 0:
        return abs(distance1)
    else:
        slope1 = (y2-y1)/(x2-x1)
        print("Distance is: ", distance1, slope1)
        return abs(distance1)


# randomizes location of food each time it gets eaten by mommaDuck
def rand_food():
    new_x = random.randint(0, 400)
    new_y = random.randint(0, 400)
    return new_x, new_y


# make babyDuck wander if wander setting is True
def wander():
    new_x = random.randint(0, 400)
    new_y = random.randint(0, 400)
    return new_x, new_y


# main game loop
while True:

    # manipulating display surface
    DISPLAYSURF.fill(dark_blue)

    # Key ##########################################################
    #  index:         0      1      2         3      4(t/f) 5(t/f) #
    # mommaDuck = [mom_x, mom_y, target_x, target_y, lost1, lost2] #
    ################################################################
    #  index:         0        1       2         3       4(t/f)    #
    # babyDuck1 = [baby_x1, baby_x2, target_x, target_y, wander]   #
    ################################################################
    #  index:         0        1       2         3       4(t/f)    #
    # babyDuck2 = [baby_x2, baby_y2, target_x, target_y, wander]   #
    ################################################################

    food = [food_x, food_y]

    # turn into mission function (send targetx, target y) if lost == true: target = baby

    # if babyduck is lost mommaDuck's target is babyDuck1
    if mDuck[4] is True:
        mDuck[2] = bDuck1[0]
        mDuck[3] = bDuck1[1]
        # if mommaDuck is at babyDuck1, babyDuck1 is no longer lost
        if mDuck[0] == mDuck[2] and mDuck[1] == mDuck[3]:
            mDuck[4] = False
            bDuck1[4] = False
            target += 1

    # if babyduck is lost mommaDuck's target is babyDuck2
    if mDuck[5] is True:
        mDuck[2] = bDuck2[0]
        mDuck[3] = bDuck2[1]
        # if mommaDuck is at babyDuck1, babyDuck2 is no longer lost
        if mDuck[0] == mDuck[2] and mDuck[1] == mDuck[3]:
            mDuck[4] = False
            bDuck2[4] = False
            target += 1
    # else mommaDuck's target is food
    else:
        mDuck[2] = food[0]
        mDuck[3] = food[1]

    if bDuck1[4] is True:
        bDuck1[2], bDuck1[3] = wander(target)
    else:
        bDuck1[2] = mDuck[0]
        bDuck1[3] = mDuck[1]

    if bDuck2[4] is True:
        bDuck2[2], bDuck2[3] = wander(target)
    else:
        bDuck2[2] = bDuck1[0]
        bDuck2[3] = bDuck1[1]

    ############################################################################################################
    # take start coordinate, check distance from neighboring coordinates, move designated duck to coordinate that
    # returns the closer coordinates to food

    mDuck[0], mDuck[1] = ck_node(mDuck[0], mDuck[1], mDuck[2], mDuck[3])
    move_to('mDuck', mDuck[0], mDuck[1])
    # same as mommaDuck pathfinder but keeps ducks 10 away from target, each one follows the duck in front of it

    if ck_distance(bDuck1[0], bDuck1[1], bDuck1[2], bDuck1[3]) >= 20:
        bDuck1[0], bDuck1[1] = ck_node(bDuck1[0], bDuck1[1], bDuck1[2], bDuck1[3])

    move_to('bDuck1', bDuck1[0], bDuck1[1])

    if ck_distance(bDuck2[0], bDuck2[1], bDuck2[2], bDuck2[3]) >= 17:
        bDuck2[0], bDuck2[1] = ck_node(bDuck2[0], bDuck2[1], bDuck2[2], bDuck2[3])

    move_to('bDuck2', bDuck2[0], bDuck2[1])

    ##############################################################################################################
    # mission complete, reset food location randomly
    if mDuck[0] == food_x and mDuck[1] == food_y:
        # send to function that changes food coordinates and prints first frame
        food_x, food_y = rand_food()
        move_to('food', food_x, food_y)
        score += 1
        print(score)

    # print food for every frame
    move_to('food', food_x, food_y)

    #############################################################################################################
    # need a better way to manipulate speed
    time.sleep(.02)

    # exit window button
    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)
