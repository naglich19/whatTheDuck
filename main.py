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
foodx = 250
foody = 300

while True: #main game loop

    DISPLAYSURF.fill(black)

    mommaDuck = pygame.draw.circle(DISPLAYSURF, yellow, (mommaDuckx, mommaDucky), 8, 0)
    babyDuck = pygame.draw.circle(DISPLAYSURF, yellow, (babyDuckx, babyDucky), 5, 0)
    food = pygame.draw.circle(DISPLAYSURF, blue, (foodx, foody), 5, 0)

    #mommaDucks mission is to get to the food as quick as possible

    if mommaDuckx < foodx:
        mommaDuckx += 3
    if mommaDuckx > foodx:
        mommaDuckx -= 3
    if mommaDucky < foody:
        mommaDucky += 3
    if mommaDucky > foody:
        mommaDucky -= 3

    if babyDuckx < mommaDuckx - 5:
        babyDuckx += 2
    if babyDuckx > mommaDuckx + 5:
        babyDuckx -= 2
    if babyDucky < mommaDucky - 5:
        babyDucky += 2
    if babyDucky > mommaDucky + 5:
        babyDucky -= 2
    time.sleep(.03)

    pygame.display.update()
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        fpsClock.tick(FPS)