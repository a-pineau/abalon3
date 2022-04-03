"""Implements the game loop and handles the user's events."""

import sys
import os

from os.path import join, dirname, abspath
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import math
import pygame
from abalone import Abalone 
from popup_win_game import PopUpWindow
from constants import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
n_snap = 0
rect_marbles = {}
rect_coordinates = []

# Game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode([SIZE_X, SIZE_Y])
    pygame.display.set_caption("aBOT_Lone")
    game = Abalone()
    compute_rect_coordinates(game, rect_coordinates)
    running = True
    moving = False
    
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
                norm_x, norm_y = normalize_coordinates(event.pos, game)
                if norm_x >= 0 and norm_y >= 0:
                    try:
                        buffer_value = game.board[norm_x][norm_y]
                    except IndexError:
                        print("Out of bounds!")
                        continue
                    else:
                        if buffer_value > 1: # Cannot move free marbles
                            moving = True
                            buffer_marble = MARBLE_IMGS[buffer_value]
                            buffer_rect = rect_marbles[(norm_x, norm_y)]
                            p1 = buffer_rect.center # Center of the selected marble
            # Updating board
            elif event.type == MOUSEBUTTONUP:
                moving = False
            # Moving single marble
            elif event.type == MOUSEMOTION and moving:
                new_norm_x, new_norm_y = normalize_coordinates(event.pos, game)
                if (new_norm_x, new_norm_y) != (norm_x, norm_y):
                    p2 = rect_marbles[(new_norm_x, new_norm_y)].center
                    d = compute_distance_marbles(p1, p2)
                    if d <= MAX_DISTANCE_MARBLE:
                        if game.board[new_norm_x][new_norm_y] == 1:
                            game.board[new_norm_x][new_norm_y] = 4


                game.board[norm_x][norm_y] = 1
                buffer_rect.move_ip(event.rel)
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

        display_marbles(screen, game, rect_coordinates, rect_marbles)
        if moving: 
            screen.blit(buffer_marble, buffer_rect)
        pygame.display.update()
    pygame.quit()
    
def compute_rect_coordinates(game, rect_coordinates):   
    """TODO

    Parameter
    ---------
    screen: pygame.Surface (required)
        Game window
    """
    for i_row, row in enumerate(game.board):
        # Number of marbles in the current row
        local_row_length = len(game.board[i_row])
        for i_col in range(len(row)):
            # The value 5 corresponds to the number of marbles in the first row
            # The board's position is defined w/ respect to the top-left marble (first marble of top-row)
            x = FIRST_TOP_LEFT_X - MARBLE_SIZE * (0.5 * (local_row_length - 5) - i_col)
            y = FIRST_TOP_LEFT_Y + MARBLE_SIZE * i_row
            rect_coordinates.append((x, y))
            
def compute_distance_marbles(p1, p2):
    """TODO

    Parameter
    ---------
    screen: pygame.Surface (required)
        Game window
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def display_marbles(screen, game, rect_coordinates, rect_marbles) -> None:
    """TODO

    Parameter
    ---------
    screen: pygame.Surface (required)
        Game window
    """
    
    screen.fill(BACKGROUND)
    iter_rect_coordinates = iter(rect_coordinates)
    for i_row, row in enumerate(game.board):
        for i_col, value in enumerate(row):
            # The value 5 corresponds to the number of marbles in the first row
            # The board's position is defined w/ respect to the top-left marble (first marble of top-row)
            x, y = next(iter_rect_coordinates)
            screen.blit(MARBLE_IMGS[value], (x, y))
            rect_marbles[(i_row, i_col)] = MARBLE_IMGS[value].get_rect(topleft = (x, y))
            pygame.draw.rect(screen, (255, 0, 140), pygame.Rect(x, y, 72, 72), 1) # Debug
        
def normalize_coordinates(mouse_position, game):
    """TODO

    Parameter
    ---------
    screen: pygame.Surface (required)
        Game window
    """
    
    x, y = mouse_position
    r = (y - FIRST_TOP_LEFT_Y) // MARBLE_SIZE
    local_row_length = len(game.board[r])
    c = (x - (FIRST_TOP_LEFT_X - 0.5 * (local_row_length - 5) * MARBLE_SIZE)) // MARBLE_SIZE
    return r, int(c)


def record_game(screen) -> None:
    """Save a snapshot of the current grid to the SNAP_FOLDER.

    Parameter
    ---------
    screen: pygame.Surface (required)
        Game window
    """

    global n_snap
    n_snap += 1
    extension = "png"
    file_name = f"snapshot_{n_snap}.{extension}"
    pygame.image.save(screen, os.path.join(SNAP_FOLDER, file_name))


if __name__ == "__main__":
    main()