import pygame, sys
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

# mommaDuck start Coordinates
mommaDuckx = 10
mommaDucky = 10
babyDuckx = 9
babyDucky = 9

# food start Coordinates
foodx = 200
foody = 200
direction = 'north'
belly = 0


# finds direct distance using coordinates
def distance(x1, x2, y1, y2):
    print("checking distance")
    distance1 = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
    slope1 = 0
    if x2 - x1 == 0:
        donothing = 1
    else:
        slope1 = (y2-y1)/(x2-x1)
        print("Distance is: ", distance1, slope1)
        return distance1

# main game loop
while True:

    DISPLAYSURF.fill(black)
    # print to display surface
    food = pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 5, 0)
    mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mommaDuckx, mommaDucky), 8, 0)
    babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (babyDuckx, babyDucky), 5, 0)

    # ducks movement
    # need to be A* algo
    # baby duck needs to be independant but gains and loses attraction to mommaDuck position
    if mommaDuckx < foodx:
        # checks for diagonal requirement
        if mommaDuckx < foodx and mommaDucky > foody:
            mommaDuckx += 1
            mommaDucky -= 1

            babyDuckx = mommaDuckx - 10
            babyDucky = mommaDucky + 10
            direction = 'SE'
        # single direction
        else:
            mommaDuckx += 1
            babyDuckx = mommaDuckx - 15
            babyDucky = mommaDucky
            direction = 'E'

    if mommaDuckx > foodx:
        if mommaDuckx > foodx and mommaDucky < foody:
            mommaDuckx -= 1
            mommaDucky += 1

            babyDuckx = mommaDuckx + 15
            babyDucky = mommaDucky - 15
            direction = 'NW'
        else:
            mommaDuckx -= 1
            babyDuckx = mommaDuckx + 15
            babyDucky = mommaDucky
            direction = 'W'

    if mommaDucky < foody:
        if mommaDucky < foody and mommaDuckx < foodx:
            mommaDuckx += 1
            mommaDucky += 1

            babyDuckx = mommaDuckx - 15
            babyDucky = mommaDucky - 15
            direction = 'SW'
        else:
            mommaDucky += 1
            babyDucky = mommaDucky - 15
            babyDuckx = mommaDuckx
            direction = 'N'

    if mommaDucky > foody:
        if mommaDucky > foody and mommaDuckx > foodx:
            mommaDuckx -= 1
            mommaDucky -= 1

            babyDuckx = mommaDuckx + 15
            babyDucky = mommaDucky + 15
            direction = 'NE'
        else:
            mommaDucky -= 1
            babyDucky = mommaDucky + 15
            babyDuckx = mommaDuckx
            direction = 'E'

    dis = distance(foodx, mommaDuckx, foody, mommaDucky)

    # mission complete, reset food location randomly
    if mommaDuckx == foodx and mommaDucky == foody:
        import random
        belly += 1
        foodx = random.randint(0, 400)
        foody = random.randint(0, 400)
        print("Food coordinates: ", foodx, foody)

        print(belly)

    time.sleep(.02)

    # exit window button
    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)