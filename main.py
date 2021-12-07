#!/usr/bin/python
#
# Hundefels 2D
# a small 2.5D game by Christian Korn
#
# VERSION = "0.1.1"
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

SCREEN_SIZE = (1024, 512)

LEVEL_PATH = "data/levels.json"

argument_list = sys.argv[1:]
OPTIONS = "hlf:"
LONG_OPTIONS = ("help", "level", "file", "fov", "rays")

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
        lv_sel = False
        for argument, value in arguments:
            if argument in ("-h", "--help"):
                logging.info("showing help")
                print(f"options: -{OPTIONS[:-1]}\n"
                      f"long options: {LONG_OPTIONS}\n\n"
                      f"-h, --help: show this help, stops the game\n"
                      f"-l, --level: load the level with the specified number\n"
                      f"-f, --file: load the specified level file\n"
                      f"\tonly available if `l' or `level' is not given\n"
                      f"--fov: set the field of view in degrees (default: 90°)\n"
                      f"--rays: set the number of rays cast (default: 90)\n"
                      f"\tlower values can help performance on lower end systems\n")
                logging.info("stopped")
                return

            elif argument in ("-l", "--level"):
                if isinstance(value, int):
                    logging.error(f"level number not an integer")
                    print("level number must be an integer")
                    continue
                lv = LEVEL_PATHS[int(value)]
                lv_sel = True

            elif argument in ("-f", "--file") and not lv_sel:
                lv = value

            # TODO implement missing arguments
            elif argument in ("--fov", "--rays"):
                logging.info(f"not implemented argument: {argument, value}")
                print("not implemented yet")

            else:
                logging.info(f"unknown argument: {argument, value}")
                print(f"unknown argument: {argument, value}")

    except getopt.error as err:
        logging.fatal(str(err))
        print(str(err))
        return

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Hundefels2D")

    logging.debug("initialized screen")

    lv = w.Level(screen)
    pl = p.Player(screen, lv, pos=lv.start_position)

    screen.fill((80, 80, 80))
    pg.display.flip()

    logging.info("setup complete")
    logging.info("starting main loop")

    perf_warn = False

    while 1:
        t = time.time() + 1/60

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

        lv.draw()
        pl.move()
        pl.draw()

        pg.display.flip()

        if time.time() >= t and not perf_warn:
            perf_warn = True
            print("performance low, game may not work as intended")
            logging.warning("performance low, game may not work as intended")

        while time.time() < t:
            continue


if __name__ == '__main__':
    main()
