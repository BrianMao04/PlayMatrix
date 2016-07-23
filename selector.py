############################
# Programmer: Kenneth Sinder
# Date: May 24, 2015
# Filename: selector.py
# Description: Selector class
############################

from button import *
pygame.font.init()

class SelectorUI(object):
    """ Pygame-based option selector. """

    def __init__(self, options, x, y, colouron=BLACK, \
                 colouroff=BLUE, font='OpenSans-Bold.ttf', title=''):
        """ (list of str,int,int,[(int,int,int)],
            [(int,int,int)],[str],[str]) -> SelectorUI

        Returns a UI selector object with the given top-left co-ordinates,
        button ON colour, button OFF colour (in RGB 3-tuple format),
        and text font. A font size of 35 is used. If a title text is provided
        it is printed on top of the entire selector (try it!)
        """
        self.enabled = True
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font, 35)
        self.options = list(options)
        self.colour_on = colouron
        self.colour_off = colouroff

        # Determine longest string from the 'options' list
        longest_option = [0, len(options[0])]
        for i in range(len(options)):
            string_length = len(options[i])
            if string_length > longest_option[1]:
                longest_option = [i, string_length]

        # Convert the longest option to an integer index - the actual string length
        # is no longer relevant so that information can be discarded.
        longest_option = longest_option[0]

        # Create labels for all of the options
        self.labels = []
        self.num_labels = len(options)
        for i in range(self.num_labels):
            text = self.options[i]
            text_surface = self.font.render(text, 1, self.colour_off)
            self.labels.append(text_surface)

        # Create a rect based on the longest string
        self.main_rect = self.labels[longest_option].get_rect()     # Get rect from Surface
        self.main_rect.topleft = self.x, self.y                     # Move rect to proper top-left co-ords
        self.thickness = 3                                          # Establish Rect thickness

        # Gather co-ordinate information based on the main rect
        self.label_width = self.main_rect.width
        self.height = self.main_rect.height

        # Create buttons so user can choose between 'labels'
        self.left_button = Button('<', self.x + self.label_width + 5, self.y, \
                                  40, colouron=self.colour_on, colouroff=self.colour_off)
        self.right_button = Button('>', self.x + self.label_width + 45, self.y, \
                                  40, colouron=self.colour_on, colouroff=self.colour_off)
        self.width = self.main_rect.width + 85

        # Keep track of currently selected label
        self.selected_label_index = 0

        # Apply the title text
        self.title = title
        self.title_surface = self.font.render(title, 1, self.colour_on)
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.topleft = self.x, self.y - self.title_rect.height - 5

    def get_selected_index(self):
        """ () -> int
        Returns the index of the currently selected option/label.
        """
        return self.selected_label_index

    def get_selected_option(self):
        """ () -> str
        Returns the text of the currently selected option.
        """
        return self.options[self.selected_label_index]

    def set_highest_option(self, limit=None):
        """ ([int]) -> None
        Sets the maximum index to which the Selector shifts.
        For example, if 3 is provided, then only options 0,
        1, 2, and 3 are able to be selected from the Selector,
        even if more options are theoretically available.
        Omitting the limit argument will reset the limit to what
        it was originally upon instantiation.
        """
        if limit is None:
            self.num_labels = len(self.options)
        else:
            self.num_labels = limit + 1
        self.update([])

    def set_direction_buttons(self, left_text='<', right_text='>'):
        """ (str, str) -> None
        Sets the left and right text of the directional buttons to
        the arguments given.
        """
        self.left_button.text = left_text
        self.right_button.text = right_text

    def correct_invalid_index(self):
        """ () -> None
        Correct the selected label index if it is physically
        out of range.
        """
        try:
            self.selected_label_index %= self.num_labels
        except ZeroDivisionError:
            self.selected_label_index = 0

    def update(self, events):
        """ (list of pygame.Event) -> None
        Updates the SelectorUI and all of its elements.
        """
        if not self.enabled:
            return
        
        # Update the pressed and hovering state of both buttons
        self.left_button.update(events)
        self.right_button.update(events)

        # Disable the button if the list cannot shift in that direction
        if self.selected_label_index > 0:
            self.left_button.enabled = True
        else:
            self.left_button.enabled = False
            self.correct_invalid_index()
        if self.selected_label_index < self.num_labels - 1:
            self.right_button.enabled = True
        else:
            self.right_button.enabled = False
            self.correct_invalid_index()

        # If the button is pressed, move the list in that direction
        if self.left_button.pressed:
            self.selected_label_index -= 1
        elif self.right_button.pressed:
            self.selected_label_index += 1

    def draw(self, surface, should_blit_rect=False):
        """ (pygame.Surface, [bool]) -> None
        Draws the SelectorUI onto the given Surface along with its elements.
        should_blit_rect is False by default, and toggles whether or not the main
        rect for the label is explicitly drawn as a thin rectangle.
        """
        if not self.enabled:
            return

        if should_blit_rect:
            pygame.draw.rect(surface, self.colour_off, self.main_rect, self.thickness)
        surface.blit(self.labels[self.selected_label_index], self.main_rect)
        if self.title:
            surface.blit(self.title_surface, self.title_rect)
            # also draw underline
            pygame.draw.line(surface, self.colour_on, self.title_rect.bottomleft, self.title_rect.bottomright, 5)
        self.left_button.draw(surface)
        self.right_button.draw(surface)
        
