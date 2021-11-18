#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.0.1"
#
# all rights reserved

import logging
import pygame as pg
from pygame.locals import *


LEVEL = ((1, 1, 1, 1, 1, 1, 1, 1),
         (1, 0, 1, 0, 0, 0, 0, 1),
         (1, 0, 1, 0, 1, 1, 0, 1),
         (1, 0, 1, 0, 1, 1, 0, 1),
         (1, 0, 1, 0, 0, 1, 0, 1),
         (1, 0, 0, 0, 0, 0, 0, 1),
         (1, 0, 0, 0, 0, 0, 0, 1),
         (1, 1, 1, 1, 1, 1, 1, 1))

SCREEN_SIZE = (1024, 512)
size = SCREEN_SIZE
