"""
Implements functions used to display informations/states related to an Abalone board.
These functions could all be staticmethod in board.py although they're in a separate file
for better readability.
"""

import pygame as pg
import constants as const
from pygame import gfxdraw

pg.init()

def overall_display(screen, board, game_over, valid_move) -> None:
    """
    Overall board's display.

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
    """
    screen.fill(const.BACKGROUND)
    message(screen, *const.RESET_GAME)
    message(screen, *const.QUIT_GAME)
    display_marbles(screen, board)
    display_new_colors(screen, board)
    display_dead_marble(screen, board) 
    display_deadzones(screen, board) 
    display_infos_move(screen, board, valid_move)
    if not game_over:
        display_player(screen, board)
    if game_over:
        display_winner(screen, game_over)

def message(screen, msg, font_size, color, position) -> None:
    """
    Displays a message on screen.

    Parameters
    ----------
    msg: string (required)
        Actual text to be displayed
    font_size: int (required)
        Font size
    color: tuple of int (required)
        Text RGB color code
    position: tuple of int (required)
        Position on screen
    """ 
    font = pg.font.SysFont("Calibri", font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(topleft=(position))
    screen.blit(text, text_rect)

def display_marbles(screen, board) -> None:
    """
    Displays marbles (Abalone's board only).

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
            rect = const.MARBLE_IMGS[value].get_rect()
            rect.center = center
            screen.blit(const.MARBLE_IMGS[value], rect)

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
    for loc, color in board.new_colors.items():
        center = board.get_center(loc)
        rect = color.get_rect()
        rect.center = center
        screen.blit(color, rect)

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
        marble = const.MARBLE_IMGS[value]
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
        b_marble = const.MARBLE_IMGS[b_val]
        y_marble = const.MARBLE_IMGS[y_val]
        screen.blit(b_marble, b_pos)
        screen.blit(y_marble, y_pos)

def display_infos_move(screen, board, valid_move) -> None:
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
    """
    if valid_move and board.new_marbles:
        message(screen, *const.CONFIRM_MOVE)
    if const.MARBLE_RED in board.new_colors.values():
        message(screen, *const.WRONG_MOVE)

def display_moving_marble(screen, board, pick, moving_marble):
    origin_center = board.get_center(pick)
    rect_free = const.MARBLE_FREE.get_rect()
    rect_free.center = origin_center
    screen.blit(const.MARBLE_FREE, rect_free)
    screen.blit(const.MARBLE_IMGS[board.get_value(pick)], moving_marble)

def display_player(screen, board) -> None:
    """
    Displays current player.

    Parameters
    ----------
    screen: pygame.Surface (required)
        Game window
    board: Board (required)
        Abalone board
    """
    if board.current_color == 2:
        message(screen, *const.CURRENT_PLAYERB)
    else:
        message(screen, *const.CURRENT_PLAYERY)

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
        message(screen, *const.BLUE_WINS)
    if game_over == 3:
        message(screen, *const.YELLOW_WINS)

def draw_path(start, end, screen, color, width) -> None:
    """
    Draws a line with two circles to enhance the visual effect.

    Parameters
    ----------
    screen: pygame.display (required)
        Game window
    color: tuple of int (required)
        Line color RGB code
    width: float (required)
        Line width
    """
    x1, y1 = start
    x2, y2 = end
    pg.draw.line(screen, color, start, end, width)
    gfxdraw.aacircle(screen, x1, y1, width + 1, color)
    gfxdraw.filled_circle(screen, x1, y1, width + 1, color)
    gfxdraw.aacircle(screen, x2, y2, width + 1, color)
    gfxdraw.filled_circle(screen, x2, y2, width + 1, color)
    