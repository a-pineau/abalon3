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
    board = Board()
    game = Game(board)
    running = True
    moving = False
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
                norm_x, norm_y = game.normalize_coordinates(event.pos)
                if norm_x >= 0 and norm_y >= 0:
                    try:
                        buffer_value = board.data[norm_x][norm_y]
                    except IndexError:
                        print("Out of bounds!")
                        continue
                    else:
                        if buffer_value > 1: # Cannot move free marbles
                            moving = True
                            buffer_marble = MARBLE_IMGS[buffer_value]
                            buffer_rect = game.rect_marbles[(norm_x, norm_y)]
                            p1 = buffer_rect.center # Center of the selected marble
            # Updating board
            elif event.type == MOUSEBUTTONUP:
                moving = False
                if valid_move:
                    board.data[new_norm_x][new_norm_y] = 2
                else:
                    board.data[norm_x][norm_y] = 2
                    board.data[new_norm_x][new_norm_y] = 1
            # Moving single marble
            elif event.type == MOUSEMOTION and moving:
                buffer_rect.move_ip(event.rel)
                board.data[norm_x][norm_y] = 1
                new_norm_x, new_norm_y = game.normalize_coordinates(event.pos)
                if (new_norm_x, new_norm_y) != (norm_x, norm_y):
                    valid_move = game.check_move_validity(p1, new_norm_x, new_norm_y)
                
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
        if moving: 
            screen.blit(buffer_marble, buffer_rect)
        pygame.display.update()
    pygame.quit()
    

if __name__ == "__main__":
    main()