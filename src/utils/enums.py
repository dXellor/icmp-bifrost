from enum import Enum, IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    IPTABLES_SETUP_ERROR = 2
    CANT_OPEN_SOCKET = 3

class Marks(IntEnum):
    SENDING = 7130
    RECEIVING = 7131

class Modes(Enum):
    CLIENT = 1,
    SERVER = 2