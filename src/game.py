"""Implements the game loop and handles the user's events."""

import sys
import os

from os.path import (join, dirname, abspath)
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 0)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import pygame as pg
import constants as const
import display as dsp
from abalone import Abalone
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
n_snap = 0

# Game loop
def main():
    pg.init()
    screen = pg.display.set_mode([const.WIDTH, const.HEIGHT])
    pg.display.set_caption("Abalon3")
    board = Abalone()
    running = True
    moving = False
    game_over = False
    valid_move = False
    path = False

    while running:
        # Events handling
        for event in pg.event.get():
            mouse = pg.mouse.get_pos()
            p_keys = pg.key.get_pressed()
            p_mouse = pg.mouse.get_pressed()
            # Quiting game
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                # Quiting game with escape or q
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                # Confirming move
                elif event.key == pg.K_SPACE:
                    moving = False
                    board.update(valid_move)
                    game_over = board.check_win()
                # Resetting game
                elif event.key == pg.K_r:
                    board.reset()
                    game_over = False
            # Selecting a single marble
            if not game_over:
                if event.type == pg.MOUSEBUTTONDOWN and not p_keys[pg.K_LSHIFT]:
                    path = True
                    pick = board.normalize_coordinates(pg.mouse.get_pos())
                    # Checking pick validity (i.e. out of board or free marble picked is invalid)
                    if not pick:
                        continue
                    # Move is valid, getting marble's data
                    moving = True
                    pick_value = board.get_value(pick)
                    pick_marble = board.rect_marbles[pick]
                    pick_center = pick_marble.center
                    # Can only pick the color being played
                    if pick_value != board.current_color:
                        moving = False
                # Releasing selection
                elif event.type == pg.MOUSEBUTTONUP:
                    moving = False
                    path = False
                    board.clear_buffers()
                # Moving single marble
                elif event.type == pg.MOUSEMOTION and moving:
                    pick_marble.move_ip(event.rel)
                    target = board.normalize_coordinates(mouse)
                    if not target:
                        continue # User's target is invalid (out of bounds)
                    # Valid target otherwise
                    target_center = board.rect_marbles[target].center
                    d = board.distance(pick_center, target_center)
                    # the target must be in the pick's neighborhood and cannot be the pick itself
                    if d <= const.MAX_DISTANCE_MARBLE and target != pick:
                        valid_move = board.move_single_marble(pick, target)
                # Moving multiple marbles
                elif p_keys[pg.K_LSHIFT] and p_mouse[0]:
                    pick = board.normalize_coordinates(mouse)
                    if not pick:
                        continue
                    centers = board.select_range(pick)
                    value = board.get_value(pick)
                    if centers:
                        valid_move = board.new_range(pick, value, centers)
        # Overall display
        dsp.overall_display(screen, board, valid_move, path)
        # Displaying the moving selected marble
        if moving: 
            origin_marble = board.rect_marbles[pick]
            screen.blit(const.MARBLE_FREE, origin_marble)
            screen.blit(const.MARBLE_IMGS[pick_value], pick_marble)
        # Updating screen
        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()