###############################
# Programmer: Kenneth Sinder
# Date: June 4, 2015
# Filename: threads.py
# Description: Thread Subclasses
###############################
import socket
import threading

CONTINUE = ['CONTINUE']
EXIT = ['EXIT']


class AIThread(threading.Thread):

    def __init__(self, aiClass, responseQueue, stopCommand, initialGameState=None, gameState=None):
        """ (Class, queue.queue, list, [dict], [dict])
        Initializes an AI Thread. The parameters are: an appropriate
        AI Class, queue containing AI decisions/moves, a special
        list that contains one string - 'CONTINUE' or 'EXIT' thread.
        Then two dictionaries of game state information. The keys to the
        dictionaries should be strings but the values can be of
        any type. gameState should be updated frequently while
        initialGameState is not expected to be modified.
        """
        threading.Thread.__init__(self)
        self.aiClass = aiClass
        self.queue = responseQueue
        if initialGameState is None:
            initialGameState = {}
        if gameState is None:
            gameState = {}
        self.initialGameState = initialGameState
        self.state = gameState
        self.command = stopCommand

    def run(self):
        ai = self.aiClass(**self.initialGameState)
        while self.command == CONTINUE:
            updated = True
            try:
                ai.update(**self.state)
            except ValueError:
                # If the AI cannot be updated properly, then do not get a new move/operation
                updated = False
            if not self.queue.full() and updated:
                self.queue.put(ai.get_next_operation())

class GameServerThread(threading.Thread):

    def __init__(self, clientSendQueue, clientReceiveQueues, ip='127.0.0.1:3000'):
        threading.Thread.__init__(self)
        self.txQueue = clientSendQueue
        self.rxQueues = clientReceiveQueues
        self.host = ip[:ip.index(':')]      # Host is the portion up to the colon
        self.port = ip[ip.index(':')+1:]    # Port is the 4 digits after colon

    def run(self):
        bufferSize = 1024
        backlog = 1

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(backlog)

        conn, addr = sock.accept()

        while 1:
            data = conn.recv(bufferSize)
            print data
            if data == 'exit':
                break
