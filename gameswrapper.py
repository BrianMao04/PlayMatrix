#############################
# Programmer: Kenneth Sinder
# Date: April 23, 2015
# Filename: gameswrapper.py
# Description: Games Wrapper class
#############################

from dneerror import GameDNEError

class GamesWrapper(object):
    """ () -> GamesWrapper
    Wrapper object for all games and AIs.
    """

    def __init__(self, suppressWarnings=True):
        """ ([bool]) -> GamesWrapper
        Instantiates and returns a new GamesWrapper object.
        Starts with no games or AIs loaded.
        Games and AIs are saved as two separate lists, where
        an index i corresponds to a particular game and its AIs.
        """
        self.games = []
        self.aiClasses = []
        self.numGames = 0
        self.shouldSuppressWarnings = suppressWarnings

    def addGame(self, game, AI=None):
        """ (Game Class, [AI Class]) -> int
        Adds and processes a new Game and corresponding AI.
        AI class must fully interoperate with the Game
        class and all related constructs.
        Returns the new total number of games loaded.
        """
        self.games.append(game)
        self.aiClasses.append(AI)
        self.numGames += 1
        return self.numGames

    def addGames(self, games, AIs):
        """ (list of Game, list of AI) -> int
        Adds and processes a list of new games
        and AIs that correspond to those games.
        Returns the new total number of games loaded.

        Throws:
            ValueError: if length(games) =/= length(AIs)
        """
        if len(games) != len(AIs):
            raise ValueError("Number of AI Classes MUST match" + \
                             "the number of Games being added.")
        self.games.extend(games)
        self.aiClasses.extend(AIs)
        self.numGames += len(games)
        return self.numGames

    def addAI(self, *AI):
        """ (*args) -> None
        Add one or more AIs to the games they support.
        """
        for ai in AI:
            added = False
            for i in range(self.numGames):
                if self.games[i].Name in ai.supported_games:
                    try:
                        if ai not in self.aiClasses[i]:
                            self.aiClasses[i].append(ai)
                    except TypeError:
                        if self.aiClasses[i] is None:
                            self.aiClasses[i] = [ai]
                        elif ai != self.aiClasses[i]:
                            self.aiClasses[i] = [self.aiClasses[i], ai]
                    added = True
            if not added:
                raise GameDNEError("Attempted to update nonexistent Game")

    def getGameClass(self, gameName):
        """ (str) -> Class
        Returns the Game class that corresponds to the given name.
        """
        for i in range(self.numGames):
            if self.games[i].Name == gameName:
                return self.games[i]
        raise GameDNEError("Attempted to return nonexistent Game")

    def removeGame(self, game):
        """ (str) -> int
        Removes a Game and corresponding AI, and
        returns the new number of games loaded.

        Throws:
            GameDNEError: if such a game does not exist
        """
        for i in range(self.numGames):
            if self.games[i].Name == game or self.games[i] == game:
                del self.games[i]
                del self.aiClasses[i]
                self.numGames -= 1
                return self.numGames
        raise GameDNEError("Attempted to remove nonexistent Game")

    @staticmethod
    def _startGame(game, AIs, numAIs, numHumans):
        #if numHumans == 1:
        gameInstance = game(AIs)
        gameInstance.runGame(numAIs, numHumans)
        #else:
        #    sendStreams = []
        #    recvStream = Queue.Queue()
        #    for i in range(numHumans):
        #        sendStreams.append(Queue.Queue())

    def launchGame(self, gameName, numAIs, numHumans, aiIndices=None):
        """ (string, int, int, [list of int]) -> None
        Launch a game with the name property of "gameName"
        with the desired number of AI players and Human players.
        The AI indices are used to choose between multiple AI classes
        for each AI bot if there is ambiguity. aiIndices MUST have
        a length of "numAIs" for obvious reasons.
        """
        if aiIndices is None:
            aiIndices = [0] * numAIs
        if len(aiIndices) != numAIs:
            raise ValueError("Number of AI classes chosen is invalid.")
        for game in self.games:
            if game.Name == gameName:
                index = self.games.index(game)
                aiClasses = []
                for i in range(numAIs):
                    try:
                        aiClass = self.aiClasses[index][aiIndices[i]]
                    except IndexError:
                        aiClass = self.aiClasses[index][0]
                        if not self.shouldSuppressWarnings:
                            print("WARNING: Attempted to use non-existent AI, used default.")
                    except TypeError:
                        aiClass = self.aiClasses[index]
                        if not self.shouldSuppressWarnings:
                            print("WARNING: Attempted to use non-existent AI, used default.")
                    if not self.isCompatible(game, aiClass):
                        raise GameDNEError("Unsupported AI. Launch aborted.")
                    aiClasses.append(aiClass)
                self._startGame(game, aiClasses, numAIs, numHumans)
                return
        raise GameDNEError("Attempted to launch nonexistent Game")

    def returnAIDescriptions(self, game):
        """ (str) -> list of str
        Returns a list of the descriptions of all AIs for
        the given game.
        """
        for i in range(self.numGames):
            if self.games[i].Name == game or self.games[i] == game:
                try:
                    return [c.Description for c in self.aiClasses[i]]
                except TypeError:
                    return self.aiClasses[i].Description
                except AttributeError:
                    return ""
        raise GameDNEError("Attempted to launch nonexistent Game")

    def updateAI(self, game, aiClass):
        """ (str, Class) -> None
        Replaces the AI or AIs for the game with the given game name
        with the given AI class.
        """
        for i in range(self.numGames):
            if self.games[i].Name == game or self.games[i] == game:
                self.aiClasses[i] = aiClass
                return
        raise GameDNEError("Attempted to update AI of nonexistent Game")

    @staticmethod
    def isCompatible(game, AI):
        """ (Game, AI) -> bool
        Returns True if the Game is compatible with
        the AI, False otherwise.
        """
        return game.Name in AI.supported_games
