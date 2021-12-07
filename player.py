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

import world as w
import entity as e


PI_HALFS = math.pi/2
TWO_PI = math.pi*2

SPEED = 3  # pixels/frame
ROT_SPEED = 0.08  # radians/frame

POS_INIT = (256., 256., TWO_PI)  # x, y, rotation
SIZ_INIT = 6
COL_INIT = (255, 255, 0)  # yellow
STA_INIT = (0., 0., 0.)  # speed forward, speed right, rotation anticlockwise

RAY_X_COLOR = (0, 255, 0)  # green
RAY_Y_COLOR = (0, 0, 255)  # blue
WALL_X_COLOR = (255, 0, 0)  # red
WALL_Y_COLOR = (127, 0, 0)  # darker red
SKY_COLOR = (127, 127, 255)  # light blue

DISTANCE = 100000

RAYS = 90

OFFSET_3D = 514
WIDTH_3D = 512


class Player(e.Entity):
    def __init__(self, srf, lvl, fov=90, rays=RAYS, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT, sta=STA_INIT):
        self.surface = srf
        self.level = lvl
        self.fov = fov*0.01745329252
        self.rays = rays
        self.position = pos
        self.color = col
        self.size = siz
        self.state = sta

        self.movement = self._set_move_speed()

        logging.info("created new Player")

    def draw(self):
        pg.draw.polygon(self.surface, SKY_COLOR, ((512, 0), (1024, 0), (1024, 255), (512, 255)))
        self._cast_rays()
        pg.draw.circle(self.surface, self.color, self.position[:2], self.size)
        line_end = (self.position[0] + 4*self.size*math.cos(-self.position[2] - 0.5*math.pi),
                    self.position[1] + 4*self.size*math.sin(-self.position[2] - 0.5*math.pi))
        pg.draw.line(self.surface, self.color, self.position[:2], line_end, int(self.size/3))

    def _cast_rays(self):
        ray_angle_y = (self.position[2] - math.pi / 2)
        ray_angle_y += self.fov / 2

        for i in range(self.rays):

            his0 = False
            vis0 = False

            if ray_angle_y < 0:
                ray_angle_y += 2 * math.pi
            elif ray_angle_y > 2 * math.pi:
                ray_angle_y -= 2 * math.pi

            ray_angle_x = ray_angle_y + PI_HALFS

            if ray_angle_x < 0:
                ray_angle_x += 2 * math.pi
            elif ray_angle_x > 2 * math.pi:
                ray_angle_x -= 2 * math.pi

            atan = 1 / math.tan(ray_angle_y)
            natan = -1 / math.tan(ray_angle_x)

            # vertical lines
            dof = 0
            if PI_HALFS < ray_angle_y < 1.5*math.pi:  # looking right
                rx = (int(self.position[0] / w.BLOCK_SIZE)) * w.BLOCK_SIZE + w.BLOCK_SIZE
                ry = (self.position[0] - rx) * natan + self.position[1]
                x_offset = w.BLOCK_SIZE
                y_offset = - x_offset*natan

            if ray_angle_y > 1.5*math.pi or PI_HALFS > ray_angle_y:  # looking left
                rx = (int(self.position[0] / w.BLOCK_SIZE)) * w.BLOCK_SIZE
                ry = (self.position[0] - rx) * natan + self.position[1]
                rx -= 1
                x_offset = - w.BLOCK_SIZE
                y_offset = - x_offset*natan

            if ray_angle_y in (PI_HALFS, 1.5*math.pi):  # looking straight up or down
                rx = self.position[0]
                ry = self.position[1]
                vis0 = True
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

            if ray_angle_y in (0, math.pi, TWO_PI):  # looking straight left or right
                rx = self.position[0]
                ry = self.position[1]
                his0 = True
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

            if hdist > vdist and not vis0:
                dist = vdist
                rx, ry = rvx, rvy
                wall_color = WALL_Y_COLOR
            elif not his0:
                dist = hdist
                rx, ry = rhx, rhy
                wall_color = WALL_X_COLOR
            else:
                dist = vdist
                rx, ry = rvx, rvy
                wall_color = WALL_Y_COLOR

            pg.draw.line(self.surface, RAY_X_COLOR, self.position[:2], (rx, ry))  # vertical

            # First-Person Viewport

            h_width = WIDTH_3D/self.rays
            h_offset = OFFSET_3D + i * h_width
            v_offset = (1 / dist+0.001)*9000
            pg.draw.line(self.surface, wall_color, (h_offset, 255-v_offset), (h_offset, 255+v_offset), int(h_width)+1)

            ray_angle_y -= self.fov / self.rays
