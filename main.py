"""Implements the game loop and handles the user's events."""

import sys
import os

from os.path import join, dirname, abspath
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import math
import pygame
from board import Board 
from game import Game
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
    change_color = False
    valid_move = False
    
    while running:
        # Events handling
        for event in pygame.event.get():
            p_keys = pygame.key.get_pressed()
            p_mouse = pygame.mouse.get_pressed()
            # Quiting game
            if event.type == QUIT:
                running = False
            # Quiting (w/ escape)/Resetting game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            # Selecting a single marble
            elif event.type == MOUSEBUTTONDOWN and not p_keys[K_LSHIFT]:
                origin_x, origin_y = game.normalize_coordinates(event.pos)
                if origin_x >= 0 and origin_y >= 0:
                    try:
                        origin_value = game.data[origin_x][origin_y]
                    except IndexError:
                        print("Out of bounds!")
                        continue
                    else:
                        if origin_value > 1: # Cannot move free marbles
                            moving = True
                            origin_color = MARBLE_IMGS[origin_value]
                            origin = game.rect_marbles[(origin_x, origin_y)]
                            origin_center = origin.center # To keep track of the initial position
            # Updating board
            elif event.type == MOUSEBUTTONUP:
                moving = False
                change_color = False
                game.update_game()
            # Moving single marble
            elif event.type == MOUSEMOTION and moving:
                change_color = False
                origin.move_ip(event.rel)
                game.data[origin_x][origin_y] = 1
                target_x, target_y = game.normalize_coordinates(event.pos)
                target_center = game.rect_marbles[(target_x, target_y)].center
                change_color =  True
                d = game.compute_distance_marbles(origin_center, target_center)
                if d <= MAX_DISTANCE_MARBLE:
                    new_color = game.move_single_marble(
                        origin_x, origin_y, origin_center, 
                        target_x, target_y, target_center
                    )
                else:
                    new_color = 5
            # Selecting multiple marbles
            elif p_keys[K_LSHIFT]:
                if not game.buffer_marbles_pos:
                    game.set_buffers()
                if p_mouse[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    for rect in game.marbles_rect:
                        if game.is_inside_marble(mouse_pos, rect.center):
                            game.select_marbles_range(rect)
                            game.compute_new_marbles_range(rect)

        game.display_marbles(screen)
        if change_color:
            target_marble = game.rect_marbles[(target_x, target_y)]
            screen.blit(MARBLE_IMGS[new_color], target_marble)
        if moving: 
            screen.blit(origin_color, origin)
        pygame.display.update()
    pygame.quit()
    

if __name__ == "__main__":
    main()