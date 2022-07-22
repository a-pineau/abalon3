"""Sets the constant variables.

In descending order:
- Window size and font property
- Colours used
- Images (please note that all images used are free to use, links provided below)
- Initial configurations
"""

import os
import pygame
from math import sqrt
from pygame.locals import *

pygame.init()
useless_screen = pygame.display.set_mode()

FONT = pygame.font.SysFont("Calibri", 42)

# Directories
FILE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(FILE_DIR, "../images")
SNAP_FOLDER = "snapshots"

# Colours
BACKGROUND = (30, 30, 30)
DEAD_ZONE = (141, 141, 141)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
BLUE = (0, 0, 255)
BLUE2 = (158, 190, 228, 255)
RED = (255, 0, 0)
RED2 = (207, 46, 46)
YELLOW = (255, 255, 0)
YELLOW2 = (249, 217, 84, 255)
GREEN = (0, 255, 0)
GREEN2 = (39, 151, 0)
GREEN3 = (102, 203, 112)
ARROW_COLOR = (255, 0, 247)

# Images
# https://www.iconshock.com/flat-icons/3d-graphics-icons/sphere-icon/
MARBLE_RED = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_red.png")
    ).convert_alpha()
MARBLE_GREEN = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_green.png")
    ).convert_alpha()
MARBLE_PURPLE = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_purple.png")
    ).convert_alpha()
MARBLE_BLUE = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_blue.png")
    ).convert_alpha()
DEAD_BLUE = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_blue.png")
    ).convert_alpha()
DEAD_BLUE.set_alpha(128)
MARBLE_YELLOW = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_yellow.png")
    ).convert_alpha()
DEAD_YELLOW = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_yellow.png")
    ).convert_alpha()
DEAD_YELLOW.set_alpha(128)
MARBLE_FREE = pygame.image.load(
    os.path.join(IMAGES_DIR, "marble_empty.png")
    ).convert_alpha()
# https://icons8.com/icon/54885/skull
SKULL = pygame.image.load(
    os.path.join(IMAGES_DIR, "skull.png")
).convert_alpha()
SKULL = pygame.transform.rotozoom(SKULL, 0, 0.7)  # Adjusting size

MARBLE_SIZE = MARBLE_RED.get_rect().size[0] # All marbles have the same size
MAX_DISTANCE_MARBLE = MARBLE_SIZE*sqrt(1.25) # Max distance between two neighbouring marbles (diagonal)

# Merging with the skull
DEAD_BLUE = DEAD_BLUE.copy()
DEAD_BLUE.blit(SKULL, (8, 8))
DEAD_YELLOW = DEAD_YELLOW.copy()
DEAD_YELLOW.blit(SKULL, (8, 8))

# Window size
WIDTH = 900
FIRST_X = WIDTH*0.6 - MARBLE_SIZE*2.5 
FIRST_Y = 65 # Defines window's height
HEIGHT = FIRST_Y*2 + MARBLE_SIZE*9

# Keys are arbitrary chosen
MARBLE_IMGS = {
    -2: DEAD_BLUE,
    -3: DEAD_YELLOW,
    1: MARBLE_FREE, 
    2: MARBLE_BLUE, 
    3: MARBLE_YELLOW,
    4: MARBLE_GREEN,
    5: MARBLE_RED,
}

# Texts
# Current Player Blue
CURRENT_PLAYERB_TXT = "Playing: Blue"
CURRENT_PLAYERB_FONT_SIZE = 35
CURRENT_PLAYERB_COLOR = BLUE2
CURRENT_PLAYERB_POSITION = WIDTH*0.01, FIRST_Y*0.15
CURRENT_PLAYERB = [
    CURRENT_PLAYERB_TXT,
    CURRENT_PLAYERB_FONT_SIZE,
    CURRENT_PLAYERB_COLOR,
    CURRENT_PLAYERB_POSITION 
]
# Current Player Yellow
CURRENT_PLAYERY_TXT = "Playing: Yellow"
CURRENT_PLAYERY_FONT_SIZE = CURRENT_PLAYERB_FONT_SIZE
CURRENT_PLAYERY_COLOR = YELLOW2
CURRENT_PLAYERY_POSITION = WIDTH*0.01, FIRST_Y*0.15
CURRENT_PLAYERY = [
    CURRENT_PLAYERY_TXT,
    CURRENT_PLAYERY_FONT_SIZE,
    CURRENT_PLAYERY_COLOR,
    CURRENT_PLAYERY_POSITION 
]
# Confirm move
CONFIRM_MOVE_TXT = "Spacebar to move"
CONFIRM_MOVE_FONT_SIZE = 35
CONFIRM_MOVE_COLOR = GREEN2
CONFIRM_MOVE_POSITION = WIDTH*0.01, FIRST_Y*0.7
CONFIRM_MOVE = [
    CONFIRM_MOVE_TXT,
    CONFIRM_MOVE_FONT_SIZE,
    CONFIRM_MOVE_COLOR,
    CONFIRM_MOVE_POSITION
]
# Wrong move
WRONG_MOVE_TXT = "Invalid move"
WRONG_MOVE_FONT_SIZE = 35
WRONG_MOVE_COLOR = RED2
WRONG_MOVE_POSITION = CONFIRM_MOVE_POSITION
WRONG_MOVE = [
    WRONG_MOVE_TXT,
    WRONG_MOVE_FONT_SIZE,
    WRONG_MOVE_COLOR,
    WRONG_MOVE_POSITION
]
# Reset Game
RESET_GAME_TXT = "Reset Game [r]"
RESET_GAME_FONT_SIZE = 30
RESET_GAME_COLOR = GREY
RESET_GAME_POSITION = WIDTH*0.01, FIRST_Y*9.25
RESET_GAME = [
    RESET_GAME_TXT,
    RESET_GAME_FONT_SIZE,
    RESET_GAME_COLOR,
    RESET_GAME_POSITION 
]
# Quit Game
QUIT_GAME_TXT = "Quit Game [q]"
QUIT_GAME_FONT_SIZE = 30
QUIT_GAME_COLOR = GREY
QUIT_GAME_POSITION = WIDTH*0.01, FIRST_Y*9.75
QUIT_GAME = [
    QUIT_GAME_TXT,
    QUIT_GAME_FONT_SIZE,
    QUIT_GAME_COLOR,
    QUIT_GAME_POSITION 
]

# Deadzones
# Position
FIRST_DZ_X = 70
FIRST_BDZ_Y = FIRST_Y + MARBLE_SIZE
FIRST_YDZ_Y = FIRST_Y + MARBLE_SIZE*5
# Blue
BLUE_DEADZONE = {
    (FIRST_DZ_X, FIRST_BDZ_Y): 1,
    (FIRST_DZ_X + MARBLE_SIZE, FIRST_BDZ_Y): 1,
    (FIRST_DZ_X + MARBLE_SIZE*2, FIRST_BDZ_Y): 1,
    (FIRST_DZ_X + MARBLE_SIZE*0.5, FIRST_BDZ_Y + MARBLE_SIZE): 1,
    (FIRST_DZ_X + MARBLE_SIZE*1.5, FIRST_BDZ_Y + MARBLE_SIZE): 1,
    (FIRST_DZ_X + MARBLE_SIZE, FIRST_BDZ_Y + MARBLE_SIZE*2): 1,
}
# Yellow
YELLOW_DEADZONE = {
    (FIRST_DZ_X + MARBLE_SIZE, FIRST_YDZ_Y): 1,
    (FIRST_DZ_X + MARBLE_SIZE*0.5, FIRST_YDZ_Y + MARBLE_SIZE): 1,
    (FIRST_DZ_X + MARBLE_SIZE*1.5, FIRST_YDZ_Y + MARBLE_SIZE): 1,
    (FIRST_DZ_X, FIRST_YDZ_Y + MARBLE_SIZE*2): 1,
    (FIRST_DZ_X + MARBLE_SIZE, FIRST_YDZ_Y + MARBLE_SIZE*2): 1,
    (FIRST_DZ_X + MARBLE_SIZE*2, FIRST_YDZ_Y + MARBLE_SIZE*2): 1,
}

# Initial Configurations
STANDARD = [
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 3, 3, 3, 1, 1],
    [3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3],
]
GERMAN_DAISY = (
    [1, 1, 1, 1, 1],
    [2, 2, 1, 1, 3, 3],
    [2, 2, 2, 1, 3, 3, 3],
    [1, 2, 2, 1, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 1, 2, 2, 1],
    [3, 3, 3, 1, 2, 2, 2],
    [3, 3, 1, 1, 2, 2],
    [1, 1, 1, 1, 1],
)
BELGIAN_DAISY = (
    [2, 2, 1, 3, 3],
    [2, 2, 2, 3, 3, 3],
    [1, 2, 2, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 2, 2, 1],
    [3, 3, 3, 2, 2, 2],
    [3, 3, 1, 2, 2],
)
DUTCH_DAISY = (
    [2, 2, 1, 3, 3],
    [2, 3, 2, 3, 2, 3],
    [1, 2, 2, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 2, 2, 1],
    [3, 2, 3, 2, 3, 2],
    [3, 3, 1, 2, 2],
)
SWISS_DAISY = (
    [1, 1, 1, 1, 1],
    [2, 2, 1, 1, 3, 3],
    [2, 3, 2, 1, 3, 2, 3],
    [1, 2, 2, 1, 1, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 1, 1, 2, 2, 1],
    [3, 2, 3, 1, 2, 3, 2],
    [3, 3, 1, 1, 2, 2],
    [1, 1, 1, 1, 1],
)
DOMINATION = (
    [1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 3],
    [2, 2, 1, 1, 1, 3, 3],
    [2, 2, 2, 2, 1, 3, 3, 3],
    [1, 1, 1, 3, 1, 3, 1, 1, 1],
    [3, 3, 3, 1, 2, 2, 2, 2],
    [3, 3, 1, 1, 1, 2, 2],
    [3, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1],
)
PYRAMID = (
    [2, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 1],
    [2, 2, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 1, 3, 3, 3, 3],
    [1, 1, 1, 1, 3, 3, 3, 3],
    [1, 1, 1, 1, 3, 3, 3],
    [1, 1, 1, 1, 3, 3],
    [1, 1, 1, 1, 3],
)
THE_WALL = (
    [1, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 3, 1, 1],
)

