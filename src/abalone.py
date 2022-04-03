import math
import random
import pygame
from pygame import gfxdraw
from pygame.locals import *
from constants import *
from copy import deepcopy

pygame.init()


class Abalone(pygame.sprite.Sprite):
    """
    A class used to represent a standard Abalone board.
    Both players have 14 marbles.
    A player loses whenever 6 of his marbles are out.
    
    Attributes
    ----------
    configuration: string (optional, default="STANDARD")
        Initial board configuration.
    marbles_rect: list
        Rectangles representing all marbles positions.
    marbles_pos: dict
        Marbles positions and its associated current value.
    buffer_marble: pygame.Surface
        Initial position of a marble being moved.
    buffer_marbles_pos: dict
        Buffer of marbles_pos used to freeze the board's state.
    marbles_2_change: dict
        Marbles to change when updating the board (if possible).
    buffer_line: string
        A visual green line used to emphazise push move.
    current_color: pygame.Surface
        Current marble's color that is being played (MARBLE_BLUE or MARBLE_YELLOW).
    buffer_message: string
        Message used to inform the player of an incorrect move.

    Methods
    -------
    build_marbles(self) -> None
        Place the marbles to their initial position.
    display_marbles(self, screen) -> None:
        Display the marbles, i.e. the board and both (blue and yellow) dead-zones.
    is_valid_neighbor(self, target_pos, h_range=False) -> bool:
        Check if a given marble is a valid neighbor.
    recolor_marbles(self, target, reset_list, reset_color, new_color=None) -> None:
        Recolor multiples marbles to have one colored marble (green or red)
    set_buffers(self, marble=None) -> None:
        Set buffers to keep track of the board's state at a given time.
    apply_buffers(self) -> None:
        Apply the buffers to get back to the previous game's state.
    clear_buffers(self) -> None:
        Clear the all the buffers at once.
    push_marbles(self, target) -> None:
        Performs a push move.
    select_single_marble(self, mouse_pos, current_marble) -> None:
        Select a single marble to be moved towards a valid spot.
    check_range_type(self) -> bool:
        Check if a range selection is valid.
    select_marbles_range(self, target) -> None:
        Select a range of connected marbles along a common axis.
    compute_new_marbles_range(self, target) -> None:
        Computes the new positions of a range of connected marbles.
    update_board(self) -> None:
        Update the state of the game.
    display_current_color(self, screen) -> None:
        Display the current color being played.
    display_error_message(self, screen) -> None:
        Display a red message whenever an invalid move is being played.
    draw_circled_line(self, screen, colour, width) -> None:
        Draw a line with two circles to enhance the visual effect.
    reset_game(self) -> None:
        Reset the game by pressing p (pygame constant K_p).

    Static Methods
    --------------
    predict_direction(origin, target) -> tuple:
        Predict the direction when computing new spot coordinates.
    compute_next_spot(origin, move_coefficients, lateral_move) -> tuple:
        Compute the next spot of given marble coordinates.
    enemy(current_color) -> pygame.Surface:
        Returns the enemy of the current color being played.
    is_inside_marble(marble_center, mouse_pos) -> bool:
        Check if the mouse cursor position is inside a marble.
    display_time_elapsed(screen) -> None:
        Display the time elapsed since the game was launched.
    """
    
    # Constructor
    # -----------
    def __init__(self, board=STANDARD):
        """Constructor.

        Calls the parent constructor and initializes all the attributes.
        It also builds to marbles to their initial positions with respect to
        the chosen configuration.

        Parameter
        ---------
        configuration: list (optional, default=STANDARD)
            Initial positions of the marbles on the board.
            the STANDARD configuration is the one commonly used in
            mainstream abalone games.
        """
        
        super().__init__()
        self.board = board

    # -------
    # def build_marbles(self) -> None:
    #     """Places the marbles to their initial position."""
    #     y_init = 30
    #     gap_y = MARBLE_SIZE
    #     for row in self.configuration:
    #         x_init = SIZE_X - 400 - len(row) * MARBLE_SIZE
    #         gap_x = MARBLE_SIZE
    #         for element in row:
    #             x = x_init + gap_x
    #             y = y_init + gap_y
    #             self.marbles_pos[(x, y)] = MARBLE_IMGS[element]
    #             self.marbles_rect.append(
    #                 MARBLE_IMGS[element].get_rect(topleft = (x, y)))
    #             gap_x += 2 * MARBLE_SIZE
    #         gap_y += 2 * MARBLE_SIZE

    def display_marbles(self, screen) -> None:
        """Display the marbles, i.e. the board and both (blue and yellow) dead-zones.

        Parameter
        ---------
        screen: pygame.Surface (required)
        """

        screen.fill(BACKGROUND)
        skull_rect = SKULL.get_rect()

        for m_pos, m_color in self.marbles_pos.items():
            screen.blit(m_color, m_pos)
        for k_dz, v_dz in self.buffer_dead_zone.items():
            screen.blit(v_dz, k_dz)
            skull_rect.center = (k_dz[0] + SHIFT_X, k_dz[1] + SHIFT_Y)
            screen.blit(SKULL, skull_rect)
        for k_blue, v_blue in self.dead_zone_blue.items():
            screen.blit(v_blue, k_blue)
            if v_blue != MARBLE_FREE:
                skull_rect.center = (k_blue[0] + SHIFT_X, k_blue[1] + SHIFT_Y)
                screen.blit(SKULL, skull_rect)
        for k_yellow, v_yellow in self.dead_zone_yellow.items():
            screen.blit(v_yellow, k_yellow)
            if v_yellow != MARBLE_FREE:
                skull_rect.center = (k_yellow[0] + SHIFT_X, k_yellow[1] + SHIFT_Y)
                screen.blit(SKULL, skull_rect)

   

def main():
    game = Abalone()

if __name__ == "__main__":
    main()




