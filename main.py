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
mommaDuckx = 10
mommaDucky = 10
babyDuckx = 9
babyDucky = 9

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


# finds direct distance using coordinates
def distance(x1, x2, y1, y2):
    print("checking distance")
    distance1 = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    if x2 - x1 == 0:
        return 0
    else:
        slope1 = (y2-y1)/(x2-x1)
        print("Distance is: ", distance1, slope1)
        return distance1, slope1


# main game loop
while True:

    # manipulating display surface
    DISPLAYSURF.fill(black)
    food = pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 5, 0)
    mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mommaDuckx, mommaDucky), 8, 0)
    babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (babyDuckx, babyDucky), 5, 0)

    ################################################################
    # ducks movement with changing (x,y) coordinates
    #
    # need to be A* algorithm needs to avoid obstacles
    #
    # baby duck needs to be linked to same pathfinder independently
    # but gains and loses attraction to mommaDuck's previous position to imitate following
    ################################################################

    dis = distance(foodx, mommaDuckx, foody, mommaDucky)

    # mission complete, reset food location randomly
    if mommaDuckx == foodx and mommaDucky == foody:
        import random
        score += 1
        foodx = random.randint(0, 400)
        foody = random.randint(0, 400)
        print("Food coordinates: ", foodx, foody)

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