#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.0.1"
#
# all rights reserved

import world as w

import math
import logging
import pygame as pg

SPEED = 1.5  # pixels/frame
ROT_SPEED = 0.06  # rad/frame

POS_INIT = (256., 256., 0.)
SIZ_INIT = 6
COL_INIT = (255, 255, 0)  # yellow
STA_INIT = (0., 0., 0.)  # speed forward, speed right, rotation anticlockwise


class Player:
    def __init__(self, srf, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT, sta=STA_INIT):
        self.surface = srf
        self.position = pos
        self.color = col
        self.size = siz
        self.state = sta

        self.movement = self._set_move_speed()

        logging.info("created new Player")

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.position[:2], self.size)
        logging.debug(f"w{self.position=}")
        line_end = (self.position[0] + 4*self.size*math.cos(-self.position[2] - 0.5*math.pi),
                    self.position[1] + 4*self.size*math.sin(-self.position[2] - 0.5*math.pi))
        pg.draw.line(self.surface, self.color, self.position[:2], line_end, int(self.size/3))

    def set_state(self, x=None, y=None, r=None):
        """ f:forward, s:sidewards (right), r:rotation (counterclockwise)"""

        self.state = (self.state[0]+x*SPEED if x is not None else self.state[0],
                      self.state[1]+y*SPEED if y is not None else self.state[1],
                      self.state[2]+r*ROT_SPEED if r is not None else self.state[2])

        logging.debug(f"state update: {self.state} {self.position}")

    def move(self):

        self.movement = self._set_move_speed()

        rot = self.position[2] + self.state[2]  # calculate new angle
        if rot < 0:
            rot += 2*math.pi
        elif rot > 2*math.pi:
            rot -= 2*math.pi

        new_pos = (self.position[0] + self.movement[0],
                   self.position[1] + self.movement[1],
                   rot)

        # keep the player in the map
        if new_pos[0] < 0:
            new_pos = 0, new_pos[1], new_pos[2]
        elif new_pos[0] > w.size[0]/2:
            new_pos = w.size[0]/2, new_pos[1], new_pos[2]

        if new_pos[1] < 0:
            new_pos = new_pos[0], 0, new_pos[2]
        elif new_pos[1] > w.size[1]:
            new_pos = new_pos[0], w.size[1], new_pos[2]

        self.position = new_pos

    def _set_move_speed(self):
        x = self.state[0]*math.cos(self.position[2]) + self.state[1]*math.sin(self.position[2])
        y = self.state[1]*math.cos(self.position[2]) - self.state[0]*math.sin(self.position[2])
        return x, y
