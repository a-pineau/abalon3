import math
import random
import pygame

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
        self.data = deepcopy(configuration)
        self.current_color = 3 # Change to random choice
        self.rect_marbles = {}
        self.rect_coordinates = []
        self.colors_2_change = {}
        self.marbles_2_change = {}
        self.buffer_dead_marble = {}
        self.dead_marbles = {}
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
                x = FIRST_TOP_LEFT_X - MARBLE_SIZE * (0.5*(len(self.data[i_row])-5) - i_col)
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

        for buffer_marble, buffer_color in self.buffer_dead_marble.items():
            screen.blit(buffer_color, buffer_marble)
            screen.blit(SKULL, (buffer_marble[0] + MARBLE_SIZE / 5, buffer_marble[1] + MARBLE_SIZE / 5))

    def normalize_coordinates(self, position):
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        x, y = position
        # Getting row index
        r = (y-FIRST_TOP_LEFT_Y) // MARBLE_SIZE 
        if 0 <= r < 9: # Abalone board game has 9 rows
            len_row = len(self.data[r])
            c = (x - (FIRST_TOP_LEFT_X - 0.5*(len(self.data[r])-5) * MARBLE_SIZE)) // MARBLE_SIZE
            if 0 <= int(c) in range(0, len_row):
                return r, int(c)
        return False
    
    def move_single_marble(self, origin_x, origin_y, origin_center, 
                           target_x, target_y, target_center) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        self.clear_buffers()
        self.marbles_2_change[(origin_x, origin_y)] = 1 # If the move is valid, the picked marble will become free
        target_value = self.data[target_x][target_y]
        buffer_target_x, buffer_target_y = target_x, target_y
        enemy = self.enemy()
        colors_seen = [self.current_color] # To keep track of the colors we meet
        sumito = False        
        end_move = False
        
        while not end_move:                
            if target_value in (enemy, self.current_color):
                colors_seen.append(target_value)
            own_marble = target_value == self.current_color
            other_marble = target_value in (enemy, 1)
            # A potential sumito occurs when the enemy color is met
            sumito = enemy in colors_seen
            # Cannot push more than 3 marbles
            too_much_marbles = colors_seen.count(self.current_color) > 3
            # The sumito is invalid if there are more enemies than the current color...
            # ... or if the current color is met after the enemy
            invalid_sumito = (colors_seen.count(enemy) >= colors_seen.count(self.current_color)
                            or enemy in colors_seen and target_value == self.current_color)
            if too_much_marbles or invalid_sumito:
                self.colors_2_change[(buffer_target_x, buffer_target_y)] = MARBLE_RED # Invalid move
                return False
            # If we keep finding our own marbles
            if own_marble and (target_x, target_y) not in self.marbles_2_change.keys():
                self.marbles_2_change[(target_x, target_y)] = self.current_color
            # Meeting an enemy or a free spot
            elif other_marble:
                if sumito:
                    if self.data[origin_x][origin_y] == self.current_color:
                        self.marbles_2_change[(target_x, target_y)] = self.current_color
                    else:
                        self.marbles_2_change[(target_x, target_y)] = enemy
                else:
                    self.marbles_2_change[(target_x, target_y)] = self.current_color
                # Loop ends if a free spot is reached
                if target_value == 1:
                    end_move = True
            # Getting the next spot
            nx = (target_center[0] - origin_center[0]) / MARBLE_SIZE
            ny = (target_center[1] - origin_center[1]) / MARBLE_SIZE
            next_spot = self.compute_next_spot(target_center, nx, ny)
            # Updating origin/target positions
            origin_center = target_center
            origin_x, origin_y = self.normalize_coordinates(origin_center)
            # Checking if a marble is being pushed out
            try:
                target_x, target_y = self.normalize_coordinates(next_spot)
            except TypeError: # If the next spot cannot be normalized, then we're killing a marble
                print("Pushing one marble out!")
                dead_x = next_spot[0] - MARBLE_SIZE//2
                dead_y = next_spot[1] - MARBLE_SIZE//2
                if self.buffer_dead_marble: self.buffer_dead_marble.clear()
                self.buffer_dead_marble[(dead_x, dead_y)] = DEAD_YELLOW
                return True
            else:
                target_center = self.rect_marbles[(target_x, target_y)].center
                target_value = self.data[target_x][target_y]
        return True
    
    def move_multiple_marbles(self, mouse_position):
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        # No need to check as a possibility (valid or not) has been found already
        if MARBLE_GREEN in self.colors_2_change.values():
            return True
        elif MARBLE_RED in self.colors_2_change.values():
            return False 
        
        pick = self.normalize_coordinates(mouse_position)
        # Incorrect selection
        if not pick:
            return False
        pick_x, pick_y = pick
        value = self.data[pick_x][pick_y]
        if value == self.current_color:
            self.marbles_2_change[(pick_x, pick_y)] = 1
        coordinates = [self.rect_marbles[(x, y)].center 
                       for x, y in self.marbles_2_change.keys()
                       if self.marbles_2_change[(x, y)] == 1]
        # Checking first self marbles range validity
        if value == self.current_color:
            if self.check_range_validity(coordinates):
                self.colors_2_change[(pick_x, pick_y)] = MARBLE_PURPLE 
            else:
                self.marbles_2_change.pop((pick_x, pick_y))
                return False
        
        # Computing the new marbles positions
        range_length = len(coordinates)
        if value != self.current_color and coordinates and range_length in (2, 3):
            target_x, target_y = self.rect_marbles[(pick_x, pick_y)].center
            origin_x, origin_y = coordinates[-1][0], coordinates[-1][1]
            nx = (target_x - origin_x) / MARBLE_SIZE
            ny = (target_y - origin_y) / MARBLE_SIZE
            new_coords = [self.compute_next_spot(c, nx, ny) for c in coordinates]
            new_coords = [self.normalize_coordinates((x, y)) for x, y in new_coords]
            # Checking if the new range is valid (out of bounds marble or occupied spot in range)
            if (any(self.exception_digger(x, y, self.data, IndexError) for x, y in new_coords) 
                or any(self.data[x][y] != 1 for x, y in new_coords)):
                if MARBLE_RED not in self.colors_2_change.values():
                    self.colors_2_change[new_coords[-1]] = MARBLE_RED
                    self.marbles_2_change.clear()
                    return False
            for coords in new_coords:
                self.colors_2_change[coords] = MARBLE_GREEN # Move OK
                self.marbles_2_change[coords] = self.current_color
            return True
        return False

    def check_range_validity(self, coordinates) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        if len(coordinates) == 3:
            d_first_2_second = self.compute_distance_marbles(coordinates[0], coordinates[1])
            d_second_2_last = self.compute_distance_marbles(coordinates[-1], coordinates[-2])
            if d_second_2_last != d_first_2_second:
                return False # A misaligned marble results in a invalid range
        elif len(coordinates) > 3:
            return False # A range of more than 3 marbles is invalid
        return True 
    
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
        self.clear_buffers()
        
    def reset_game(self, configuration=STANDARD):
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game 
        """
        self.data = deepcopy(configuration)
        self.clear_buffers()
        self.dead_marbles.clear()

    def clear_buffers(self):
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        
        self.marbles_2_change.clear()
        self.colors_2_change.clear()
        self.buffer_dead_marble.clear()
        
    @staticmethod
    def exception_digger(pick, data, exception_type) -> bool:
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        x, y = pick
        if (x, y) != (None, None):
            try:
                data[x][y] if exception_type == IndexError else data[(x, y)]
            except exception_type:
                return True
            else:
                return False
        return True

    @staticmethod
    def compute_next_spot(origin, vector_x, vector_y):
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
        spot_x = origin[0] + MARBLE_SIZE * vector_x
        spot_y = origin[1] + MARBLE_SIZE * vector_y
        return int(spot_x), int(spot_y)
    
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
    def compute_distance(p1, p2):
        """Compute the distance between two points (p1, p2)."""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def main():
    game = Game()

if __name__ == "__main__":
    main()




