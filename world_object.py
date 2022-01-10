#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# all rights reserved

import logging

import entity as e


POS_INIT = (100., 100., 0.)  # x, y, rotation
COL_INIT = (0, 255, 255)  # aqua
SIZ_INIT = 4


class WorldObject(e.Entity):
    """
    static, non interacting entity
    """
    def __init__(self, srf, pos=POS_INIT, col=COL_INIT, siz=SIZ_INIT):
        self._surface = srf
        self.position = pos
        self.color = col
        self._size = siz

        logging.info("created new WorldObject")
