import pygame, sys
import time

from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 400), 0, 0)
pygame.display.set_caption('what The Duck')

#color palette

black = (35, 50, 80)
blue = (50, 150, 255)
yellow = (255, 255, 0)

#mommaDuck start Coordinates
mommaDuckx = 10
mommaDucky = 10
babyDuckx = 9
babyDucky = 9
#food start Coordinates
foodx = 200
foody = 200

belly = 0

while True: #main game loop

    DISPLAYSURF.fill(black)

    food = pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 5, 0)

    mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mommaDuckx, mommaDucky), 8, 0)
    babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (babyDuckx, babyDucky), 5, 0)


    #mommaDucks mission is to get to the food as quick as possible

    if mommaDuckx < foodx:
        mommaDuckx += 1
    if mommaDuckx > foodx:
        mommaDuckx -= 1
    if mommaDucky < foody:
        mommaDucky += 1
    if mommaDucky > foody:
        mommaDucky -= 1

#    if babyDuckx < mommaDuckx - 1:
#        babyDuckx += 2
#   if babyDuckx > mommaDuckx + 1:
#        babyDuckx -= 2
#    if babyDucky < mommaDucky - 1:
#        babyDucky += 2
#    if babyDucky > mommaDucky + 1:
#       babyDucky -= 2

    def distance(x1,x2,y1,y2):
        print ("checking distance")
        m = 0
        if x2-x1 != 0:
            m = (y2-y1)/(x2-x1)
        print("Slope is: ", m)


    distance(foodx, foody, mommaDuckx, mommaDucky)

    if mommaDuckx == foodx and mommaDucky == foody:
        import random
        belly += 1
        foodx = random.randint(0, 400)
        foody = random.randint(0, 400)
        print("Food coordinates: ", foodx, foody)

        print (belly)


    time.sleep(.02)


    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)