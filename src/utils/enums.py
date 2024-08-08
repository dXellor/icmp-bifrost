from enum import Enum, IntEnum

class ExitCodes(IntEnum):
    SUCCESS = 0
    INVALID_ARGUMENTS = 1
    IPTABLES_SETUP_ERROR = 2
    CANT_OPEN_SOCKET = 3

class Marks(IntEnum):
    TO_SERVER = 7130
    FROM_SERVER = 7131
    FROM_CLIENT = 7132
    TO_CLIENT = 7133

class Modes(Enum):
    CLIENT = 1,
    SERVER = 2