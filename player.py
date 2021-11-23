#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.0.1"
#
# all rights reserved


import world as w

import logging
import pygame as pg

SPEED = 2

POS_INIT = (256., 256.)
COL_INIT = (255, 255, 0)  # yellow
SIZ_INIT = 6
STA_INIT = (0., 0.)


class Player:
    def __init__(self, srf, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT, sta=STA_INIT):
        self.surface = srf
        self.position = pos
        self.color = col
        self.size = siz
        self.state = sta

        logging.info("created new Player")

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.position, self.size)

    def set_state(self, x=None, y=None):
        self.state = (self.state[0]+x*SPEED if x is not None else self.state[0],
                      self.state[1]+y*SPEED if y is not None else self.state[1])

        logging.debug(f"state update: {self.state}")

    def move(self):
        new_pos = self.position[0] + self.state[0], self.position[1] + self.state[1]

        if new_pos[0] < 0:
            new_pos = 0, new_pos[1]
        elif new_pos[0] > w.size[0]:
            new_pos = w.size[0], new_pos[1]

        if new_pos[1] < 0:
            new_pos = new_pos[0], 0
        elif new_pos[1] > w.size[1]:
            new_pos = new_pos[0], w.size[1]

        self.position = new_pos
