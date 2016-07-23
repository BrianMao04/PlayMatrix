#################################
# Programmer: Kenneth Sinder
# Date: April 20, 2015
# Filename: aiPlayer.py
# Description: AI Player class
#################################

import random
from ai import AI

class RPSRandAI(AI):
    """ (**kwargs) -> RPSRandAI
    AI controller for Rock/Paper/Scissors-type game
    Uses pseudorandom choice-based algorithm.
    See: https://docs.python.org/2/library/random.html
    
    As with all classes in this project that inherit from AI,
    make sure that all of the information required in game_state_params
    is supplied, either when instantiating the AI, or when updating,
    in kwargs format.
    e.g.
    >>> ai = RPSRandAI(moveOptions=('rock','paper','scissors'))
    """

    Description = "Pseudorandom AI"
    game_state_params = ["moveOptions"]
    supported_games = ["Rock, Paper, Scissors"]

    def get_next_operation(self):
        """ () -> str
        Returns one of the game objects, selected pseudorandomly.
        """
        return random.choice(self.game_state["moveOptions"])
