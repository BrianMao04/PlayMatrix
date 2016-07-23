#############################
# Programmers: Brian Mao (Game)
#              Kenneth Sinder (AI) 
# Date: April 23, 2015
# Filename: rock_paper_scissors_game.py
# Description: Rock Paper Scissors Game
#              Can run standalone or with PlayMatrix
#############################

# Add top-level directory to the list of import paths
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# Perform imports and initializations
import random
from game import *
from colours import *
from button import Button

pygame.font.init()
pygame.init()

MoveOptions = ["Rock", "Paper", "Scissors"]
MoveInequalities = [["Rock", "Scissors"], ["Scissors", "Paper"], ["Paper", "Rock"]]
genericfont = pygame.font.Font('freesansbold.ttf', 100)
genericfont2 = pygame.font.Font('freesansbold.ttf', 30)


class RockPaperScissors(Game):
    Name = "Rock, Paper, Scissors"
    Version = 1.0
    logo_path = "RPS//gamelogo.png"
    rock_path = "RPS//rock.png"
    scissors_path = "RPS//scissors.png"
    paper_path = "RPS//paper.png"

    def __init__(self, AIClasses):
        """ (Class, str) -> Game
        Instantiate Game object with expected properties of a rock paper scissors game.
        """
        Game.__init__(self, AIClasses, self.logo_path)
        self.window_length = 640
        self.window_width = 480
        self.backgroundColour = CORNFLOWER_BLUE
        self.logo = None
        self.scores = [0, 0]
        self.gameWindow = None

    @staticmethod
    def capitalize(string):
        """ (str) -> str
        Returns the input string, but with the first letter capitalized.
        """
        return string[0].upper() + string[1:].lower()

    def redraw_game_window(self, surface, buttons, events):  # Main redraw function that makes most outputs
        """ (Surface, list of Button, list of Event, Player, Player)
        Draws all given buttons and the score of the given players on the
        given Surface object. A (preferably cloned) list of events
        is used to update the Buttons as well. The Pygame display is
        also updated and filled accordingly.
        """
        surface.fill(self.backgroundColour)
        self.text(surface, "Player 1 Score", (120, 20), genericfont2, (0, 0, 0))
        self.text(surface, self.scores[0], (100, 90), genericfont)
        self.text(surface, "Player 2 Score", (450, 20), genericfont2, (0, 0, 0))
        self.text(surface, self.scores[1], (450, 90), genericfont)

        for button in buttons:
            button.update(events)  # Update button state for hovering+clicking
            button.draw(surface)
        pygame.display.update()

    def redraw_move_window(self, surface, buttons, events, human_picture, cpu_picture):
        surface.fill(self.backgroundColour)
        self.text(surface, "Player 1 Score", (120, 20), genericfont2, (0, 0, 0))
        self.text(surface, self.scores[0], (100, 90), genericfont)
        self.text(surface, "Player 2 Score", (450, 20), genericfont2, (0, 0, 0))
        self.text(surface, self.scores[1], (450, 90), genericfont)

        self.text(surface, "P1 Chose: ", (150, 150), genericfont2, (0, 0, 0))
        surface.blit(human_picture, ((self.window_width / 2 - 150), 200))
        self.text(surface, "P2 Chose: ", (450, 150), genericfont2, (0, 0, 0))
        surface.blit(cpu_picture, ((self.window_width / 2 + 150), 200))

        for button in buttons:
            button.update(events)  # Update button state for hovering+clicking
            button.draw(surface)
        pygame.display.update()

        pygame.time.delay(2000)

    def update_score(self, p1move, p2move):
        """ (str, str) -> None
        Updates the score based on the moves.
        """
        if p1move == p2move:
            pass
        elif [p1move, p2move] in MoveInequalities:
            self.scores[0] += 1
        else:
            self.scores[1] += 1

    def runGame(self, numAIs, numHumans):
        """ (int, int) -> None
        Executes the game, instantiating the desired number of AI
        players. The number of humans does not need to be provided.
        """
        Game.runGame(self, numAIs, numHumans, moveOptions=MoveOptions, moveInequalities=MoveInequalities,
                                     lastEnemyMove=random.choice(MoveOptions))

        # Internal record of human / AI players
        controllers = [-1, -1]  # -1 represents a human player, 0 represents AI player
        for i in range(0, numAIs):
            controllers[i] = 0

        buttons = []
        if -1 in controllers:
            rock_button = Button("Rock", 100, 350, colouron=(200, 200, 0), colouroff=(0, 0, 0))
            paper_button = Button("Paper", 250, 350, w=110, h=40, colouron=(200, 200, 0), colouroff=(0, 0, 0))
            scissors_button = Button("Scissors", 400, 350, w=180, h=40, colouron=(200, 200, 0), colouroff=(0, 0, 0))
            buttons = [rock_button, paper_button, scissors_button]
            buttons_as_dict = {b.text: b for b in buttons}  # Convert the buttons to a user-friendly dictionary

        self.gameWindow = pygame.display.set_mode((self.window_length, self.window_width))

        items_width = 90
        try:
            # Attempt to load the pictures with their full file path
            self.logo = self.loadPicture(self.logo_path, items_width)
            rock_picture = self.loadPicture(self.rock_path, items_width)
            paper_picture = self.loadPicture(self.paper_path, items_width)
            scissors_picture = self.loadPicture(self.scissors_path, items_width)
        except pygame.error:
            # Load the pictures from the current folder instead
            self.logo = self.loadPicture(self.logo_path[self.logo_path.index('/') + 2:], items_width)
            rock_picture = self.loadPicture(self.rock_path[self.rock_path.index('/') + 2:], items_width)
            paper_picture = self.loadPicture(self.paper_path[self.paper_path.index('/') + 2:], items_width)
            scissors_picture = self.loadPicture(self.scissors_path[self.scissors_path.index('/') + 2:], items_width)
        item_pictures = {"Rock": rock_picture, "Paper": paper_picture, "Scissors": scissors_picture}

        events = []
        while not self.shouldQuit(events):
            events = pygame.event.get()
            if controllers == [0, -1]:
                for player_move in buttons_as_dict:
                    if buttons_as_dict[player_move].pressed:
                        cpu_move = self.capitalize(self.getAIMove(0))
                        self.update_score(player_move, cpu_move)
                        self.setGameStateInfo(0, lastEnemyMove=cpu_move)
                        self.redraw_move_window(self.gameWindow, buttons, events,
                                                item_pictures[player_move], item_pictures[cpu_move])
            elif controllers == [0, 0]:
                moves = []
                for i in range(len(controllers)):
                    moves.append(self.capitalize(self.getAIMove(i)))
                self.update_score(moves[0], moves[1])
                self.setGameStateInfo(0, lastEnemyMove=moves[1])
                self.setGameStateInfo(1, lastEnemyMove=moves[0])
                self.redraw_move_window(self.gameWindow, [], events, item_pictures[moves[0]], item_pictures[moves[1]])
            self.redraw_game_window(self.gameWindow, buttons, events)

        self.stopAllAIThreads()
        if __name__ == "__main__":
            pygame.quit()
        # -------------------------------


if __name__ == "__main__":
    from randAI import RPSRandAI
    # Only one AI class must be provided to the constructor since only one AI
    # bot will be used. (i.e. Default mode is player vs. CPU)
    game = RockPaperScissors([RPSRandAI])
    game.runGame(1, 1)
