#############################
# Programmer: Kenneth Sinder
# Date: April 23, 2015
# Filename: dneerror.py
# Description: Game Does Not Exist Error class
#############################

class GameDNEError(Exception):
    """
    Exception that is thrown whenever a nonexistant
    game is trying to be launched or accessed.
    """
