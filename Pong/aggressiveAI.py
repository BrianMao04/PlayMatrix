#########################################
# Programmers: Kenneth Sinder
# Date: May 26, 2015
# File Name: aggressiveAI.py
# Description: Aggressive Pong AI :) 
#########################################

from ai import AI

class AggressivePongAI(AI):

    Description = "Aggressive Pong AI"

    game_state_params = ['ball_y', 'paddle_y']

    supported_games = ["Pong"]

    def __init__(self):
        """ () -> AggressivePongAI
        Returns an aggressive pong AI. Requires no initial
        game state information.
        """
        AI.__init__(self)

    def update(self, **kwargs):
        """ (**kwargs) -> None
        Updates the aggressive AI.
        Remember, the ball_x, ball_y, ball_vx (x speed), ball_vy
        (y speed), paddle_x, and paddle_y, MUST be supplied
        on every game iteration.
        """
        AI.update(self, **kwargs)

    def get_next_operation(self):
        """ () -> str
        Returns "up" or "down" depending on the direction
        the paddle should move.
        """
        if self.game_state['ball_y'] > self.game_state['paddle_y']:
            return "down"
        return "up"
