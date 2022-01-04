#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# all rights reserved

import getopt
import logging
import sys
import time

import pygame as pg
from pygame.locals import *

import player as p
import world as w
import world_object as wo

SCREEN_SIZE_FP = (1024, 512)
SCREEN_SIZE_MAP = (512, 512)

LEVEL_PATHS = (None,
               "data/levels/lv1.json",
               "data/levels/lv2.json",
               "data/levels/lv3.json")

argument_list = sys.argv[1:]
OPTIONS = "hl:"
LONG_OPTIONS = ("help", "level", "fov", "rays")

# noinspection PyArgumentList
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S",
                    filename="hf2d.log", encoding="utf-8", filemode="w", level=logging.DEBUG)


def main():
    logging.info("starting")
    logging.info(f"{argument_list=}")

    # parse command line arguments
    try:
        arguments, values = getopt.getopt(argument_list, OPTIONS, LONG_OPTIONS)
        lv = None
        rays = 90
        fov = 90
        for argument, value in arguments:
            if argument in ("-h", "--help"):
                logging.info("showing help")
                print(f"options: -{OPTIONS[:-1]}\n"
                      f"long options: {LONG_OPTIONS}\n\n"
                      f"-h, --help: show this help, stops the game\n"
                      f"-l, --level: load the level with the specified number or path\n"
                      f"--fov: set the field of view in degrees (default: 90°)\n"
                      f"--rays: set the number of rays cast (default: 90)\n"
                      f"\tlower values can help performance on lower end systems\n")
                logging.info("stopped")
                return

            elif argument in ("-l", "--level"):
                try:
                    lv = LEVEL_PATHS[int(value)]
                    logging.info(f"level selected by number: {lv}")
                except ValueError:
                    lv = value
                    logging.info(f"level selected by file: {lv}")

            elif argument == "--fov":
                try:
                    fov = int(value)
                except ValueError:
                    logging.error(f"fov not an integer")
                    print("fov must be an integer")
                    continue

            elif argument == "--rays":
                try:
                    rays = int(value)
                except ValueError:
                    logging.error(f"rays not an integer")
                    print("rays must be an integer")
                    continue

            else:
                logging.info(f"unknown argument: {argument, value}")
                print(f"unknown argument: {argument, value}")

    except getopt.error as err:
        logging.fatal(str(err))
        print(str(err))
        return

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE_FP)
    pg.display.set_caption("Hundefels2D")

    logging.info("initialized screen")

    lvl = w.Level(screen, lv)
    pl = p.Player(screen, lvl, rays=rays, fov=fov, pos=lvl.start_position)

    entities = [wo.WorldObject(screen, position) for position in lvl.entities]

    screen.fill((80, 80, 80))
    pg.display.flip()

    logging.info("setup complete")
    logging.info("starting main loop")

    perf_warn = False

    while 1:
        t = time.time() + 1/60
        t_warn = time.time() + 1/50

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
                if event.key == K_RIGHT:
                    pl.set_state(r=-1)
                if event.key == K_LEFT:
                    pl.set_state(r=1)

            elif event.type == KEYUP:
                if event.key == K_w:
                    pl.set_state(y=1)
                if event.key == K_a:
                    pl.set_state(x=1)
                if event.key == K_s:
                    pl.set_state(y=-1)
                if event.key == K_d:
                    pl.set_state(x=-1)
                if event.key == K_RIGHT:
                    pl.set_state(r=1)
                if event.key == K_LEFT:
                    pl.set_state(r=-1)

        screen.fill((80, 80, 80))

        lvl.draw()
        pl.move()
        pl.draw(entities)

        pg.display.flip()

        if time.time() >= t_warn and not perf_warn:
            perf_warn = True
            print("performance low, game may not work as intended")
            logging.warning("low performance")

        while time.time() < t:
            time.sleep(1/240)


if __name__ == '__main__':
    main()
