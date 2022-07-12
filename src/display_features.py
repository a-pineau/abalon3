import pygame

from pygame import gfxdraw
from pygame.locals import *
from constants import *

pygame.init()

def draw_circled_line(start, end, screen, line_color, line_width) -> None:
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
    pygame.draw.line(screen, line_color, start, end, line_width)
    gfxdraw.aacircle(screen, x1, y1, line_width + 1, line_color)
    gfxdraw.filled_circle(screen, x1, y1, line_width + 1, line_color)
    gfxdraw.aacircle(screen, x2, y2, line_width + 1, line_color)
    gfxdraw.filled_circle(screen, x2, y2, line_width + 1, line_color)
    
def display_message(screen, message, font_size, position, color):
    """TODO
    """
    my_font = pygame.font.SysFont("Sans", font_size)
    msg = my_font.render(message, True, color)
    msg_rect = msg.get_rect(center=(position[0], position[1]))
    screen.blit(msg, msg_rect)
    
def falling_marble(screen):
    pass