#################################
# Programmer: Kenneth Sinder
# Date: May 11, 2015
# Filename: numberphileAI.py
# Description: AI player class (Numberphile algo)
#################################

import random
from ai import AI

class RPSNumberphileAI(AI):
    """ (**kwargs) -> RPSNumberphileAI
    AI controller for Rock/Paper/Scissors
    Uses Numberphile algorithm.
    See: https://www.youtube.com/watch?v=rudzYPHuewc

    e.g.
    >>> options = ('rock', 'paper', 'scissors')
    >>> inequalities = (('rock', 'scissors'), ('scissors', 'paper'), ('paper', 'rock'))
    >>> ai = RPSNumberphileAI(moveOptions=options, moveInequalities=inequalities)
    >>> ai.update(lastEnemyMove="rock")
    """

    Description = "Numberphile Algorithm"
    game_state_params = ["moveOptions", "moveInequalities", "lastEnemyMove"]
    supported_games = ["Rock, Paper, Scissors"]

    def get_next_operation(self):
        """ () -> str
        Decide the optimal next move using the Numberphile algorithm.
        Returns this move as a string.
        """
        # Determine if this AI won the last round
        try:
            wonLastRound = self.won(self.move, self.game_state["lastEnemyMove"])
        except (AttributeError, KeyError):
            # If no past move exists, pick one pseudorandomly
            self.move = random.choice(self.game_state["moveOptions"])
            return self.move

        # (Numberphile algorithm) If lost, then play the move that wasn't played
        if not wonLastRound:
            self.move = self.getNewMove([self.move, self.game_state["lastEnemyMove"]])
        # If won, then play what the enemy just played
        else:
            self.move = self.game_state["lastEnemyMove"]

        return self.move

    # ----- Helper methods ----- #

    def won(self, move1, move2):
        """ (str, str) -> bool
        Returns True if move1 beats move2, else False.
        """
        for winner, loser in self.game_state["moveInequalities"]:
            if move1 == winner and move2 == loser:
                return True
        return False

    def getNewMove(self, oldMoves):
        """ (list of str) -> str
        Returns the first possible move in the sequence
        of possible moves that is NOT in the input sequence 'oldMoves'.

        Raises:
            IndexError: unique/original move not found
        """
        for move in self.game_state["moveOptions"]:
            if move not in oldMoves:
                return move
        raise IndexError("Unique move not found")
