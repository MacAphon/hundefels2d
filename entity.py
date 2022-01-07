#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
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

POS_INIT = (100., 100., 0.)  # x, y, rotation
COL_INIT = (0, 255, 255)  # aqua
SIZ_INIT = 4
STA_INIT = (0., 0., 0.)


class Entity:
    def __init__(self, srf, lvl, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT):
        self._surface = srf
        self._level = lvl
        self.position = pos
        self.color = col
        self._size = siz
        self._state = STA_INIT
        self._speed = SPEED
        self._rot_speed = ROT_SPEED

        self.movement = self._set_move_speed()

        logging.info("created new Entity")

    def draw(self):
        pg.draw.circle(self._surface, self.color, self.position[:2], self._size)

    def set_state(self, x=None, y=None, r=None):
        """x:sidewards(right), y:forward, r:rotation (counterclockwise)"""
        self._state = (self._state[0] + x * self._speed if x is not None else self._state[0],
                       self._state[1] + y * self._speed if y is not None else self._state[1],
                       self._state[2] + r * self._rot_speed if r is not None else self._state[2])

        logging.debug(f"entity state update: {type(self)} {self._state} {self.position}")

    def move(self):
        self.movement = self._set_move_speed()

        rot = self.position[2] + self._state[2]  # calculate new angle
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

        # collision check
        A = 11
        B = 53
        if self._level.map[int(new_pos[1]/64)][int(new_pos[0]/64)] != 0:

            p_chk_v = new_pos[0] - math.floor(new_pos[0]/64)*64  # amount of intrusion into blocks
            p_chk_h = new_pos[1] - math.floor(new_pos[1] / 64) * 64
            # vertical
            if p_chk_h < p_chk_v < A or p_chk_v < A < p_chk_h:
                new_pos = new_pos[0] - p_chk_v, new_pos[1], new_pos[2]
            elif p_chk_h > p_chk_v > B or p_chk_v > B > p_chk_h:
                new_pos = new_pos[0] + p_chk_v - B, new_pos[1], new_pos[2]
            # horizontal
            elif p_chk_v < p_chk_h < A or p_chk_h < A < p_chk_v:
                new_pos = new_pos[0], new_pos[1] - p_chk_h, new_pos[2]
            elif p_chk_v > p_chk_h > B or p_chk_h > B > p_chk_v:
                new_pos = new_pos[0], new_pos[1] + p_chk_h - B, new_pos[2]

        self.position = new_pos

    def _set_move_speed(self):
        """calculate absolute movement speed from movement relative to rotation"""
        x = self._state[0] * math.cos(self.position[2]) + self._state[1] * math.sin(self.position[2])
        y = self._state[1] * math.cos(self.position[2]) - self._state[0] * math.sin(self.position[2])
        return x, y