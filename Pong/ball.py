                                                               #########################################
# Programmers: Kenneth Sinder
# Date: May 21, 2015
# File Name: ball.py
# Description: Ball Class 
#########################################

from colours import *
import pygame, random
pygame.init()

class Ball(object):

    top_speed = 8
    
    def __init__(self, x, y, radius=50, colour=WHITE):
        """ (int, int, [int], [(int, int, int)]) -> Ball
        Returns a Ball object.
        """
        self.x = x
        self.y = y
        self.shift_x = 0
        self.shift_y = 0
        self.radius = radius
        self.colour = colour
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2*self.radius,2*self.radius)

    def __str__(self):
        """ () -> str
        Returns a string containing the properties of the Ball.
        """
        return "x: {0}, y: {1}, r: {2}".format(self.x, self.y, self.radius)

    def launch(self, x=None, y=None, shift_x=None, shift_y=None):
        """ ([int], [int, [int], [int])
        Launch the ball by giving it the desired x speed and y speed.
        Send in a random direction if a speed is not given.
        If an x and y position is not provided, the position is unchanged.
        """
        if shift_x is None:
            shift_x = random.choice((-self.top_speed, self.top_speed))
        if shift_y is None:
            shift_y = random.choice((-self.top_speed, self.top_speed))
        self.shift_x = shift_x
        self.shift_y = shift_y
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def update(self):
        """ () -> None
        Updates the ball position.
        """
        self.x += self.shift_x
        self.y += self.shift_y
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2*self.radius,2*self.radius)

    def draw(self, surface):
        """ (pygame.Surface) -> None
        Draws the Ball as a pygame circle onto the given Surface.
        """
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius)
                           
