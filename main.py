import pygame
import sys
import time
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


class Node:
    # initialize for find_best_path. need to better understand this
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def find_best_path(maze, start, end):

    # create start and end nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # inititalize both open and closed lists
    open_list = []
    closed_list = []

    # add the start node
    open_list.append(start_node)

    # loop until you find the end
    while len(open_list) > 0:

        # get current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # pop current off open list and add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0 :
                continue

            # make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # create new node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # loop through children
        for child in children:

            # child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) **2)
            child.f = child.g + child.h

            # child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            #add the child to the open list
            open_list.append(child)


def move_to(item, coord):
    # gives items new location and draws on display surface
    # time delay is to immitate speed, need a surefire way to decide this,
    # pixel movement? path[index] % 2?
    if item == 'food':
        pygame.draw.circle(DISPLAYSURF, blue, (coord), 2, 0)
    if item == 'mommaDuck':
        time.sleep(.01)
        pygame.draw.circle(DISPLAYSURF, yellow, (coord), 5, 0)
    if item == 'babyDuck':
        time.sleep(.0005)
        pygame.draw.circle(DISPLAYSURF, yellow, (coord), 2, 0)


def main():

    # starting variables

    maze = [[0] * 400] * 400
    food = (200, 200)
    score = 0
    mDuck = (20, 20)
    index = 0
    new_food = True

    # main game loop
    while True:

        # repeatedly draw/refresh display surface
        DISPLAYSURF.fill(dark_blue)

        # creates new path if there is a new target
        if new_food is True:
            path = find_best_path(maze, mDuck, food)
            index = 0
            new_food = False

        mDuck = path[index]
        move_to('mommaDuck', path[index])

        # immitates following by picking 10 locations in path behind momma

        if index > 10:
            move_to('babyDuck', path[index - 10])
        else:
            move_to('babyDuck', path[0])
        if index > 20:
            move_to('babyDuck', path[index - 18])
        else:
            move_to('babyDuck', path[0])
        print(path[index])

        # if momma finds food, make new food
        # i want to have a food limit, a belly limit. when reached, babies wandered.
        # belly slowly empties, when empty, momma finds babies, and continues hunt
        if mDuck == food:
            path = 0
            index = 0
            new_food = True
            food = (random.randint(10, 390), random.randint(10, 390))
            score += 1
            move_to('food',food)
            print(score)
        move_to('food', food)
        index += 1
        # exit window button
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
