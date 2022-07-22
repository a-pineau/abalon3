"""
Implements functions used to display informations/states related to an Abalone board.
"""

import pygame as pg
from pygame import gfxdraw
from constants import *

pygame.init()

def overall_display(screen, board, valid_move, path) -> None:
    """
    TODO
    """
    display_marbles(screen, board)
    display_new_colors(screen, board)
    display_dead_marble(screen, board) 
    display_infos_move(screen, valid_move, path, board)
    display_deadzones(screen, board) 
    display_player(screen, board)
    message(screen, *RESET_GAME)
    message(screen, *QUIT_GAME)

def display_marbles(screen, board) -> None:
    """
    TODO
    """
    screen.fill(BACKGROUND)
    iter_rect_coordinates = iter(board.rect_coordinates)
    # Displays the board
    for i_row, row in enumerate(board.data):
        for i_col, value in enumerate(row):
            x, y = next(iter_rect_coordinates)
            screen.blit(MARBLE_IMGS[value], (x, y))
            # Also updates the rect marbles
            r = MARBLE_IMGS[value].get_rect(topleft = (x, y))
            board.rect_marbles[(i_row, i_col)] = r

def display_new_colors(screen, board) -> None:
    """
    TODO
    """
    for coords, new_color in board.new_colors.items():
        marble = board.rect_marbles[coords]
        screen.blit(new_color, marble)

def display_dead_marble(screen, board) -> None:
    """
    TODO
    """
    if board.buffer_dead_marble:
        pos = next(iter(board.buffer_dead_marble.keys()))
        value = next(iter(board.buffer_dead_marble.values()))
        marble = MARBLE_IMGS[value]
        marble_rect = marble.get_rect()
        marble_rect.center = pos
        screen.blit(marble, marble_rect)

def display_deadzones(screen, board) -> None:
    """
    TODO
    """
    deadzones = zip(board.blue_deadzone.items(), board.yellow_deadzone.items())
    for (b_pos, b_val), (y_pos, y_val) in deadzones:
        b_marble = MARBLE_IMGS[b_val]
        y_marble = MARBLE_IMGS[y_val]
        screen.blit(b_marble, b_pos)
        screen.blit(y_marble, y_pos)

def display_infos_move(screen, valid_move, path, board) -> None:
    """
    TODO
    """
    if valid_move and board.new_marbles:
        message(screen, *CONFIRM_MOVE)
        if path:
            first_entry = list(board.new_marbles.keys())[0]
            if board.buffer_dead_marble:
                last_entry = list(board.buffer_dead_marble.keys())[0]
                last_center = last_entry[0], last_entry[1]
            else:
                last_entry = list(board.new_marbles.keys())[-1]
                last_center = board.rect_marbles[last_entry].center
            first_center = board.rect_marbles[first_entry].center
            draw_path(first_center, last_center, screen, GREEN3, 3)
    if not valid_move and board.new_colors:
        message(screen, *WRONG_MOVE)

def display_player(screen, board) -> None:
    """
    TODO
    """
    if board.current_color == 2:
        message(screen, *CURRENT_PLAYERB)
    else:
        message(screen, *CURRENT_PLAYERY)

def message(screen, msg, font_size, color, position) -> None:
    """
    TODO
    """ 
    font = pg.font.SysFont("Calibri", font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(topleft=(position))
    screen.blit(text, text_rect)

def draw_path(start, end, screen, color, width) -> None:
    """Draw a line with two circles to enhance the visual effect.

    Parameters
    ----------
    screen: pygame.display (required)
        Game window
    colour: tuple of integers (required)
        Colour's RGB code
    width: float (required)
        Line's width
    """
    x1, y1 = start
    x2, y2 = end
    pygame.draw.line(screen, color, start, end, width)
    gfxdraw.aacircle(screen, x1, y1, width + 1, color)
    gfxdraw.filled_circle(screen, x1, y1, width + 1, color)
    gfxdraw.aacircle(screen, x2, y2, width + 1, color)
    gfxdraw.filled_circle(screen, x2, y2, width + 1, color)
    