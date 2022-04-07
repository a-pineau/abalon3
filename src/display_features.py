import pygame

from pygame import gfxdraw
from pygame.locals import *
from constants import *

pygame.init()

def draw_circled_line(start, end, screen, colour, width) -> None:
    """Draw a line with two circles to enhance the visual effect.

    Parameters
    ----------
    screen: pygame.display (required)
        Game window
    colour: tuple of integers (required)
        Colour's RGB code
    width: float (required)
        Line's width
    """
    x1, y1 = start
    x2, y2 = end
    pygame.draw.line(screen, colour, start, end, width)
    gfxdraw.aacircle(screen, x1, y1, width + 1, colour)
    gfxdraw.filled_circle(screen, x1, y1, width + 1, colour)
    gfxdraw.aacircle(screen, x2, y2, width + 1, colour)
    gfxdraw.filled_circle(screen, x2, y2, width + 1, colour)