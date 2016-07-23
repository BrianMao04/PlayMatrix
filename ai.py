#############################
# Programmer: Kenneth Sinder
# Date: May 11, 2015
# Filename: ai.py
# Description: AI Base Class
#############################

class AI(object):
    """ (**kwargs) -> AI
    Returns an AI controller object that makes a decision based on the game state.
    Call  help(AI.__init__)  for more information.
    """

    # Note: subclass AI Description should be specific/unique to the game and AI style
    # e.g. Description = "Aggressive Tanks AI"  or  Description = "Casual Pong AI" (must be string)
    Description = "Standard AI"

    # List of strings, contains all necessary game state information e.g. "last_move"
    game_state_params = []

    # Games that the AI supports - usually this is one one game - must be str list
    supported_games = []

    def __init__(self, **initial_game_state):
        """ (**kwargs) -> AI
        Returns an AI controller object.
        Initial_game_state is a keyword argument that contains game constants that don't
        need to be supplied on every iteration of the game e.g. different moves in rock paper scissors.

        >>> default_AI = AI(move_options=('rock', paper', 'scissors'))
        """
        self.initial_game_state = initial_game_state.copy()
        self.game_state = initial_game_state.copy()

    def __str__(self):
        """ () -> str
        Returns the AI description
        """
        return self.Description
        
    def update(self, **kwargs):
        """ (**kwargs) -> None
        Updates the AI object with all of the game state objects.
        These can include strings, integers, floats...etc.
        These values are accompanied by a keyword, and all keywords specified
        in the self.game_state_params list must be covered.

        Throws:
            ValueError: if kwargs violates the contract set forth by game_state_params
        """
        
        for game_property in self.game_state_params:    # Check that all obligated gamestate...
            if game_property not in kwargs and \
               game_property not in self.initial_game_state:    # ...properties are supplied
                raise ValueError("Game state contract violated: " + game_property + " missing")
        for game_property in kwargs:                    # Update game state dictionary with the new information
            self.game_state[game_property] = kwargs[game_property]

    def get_next_operation(self):
        """ () -> object
        Returns the next move, assuming that the AI was updated.

        Throws:
            NotImplementedError: if abstract method is not overridden
        """
        raise NotImplementedError("Abstract method not overridden.")
        
