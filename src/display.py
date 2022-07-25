"""
Implements functions used to display informations/states related to an Abalone board.
"""

import pygame as pg
from pygame import gfxdraw
from constants import *

pg.init()

def overall_display(screen, board, game_over, valid_move, path) -> None:
    """
    Overall board's display
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    game_over: bool (required)
        True if the game has ended, False otherwise
    valid_move: bool (required)
        True if a valid move has been performed, False otherwise
    path: bool (required)
        True if a path is drawn to emphasize a push, False otherwise
    """
    screen.fill(BACKGROUND)
    message(screen, *RESET_GAME)
    message(screen, *QUIT_GAME)
    display_marbles(screen, board)
    display_new_colors(screen, board)
    display_dead_marble(screen, board) 
    display_infos_move(screen, board, valid_move, path)
    display_deadzones(screen, board) 
    display_player(screen, board, game_over)
    display_winner(screen, game_over)

def display_marbles(screen, board) -> None:
    """
    Displays marbles (Abalone's board only)
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    """
    for i_r, r in enumerate(board.data):
        for i_c, value in enumerate(r):
            center = board.get_center((i_r, i_c))
            rect = MARBLE_IMGS[value].get_rect()
            rect.center = center
            screen.blit(MARBLE_IMGS[value], rect)


def display_new_colors(screen, board) -> None:
    """
    Displays marbles with chaning colors.
    Red when the move is invalid, green when valid, and purple when selecting a range.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board

    """
    for index, new_color in board.new_colors.items():
        center = board.get_center(index)
        rect = new_color.get_rect()
        rect.center = center
        screen.blit(new_color, rect)

def display_dead_marble(screen, board) -> None:
    """
    Displays a marble that is potentially being killed.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
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
    Displays both blue and yellow deadzones.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    """
    deadzones = zip(board.blue_deadzone.items(), board.yellow_deadzone.items())
    for (b_pos, b_val), (y_pos, y_val) in deadzones:
        b_marble = MARBLE_IMGS[b_val]
        y_marble = MARBLE_IMGS[y_val]
        screen.blit(b_marble, b_pos)
        screen.blit(y_marble, y_pos)

def display_infos_move(screen, board, valid_move, path) -> None:
    """
    Displays validity of a move.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    valid_move: bool
        True if the current move is valid, False otherwise
    path: bool (required)
        True if a path is drawn to emphasize a push, False otherwise
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
                last_center = board.get_center(last_entry)
            first_center = board.get_center(first_entry)
            draw_path(first_center, last_center, screen, GREEN3, 3)
    if MARBLE_RED in board.new_colors.values():
        message(screen, *WRONG_MOVE)

def display_player(screen, board, game_over) -> None:
    """
    Displays current player.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    """
    if not game_over:
        if board.current_color == 2:
            message(screen, *CURRENT_PLAYERB)
        else:
            message(screen, *CURRENT_PLAYERY)

def display_winner(screen, game_over) -> None:
    """
    Displays winner.
    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    game_over: int
        Defines which player won
    """
    if game_over == 2:
        message(screen, *BLUE_WINS)
    if game_over == 3:
        message(screen, *YELLOW_WINS)

def message(screen, msg, font_size, color, position) -> None:
    """
    Displays a message on screen.
    Parameters
    ----------

    """ 
    font = pg.font.SysFont("Calibri", font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(topleft=(position))
    screen.blit(text, text_rect)

def draw_path(start, end, screen, color, width) -> None:
    """Draws a line with two circles to enhance the visual effect.

    Parameters
    ----------
    screen: pygame.display (required)
        Game window
    color: tuple of int (required)
        color's RGB code
    width: float (required)
        Line's width
    """
    x1, y1 = start
    x2, y2 = end
    pg.draw.line(screen, color, start, end, width)
    gfxdraw.aacircle(screen, x1, y1, width + 1, color)
    gfxdraw.filled_circle(screen, x1, y1, width + 1, color)
    gfxdraw.aacircle(screen, x2, y2, width + 1, color)
    gfxdraw.filled_circle(screen, x2, y2, width + 1, color)
    