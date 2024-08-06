from enum import Enum

class ExitCodes(Enum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    UNRECOGNIZED_ARGUMENTS = 2
    CANT_OPEN_SOCKET = 3

class Marks(Enum):
    SENDING = 7130
    RECEIVING = 7131