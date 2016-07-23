#########################################
# Programmers: Kenneth Sinder
# Date: May 22, 2015
# File Name: paddle.py
# Description: Paddle Class 
#########################################

from colours import *
import pygame
pygame.init()

class Paddle(object):

    top_speed = 5

    def __init__(self, x, y, width=20, height=110, colour=WHITE):
        """ (int, int, [int], [int], [(int, int, int)]) -> Paddle
        Returns a Paddle object with the given TOP-LEFT
        co-ordinates and optional width and height.
        """
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        """ () -> str
        Returns a string with the properties of the Paddle.
        """
        return "x: {0}, y: {1}, w: {2}, h: {3}".format(self.x, self.y,
                                                       self.width, self.height)

    def move_up(self):
        """ () -> None
        Shift the paddle upwards.
        """
        self.y -= self.top_speed

    def move_down(self):
        """ () -> None
        Shift the paddle downwards.
        """
        self.y += self.top_speed

    def update(self):
        """ () -> None
        Updates the Paddle.
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """ (pygame.Surface) -> None
        Draws the Paddle as a rectangle on the given Surface.
        """
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width,
                                                self.height))
