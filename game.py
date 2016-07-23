#############################
# Programmer: Kenneth Sinder
# Date: April 23, 2015
# Filename: game.py
# Description: Default Game class
#############################

from __future__ import division
import pygame, Queue, threads
from pygame.locals import *
from colours import *


class Game(object):
    """ (Class, str) -> Game
    Returns an instance of Game.
    """

    Name = "Game"
    Version = 0.0
    MaxAIPlayers = 2
    MaxHumanPlayers = 2
    MaxTotalPlayers = 2
    MinTotalPlayers = 2

    def __init__(self, AIClasses, logo_path):
        """ (list of Class, str) -> Game
        Returns a Game object. AIClasses corresponds to a list
        of AI classes, one for each AI bot that gets instantiated.
        Some users will want different AIs to have different algorithms.
        """
        self.aiClasses = AIClasses
        self.logo_path = logo_path
        self.logo = None
        pygame.display.set_caption(self.__str__())  # Set the display caption
        try:
            self.logo = self.loadPicture(self.logo_path)
        except (pygame.error, OSError):
            # If the logo cannot be loaded, leave the logo attribute as None
            pass
        self.numAIs = 0
        self.numHumans = 0

        # Override or update in subclass run_game()
        self.initialGameState = {}

        self.gameStates = []

        self.aiThreads = []
        self.aiThreadStopCommands = []
        self.aiQueues = []

    def __str__(self):
        """ (None) -> str
        Returns a string representation of the Game object
        that contains the game's name and version in a
        user-friendly one-line string.
        Should not be overridden unless absolutely
        necessary.
        """
        return self.Name + " " + str(self.Version)

    def setNumPlayers(self, numAIs, numHumans):
        """ (int, int) -> None
        Verifies that the number of AI players and number
        of human players is within the necessary specification
        and sets these attributes.

        Raises:
            ValueError: if the values are invalid
        """
        if not 0 <= numAIs <= self.MaxAIPlayers:
            raise ValueError("Invalid AI Player Count")
        if not 0 <= numHumans <= self.MaxHumanPlayers:
            raise ValueError("Invalid Human Player Count")
        if not self.MinTotalPlayers <= numAIs + numHumans <= self.MaxTotalPlayers:
            raise ValueError("Invalid Total Player Count")
        self.numAIs = numAIs
        self.numHumans = numHumans

    def startAIThreads(self, queueMaxSize=10):
        """ ([int]) -> None
        Initializes the AI threads. MUST be called at the top of run_game.
        """
        self.aiThreadStopCommands = [threads.CONTINUE[:] for i in range(len(self.aiClasses))]
        self.gameStates = [{} for i in range(len(self.aiClasses))]
        for i in range(len(self.aiClasses)):
            aiOutputQueue = Queue.Queue(queueMaxSize)
            aiThread = threads.AIThread(self.aiClasses[i], aiOutputQueue, self.aiThreadStopCommands[i],
                                        self.initialGameState, self.gameStates[i])

            aiThread.start()
            self.aiThreads.append(aiThread)
            self.aiQueues.append(aiOutputQueue)

    def removeThread(self, i=0):
        """ ([int]) -> None
        Removes the AI thread with the given index.
        """
        self.aiThreadStopCommands[i] = threads.EXIT
        self.aiThreads.pop(i)
        self.aiThreadStopCommands.pop(i)
        self.aiQueues.pop(i)

    def stopAllAIThreads(self):
        """ Stops all AI threads - MUST be called when the game is finished execution! """
        for i in range(len(self.aiThreadStopCommands)):
            self.aiThreadStopCommands[i].append(threads.EXIT)

    def getAIMove(self, i=0):
        """ ([int]) -> object
        Returns a move from the queue representing the
        AI with index i. Returns None if no such move
        exists.
        """
        if not self.aiQueues[i].empty():
            return self.aiQueues[i].get()

    def setInitialGameStateInfo(self, **gameState):
        """ (**kwargs) -> None
        Set the initial game state information to be sent to AI
        threads. If this method is called, it MUST be called before
        startAIThreads(...).
        """
        for gameProperty in gameState:
            self.initialGameState[gameProperty] = gameState[gameProperty]

    def setGameStateInfo(self, aiIndex, **gameState):
        """ (int, **kwargs) -> None
        Set the game state information to be sent to the AI
        thread with the given index.
        This method should be called for each AI,
        on every iteration of the game loop in run_game.
        """
        for gameProperty in gameState:
            self.gameStates[aiIndex][gameProperty] = gameState[gameProperty]

    @staticmethod
    def get2DList(i, j, value=0):
        """ (int, int) -> list of list of object
        Returns an i x j 2D list initialized with the
        given value.
        >>> Game.get2DList(2, 3)
        [[0, 0], [0, 0], [0, 0]]
        """
        return [[value for a in range(i)] for b in range(j)]

    @staticmethod
    def text(surface, text, coords, font, clr=WHITE, antialiasing=True):
        """ (pygame.Surface, str, (int, int), pygame.Font, [(int, int, int)]) -> None
        Draws text with the given font at the given x, y center
        co-ordinate tuple. The default colour is white unless a different
        RGB tuple is supplied. Anti-aliased (smoothened) text by default.
        The given Surface should be the main window of the Game.
        """
        fontsurface = font.render(str(text), antialiasing, clr)  # Render the text onto the new surface
        fontrect = fontsurface.get_rect()  # Get boundaries of text surface
        fontrect.center = coords  # Center of text surface becomes cord parameter
        surface.blit(fontsurface, fontrect)  # Copy font surface into game window

    @staticmethod
    def loadPicture(filepath, target_width=None, target_height=None):
        """ (str, [int], [int]) -> pygame.Surface
        Loads a picture from the given filepath and returns a Surface object
        that contains the image. If a width is supplied, the image is scaled to
        that width and the aspect ratio is preserved. If a width and height
        are provided, then the Surface is scaled to the given values.
        """
        picture = pygame.image.load(filepath).convert_alpha()  # Load image and convert image pixel format
        if target_width is not None and target_height is not None:
            picture = pygame.transform.scale(picture, (target_width, target_height))
        elif target_width is not None:
            ratio = picture.get_height() / picture.get_width()
            picture = pygame.transform.scale(picture, (target_width, int(target_width * ratio)))
        return picture

    @staticmethod
    def shouldQuit(events):
        """ ([str]) -> bool
        Returns True if the game loop should be aborted, otherwise False.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return True
        for event in events:
            if event.type == pygame.QUIT:
                return True
        return False

    def runGame(self, numAIs, numHumans, **initialGameStateInfo):
        """ (int, int, *args) -> None
        Executes the Game with the given number of AIs
        instantiated and activated. Note that the default
        implementation of Game does not include any functionality
        and this method MUST be overridden in subclasses.
        """
        self.setNumPlayers(numAIs, numHumans)
        self.setInitialGameStateInfo(**initialGameStateInfo)
        self.startAIThreads()

    def draw(self, surface):
        """ (pygame.Surface) -> None
        Draws the game field onto the given Surface object.
        No default implementation - should be overridden
        or replaced with an equivalent method.
        """
        raise NotImplementedError("Cannot call on abstract method.")
