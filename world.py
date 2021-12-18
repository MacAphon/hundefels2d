#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# all rights reserved

import math
import logging
import json

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

SIZE = 8
BLOCK_SIZE = 512/SIZE

SCREEN_SIZE = (1024, 512)
size = SCREEN_SIZE


def _load_file(file):
    """
    read a JSON file and return the level data
    :param file: String
    :return: List, int, [int, int, int], List, List
    """
    logging.info(f"started reading file")
    with open(file, "r") as file:
        s = json.loads(file.read())
        entities = s["entities"] if "entities" in s else []
        enemies = s["enemies"] if "enemies" in s else []
        return s["map"], s["size"], s["start_pos"], entities, enemies


class Level:
    def __init__(self, srf, file=None):
        """

        :param srf:
        :param file:
        """
        self._surface = srf
        if file is not None:
            self.map, self.size, self.start_position, self.entities, self.enemies = _load_file(file)
            self.start_position = (self.start_position[0], self.start_position[1], self.start_position[2]*0.01745329252)
            self.block_size = 512 / self.size
        else:
            self.map = LEVEL
            self.block_size = BLOCK_SIZE
            self.size = SIZE
            self.start_position = START_POS
            self.entities = ENTITIES
            self.enemies = ENEMIES

    def draw(self):
        for y, yv in enumerate(self.map):
            for x, xv in enumerate(yv):
                if xv == 1:
                    color = (255, 255, 255)  # white
                else:
                    color = (0, 0, 0)  # black

                # calculate coordinates of block vertices, add one pixel of border around them
                positions = ((x * self.block_size + 1, y * self.block_size + 1),
                             ((x + 1) * self.block_size - 1, y * self.block_size + 1),
                             ((x + 1) * self.block_size - 1, (y + 1) * self.block_size - 1),
                             (x * self.block_size + 1, (y + 1) * self.block_size - 1))

                pg.draw.polygon(self._surface, color, positions)
