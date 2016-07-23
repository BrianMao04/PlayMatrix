#############################
# Programmer: Kenneth Sinder
# Date: April 27, 2015
# Filename: windowsettings.py
# Description: Window Settings class
#############################

import pygame
from pygame.locals import *

class WindowSettings(object):
    """ ([int], [int]) -> WindowSettings
    Stores window settings, which can be
    supplied or loaded from file.
    """

    def __init__(self, width=None, height=None):
        """ () -> WindowSettings
        Returns a WindowSettings object.
        Has 0 width and 0 height by default if not
        provided.
        """
        if width is None:
            self.w = 0
        else:
            self.w = width
        if height is None:
            self.h = 0
        else:
            self.h = height
        self.flags = 0

    def __str__(self):
        """ () -> str
        Returns the width and height.
        """
        return "Width: {0}, Height: {1}".format(self.w, self.h)

    def getWidth(self):
        """ () -> int
        Returns the saved width as an integer.
        """
        return self.w

    def getHeight(self):
        """ () -> (int, int)
        Returns the saved height as an integer.
        """
        return self.h

    def getDimensions(self):
        """ () -> (int, int)
        Returns the width and height as a 2-tuple of integers.
        """
        return self.getWidth(), self.getHeight()

    def setDimensions(self, width=None, height=None):
        """ ([int], [int]) -> None
        Sets the width and height to the given values.
        """
        if not width is None:
            self.w = width
        if not height is None:
            self.h = height

    def getFlags(self):
        """ () -> int
        Returns the display flags to be called with set_mode()
        """
        return self.flags

    def addFlags(self, *flags):
        """ (int*) -> None
        Adds one or more flags to the list of flags.
        """
        for flag in flags:
            self.flags |= flag

    def loadFromFile(self, filename):
        """ (str) -> None
        Load width, height, and flags from file.
        Width is first line, height is second line,
        flags as strings on subsequent lines.
        e.g. Within pong_window_settings.txt:
        640
        480
        FULLSCREEN
        DOUBLEBUFFERED
        Before loading window:
        window_settings.loadFromFile('pong_window_settings.txt')
        """
        # Read from file and gather info
        flags = []
        inputFile = open(filename, 'r')
        width = int(inputFile.readline())
        height = int(inputFile.readline())
        for line in inputFile:
            # Establish a dictionary of setting phrases -> pygame settings flag
            possibleSettings = {'fullscreen': pygame.FULLSCREEN,
                                'doublebuf': pygame.DOUBLEBUF,
                                'hwsurface': pygame.HWSURFACE,
                                'opengl': pygame.OPENGL,
                                'resizable': pygame.RESIZABLE,
                                'noframe': pygame.NOFRAME,
                                'hwaccel': pygame.HWACCEL}
            # For each of the settings, if they are found in the line, append it
            for setting in possibleSettings:
                if self.stringHas(line, setting):
                    flags.append(possibleSettings[setting])
        # Close the file
        inputFile.close()
        # Apply collected info
        self.w = width
        self.h = height
        self.addFlags(*flags)
                
    @staticmethod
    def stringHas(string, substring):
        """ (str, str) -> bool
        Returns True if the substring can be found inside
        the first string, regardless of lowercase/uppercase.
        """
        return substring.lower() in string.lower()
        
    
