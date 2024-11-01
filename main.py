import sys

import pygame as pg

from constants import FPS, SCREEN_SIZE
from game import Game
from helper_functions import load_levels


def main():
    """This is where the game loop is. Initialize the screen and other pygame stuff. Loads all the levels."""
    pg.init()
    pg.mouse.set_visible(False)
    clock = pg.time.Clock()
    pg.display.set_caption("Platformer gaming")
    window = pg.display.set_mode(SCREEN_SIZE, display=0, flags=pg.SCALED)
    data = load_levels("assets/levels/")
    levels = [Game(lvl_data, window) for lvl_data in data]

    lvl_idx = 0
    game = levels[lvl_idx]
    game.start_screen()
    while game.state != "quit":
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                game.state = "quit"
                break
            # I have no idea how else to do double jumps, sorry
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and game.player.jumping < 2:
                    game.player.jump()
        game.run()
        match game.state:
            case "dead":
                restart = game.end_screen(False)
                if restart:
                    game = Game(data[lvl_idx], window)
                    game.tutorial = False
                    continue
                game.state = "quit"
            case "next":
                lvl_idx += 1
                if lvl_idx >= len(levels):
                    restart = game.end_screen(True)
                    if restart:
                        lvl_idx = 0
                        game = Game(data[lvl_idx], window)
                        game.tutorial = False
                        continue

                    game.state = "quit"
                game = levels[lvl_idx]
                game.tutorial = False
            case _:
                continue
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
