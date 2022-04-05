import math
import random
import pygame

from board import Board
from pygame import gfxdraw
from pygame.locals import *
from constants import *
from copy import deepcopy

pygame.init()


class Game(pygame.sprite.Sprite):
    """
    A class used to represent a standard Abalone board.
    Both players have 14 marbles.
    A player loses whenever 6 of his marbles are out.
    
    Attributes
    ----------

    Methods
    -------


    Static Methods
    --------------

    """
    
    # Constructor
    # -----------
    def __init__(self, configuration=STANDARD):
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
        self.data = configuration
        self.rect_marbles = {}
        self.rect_coordinates = []
        self.marbles_2_change = {}
        self.current_color = 2 # Change to random choice
        self.compute_rect_coordinates()
        
    def compute_rect_coordinates(self):   
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        for i_row, row in enumerate(self.data):
            # Number of marbles in the current row
            for i_col in range(len(row)):
                # The value 5 corresponds to the number of marbles in the first row
                # The board's position is defined w/ respect to the top-left marble (first marble of top-row)
                x = FIRST_TOP_LEFT_X - MARBLE_SIZE * (0.5 * (len(self.data[i_row]) - 5) - i_col)
                y = FIRST_TOP_LEFT_Y + MARBLE_SIZE * i_row
                self.rect_coordinates.append((x, y))

    def display_marbles(self, screen) -> None:
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        
        screen.fill(BACKGROUND)
        iter_rect_coordinates = iter(self.rect_coordinates)
        for i_row, row in enumerate(self.data):
            for i_col, value in enumerate(row):
                x, y = next(iter_rect_coordinates)
                screen.blit(MARBLE_IMGS[value], (x, y))
                self.rect_marbles[(i_row, i_col)] = MARBLE_IMGS[value].get_rect(topleft = (x, y))
                pygame.draw.rect(screen, RED_2, pygame.Rect(x, y, 72, 72), 1) # Debug
            
    def normalize_coordinates(self, mouse_position) -> tuple:
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        
        x, y = mouse_position
        r = (y - FIRST_TOP_LEFT_Y) // MARBLE_SIZE
        c = (x - (FIRST_TOP_LEFT_X - 0.5 * (len(self.data[r]) - 5) * MARBLE_SIZE)) // MARBLE_SIZE
        return r, int(c)
    
    def move_single_marble(self, buffer_marble_center, target_x, target_y) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        target_marble = self.rect_marbles[(target_x, target_y)]
        target_value = self.data[target_x][target_y]
        d = self.compute_distance_marbles(buffer_marble_center, target_marble.center)
        end_move = False
        while not end_move:
            # Targetted marble is too far away or is an enemy -> impossible
            if d > MAX_DISTANCE_MARBLE or target_value == self.enemy:
                valid_move = False
                new_color = 5
                end_move = True
            # Targetted marble is in range and is free -> possible
            elif d <= MAX_DISTANCE_MARBLE and target_value == 1:
                valid_move = True
                new_color = 4
                end_move = True
            elif target_value == self.current_color:
                end_move = True                
                
        return valid_move, new_color

    
    def update_game(self, valid_move):
        """Save a snapshot of the current grid to the SNAP_FOLDER.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        pass
    
    def push_marbles(self):
        pass
    
    
    def enemy(self) -> int:
        """Returns the enemy of the current color being played."""
        return 3 if self.current_color == 2 else 2
    
    
    # Static Methods
    # --------------
    
    @staticmethod
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
        
        
    @staticmethod
    def compute_distance_marbles(p1, p2):
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def main():
    game = Game()

if __name__ == "__main__":
    main()




