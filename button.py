############################
# Programmer: Brian Mao
# Date: May 2015
# Filename: button.py
# Description: Button class
############################
import pygame
from pygame.locals import *
from colours import *
pygame.font.init()


class Button(object):
    """ An on-screen Pygame-based button. """
    
    def __init__(self, text, x, y, w=100, h=40, middle=False, colouron=BLACK,
                 colouroff=BLUE, font='freesansbold.ttf'):
        """ (str, int, int, [int], [int], [bool], \
            [(int,int,int)], [(int,int,int)], [str]) -> Button
            
        Returns a Button with the given properties.
        """
        self.text = text                                        # caption
        if middle:                                              # center the button at the given co-ordinates
            x -= w // 2                                         # if the user requests this
            y -= h // 2
        self.rect = pygame.Rect(x, y, w, h)                     # Rect bounds
        self.colour_on = colouron                               # active colour
        self.colour_off = colouroff                             # inactive colour
        self.pressed = False                                    
        self.hovering = False                                   # mouse-over flag
        self.font_surf = None                                   # font Surface
        self.font_rect = None                                   # font Rect bounds
        self.font = pygame.font.Font(font, 32)
        self.enabled = True
        self.init_text()                                        # initialize text

    def init_text(self):
        # must be called before using the button to initialize the text Rect and Surface
        self.font_surf = self.font.render(self.text, True, self.colour_on)
        self.font_rect = self.font_surf.get_rect()
        self.font_rect.centerx = (self.rect.left + self.rect.right) / 2
        self.font_rect.centery = (self.rect.top + self.rect.bottom) / 2

    def correct_text_overflow(self, can_shift_left=False):
        """ ([bool]) -> None
        Resizes the button to fit the text inside of it if there
        is an overflow.
        """
        if not self.rect.contains(self.font_rect):
            x, y = self.rect.topleft
            self.rect = self.font_rect.copy()
            if not can_shift_left:
                self.rect.topleft = x, y
                self.font_rect.topleft = x, y
            else:
                self.rect.center = x, y
                self.font_rect.center = x, y

    def update(self, events):
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        # determine if the mouse cursor is hovering or clicking the button
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        self.pressed = False
        for event in events:
            if event.type == MOUSEBUTTONUP and self.hovering:
                self.pressed = True

    def draw(self, surface):
        try:
            if not self.enabled:
                return
        except AttributeError:
            pass
        # draw a button as a rectangle with text; also update the font Surface
        if self.hovering:
            pygame.draw.rect(surface, self.colour_on, self.rect, 2)
            self.font_surf = self.font.render(self.text, True, self.colour_on)
        else:
            pygame.draw.rect(surface, self.colour_off, self.rect, 2)
            self.font_surf = self.font.render(self.text, True, self.colour_off)
        # blit the text onto the game window
        surface.blit(self.font_surf, self.font_rect)
