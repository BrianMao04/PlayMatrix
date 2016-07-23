############################
# Programmer: Kenneth Sinder
# Date: June 6, 2015
# Filename: platformtest.py
# Description: Unit Tests for Platform
############################

import unittest
from dneerror import GameDNEError
from gameswrapper import GamesWrapper as Wrapper
from game import Game
from ai import AI

class TestPlatform(unittest.TestCase):
    """ Tests the important GamesWrapper class.
     NOTE: This set of unit tests is not a good
     guideline or reference for extending or using
     PlayMatrix It is only meant to act as a
     unit test. """

    def testInit(self):
        w = Wrapper()
        result = w.numGames
        expected = 0
        self.assertEqual(result, expected)

    def testAddGame(self):
        w = Wrapper()
        w.addGame(Game, AI)
        self.assertEqual(w.numGames, 1)
        self.assertEqual(len(w.games), 1)
        self.assertEqual(len(w.aiClasses), 1)
        self.assertTrue(Game in w.games)
        self.assertTrue(AI in w.aiClasses)
        with self.assertRaises(IndexError):
            result = w.games[1]

    def testAddGames(self):
        w = Wrapper()
        a = [AI] * 2
        g = [Game] * 2
        w.addGames(g, a)
        self.assertEqual(w.numGames, 2)
        self.assertEqual(len(w.games), 2)
        self.assertEqual(len(w.aiClasses), 2)
        self.assertEqual(g, w.games)
        self.assertEqual(a, w.aiClasses)
        with self.assertRaises(IndexError):
            result = w.games[2]

    def testAddAI(self):
        w = Wrapper()
        class A(AI): supported_games = 'foo'
        class G(Game): Name = 'bar'
        w.addGame(G, AI)
        with self.assertRaises(GameDNEError):
            w.addAI(A)
        class A(AI): supported_games = 'bar'
        w.addAI(A)
        self.assertEqual(len(w.aiClasses), 1)

    def testGetGameClass(self):
        w = Wrapper()
        w.addGame(Game, AI)
        result = w.getGameClass(Game.Name)
        expected = Game
        self.assertEqual(result, expected)

    def testRemoveGame(self):
        w = Wrapper()
        w.addGame(Game)
        result = w.removeGame(Game)
        expected = 0
        self.assertEqual(result, expected)
        w.addGame(Game)
        result = w.removeGame(Game.Name)
        self.assertEqual(result, expected)

    def testLaunchGame(self):
        w = Wrapper()
        class G(Game):
            def __init__(self, A):
                Game.__init__(self, A, '')
        temp = AI.supported_games
        AI.supported_games = Game.Name
        w.addGame(G, AI)
        with self.assertRaises(ValueError):
            w.launchGame(Game.Name, 2, 0, [0])
        AI.supported_games = temp
        with self.assertRaises(GameDNEError):
            w.launchGame(Game.Name, 1, 1)

    def testReturnAIDescriptions(self):
        w = Wrapper()
        class A(AI): Description = 'foo'; supported_games = Game.Name
        class B(A): Description = 'bar'
        w.addGame(Game)
        w.addAI(A)
        w.addAI(B)
        w.returnAIDescriptions(Game.Name)

if __name__ == '__main__':
    unittest.main(exit=False)
