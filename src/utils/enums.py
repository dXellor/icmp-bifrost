from enum import Enum, IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    IPTABLES_SETUP_ERROR = 2
    CANT_OPEN_SOCKET = 3

class Marks(IntEnum):
    CLIENT_SENDING = 7130
    CLIENT_RECEIVING = 7131
    SERVER_SENDING = 7132
    SERVER_RECEIVING = 7133

class Modes(Enum):
    CLIENT = 1,
    SERVER = 2