#########################################
# Programmers: Kenneth Sinder
# Date: May 22, 2015
# File Name: pong.py
# Description: Pong Class 
#########################################

# Add top-level directory to the list of import paths
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# Perform imports and initializations
from game import *
pygame.font.init()
pygame.init()
from Pong.paddle import *
from Pong.ball import *

font = pygame.font.Font('freesansbold.ttf', 65)

class Pong(Game):

    Name = "Pong"
    Version = 0.6
    MaxAIPlayers = 2
    MaxHumanPlayers = 2
    MaxTotalPlayers = 2
    logo_path = "Pong\\pong.png"

    def __init__(self, AIClasses, WIDTH=640, HEIGHT=480, fps=60):
        """ ([int], [int], [int]) -> Pong
        Returns a Pong game.
        """
        Game.__init__(self, AIClasses, self.logo_path)
        self.width = WIDTH
        self.height = HEIGHT
        self.fps = fps
        self.bottom = self.height
        self.top = self.left = 0
        self.right = self.width
        self.fps_clock = pygame.time.Clock()
        self.game_window = pygame.display.set_mode((self.width,self.height))
        self.left_paddle = self.right_paddle = None
        
    def showscore(self,text,cord):
        fontsurface= font.render(str(text), False, WHITE)
        fontrect=fontsurface.get_rect()
        fontrect.center=cord
        self.game_window.blit(fontsurface,fontrect)

    def redraw_game_window(self, events=[], buttons=[]):
        """ ([list of pygame.Event], [list of Button]) -> None
        Draws all objects onto the game window and updates the display.
        If a list of buttons is provided, each one is updated and drawn.
        A list of events is needed to update the buttons.
        """
        self.game_window.fill(BLACK)
        
        pygame.draw.line(self.game_window, ORANGE, (self.width/2, 0), (self.width/2, self.height), 7)#middle divider
        
        self.ball.draw(self.game_window)
        self.left_paddle.draw(self.game_window)
        self.right_paddle.draw(self.game_window)
        
        pygame.draw.rect(self.game_window, ORANGE, (0,0, self.width, self.height), 20)  #border
        
        self.showscore(self.left_player_score,(self.width/2-90,50))
        self.showscore(self.right_player_score,(self.width/2+90,50))
        
##        # include paddles and ball drawing
##        for button in buttons:
##            button.update(events)
##            button.draw(self.game_window)
        #create buttons in run and implemnt them later (exit button)
        self.fps_clock.tick(self.fps)
        pygame.display.update()

    def game_over_screen(self):
        """ ([list of pygame.Event], [list of Button]) -> None
        Draws all objects onto the game window and updates the display.
        If a list of buttons is provided, each one is updated and drawn.
        A list of events is needed to update the buttons.
        """
        self.game_window.fill(BLACK)

        pygame.draw.line(self.game_window, ORANGE, (self.width/2, 0), (self.width/2, self.height), 7)#middle divider

        #self.ball.draw(self.game_window)
        #self.left_paddle.draw(self.game_window)
        #self.right_paddle.draw(self.game_window)

        pygame.draw.rect(self.game_window, ORANGE, (0,0, self.width, self.height), 20)  #border
        self.text(self.game_window, "Game Over",(self.width/2,self.height-300),font)

        self.showscore(self.left_player_score,(self.width/2-90,50))
        self.showscore(self.right_player_score,(self.width/2+90,50))

        if self.left_player_score > self.right_player_score:
            self.text(self.game_window, "Player 1 Wins",(self.width/2,self.height-150),font)

        if self.right_player_score > self.left_player_score:
            self.text(self.game_window, "Player 2 Wins",(self.width/2,self.height-150),font)


##        # include paddles and ball drawing
##        for button in buttons:
##            button.update(events)
##            button.draw(self.game_window)
        #create buttons in run and implemnt them later (exit button)
        self.fps_clock.tick(self.fps)
        pygame.display.update()
        pygame.time.delay(5000)


    def runGame(self, numAIs, numHumans):
        """ (int, int) -> None
        Runs Pong, based on the number of AIs and number of Humans given.
        """
        Game.runGame(self, numAIs, numHumans)

        self.left_paddle = Paddle(30, 50, colour=CORNFLOWER_BLUE)
        self.right_paddle = Paddle(self.width - 50, 50, colour=CORNFLOWER_BLUE)
        self.ball = Ball(self.width / 2, self.height / 2, 15)

        self.left_player_score=0
        self.right_player_score=0

        controllers = [-1, -1]  # -1 represents human player, 0 represents AI controller
        for i in range(numAIs):
            controllers[i] = 0

        game_on = True
        self.ball.launch()

        while game_on:    
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    game_on = False
                    
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_ESCAPE]:
                game_on = False
                break

            if controllers[0] != -1:
                self.setGameStateInfo(0, ball_y=self.ball.y, paddle_y=self.left_paddle.y)
            if controllers[1] != -1:
                self.setGameStateInfo(1, ball_y=self.ball.y, paddle_y=self.right_paddle.y)

            if controllers[0] == -1:
                if keys[pygame.K_w] and self.left_paddle.y > 0:
                    self.left_paddle.move_up()
                if keys[pygame.K_s] and self.left_paddle.y < self.height - self.left_paddle.height:
                    self.left_paddle.move_down()
            else:
                ai_move = self.getAIMove(0)
                if ai_move == "up" and self.left_paddle.y > 0:
                    self.left_paddle.move_up()
                if ai_move == "down" and self.left_paddle.y < self.height - self.left_paddle.height:
                    self.left_paddle.move_down()
            if controllers[1] == -1:
                if keys[pygame.K_UP] and self.right_paddle.y > 0:
                    self.right_paddle.move_up()
                if keys[pygame.K_DOWN] and self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down()
            else:
                ai_move = self.getAIMove(1)
                if ai_move == "up" and self.right_paddle.y > 0:
                    self.right_paddle.move_up()
                if ai_move == "down" and self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down()

            self.ball.update()
            self.left_paddle.update()
            self.right_paddle.update()

            if self.ball.rect.colliderect(self.left_paddle.rect):
                self.ball.shift_x *= -1
                self.ball.x+=self.ball.radius

            if self.ball.rect.colliderect(self.right_paddle.rect):
                self.ball.shift_x *= -1
                self.ball.x-=self.ball.radius
                

            if self.ball.y + self.ball.radius>=self.height or self.ball.y - self.ball.radius<=0:
                self.ball.shift_y *=-1

                
                

                #---------------------

            if self.ball.x + self.ball.radius >self.width:
                self.left_player_score+=1
                self.ball.launch(self.width // 2, self.height // 2,-self.ball.top_speed)

            if self.ball.x - self.ball.radius <0:
                self.right_player_score+=1
                self.ball.launch(self.width // 2, self.height // 2, self.ball.top_speed)
        
            self.redraw_game_window(events)

            if self.left_player_score>6 or self.right_player_score>6:
                self.game_over_screen()
                if __name__ == '__main__': pygame.quit()
                break

        self.stopAllAIThreads()
        if __name__ == '__main__': pygame.quit()
        
#-------------------------------
if __name__ == "__main__":
    from aggressiveAI import *
    game = Pong([AggressivePongAI])
    game.run_game(1, 1)

    

    
