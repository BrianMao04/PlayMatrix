#################################
# Programmer: Kenneth Sinder
# Date: April 20, 2015
# Filename: player.py
# Description: Base Player class
#################################

from random import choice

class Player():
    """ ([bool]) -> Player
    Generic player for Rock/Paper/Scissors.
    """

    def __init__(self, moveOptions, moveInequalities, AI=False):
        self.isAI = AI
        self.moveOptions = moveOptions
        self.moveInequalities = moveInequalities
        self.move = choice(self.moveOptions)
        self.enemyMove = choice(self.moveOptions)
        self.ready = False
        self.score = 0

    def __str__(self):
        """ () -> str
        Returns type of Player (AI/Non-AI) as a string.
        """
        return "AI-based Player" if self.isAI else "Non-AI Player"

    def update(self):
        """ () -> None
        Updates the Player state.
        """
        raise NotImplementedError("This functionality is not defined.")

    def getScore(self):
        """ () -> int
        Returns the current score of the Player.
        """
        return self.score

    def isReady(self):
        """ () -> bool
        Returns True if the Player is ready to send a move, else False.
        """
        return self.ready

    def setMove(self, move):
        """ (str) -> None
        Set the Player's next move.
        """
        self.move = move
        self.ready = True

    def getMove(self):
        """ () -> str
        Returns the next move.

        Raises:
            StandardError: if the Player is unready
        """
        if not self.isReady():
            raise StandardError("Player '" + self.__str__() + "' is unready.")
        self.ready = False
        return self.move

    def setLastEnemyMove(self, move):
        """ (str) -> None
        Save the input move string as the last move.

        Raises:
            ValueError: if move is unrecognized
        """
        if not move in self.moveOptions:
            return ValueError("Move is undefined.")
        self.enemyMove = move
