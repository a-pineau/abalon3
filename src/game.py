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
                pygame.draw.rect(screen, RED2, pygame.Rect(x, y, 72, 72), 1) # Debug
            
    def normalize_coordinates(self, position) -> tuple:
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        
        x, y = position
        r = (y - FIRST_TOP_LEFT_Y) // MARBLE_SIZE
        c = (x - (FIRST_TOP_LEFT_X - 0.5 * (len(self.data[r]) - 5) * MARBLE_SIZE)) // MARBLE_SIZE
        return r, int(c)
    
    def move_single_marble(self, origin_x, origin_y, origin_center, 
                           target_x, target_y, target_center) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        print("LOL")
        self.marbles_2_change.clear()
        self.marbles_2_change[(origin_x, origin_y)] = 1
        enemy = self.enemy()
        # To keep track of the colors we meet
        colors_seen = [self.current_color]
        valid_move = False
        sumito = False        
        end_move = False
        
        while not end_move:
            # Checking if we are killing a marble (out of bounds)
            try:
                self.rect_marbles[(target_x, target_y)].center
            except KeyError:
                self.marbles_2_change[(origin_x, origin_y)] = self.current_color
                valid_move = True
                break
            else:
                target_center = self.rect_marbles[(target_x, target_y)].center
                target_value = self.data[target_x][target_y]
                
            if target_value in (enemy, self.current_color):
                colors_seen.append(target_value)
            own_marble = target_value == self.current_color
            other_marble = target_value in (enemy, 1)
            too_much_marbles = colors_seen.count(self.current_color) > 3
            sumito = enemy in colors_seen
            wrong_sumito = (colors_seen.count(enemy) >= colors_seen.count(self.current_color)
                            or enemy in colors_seen and target_value == self.current_color)
            
            # Impossible move
            if too_much_marbles or wrong_sumito:
                valid_move = False
                break
            # If we keep finding our own marbles
            if own_marble and (target_x, target_y) not in self.marbles_2_change.keys():
                self.marbles_2_change[(target_x, target_y)] = self.current_color
            # Meeting an enemy or a free spot
            elif other_marble:
                if sumito:
                    print(colors_seen)
                    print("target center", target_center)
                    self.marbles_2_change[(origin_x, origin_y)] = self.current_color
                    self.marbles_2_change[(target_x, target_y)] = enemy
                else:
                    self.marbles_2_change[(target_x, target_y)] = self.current_color
                # Loop ends if its a free spot unless a single marble is trying to push
                if target_value == 1:
                    valid_move = True
                    end_move = True
            # Getting the next spot
            next_spot = self.compute_next_spot(origin_center, target_center)
            # print("origin_center=", origin_center)
            # print("target_center=", target_center)
            # print("next_spot=", next_spot)
            origin_center = target_center
            origin_x, origin_y = self.normalize_coordinates(origin_center)
            target_x, target_y = self.normalize_coordinates(next_spot)
            
        return valid_move
    
    def update_game(self, valid_move):
        """Save a snapshot of the current grid to the SNAP_FOLDER.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        if valid_move:
            for pos, value in self.marbles_2_change.items():
                x, y = pos
                self.data[x][y] = value
        self.marbles_2_change.clear()

    @staticmethod
    def compute_next_spot(origin, target):
        """Compute the next spot of given marble coordinates.

        Parameters
        ----------
        origin: tuple of integers (required)
            Initial marble
        target: tuple of integers (required)
            Targetted marble
        Returns
        -------
        spot_x, spot_y: tuple of integers
            Coordinates of the next spot
        """
        
        spot_x = 2 * target[0] - origin[0]
        spot_y = 2 * target[1] - origin[1]
        return spot_x, spot_y
    
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
    print("tg")
    main()




