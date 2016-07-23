#############################
# Programmer: Brian Mao
# Date: May 5, 2015
# Filename: PictureButton.py
# Description: Picture Button
#############################

import pygame
pygame.font.init()

from button import Button

class PictureButton(Button):
    def __init__(self, filepath, x, y, w=100, h=40, middle=False, colouron=(0,0,0), colouroff=(5,5,255),
                 font='OpenSans-Bold.ttf'):
        """ (str, int, int, [int], [int], [bool], [(int, int, int)], [(int, int, int)]) -> PictureButton
        Returns a PictureButton with the given x and y co-ordinate.
        The x and y refer to a middle coordinate if "middle" is True.
        The filepath is saved and the image is internally loaded.
        The width and height are ignored.
        """
        Button.__init__(self, "", x, y, w, h, middle, colouron, colouroff, font)
        self.filepath = filepath                                # caption
        self.x, self.y = x, y
        if middle:                                              # center the button at the given co-ordinates
            self.x -= w // 2                                         # if the user requests this
            self.y -= h // 2
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, w, h)                     # Rect bounds
        self.colour_on = colouron                               # active colour
        self.colour_off = colouroff                             # inactive colour
        self.pressed = False                                    
        self.hovering = False
        self.font = pygame.font.Font(font, 32)
        self.load_picture(filepath)
    
    def load_picture(self, filepath):
        """ (str) -> None
        Loads the picture with the given filepath as the "picture" property.
        """
        self.picture = pygame.image.load(filepath)
        self.picture = self.picture.convert_alpha()
        self.picture = pygame.transform.scale(self.picture,(self.width, self.height))

    def load_hover_text(self, text):
        """ (str) -> None
        Updates the button's hover text. By default, a PictureButton has no hover text,
        so only the picture is displayed, even when the mouse is hovering.
        """
        self.text = str(text)
        self.font_surf = self.font.render(self.text, True, self.colour_on)
        self.font_rect = self.font_surf.get_rect()
        self.font_rect.topleft = self.x, self.y + self.height
        
    def draw(self, surface):
        """ (Surface) -> None
        Draws the PictureButton.
        """
        rect = self.picture.get_rect()
        rect.topleft = self.x, self.y
        # draw a button as a rectangle with text; also update the font Surface
        if self.hovering:
            pygame.draw.rect(surface, self.colour_on, rect, 4)
            if self.text: 
                surface.blit(self.font_surf, self.font_rect)
        else:
            pygame.draw.rect(surface, self.colour_off, rect, 4)
        # blit the picture onto the game window
        surface.blit(self.picture, rect)
