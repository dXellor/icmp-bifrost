import struct

class ICMPPacket():

    def __init__(self, source_address: str, destination_address: str):
        self.source_address = source_address
        self.destination_address = destination_address
        self.type = 8
        self.code = 0
        self.checksum = 0
        self.id = 0
        self.seq = 0
        self.payload = bytes()

    def __str__(self):
        pass

    def __calculate_checksum(self):
        pass

    def get_raw(self) -> bytes:
        self.seq = len( self.payload )
        return struct.pack(
            '!bbhhh',
            self.type,
            self.code,
            self.checksum,
            self.id,
            self.seq,
        ) + self.payload
        