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
        self.current_color = 2 # Change to random choice
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
            for i_col in range(len(row)):
                x = FIRST_X - MARBLE_SIZE * (0.5*(len(row) - 5) - i_col) 
                y = FIRST_Y + MARBLE_SIZE * i_row
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
        # Displaying the board
        for i_row, row in enumerate(self.data):
            for i_col, value in enumerate(row):
                x, y = next(iter_rect_coordinates)
                screen.blit(MARBLE_IMGS[value], (x, y))
                self.rect_marbles[(i_row, i_col)] = MARBLE_IMGS[value].get_rect(topleft = (x, y))
        # Displaying the current dead marble (if any)
        for buffer_marble, buffer_color in self.buffer_dead_marble.items():
            screen.blit(buffer_color, buffer_marble)
            skull_x = buffer_marble[0] + MARBLE_SIZE/5
            skull_y = buffer_marble[1] + MARBLE_SIZE/5
            screen.blit(SKULL, (skull_x, skull_y))
        # Displaying the deadzone
        # TODO

    # Not used (so far)
    def get_marble_coordinates(self, index) -> tuple:
        r, c = index
        len_r = len(self.data[r])
        m_x = FIRST_X - MARBLE_SIZE * (0.5*(len_r-5) - c)
        m_y = FIRST_Y + MARBLE_SIZE * r
        return int(m_x), m_y

    def get_center(self, index, topleft=None):
        """
        TODO
        """
        if not topleft:
            m_x, m_y = self.get_marble_coordinates(index)
        else:
            m_x, m_y = topleft
        c_x = int(m_x + MARBLE_SIZE*0.5)
        c_y = int(m_y + MARBLE_SIZE*0.5)
        return c_x, c_y

    def get_value(self, index):
        """TODO"""
        r, c = index
        return self.data[r][c]

    def normalize_coordinates(self, position):
        """TODO

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        x, y = position
        # Getting row index
        r = (y-FIRST_Y) // MARBLE_SIZE 
        if 0 <= r < len(self.data): # len(self.data) = 9: Abalone board game has 9 rows
            len_row = len(self.data[r])
            c = (x - (FIRST_X - 0.5*(len_row-5) * MARBLE_SIZE)) // MARBLE_SIZE
            if 0 <= int(c) in range(0, len_row):
                return r, int(c)
        return False
    
    def move_single_marble(self, origin, target) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        self.clear_buffers()
        self.marbles_2_change[origin] = 1 # If the move is valid, the picked marble will become free
        origin_center = self.rect_marbles[origin].center
        target_center = self.rect_marbles[target].center
        target_value = self.get_value(target)
        buffer_target = target
        friend = self.current_color
        enemy = self.enemy()
        colors = [friend] # To keep track of the colors we meet
        sumito = False        
        end_move = False
        
        while not end_move:        
            # Checking if we're killing a marble (this cannot occur during the first iteration)
            if not target:
                print("Pushing one marble out!")
                dead = (next_spot[0]-MARBLE_SIZE//2, next_spot[1]-MARBLE_SIZE//2)
                if self.buffer_dead_marble: 
                    self.buffer_dead_marble.clear()
                last_marble = colors[-1]
                self.buffer_dead_marble[dead] = MARBLE_IMGS[-last_marble]
                return True
            else:
                target_center = self.rect_marbles[target].center
                target_value = self.get_value(target)
                    
            if target_value in (enemy, friend):
                colors.append(target_value)
            own_marble = target_value == friend
            other_marble = target_value in (enemy, 1)
            # A potential sumito occurs when the enemy color is met
            sumito = enemy in colors
            # Cannot push more than 3 marbles
            too_much_marbles = colors.count(friend) > 3
            # Checking for a potential invalid sumito
            too_much_enemy = colors.count(enemy) >= colors.count(friend)
            squeezed_enemy = enemy in colors and target_value == friend
            invalid_sumito = too_much_enemy or squeezed_enemy
            if too_much_marbles or invalid_sumito:
                self.colors_2_change[buffer_target] = MARBLE_RED # Invalid move
                return False
            # If we keep finding our own marbles
            if own_marble and target not in self.marbles_2_change.keys():
                self.marbles_2_change[target] = friend
            # Meeting an enemy or a free spot
            elif other_marble:
                if sumito:
                    if self.get_value(origin) == friend:
                        self.marbles_2_change[target] = friend
                    else:
                        self.marbles_2_change[target] = enemy
                else:
                    self.marbles_2_change[target] = friend
                # Loop ends if a free spot is reached
                if target_value == 1:
                    end_move = True
            # Getting the next spot
            nx = (target_center[0]-origin_center[0]) / MARBLE_SIZE
            ny = (target_center[1]-origin_center[1]) / MARBLE_SIZE
            next_spot = self.compute_next_spot(target_center, nx, ny)
            # Updating origin/target positions
            origin_center = target_center
            origin = self.normalize_coordinates(origin_center)
            target = self.normalize_coordinates(next_spot)
        return True
    
    def select_range(self, pick):
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        # No need to check as a possibility (valid or not) has been found already
        if MARBLE_GREEN in self.colors_2_change.values():
            return list()
        elif MARBLE_RED in self.colors_2_change.values():
            return list() 
        value = self.get_value(pick)
        if value == self.current_color:
            # Selected marble will become a free spot (if possible)
            self.marbles_2_change[pick] = 1 
        centers = [self.get_center(c) for c in self.marbles_2_change.keys()]
        # Checking range validity
        if self.check_range(centers):
            self.colors_2_change[pick] = MARBLE_PURPLE 
        else:
            self.marbles_2_change.pop(pick)
        return centers

    def new_range(self, pick, centers):
        """
        TODO
        """
        print(centers)
        target = self.rect_marbles[pick].center
        origin = centers[-1][0], centers[-1][1]
        nx = (target[0] - origin[0]) / MARBLE_SIZE
        ny = (target[1] - origin[1]) / MARBLE_SIZE
        new_coords = [self.compute_next_spot(c, nx, ny) for c in centers]
        new_coords = [self.normalize_coordinates(c) for c in new_coords]
        if any(self.get_value(c) != 1 for c in new_coords):
            if MARBLE_RED not in self.colors_2_change.values():
                self.colors_2_change[new_coords[-1]] = MARBLE_RED
                self.marbles_2_change.clear()
                return False
        for coords in new_coords:
            self.colors_2_change[coords] = MARBLE_GREEN # Move OK
            self.marbles_2_change[coords] = self.current_color
        return True

    def check_range(self, centers) -> bool:
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        if len(centers) == 3:
            p1, p2, p3 = centers[0], centers[1], centers[2]
            d_first_to_second = self.compute_distance(p1, p2)
            d_second_to_third = self.compute_distance(p2, p3)
            if d_second_to_third != d_first_to_second:
                return False # A misaligned marble results in an invalid range
        elif len(centers) > 3:
            return False # A range of more than 3 marbles is invalid
        return True 
    
    def update(self, valid_move):
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
        
    def reset_board(self, configuration=STANDARD):
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
    def compute_next_spot(origin, nx, ny):
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
        spot_x = origin[0] + MARBLE_SIZE * nx
        spot_y = origin[1] + MARBLE_SIZE * ny
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
    pass

if __name__ == "__main__":
    main()




