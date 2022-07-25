import sys
import os

from os.path import (join, dirname, abspath)
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import pygame as pg
import constants as const
import display as dsp
from board import Board

SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "snapshots")
n_snap = 0

# Game loop
def main():
    """Implements the game loop and handles the user's events"""
    pg.init()
    screen = pg.display.set_mode([const.WIDTH, const.HEIGHT])
    pg.display.set_caption("Abalon3")
    board = Board()
    record = False
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
                # Quiting game with or q
                if event.key == event.key == pg.K_q:
                    running = False
                # Confirming move and possible update
                elif event.key == pg.K_SPACE:
                    moving = False
                    if valid_move:
                        board.update()
                    game_over = board.check_win()
                    board.clear_buffers()
                # Resetting game
                elif event.key == pg.K_r:
                    board.reset()
                    game_over = False
                    path = False
            # Selecting a single marble
            if not game_over:
                if event.type == pg.MOUSEBUTTONDOWN and not p_keys[pg.K_LSHIFT]:
                    path = True
                    pick = board.normalize_coordinates(pg.mouse.get_pos())
                    # Checking pick validity 
                    # Cant be out of bounds or must be current color
                    if not pick or pick and board.get_value(pick) != board.current_color:
                        continue
                    # Move is valid, getting marble's data
                    moving = True
                    pick_value = board.get_value(pick)
                    pick_center = board.get_center(pick)
                    pick_marble = const.MARBLE_IMGS[pick_value].get_rect()
                    pick_marble.center = pick_center
                # Releasing selection
                elif event.type == pg.MOUSEBUTTONUP:
                    moving = False
                    path = False
                    board.clear_buffers()
                # Moving single marble
                elif event.type == pg.MOUSEMOTION and moving:
                    valid_move = False
                    pick_marble.move_ip(event.rel)
                    target = board.normalize_coordinates(mouse)
                    if not target:
                        continue # User's target is invalid (out of bounds)
                    # Valid target otherwise
                    target_center = board.get_center(target)
                    d = board.distance(pick_center, target_center)
                    # the target must be in the pick's neighborhood and cannot be the pick itself
                    if d <= const.MAX_DISTANCE_MARBLE and target != pick:
                        valid_move = board.push_marble(pick, target)
                # Moving multiple marbles
                elif p_keys[pg.K_LSHIFT] and p_mouse[0]:
                    pick = board.normalize_coordinates(mouse)
                    if not pick:
                        continue
                    value = board.get_value(pick)
                    centers = board.select_range(pick, value)
                    if centers:
                        valid_move = board.new_range(pick, centers)
        # Overall display
        dsp.overall_display(screen, board, game_over, valid_move, path)
        # Displaying the moving selected marble
        if moving: 
            origin_center = board.get_center(pick)
            rect_free = const.MARBLE_FREE.get_rect()
            rect_free.center = origin_center
            screen.blit(const.MARBLE_FREE, rect_free)
            screen.blit(const.MARBLE_IMGS[pick_value], pick_marble)
        # Updating screen
        pg.display.update()
    pg.quit()

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
    pg.image.save(screen, os.path.join(SNAP_FOLDER, file_name))


if __name__ == "__main__":
    main()