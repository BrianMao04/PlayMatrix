#############################
# Programmer: Kenneth Sinder
# Date: April 23, 2015
# Filename: playmatrix.py
# Description: Game Platform class
#############################

from __future__ import division
import pygame
from gameswrapper import GamesWrapper
from windowsettings import WindowSettings
from pygame.locals import *
from colours import *
from button import Button
from selector import SelectorUI
from PictureButton import PictureButton

pygame.init()
pygame.font.init()

MAIN_WINDOW_CONFIG_PATH = 'config.txt'


class GamePlatform(object):
    """ (GamesWrapper, WindowSettings) -> GamePlatform
    Main Game Platform class. Handles the
    main window and any selected games. MUST
    call initializeGamesList() and
    initializeWindow() before run()
    or update().
    """

    Name = "PlayMatrix"
    CompanyName = "Square Matrix Solutions"
    Version = "1.0.0"

    def __init__(self, gamesWrapper, windowSettings):
        """ (GamesWrapper, WindowSettings) -> GamePlatform
        Creates and returns a GamePlatform object with
        the games from the given "gamesWrapper" object
        and window options from the
        "windowSettings" structure.
        """
        self.gamesLibrary = gamesWrapper
        self.windowSettings = windowSettings
        self.maximizeOverride = True
        self.mouseX, self.mouseY = 0, 0
        self.mouseClicking = False
        self.backgroundColour = BLUE
        self.genericFont = pygame.font.Font('OpenSans-Bold.ttf', 30)
        self.gamesButtons = []
        self.otherButtons = []
        self.logo = None

    def __str__(self):
        """ () -> str
        Returns a string representation of the GamePlatform.
        """
        return "{0} by {1}, version {2}".format(self.Name, self.CompanyName,
                                                self.Version)

    def text(self, text, coords, fontObj, clr=WHITE, centre=True):
        """ (str, (int, int), pygame.font.Font, [(int, int, int)], [bool]) -> None
        Renders and applies the given text string at the given
        co-ordinates on the main window. Colour is white if not
        specified. Co-ordinates are centre rather than top-left if
        not specified.
        """
        fontsurface = fontObj.render(str(text), 1, clr)
        fontrect = fontsurface.get_rect()
        if centre:
            fontrect.center = coords
        else:
            fontrect.topleft = coords
        self.mainWindow.blit(fontsurface, fontrect)

    def loadPicture(self, filepath, clr=WHITE, width=None, height=None):
        """ (str, [(int, int, int)], [int], [int]) -> pygame.Surface
        Loads an image and returns the Surface object representing
        the image. No co-ordinates are applied; the Surface
        will have to be blitted to the correct Rect or co-ords.
        If a colour is supplied, this colour is eliminated from the
        given image, otherwise white is removed.
        Scales image to the given width and height
        """
        picture = pygame.image.load(filepath)
        picture.set_colorkey(clr)
        picture = picture.convert_alpha()
        if not width is None and not height is None:
            picture = pygame.transform.scale(picture, (width, height))
        return picture

    def redrawMainWindow(self, events):
        """ (list of pygame.Event) -> None
        Redraws the main window.
        """
        self.mainWindow.fill(self.backgroundColour)  # clears screen
        bannerWidth = self.windowSettings.getDimensions()[0]
        bannerHeight = 150
        pygame.draw.rect(self.mainWindow, CORNFLOWER_BLUE, (0, 0, bannerWidth, bannerHeight))
        logoX, logoY = self.windowSettings.getDimensions()[0] // 2, bannerHeight // 2
        logoX -= self.logo.get_width() // 2
        logoY -= self.logo.get_height() // 2
        self.mainWindow.blit(self.logo, (logoX, logoY))

        for button in self.gamesButtons + self.otherButtons[:-2]:
            button.update(events)
            button.draw(self.mainWindow)

        pygame.display.update()

    def redrawAIWindow(self, game, events):
        """ (str, list of pygame.Event) -> None
        Redraws the game/AI selection panel window.
        """
        self.mainWindow.fill(self.backgroundColour)  # clears screen

        self.text("Select number of AI Players: ", (100, 200), self.genericFont, centre=False)
        self.text("Select number of Human Players: ", (100, 100), self.genericFont, centre=False)
        aiButtonInitialY = 300
        for i in range(len(self.aiSelectors[game])):
            self.aiSelectors[game][i].update(events)
            self.aiSelectors[game][i].draw(self.mainWindow)
        for button in self.otherButtons:
            button.update(events)
            button.draw(self.mainWindow)
        for selector in [self.aiCountSelector, self.humanCountSelector]:
            selector.draw(self.mainWindow)
        pygame.display.update()

    def initializeGamesList(self):
        """ () -> None
        Creates buttons for every game in the
        game library.
        """
        self.gamesButtons = []  # Clear the games list to start with a clean slate
        initialX = 20
        x = initialX
        y = 160
        w = 300
        h = 300
        spacing = 20
        for game in self.gamesLibrary.games:
            b = PictureButton(game.logo_path, x, y, w, h, colouron=WHITE, colouroff=GREY)
            b.load_hover_text(game.Name)
            self.gamesButtons.append(b)
            x += w + spacing
            if x + w + spacing > self.windowSettings.getWidth():
                x = initialX
                y += h + spacing

        # Load and initialize AI Selectors
        self.aiSelectors = {}  # Dictionary key represents game as string, Value is list of selectors
        spacing = 60
        for i in range(self.gamesLibrary.numGames):
            x = 100
            y = 350
            gameName = self.gamesLibrary.games[i].Name
            AIs = self.gamesLibrary.aiClasses[i]
            try:
                aiList = AIs[:]
            except TypeError:
                aiList = [AIs]
            selectors = []
            for i in range(self.gamesLibrary.games[i].MaxAIPlayers):
                try:
                    selector = SelectorUI([ai.Description for ai in aiList], x, y, colouron=WHITE, colouroff=GRAY,
                                          title="Choose for AI #{0}: ".format(i + 1))
                    selectors.append(selector)
                    x += selector.width + spacing
                    if x + w + spacing > self.windowSettings.getWidth():
                        x = initialX
                        y += h + spacing
                except AttributeError:
                    pass  # If there are no AIs, do not make selectors for them
            self.aiSelectors[gameName] = selectors

    def initializeWindowSettings(self):
        """() -> None
        Loads the window settings and prepares the PlayMatrix
        main window.

        Throws:
            EnvironmentError: if flags or resolution are invalid
        """
        if self.maximizeOverride:
            width = pygame.display.list_modes()[0][0]  # Get native resolution
            height = pygame.display.list_modes()[0][1]
            self.windowSettings.setDimensions(width, height)
            self.windowSettings.addFlags(FULLSCREEN)
        if not pygame.display.mode_ok(self.windowSettings.getDimensions(), \
                                      self.windowSettings.getFlags()):
            raise EnvironmentError("Flags or resolution is invalid.")
        self.mainWindow = pygame.display.set_mode(self.windowSettings.getDimensions(), \
                                                  self.windowSettings.getFlags())
        pygame.display.set_caption(self.__str__())

    def run(self):
        """ () -> None
        Runs PlayMatrix.
        """
        windowW, windowH = self.windowSettings.getDimensions()
        self.mainWindow.fill(self.backgroundColour)
        exitButton = Button("Exit", 20, windowH - 70, colouron=WHITE, colouroff=GREY)
        backButton = Button("Back", 20, windowH - 120, colouron=WHITE, colouroff=GREY)
        launchButton = Button("Launch Game!", windowW // 2, windowH - 50, colouron=WHITE, colouroff=GREY)
        launchButton.correct_text_overflow(True)
        self.otherButtons = [exitButton, backButton, launchButton]
        self.aiCountSelector = None
        self.humanCountSelector = None
        numberOfAIs = numberOfHumans = 0
        selected_game_class = None
        gameselectionmode = True
        selected_game = ""
        AIselectionmode = False

        if self.logo is None:
            self.logo = self.loadPicture("logo.png", width=210, height=135)

        running = True
        while running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE] or exitButton.pressed:
                break

            if gameselectionmode:

                for event in events:
                    if event.type == QUIT:
                        running = False
                        break

                for i in range(len(self.gamesButtons)):
                    if self.gamesButtons[i].pressed:
                        selected_game = self.gamesButtons[i].text

                        aiMax = self.gamesLibrary.games[i].MaxAIPlayers
                        huMax = self.gamesLibrary.games[i].MaxHumanPlayers
                        aiRange = ['  ' + str(i) + '  ' for i in range(aiMax + 1)]
                        huRange = ['  ' + str(i) + '  ' for i in range(huMax + 1)]
                        self.aiCountSelector = SelectorUI(aiRange, 670, 200,
                                                          font='OpenSans-Regular.ttf', colouroff=GREY, colouron=WHITE)
                        self.humanCountSelector = SelectorUI(huRange, 670, 100,
                                                             font='OpenSans-Regular.ttf', colouroff=GREY,
                                                             colouron=WHITE)
                        self.aiCountSelector.set_direction_buttons('-', '+')
                        self.humanCountSelector.set_direction_buttons('-', '+')
                        selected_game_class = self.gamesLibrary.getGameClass(selected_game)
                        gameselectionmode = False
                        AIselectionmode = True
                        break
                self.redrawMainWindow(events)  # Redraw

            if AIselectionmode:

                for event in events:
                    if event.type == QUIT:
                        running = False
                        break

                if self.otherButtons[-1].pressed:  # If launch game button pressed, launch the game!
                    self.gamesLibrary.launchGame(selected_game, numberOfAIs, numberOfHumans,
                                                 [self.aiSelectors[selected_game][i]. \
                                                  get_selected_index() for i in range(numberOfAIs)])
                    self.initializeWindowSettings()

                self.aiCountSelector.update(events)
                if self.aiCountSelector.right_button.pressed or self.aiCountSelector.left_button.pressed:
                    remaining_players = selected_game_class.MaxTotalPlayers - \
                                        self.aiCountSelector.get_selected_index()
                    self.humanCountSelector.set_highest_option(remaining_players)
                self.humanCountSelector.update(events)
                if self.humanCountSelector.right_button.pressed or self.humanCountSelector.left_button.pressed:
                    remaining_players = selected_game_class.MaxTotalPlayers - \
                                        self.humanCountSelector.get_selected_index()
                    self.aiCountSelector.set_highest_option(remaining_players)
                numberOfAIs = self.aiCountSelector.get_selected_index()
                numberOfHumans = self.humanCountSelector.get_selected_index()

                for i in range(len(self.aiSelectors[selected_game])):
                    if i + 1 > numberOfAIs:
                        self.aiSelectors[selected_game][i].enabled = False
                    else:
                        self.aiSelectors[selected_game][i].enabled = True

                if self.otherButtons[1].pressed:  # If the back button is pressed
                    gameselectionmode = True  # change back to game selecting mode
                    AIselectionmode = False  # this reloads the main window

                minTotal = selected_game_class.MinTotalPlayers
                maxTotal = selected_game_class.MaxTotalPlayers
                if not minTotal <= numberOfAIs + numberOfHumans <= maxTotal:
                    launchButton.enabled = False
                else:
                    launchButton.enabled = True

                self.redrawAIWindow(selected_game, events)  # Redraw all objects in the options screen

        pygame.quit()


# --------------------------------------------
def startPlatform(gamesList, aiList):
    """ (list of Class, list of Class) -> None
    Take in a list of Game classes and AI classes
    and perform all actions necessary to start
    the games portal.
    """

    # Set up and load window settings
    windowSettings = WindowSettings()
    windowSettings.loadFromFile(MAIN_WINDOW_CONFIG_PATH)

    # Instantiate GamesWrapper()
    games = GamesWrapper()

    # Add games from the gamesList to the games library
    for game in gamesList:
        games.addGame(game)

    # Take all of the AIs from the list above and apply them to the
    # supported games.
    for ai in aiList:
        games.addAI(ai)

    # Instantiate and launch the game platform
    platform = GamePlatform(games, windowSettings)
    platform.initializeWindowSettings()
    platform.initializeGamesList()
    platform.run()

# --------------------------------------------

if __name__ == "__main__":
    # ------------------ GAME AND AI IMPORTS ------------- #
    # AIs and Games can be placed in folders to make the folder
    # structure tidy. Just make sure to put a blank __init__.py file
    # in the folder, and import it as a module.
    # Look at the rock/paper/scissors example below for hints.
    # Refer to the manual for more information.

    # Rock Paper Scissors
    from RPS.rock_paper_scissors_game import RockPaperScissors
    from RPS.randAI import RPSRandAI
    from RPS.numberphileAI import RPSNumberphileAI

    # Pong
    from Pong.pong import Pong
    from Pong.aggressiveAI import AggressivePongAI
    # ---------------------------------------------------- #

    # ------------------ ADD GAMES HERE ------------------ #
    # Add your game classes to the list below. PlayMatrix  
    # takes care of adding it to the games library. Consult
    # the manual, Section 1.2 to make sure you have        
    # followed all proper guidelines for creating a game.  
    gamesList = [RockPaperScissors, Pong]
    # ---------------------------------------------------- #

    # ------------------   ADD AI HERE  ------------------ #
    # If you have made your own AI, make sure that you have imported
    # it above and add the class to the list below in any order.
    # That's all there is to it. PlayMatrix takes care of the rest!
    aiList = [RPSRandAI, RPSNumberphileAI, AggressivePongAI]
    # ---------------------------------------------------- #

    startPlatform(gamesList, aiList)  # Does the rest of the work "automatically"
