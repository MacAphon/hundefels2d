#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.0.2"
#
# all rights reserved

import world as w

import math
import logging
import pygame as pg


SPEED = 1.5  # pixels/frame
ROT_SPEED = 0.08  # rad/frame

POS_INIT = (256., 256., 2*math.pi)  # x, y, rotation
SIZ_INIT = 6
COL_INIT = (255, 255, 0)  # yellow
STA_INIT = (0., 0., 0.)  # speed forward, speed right, rotation anticlockwise

RAY_X_COLOR = (0, 255, 0)  # green
RAY_Y_COLOR = (0, 0, 255)  # blue
WALL_X_COLOR = (255, 0, 0)  # red
WALL_Y_COLOR = (127, 0, 0)  # darker red

DISTANCE = 100000

RAYS = 1
FOV = math.pi/2  # 90 degrees


class Player:
    def __init__(self, srf, lvl, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT, sta=STA_INIT):
        self.surface = srf
        self.level = lvl
        self.position = pos
        self.color = col
        self.size = siz
        self.state = sta

        self.movement = self._set_move_speed()

        logging.info("created new Player")

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.position[:2], self.size)
        line_end = (self.position[0] + 4*self.size*math.cos(-self.position[2] - 0.5*math.pi),
                    self.position[1] + 4*self.size*math.sin(-self.position[2] - 0.5*math.pi))
        self._cast_rays()
        pg.draw.line(self.surface, self.color, self.position[:2], line_end, int(self.size/3))

    def _cast_rays(self):
        ray_angle_y = (self.position[2] - math.pi / 2)

        for i in range(RAYS):

            if ray_angle_y < 0:
                ray_angle_y += 2 * math.pi
            elif ray_angle_y > 2 * math.pi:
                ray_angle_y -= 2 * math.pi

            ray_angle_x = ray_angle_y + math.pi/2

            if ray_angle_x < 0:
                ray_angle_x += 2 * math.pi
            elif ray_angle_x > 2 * math.pi:
                ray_angle_x -= 2 * math.pi

            atan = 1 / math.tan(ray_angle_y)
            natan = -1 / math.tan(ray_angle_x)

            # vertical lines
            dof = 0
            if math.pi/2 < ray_angle_y < 1.5*math.pi:  # looking right
                rx = (int(self.position[0] / w.BLOCK_SIZE)) * w.BLOCK_SIZE + w.BLOCK_SIZE
                ry = (self.position[0] - rx) * natan + self.position[1]
                x_offset = w.BLOCK_SIZE
                y_offset = - x_offset*natan

            if ray_angle_y > 1.5*math.pi or math.pi/2 > ray_angle_y:  # looking left
                rx = (int(self.position[0] / w.BLOCK_SIZE)) * w.BLOCK_SIZE
                ry = (self.position[0] - rx) * natan + self.position[1]
                rx -= 1
                x_offset = - w.BLOCK_SIZE
                y_offset = - x_offset*natan

            if ray_angle_y in (math.pi/2, 1.5*math.pi):  # looking straight up or down
                rx = self.position[0]
                ry = self.position[1]
                dof = w.SIZE

            while dof < w.SIZE:  # check for walls
                mx = int(rx/64)
                my = int(ry/64)
                logging.debug(f"0: angle={self.position[2]} {mx=} {my=} {natan=}")
                if 0 <= mx < w.SIZE and 0 <= my < w.SIZE:
                    if self.level.map[my][mx] == 1:  # hit wall
                        dof = w.SIZE
                    else:
                        rx += x_offset
                        ry += y_offset
                        dof += 1
                else:
                    rx += x_offset
                    ry += y_offset
                    dof += 1
                logging.debug(f"1: angle={self.position[2]} {mx=} {my=} {natan=}")

            rvx = rx
            rvy = ry

            ########################################################################
            # horizontal lines
            dof = 0
            if ray_angle_y > math.pi:  # looking up
                ry = (int(self.position[1] / w.BLOCK_SIZE)) * w.BLOCK_SIZE
                rx = (self.position[1] - ry) * atan + self.position[0]
                ry -= 1
                y_offset = - w.BLOCK_SIZE
                x_offset = - y_offset*atan

            if ray_angle_y < math.pi:  # looking down
                ry = (int(self.position[1] / w.BLOCK_SIZE)) * w.BLOCK_SIZE + w.BLOCK_SIZE
                rx = (self.position[1] - ry) * atan + self.position[0]
                y_offset = w.BLOCK_SIZE
                x_offset = - y_offset*atan

            if ray_angle_y in (0, math.pi, 2*math.pi):  # looking straight left or right
                rx = self.position[0]
                ry = self.position[1]
                dof = w.SIZE

            while dof < w.SIZE:  # check for walls
                mx = int(rx/64)
                my = int(ry/64)
                if 0 <= mx < w.SIZE and 0 <= my < w.SIZE:
                    if self.level.map[my][mx] == 1:  # hit wall
                        dof = w.SIZE
                    else:
                        rx += x_offset
                        ry += y_offset
                        dof += 1
                else:
                    rx += x_offset
                    ry += y_offset
                    dof += 1

            rhx = rx
            rhy = ry

            vdist = math.sqrt((rvx-self.position[0])**2+(rvy-self.position[1])**2)
            hdist = math.sqrt((rhx-self.position[0])**2+(rhy-self.position[1])**2)

            if vdist > hdist:
                rx, ry = rhx, rhy
                col = RAY_X_COLOR
            else:
                rx, ry = rvx, rvy
                col = RAY_Y_COLOR

            pg.draw.line(self.surface, col, self.position[:2], (rx, ry))  # vertical

    def set_state(self, x=None, y=None, r=None):
        """ f:forward, s:sidewards (right), r:rotation (counterclockwise)
        """
        self.state = (self.state[0]+x*SPEED if x is not None else self.state[0],
                      self.state[1]+y*SPEED if y is not None else self.state[1],
                      self.state[2]+r*ROT_SPEED if r is not None else self.state[2])

        logging.debug(f"player state update: {self.state} {self.position}")

    def move(self):
        self.movement = self._set_move_speed()

        rot = self.position[2] + self.state[2]  # calculate new angle
        if rot <= 0:  # reset the angle if it is outside normal range
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
        """ calculate absolute movement speed from movement relative to player rotation
        """
        x = self.state[0]*math.cos(self.position[2]) + self.state[1]*math.sin(self.position[2])
        y = self.state[1]*math.cos(self.position[2]) - self.state[0]*math.sin(self.position[2])
        return x, y
