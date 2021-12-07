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
ENTITIES = ()
ENEMIES = ()
NAME = "test"
START_POS = (255, 255, 2*math.pi)

BLOCK_SIZE = 64
SIZE = 8
MAP_X = 8
MAP_Y = 8

SCREEN_SIZE = (1024, 512)
size = SCREEN_SIZE


class Level:
    def __init__(self, srf, file=None, pos=(0, 0)):
        self.surface = srf
        if file is not None:
            self.map, self.block_size, self.start_position, self.entities, self.enemies = self._load_file(file)
        else:
            self.map = LEVEL
            self.block_size = BLOCK_SIZE
            self.start_position = START_POS
            self.entities = ENTITIES
            self.enemies = ENEMIES
        self.position = pos

    def draw(self):
        for y, yv in enumerate(self.map):
            for x, xv in enumerate(yv):
                if xv == 1:
                    color = (255, 255, 255)  # white
                else:
                    color = (0, 0, 0)  # black

                # calculate coordinates of block vertices, add one pixel of border around them
                positions = ((self.position[0] + x*self.block_size + 1,
                              self.position[1] + y*self.block_size + 1),

                             (self.position[0] + (x+1)*self.block_size - 1,
                              self.position[1] + y*self.block_size + 1),

                             (self.position[0] + (x+1)*self.block_size - 1,
                              self.position[1] + (y+1)*self.block_size - 1),

                             (self.position[0] + x*self.block_size + 1,
                              self.position[1] + (y+1)*self.block_size - 1))

                pg.draw.polygon(self.surface, color, positions)
