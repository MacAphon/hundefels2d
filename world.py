#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.1.1"
#
# all rights reserved

import math
import logging

import pygame as pg


LEVEL = ((1, 1, 1, 1, 1, 1, 1, 1),
         (1, 0, 1, 0, 0, 0, 0, 1),
         (1, 0, 1, 0, 0, 0, 0, 1),
         (1, 0, 1, 0, 0, 0, 0, 1),
         (1, 0, 1, 0, 0, 0, 0, 1),
         (1, 0, 0, 0, 0, 1, 0, 1),
         (1, 0, 0, 0, 0, 0, 0, 1),
         (1, 1, 1, 1, 1, 1, 1, 1))
NAME = "test"
START_POS = (255, 255, 2*math.pi)

BLOCK_SIZE = 64
SIZE = 8
MAP_X = 8
MAP_Y = 8

SCREEN_SIZE = (1024, 512)
size = SCREEN_SIZE


class Level:
    def __init__(self, srf, file=None, pos=(0, 0), start_pos=START_POS):
        self.surface = srf
        if file is not None:
            pass
        else:
            self.map = LEVEL
        self.position = pos
        self.start_position = start_pos

    def draw(self):
        for y, yv in enumerate(self.map):
            for x, xv in enumerate(yv):
                if xv == 1:
                    color = (255, 255, 255)  # white
                else:
                    color = (0, 0, 0)  # black

                # calculate coordinates of block vertices, add one pixel of border around them
                positions = ((self.position[0] + x * BLOCK_SIZE+1, self.position[1] + y * BLOCK_SIZE+1),
                             (self.position[0] + (x+1) * BLOCK_SIZE-1, self.position[1] + y * BLOCK_SIZE+1),
                             (self.position[0] + (x+1) * BLOCK_SIZE-1, self.position[1] + (y+1) * BLOCK_SIZE-1),
                             (self.position[0] + x * BLOCK_SIZE+1, self.position[1] + (y+1) * BLOCK_SIZE-1))

                pg.draw.polygon(self.surface, color, positions)
