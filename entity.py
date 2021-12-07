#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.1.1"
#
# all rights reserved

import logging
import math

import pygame as pg

import world as w


PI_HALFS = math.pi/2
TWO_PI = math.pi*2

SPEED = 2  # pixels/frame
ROT_SPEED = 0.04  # radians/frame

POS_INIT = (100, 100, 0)  # x, y, rotation
COL_INIT = (0, 255, 255)  # aqua
SIZ_INIT = 4
STA_INIT = (0., 0., 0.)


class Entity:
    def __init__(self, srf, lvl, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT, sta=STA_INIT):
        self.surface = srf
        self.level = lvl
        self.position = pos
        self.color = col
        self.size = siz
        self.state = sta

        self.movement = self._set_move_speed()

        logging.info("created new Entity")

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.position[:2], self.size)

    def set_state(self, x=None, y=None, r=None):
        """ x:sidewards(right), y:forward, r:rotation (counterclockwise)
        """
        self.state = (self.state[0] + x * SPEED if x is not None else self.state[0],
                      self.state[1] + y * SPEED if y is not None else self.state[1],
                      self.state[2] + r * ROT_SPEED if r is not None else self.state[2])

        logging.debug(f"entity state update: {type(self)} {self.state} {self.position}")

    def move(self):
        self.movement = self._set_move_speed()

        rot = self.position[2] + self.state[2]  # calculate new angle
        if rot <= 0:  # reset the angle if it is outside normal range
            rot += TWO_PI
        elif rot > TWO_PI:
            rot -= TWO_PI

        new_pos = (self.position[0] + self.movement[0],
                   self.position[1] + self.movement[1],
                   rot)

        # keep the entity in the map
        if new_pos[0] < 0:
            new_pos = 0, new_pos[1], new_pos[2]
        elif new_pos[0] > w.size[0] / 2:
            new_pos = w.size[0] / 2, new_pos[1], new_pos[2]

        if new_pos[1] < 0:
            new_pos = new_pos[0], 0, new_pos[2]
        elif new_pos[1] > w.size[1]:
            new_pos = new_pos[0], w.size[1], new_pos[2]

        self.position = new_pos

    def _set_move_speed(self):
        """ calculate absolute movement speed from movement relative to rotation
        """
        x = self.state[0] * math.cos(self.position[2]) + self.state[1] * math.sin(self.position[2])
        y = self.state[1] * math.cos(self.position[2]) - self.state[0] * math.sin(self.position[2])
        return x, y