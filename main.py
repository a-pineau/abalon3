"""Implements the game loop and handles the user's events."""

import sys
import os

from os.path import join, dirname, abspath
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import math
import pygame
from game import Game
from display_features import *
from popup_win_game import PopUpWindow
from constants import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
n_snap = 0

# Game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode([SIZE_X, SIZE_Y])
    pygame.display.set_caption("aBOT_Lone")
    game = Game()
    running = True
    moving = False
    valid_move = False
    single = False
    multiple = False

    while running:
        # Events handling
        for event in pygame.event.get():
            p_keys = pygame.key.get_pressed()
            p_mouse = pygame.mouse.get_pressed()
            # Quiting game
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                 # Quiting (w/ escape)/Resetting game
                if event.key == K_ESCAPE:
                    running = False
                # Confirm move
                elif event.key == K_SPACE:
                    moving = False
                    single = False
                    game.update_game(valid_move)
            # Selecting a single marble
            elif event.type == MOUSEBUTTONDOWN and not p_keys[K_LSHIFT]:
                single = True
                origin_x, origin_y = game.normalize_coordinates(event.pos)
                move_data = game.check_pick_validity(origin_x, origin_y)
                if not move_data["valid"]:
                    continue
                else:
                    moving = True
                    valid_move = False
                    origin = move_data["origin_marble"]
                    origin_center = move_data["origin_center"]
                    origin_value = move_data["origin_value"]
                    print("ORIGIN CENTER", origin_center)
            # Updating board
            elif event.type == MOUSEBUTTONUP:
                moving = False
                single = False
                game.clear_buffers()
            # Moving single marble
            elif event.type == MOUSEMOTION and moving:
                origin.move_ip(event.rel)
                target_x, target_y = game.normalize_coordinates(event.pos)
                if game.exception_digger(target_x, target_y, game.rect_marbles, KeyError):
                    continue
                target_center = game.rect_marbles[(target_x, target_y)].center
                d = game.compute_distance_marbles(origin_center,  target_center)
                if d <= MAX_DISTANCE_MARBLE and target_center != origin_center:
                    valid_move = game.move_single_marble(
                        origin_x, origin_y, origin_center, 
                        target_x, target_y, target_center
                    )
            # Moving multiple marbles
            elif p_keys[K_LSHIFT]:
                if p_mouse[0]:
                    valid_move = game.move_multiple_marbles(pygame.mouse.get_pos())
                
        # Overall display
        game.display_marbles(screen)
        # :)))))))))))))
        for coords, new_color in game.colors_2_change.items():
            marble = game.rect_marbles[coords]
            screen.blit(new_color, marble)
        if moving: 
            origin_marble = game.rect_marbles[(origin_x, origin_y)]
            screen.blit(MARBLE_FREE, origin_marble)
            screen.blit(MARBLE_IMGS[origin_value], origin)
        # Drawing a line to indicate which push move is being done
        if valid_move and game.marbles_2_change:
            display_message(screen, CONFIRM_MOVE, 30, (SIZE_X / 2, FIRST_TOP_LEFT_Y / 2), WHITE)
            if single:
                end_x, end_y = list(game.marbles_2_change.keys())[-1]
                end_marble = game.rect_marbles[(end_x, end_y)]
                for coords, value in game.marbles_2_change.items():
                    if value > 1: 
                        marble = game.rect_marbles[coords]
                        screen.blit(MARBLE_IMGS[value], marble)
                draw_circled_line(origin_center, end_marble.center, screen, GREEN3, 3)
            elif multiple:
                for coords, new_color in game.colors_2_change.items():
                    marble = game.rect_marbles[coords]
                    screen.blit(new_color, marble)
        # Updating screen
        pygame.display.update()
    pygame.quit()
    

if __name__ == "__main__":
    main()