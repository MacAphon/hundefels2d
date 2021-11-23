#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.0.1"
#
# all rights reserved

import player as p
import world as w


import sys
import math
import os
import getopt
import time
import logging
import pygame as pg
from socket import *
from pygame.locals import *


SCREEN_SIZE = (1024, 512)

P_POSITION_INIT = (512., 255.)
P_COLOR_INIT = (255, 255, 0)  # yellow
P_STATE_INIT = (0., 0.)
P_SIZE_INIT = 8


# noinspection PyArgumentList
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S",
                    filename="hf2d.log", encoding="utf-8", filemode="w", level=logging.DEBUG)


def main():
    logging.info("started")
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Hundefels2D")

    logging.debug("initialized screen")

    pl = p.Player(screen)
    lv = w.Level(screen)

    screen.fill((80, 80, 80))
    pg.display.flip()

    logging.info("setup complete")
    logging.info("starting main loop")

    perf_warn = False

    while 1:
        t = time.perf_counter() + 1/60

        for event in pg.event.get():
            if event.type == QUIT:
                logging.info("stopped")
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    pl.set_state(y=-1)
                if event.key == K_a:
                    pl.set_state(x=-1)
                if event.key == K_s:
                    pl.set_state(y=1)
                if event.key == K_d:
                    pl.set_state(x=1)

            elif event.type == KEYUP:
                if event.key == K_w:
                    pl.set_state(y=1)
                if event.key == K_a:
                    pl.set_state(x=1)
                if event.key == K_s:
                    pl.set_state(y=-1)
                if event.key == K_d:
                    pl.set_state(x=-1)

        screen.fill((80, 80, 80))

        lv.draw()
        pl.move()
        pl.draw()

        pg.display.flip()

        if time.perf_counter() >= t and not perf_warn:
            perf_warn = True
            logging.warning("performance low, game may not work as intended")

        while time.perf_counter() < t:
            pass


if __name__ == '__main__':
    main()
