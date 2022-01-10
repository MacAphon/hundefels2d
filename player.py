#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# all rights reserved

import math
import logging

import pygame as pg
from numba import njit

import entity as e

PI_HALFS = math.pi / 2
TWO_PI = math.pi * 2

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

DISTANCE = 1000000

RAYS = 90

OFFSET_3D = 514
WIDTH_3D = 512

VIEWPORT_CLIP = pg.Rect(512, 0, 512, 512)
MAP_CLIP = pg.Rect(0, 0, 512, 512)


# function is outside of the class to work around limitations of numba
@njit()  # make the function run a lot faster by using just in time compilation
def _cast_rays(rays: int, fov: float, position: tuple, level_map: list, block_size: int, level_size: int):
    """
    calculate the length of rays on the map
    """
    ray_angle_y = (position[2] - PI_HALFS)
    ray_angle_y += fov / 2

    rays_list = []

    for i in range(rays):

        his0 = False
        vis0 = False

        if ray_angle_y < 0:
            ray_angle_y += TWO_PI
        elif ray_angle_y > TWO_PI:
            ray_angle_y -= TWO_PI

        ray_angle_x = ray_angle_y + PI_HALFS

        if ray_angle_x < 0:
            ray_angle_x += TWO_PI
        elif ray_angle_x > TWO_PI:
            ray_angle_x -= TWO_PI

        atan = 1 / math.tan(ray_angle_y)
        natan = -1 / math.tan(ray_angle_x)

        # vertical lines
        dof = 0
        if PI_HALFS < ray_angle_y < 1.5 * math.pi:  # looking right
            rx = (int(position[0] / block_size)) * block_size + block_size
            ry = (position[0] - rx) * natan + position[1]
            x_offset = block_size
            y_offset = - x_offset * natan

        if ray_angle_y > 1.5 * math.pi or PI_HALFS > ray_angle_y:  # looking left
            rx = (int(position[0] / block_size)) * block_size
            ry = (position[0] - rx) * natan + position[1]
            rx -= 1
            x_offset = - block_size
            y_offset = - x_offset * natan

        if ray_angle_y in (PI_HALFS, 1.5 * math.pi):  # looking straight up or down
            rx = position[0]
            ry = position[1]
            vis0 = True
            dof = level_size

        while dof < level_size:  # check for walls
            mx = int(rx / block_size)
            my = int(ry / block_size)
            if 0 <= mx < level_size and 0 <= my < level_size:
                if level_map[my][mx] == 1:  # hit wall
                    dof = level_size
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
            ry = (int(position[1] / block_size)) * block_size
            rx = (position[1] - ry) * atan + position[0]
            ry -= 1
            y_offset = - block_size
            x_offset = - y_offset * atan

        if ray_angle_y < math.pi:  # looking down
            ry = (int(position[1] / block_size)) * block_size + block_size
            rx = (position[1] - ry) * atan + position[0]
            y_offset = block_size
            x_offset = - y_offset * atan

        if ray_angle_y in (0., math.pi, TWO_PI):  # looking straight left or right
            rx = position[0]
            ry = position[1]
            his0 = True
            dof = level_size

        while dof < level_size:  # check for walls
            mx = int(rx / block_size)
            my = int(ry / block_size)
            if 0 <= mx < level_size and 0 <= my < level_size:
                if level_map[my][mx] == 1:  # hit wall
                    dof = level_size
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

        # calculate the shorter distance
        vdist = math.sqrt((rvx - position[0]) ** 2 + (rvy - position[1]) ** 2)  # pythagoras
        hdist = math.sqrt((rhx - position[0]) ** 2 + (rhy - position[1]) ** 2)

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

        rays_list.append((dist, ray_angle_y, i, wall_color, (rx, ry)))

        ray_angle_y -= fov / rays
    return rays_list

##############################################################################


class Player(e.Entity):
    """
    player controlled entity, camera of the game
    """
    def __init__(self, srf, lvl, fov=90, rays=RAYS, pos=POS_INIT):
        self._surface = srf
        self._level = lvl
        self._fov = fov * 0.01745329252  # convert degrees to radians
        self._rays = rays
        self.position = pos
        self._color = COL_INIT
        self._size = SIZ_INIT
        self._state = STA_INIT
        self._speed = SPEED
        self._rot_speed = ROT_SPEED

        self.movement = self._set_move_speed()

        # call the function once to force numba to compile it
        _cast_rays(self._rays, self._fov, self.position,
                   self._level.map, self._level.block_size, self._level.size)

        logging.info("created new Player")

    def draw(self, entities):
        """
        draw the viewport and the player on the map
        """

        pg.draw.polygon(self._surface, SKY_COLOR, ((512, 0), (1024, 0), (1024, 255), (512, 255)))  # sky

        self._draw_rays(_cast_rays(self._rays, self._fov, self.position,
                                   self._level.map, self._level.block_size, self._level.size),
                        VIEWPORT_CLIP, MAP_CLIP, entities)

        pg.draw.circle(self._surface, self._color, self.position[:2], self._size)  # player circle
        # line showing where the player is looking
        line_end = (self.position[0] + 4 * self._size * math.cos(-self.position[2] - PI_HALFS),
                    self.position[1] + 4 * self._size * math.sin(-self.position[2] - PI_HALFS))
        pg.draw.line(self._surface, self._color, self.position[:2], line_end, int(self._size / 3))

        for entity in entities:
            entity.draw()

    def _entity_viewport_position(self, entity):
        """
        calculate the horizontal position of an entity in the viewport based on it's an the players positions
        """

        dist = math.dist(self.position[:2], entity.position[:2])

        a = (self.position[0]-entity.position[0])  # delta x
        a += 0.00001 if a == 0 else 0  # make a != 0
        abs_angle = math.atan((self.position[1]-entity.position[1])/a)  # atan(delta y/delta x)

        rel_angle = self.position[2] + abs_angle
        if a <= 0:  # keep the entity "in place" when to the left of it
            rel_angle += math.pi
        rel_angle = rel_angle - TWO_PI if rel_angle > TWO_PI else rel_angle  # keep rel_angle below 2*pi
        rel_angle = rel_angle + TWO_PI if rel_angle < 0 else rel_angle  # keep rel_angle above 0

        rel_angle += self._fov/2

        return dist, (rel_angle / self._fov) * 512

    def _draw_rays(self, rays, viewport_clip, map_clip, entities):
        """
        draws rays and entities
        """
        vp_positions = [(self._entity_viewport_position(entity), entity) for entity in entities]
        vp_positions.sort()  # sort by distance
        vp_positions.reverse()  # furthest entity first

        rendered_rays = []

        for entity in vp_positions:  # draw everything behind the entity that has not yet been rendered
            (e_dist, e_pos), e_vals = entity
            for ray in rays:
                if ray[0] >= e_dist and ray not in rendered_rays:
                    self._draw_ray(ray, map_clip, viewport_clip)
                    rendered_rays.append(ray)
                else:
                    continue

            self._surface.set_clip(viewport_clip)  # only draw in the viewport
            e_vals.draw_viewport(e_dist, e_pos)
            self._surface.set_clip(None)

        for ray in rays:  # fraw everything in front of all entities
            if ray not in rendered_rays:
                self._draw_ray(ray, map_clip, viewport_clip)

    def _draw_ray(self, ray, map_clip, viewport_clip):
        """
        draws a single ray
        """
        self._surface.set_clip(map_clip)  # only draw in the map

        dist, angle, i, wall_color, r_end = ray
        pg.draw.line(self._surface, RAY_X_COLOR, self.position[:2], r_end)  # map ray

        # First-Person Viewport
        self._surface.set_clip(viewport_clip)  # only draw in the viewport
        h_width = WIDTH_3D / self._rays
        h_offset = OFFSET_3D + i * h_width
        v_offset = (1 / (dist + 0.001)) * 9000
        pg.draw.line(self._surface, wall_color, (h_offset, 255 - v_offset), (h_offset, 255 + v_offset),
                     int(h_width) + 1)

        self._surface.set_clip(None)
