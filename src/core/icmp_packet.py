import struct

class ICMPPacket():

    def __init__(self, destination_address: str):
        self.destination_address = destination_address
        self.type = 8
        self.code = 0
        self.checksum = 0
        self.id = 0
        self.seq = 0
        self.payload = bytes()

    def get_raw(self, calculate_checksum = True) -> bytes:
        if calculate_checksum:
            self.checksum = self.__calculate_checksum()
        return struct.pack(
            '!BBHHH',
            self.type,
            self.code,
            self.checksum,
            self.id,
            self.seq,
        ) + self.payload

    def __calculate_checksum(self):
        self.checksum = 0
        packet = self.get_raw( False )

        checksum_result = 0
        for i in range( 0, len( packet ), 2 ):
            checksum_result += ( packet[i] << 8 ) + ( struct.unpack( 'B', packet[i + 1:i + 2] )[0] if len( packet[i + 1:i + 2] ) else 0 )

        checksum_result = ( checksum_result >> 16 ) + ( checksum_result & 0xFFFF )
        checksum_result += ( checksum_result >> 16 )
        checksum_result = ~checksum_result & 0xFFFF
        return checksum_result
        