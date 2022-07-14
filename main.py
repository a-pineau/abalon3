"""Implements the game loop and handles the user's events."""

import sys
import os

from os.path import join, dirname, abspath
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import math
import pygame as pg
import constants as const
from game import Game
from display_features import *
from popup_win_game import PopUpWindow
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
n_snap = 0

# Game loop
def main():
    pg.init()
    screen = pg.display.set_mode([const.WIDTH, const.HEIGHT])
    pg.display.set_caption("aBOT_Lone")
    game = Game()
    running = True
    moving = False
    valid_move = False
    single = False
    multiple = False

    while running:
        # Events handling
        for event in pg.event.get():
            p_keys = pg.key.get_pressed()
            p_mouse = pg.mouse.get_pressed()
            # Quiting game
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                 # Quiting (w/ escape)/Resetting game
                if event.key == pg.K_ESCAPE:
                    running = False
                # Confirming move
                elif event.key == pg.K_SPACE:
                    moving = False
                    single = False
                    game.update_game(valid_move)
                # Resetting game
                elif event.key == pg.K_r:
                    game.reset_game()
            # Selecting a single marble
            elif event.type == pg.MOUSEBUTTONDOWN and not p_keys[pg.K_LSHIFT]:
                single = True
                pick = game.normalize_coordinates(event.pos)
                # Checking pick validity (i.e. out of board or free marble picked is invalid)
                try:
                    game.rect_marbles[pick]
                except KeyError:
                    print("Pick out of bounds!")
                    continue
                else: # Move is valid, getting marble's data
                    moving = True
                    valid_move = False
                    pick_x, pick_y = pick
                    pick_value = game.data[pick_x][pick_y]
                    pick_marble = game.rect_marbles[(pick_x, pick_y)]
                    pick_center = pick_marble.center
                    if pick_value == 1: 
                        moving = False
            # Updating board
            elif event.type == pg.MOUSEBUTTONUP:
                moving = False
                single = False
                game.clear_buffers()
            # Moving single marble
            elif event.type == pg.MOUSEMOTION and moving:
                pick_marble.move_ip(event.rel)
                target = game.normalize_coordinates(event.pos)
                try:
                    target_x, target_y = target
                except TypeError:
                    print('Target out of bounds!')
                    continue # User's target is invalid (out of bounds)
                # Valid target otherwise
                target_x, target_y = target
                target_center = game.rect_marbles[(target_x, target_y)].center
                d = game.compute_distance(pick_center, target_center)
                # the target must be in the pick neighborhood and cannot be the pick itself
                if d <= const.MAX_DISTANCE_MARBLE and target_center != pick_center:
                    valid_move = game.move_single_marble(
                        pick_x, pick_y, pick_center, 
                        target_x, target_y, target_center
                    )
            # Moving multiple marbles
            elif p_keys[pg.K_LSHIFT]:
                if p_mouse[0]:
                    valid_move = game.move_multiple_marbles(pg.mouse.get_pos())
        # Overall display
        game.display_marbles(screen)
        # :)))))))))))))
        for coords, new_color in game.colors_2_change.items():
            marble = game.rect_marbles[coords]
            screen.blit(new_color, marble)
        if moving: 
            origin_marble = game.rect_marbles[(pick_x, pick_y)]
            screen.blit(const.MARBLE_FREE, origin_marble)
            screen.blit(const.MARBLE_IMGS[pick_value], pick_marble)
        # Drawing a line to indicate which push move is being done
        if valid_move and game.marbles_2_change:
            display_message(
                screen, 
                const.CONFIRM_MOVE, 30, 
                (const.WIDTH*0.5, const.FIRST_TOP_LEFT_Y*0.5), 
                const.GREEN3
            )
            if single:
                end_x, end_y = list(game.marbles_2_change.keys())[-1]
                end_marble = game.rect_marbles[(end_x, end_y)]
                for coords, value in game.marbles_2_change.items():
                    if value > 1: 
                        marble = game.rect_marbles[coords]
                        screen.blit(const.MARBLE_IMGS[value], marble)
                draw_circled_line(pick_center, end_marble.center, screen, const.GREEN3, 3)
            elif multiple:
                for coords, new_color in game.colors_2_change.items():
                    marble = game.rect_marbles[coords]
                    screen.blit(new_color, marble)
        elif not valid_move and game.colors_2_change:
            display_message(
                screen, 
                const.WRONG_MOVE, 
                30, 
                (const.WIDTH*0.5, const.FIRST_TOP_LEFT_Y*0.5), 
                const.RED2
            )
        # Updating screen
        pg.display.update()
    pg.quit()
    

if __name__ == "__main__":
    main()