import math
import random
import pygame as pg
import display as dsp

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
        self.blue_deadzone = deepcopy(BLUE_DEADZONE)
        self.yellow_deadzone = deepcopy(YELLOW_DEADZONE)
        self.current_color = random.choice((2, 3))
        self.scores = {"Blue": 0, "Yellow": 0}
        self.new_colors = {}
        self.new_marbles = {}
        self.buffer_dead_marble = {}

    def get_enemy(self) -> int:
        """Returns the enemy of the current color being played."""
        return 3 if self.current_color == 2 else 2

    def get_coordinates(self, index) -> tuple:
        """
        TODO
        """
        r, c = index
        len_r = len(self.data[r])
        m_x = FIRST_X - MARBLE_SIZE * (0.5*(len_r-5) - c)
        m_y = FIRST_Y + MARBLE_SIZE * r
        return int(m_x), m_y

    def get_center(self, index, topleft=None):
        """
        TODO
        """
        if topleft is not None:
            m_x, m_y = topleft
        else:
            m_x, m_y = self.get_coordinates(index)
        c_x = int(m_x + MARBLE_SIZE*0.5)
        c_y = int(m_y + MARBLE_SIZE*0.5)
        return c_x, c_y

    def get_value(self, index):
        """TODO"""
        r, c = index
        return self.data[r][c]

    def check_win(self):
        """
        TODO
        """
        if self.scores["Blue"] == 6:
            return 2
        if self.scores["Yellow"] == 6:
            return 3
        return False

    def normalize_coordinates(self, position):
        """
        TODO
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
        """
        TODO
        """
        self.clear_buffers()
        self.new_marbles[origin] = 1 # If the move is valid, the picked marble will become free
        origin_center = self.get_center(origin)
        target_center = self.get_center(target)
        target_value = self.get_value(target)
        buffer_target = target
        friend = self.current_color
        enemy = self.get_enemy()
        colors = [friend] # To keep track of the colors we meet
        sumito = False        

        while True:        
            # Checking if we're killing a marble (this cannot occur during the first iteration)
            if not target:
                # Position of the buffer dead marble
                dead = next_spot[0], next_spot[1]
                if self.buffer_dead_marble: 
                    self.buffer_dead_marble.clear()
                last_marble = colors[-1]
                self.buffer_dead_marble[dead] = -last_marble
                return True
            else:
                target_center = self.get_center(target)
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
                self.new_colors[buffer_target] = MARBLE_RED # Invalid move
                return False
            # If we keep finding our own marbles
            if own_marble and target not in self.new_marbles.keys():
                self.new_marbles[target] = friend
            # Meeting an enemy or a free spot
            elif other_marble:
                if sumito:
                    if self.get_value(origin) == friend:
                        self.new_marbles[target] = friend
                    else:
                        self.new_marbles[target] = enemy
                else:
                    self.new_marbles[target] = friend
                # Loop ends if a free spot is reached
                if target_value == 1:
                    return True
            # Getting the next spot
            nx = (target_center[0] - origin_center[0]) / MARBLE_SIZE
            ny = (target_center[1] - origin_center[1]) / MARBLE_SIZE
            next_spot = self.next_spot(target_center, nx, ny)
            # Updating origin/target positions
            origin_center = target_center
            origin = self.normalize_coordinates(origin_center)
            target = self.normalize_coordinates(next_spot)
    
    def select_range(self, pick):
        """
        TODO
        """
        # No need to check as a possibility (valid or not) has been found already
        if MARBLE_GREEN in self.new_colors.values():
            return None
        elif MARBLE_RED in self.new_colors.values():
            return None 
        value = self.get_value(pick)
        if value == self.current_color:
            # Selected marble will become a free spot (if possible)
            self.new_marbles[pick] = 1 
        centers = [self.get_center(c) for c in self.new_marbles.keys()]
        # Checking range validity
        if self.check_range(value, centers):
            self.new_colors[pick] = MARBLE_PURPLE 
        return centers

    def check_range(self, value, centers) -> bool:
        """
        TODO
        """
        if value != self.current_color:
            return False
        if len(centers) == 2:
            p0, p1 = centers[0], centers[1]
            d_p0_p1 = self.distance(p0, p1)
            # Only neighbouring marbles can form a range of 2
            if d_p0_p1 > MAX_DISTANCE_MARBLE:
                return False
        if len(centers) == 3:
            p0, p1, p2 = centers[0], centers[1], centers[2]
            d_p0_p1 = self.distance(p0, p1)
            d_p0_p2 = self.distance(p0, p2)
            # A misaligned range of 3 results in an invalid range
            if int(d_p0_p2) != int(d_p0_p1*2):
                return False
        # A range of more than 3 marbles is invalid 
        elif len(centers) > 3:
            return False 
        return True 

    def new_range(self, pick, value, centers):
        """
        TODO
        """
        if value != self.current_color and len(centers) in (2, 3):
            target = self.get_center(pick)
            origin = centers[-1][0], centers[-1][1]
            nx = (target[0] - origin[0]) / MARBLE_SIZE
            ny = (target[1] - origin[1]) / MARBLE_SIZE
            new_coords = [self.next_spot(c, nx, ny) for c in centers]
            new_coords = [self.normalize_coordinates(c) for c in new_coords]
            # If new_coords cannot be all normalized, an out of bounds has been reached
            if not all(new_coords):
                nonfree_spots = False
            else:
                # If one on the new spots isn't free
                nonfree_spots = any(self.get_value(c) != 1 for c in new_coords)
            # Or if the target isn't in the neigbourhood
            not_neighbour = self.distance(centers[-1], target) > MAX_DISTANCE_MARBLE
            if nonfree_spots or not_neighbour:
                if MARBLE_RED not in self.new_colors.values():
                    self.new_colors[new_coords[-1]] = MARBLE_RED
                    self.new_marbles.clear()
                    return False
            # Valid move otherwise
            for coords in new_coords:
                self.new_colors[coords] = MARBLE_GREEN 
                self.new_marbles[coords] = self.current_color
            return True
        return False
    
    def update(self, valid_move):
        """
        TODO
        """
        print(valid_move)
        if valid_move:
            # Updating board
            for pos, value in self.new_marbles.items():
                x, y = pos
                self.data[x][y] = value
            # Updating deadzone if killing one marble
            if self.buffer_dead_marble:
                value = next(iter(self.buffer_dead_marble.values()))
                # Getting the deadzone corresponding to the killed marble (blue or yellow)
                if value == -2:
                    self.scores["Yellow"] += 1
                    deadzone = self.blue_deadzone
                else:
                    self.scores["Blue"] += 1
                    deadzone = self.yellow_deadzone
                for pos in deadzone:
                    if deadzone[pos] == 1:
                        deadzone[pos] = value
                        break
            self.current_color = self.get_enemy()
        self.clear_buffers()
        
    def reset(self, configuration=STANDARD):
        """
        TODO
        """
        self.current_color = random.choice((2, 3))
        self.scores["Blue"] = 0
        self.scores["Yellow"] = 0
        self.data = deepcopy(configuration)
        self.blue_deadzone = deepcopy(BLUE_DEADZONE)
        self.yellow_deadzone = deepcopy(YELLOW_DEADZONE)
        self.clear_buffers()

    def clear_buffers(self):
        """TODO.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """
        
        self.new_marbles.clear()
        self.new_colors.clear()
        self.buffer_dead_marble.clear()
            
    ######### Static Methods #########
    @staticmethod
    def next_spot(origin, nx, ny):
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
    def distance(p1, p2):
        """Compute the distance between two points (p1, p2)."""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def main():
    pass

if __name__ == "__main__":
    main()




