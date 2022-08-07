"""Tasks.

Please only complete sections 3.1.2. Vehicle Speed and Direction
CAN Message in Python and C++

Parameter Group Number (PGN)
NOTE: Full packet ID looks like 0x18FEE8AA in the log.

Plan:
1. Extract every line in the log.
2. Find packet ID containig PGN for Vehicle Speed and Direction CAN MSG
3. Extract packet ID data
4. Extract data bytes
5. Grab Speed and Direction Bytes and change to little endian.
"""
import time
import json

CAN_MSG_OFFSET = 0
PGN_SPEED_DIR         = "18FEE8AA"
PGN_SPEED_OFFSET      = 4
PGN_DIR_OFFSET        = 4
PGN_SPEED_OFFSET_END  = 8
PGN_OFFSET            = 2
PGN_OFFSET_END        = 6
TRANS_OFFSET          = 0
DATA_LENGTH_OFFSET    = 1
SENT_BY_OFFSET        = 6
DATABYTE_OFFSET       = 1
EPOCH_TIME_OFFSET     = 0

DEBUG = True
# DEBUG = False
# DEBUG_LOGS = True
DEBUG_LOGS = False
# DEBUG_PACKET_ID = True
DEBUG_PACKET_ID = False
# DEBUG_DATA_BYTES = True
DEBUG_DATA_BYTES = False
# DEBUG_LITTLE_ENDIAN = True
DEBUG_LITTLE_ENDIAN = False

VEHICLE_DIRECTION_RES = 1 / 128
VEHICLE_SPEED_RES     = 1 / 256

class FindSpeedDirInLog:
    """Log class."""
    
    def __init__(self, log: str) -> None:
        """Use to find the Speed and Direction in log."""
        self.logs = {}
        self.log = log
        self.counter = 0
        self.total_found = 0
        self.max_speed = 0
        self.min_speed = 0
        self.max_direction = 0
        
    def store_log_spdDir(self) -> None:
        """Parse the log and stores in dictionary."""
        file = open(self.log, "r+")
        for line in file:
            data = (line.strip().split())
            time_epoch = data[0]
            bus_channel = data[1]
            data_packet = data[2]
            self.find_speed_dir_data_store(data_packet, data)
        file.close()
    
    def convert_epoch_time(self, epoch_data: str) -> str:
        """Convert epoch time to days and time."""
        datetime = time.localtime(float(epoch_data.replace('(', '')
                                            .replace(')', '')))
        new_time = time.strftime('%Y-%m-%d %H:%M:%S', datetime)
        print(new_time)
        return new_time
    
    def convert_to_lil_endian_hex(self, val: str) -> int:
        """Step 5: convert to little endian.
        
        Brief
        -----
        Converts hex string into little endian.
        """
        little_hex = bytearray.fromhex(val)
        little_hex.reverse()
        str_little = ''.join(format(x, '02x') for x in little_hex)
        if DEBUG_LITTLE_ENDIAN:
            print(f'''+++++++++++++++++++++++++++++++++++++++++++++++++++++
                  \rBytearray: {little_hex}
                  \rTwo Digit Format: {str_little}
                  \rDecimal: {int(str_little, 16)}
                  \r+++++++++++++++++++++++++++++++++++++++++++++++++++++\n''')
        return int(str_little, 16)

    def extract_log(self) -> None:
        """Step 1.
        
        Brief
        -----
        Extract log line by line.
        """
        file = open(self.log, "r+")

        for line in file:
            data = (line.strip().split())
            epoch_time = data[0]
            deviceId = data[1]
            can_msg = data[2]
            self.find_speed_dir_packetId(can_msg, data)

            if DEBUG_LOGS:
                print(epoch_time, deviceId, can_msg)

        file.close()
    
    def get_machine_speed(self, data_bytes: str) -> float:
        """Step 5.
        
        Brief
        -----
        Parses data byte and grab machine speed in 3rd and 4th byte.
        """
        speed_hex = data_bytes[PGN_SPEED_OFFSET:PGN_SPEED_OFFSET_END]
        val = self.convert_to_lil_endian_hex(speed_hex)
        offset = 0
        rpm = 0.125 * val + offset
        mm_tire = 0.250 # Assuming tire is 250 mm (SUV average)
        output = 0.1885 * rpm * mm_tire # Formula to convert to kmh
        self.min_speed = min(self.min_speed, output)
        self.max_speed = max(output, self.max_speed)
        print("Machine speed in km/h", output)
        return output
        
    def get_machine_direction(self, data_bytes: str) -> float:
        """Step 5.
        
        Brief
        -----
        Parses data byte and grab machine direction in 1st and 2nd byte.
        """
        dir_hex = data_bytes[:PGN_DIR_OFFSET]
        val = self.convert_to_lil_endian_hex(dir_hex)
        scale = VEHICLE_DIRECTION_RES
        offset = 0
        output = scale * val + offset
        self.max_direction = max(self.max_direction, output)
        print("Machine Direction in degrees", output)
        return output
    
    def get_data_bytes_data(self, data_bytes: str) -> None:
        """Step 4.
        
        Brief
        -----
        Parses the data bytes for PGN 0xFEE8.
        
        Notes
        -----
        Covnvert to little-endian.
            >>> BC653D00C762814D
                >>> BC65 -> 65BC Machine Heading in degrees.
                >>> 3D00 -> 003D Machine Speed in km/hr.
                >>> 762814D -> Reserved.
        """
        if DEBUG_DATA_BYTES:
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('DEBUG data btyes:', data_bytes)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        
    def get_packetId_data(self, packetId: str) -> None:
        """Step 3.
        
        Brief
        -----
        Parses the packet ID.
        
        Notes
        -----
        0x18FEE8AA
        """
        pgn = packetId[PGN_OFFSET:PGN_OFFSET_END]
        trans_rate = packetId[TRANS_OFFSET]
        data_length = packetId[DATA_LENGTH_OFFSET]
        sender = packetId[SENT_BY_OFFSET:]
        if DEBUG_PACKET_ID:
            print(f'''+++++++++++++++++++++++++++++++++++++++++++++++++++++
                  \rPGN: {pgn}
                  \rTransmission Rate: {trans_rate}
                  \rData Length: {data_length}
                  \rSender: {sender}
                  \r+++++++++++++++++++++++++++++++++++++++++++++++++++++\n''')

    def find_speed_dir_packetId(self, can_msg: str, full_data: str) -> None:
        """Step 2.
        
        Brief
        -----
        Find packet ID containing Vehicle speed and direction.
        
        Parameters
        ----------
        can_msg
            Data packet containing CAN message.
        full_data
            Data containing time, deviceId, and CAN message
        
        Note
        ----
        Full packet ID looks like 0x18FEE8AA in the log.
        """
        can_msg = can_msg.replace("0x", "").split("#")
        
        if can_msg[CAN_MSG_OFFSET] == PGN_SPEED_DIR:
            self.convert_epoch_time(full_data[EPOCH_TIME_OFFSET])
            self.get_packetId_data(can_msg[CAN_MSG_OFFSET])
            self.get_data_bytes_data(can_msg[DATABYTE_OFFSET])
            self.get_machine_direction(can_msg[DATABYTE_OFFSET])
            self.get_machine_speed(can_msg[DATABYTE_OFFSET])
            self.total_found += 1
    
    def find_speed_dir_data_store(self, data: str, full_data: str) -> None:
        """Store in a JSON structure."""
        data = data.replace("0x", "").split("#")
        if data[CAN_MSG_OFFSET] == PGN_SPEED_DIR:
            trans_rate = data[CAN_MSG_OFFSET][TRANS_OFFSET]
            data_length = data[CAN_MSG_OFFSET][DATA_LENGTH_OFFSET]
            pgn = data[CAN_MSG_OFFSET][PGN_OFFSET:PGN_OFFSET_END]
            data_bytes = data[DATABYTE_OFFSET]
            sender = data[CAN_MSG_OFFSET][SENT_BY_OFFSET:]
            datetime = time.localtime(float(full_data[0].replace('(', '')
                                            .replace(')', '')))
            self.logs[self.counter] = {
                "time_epoch": full_data[0],
                "datetime": time.strftime('%Y-%m-%d %H:%M:%S', datetime),
                "bus_channel": full_data[1],
                "data_packet": full_data[2],
                "trans_rate": trans_rate,
                "data_length": data_length,
                "pgn": pgn,
                "sender": sender,
                "data_bytes": data_bytes,
                "speedkm/h": self.get_machine_speed(data_bytes),
                "dirDegrees": self.get_machine_direction(data_bytes),
            } 
            self.counter += 1
    
    def get_total_found(self):
        """Total packet ID for Speed and Direction."""
        print("Total Packet ID found:", self.total_found)
        return self.total_found
    
    def get_max_speed(self):
        """Max speed of machine."""
        print("Max speed:", self.max_speed)
        return self.max_speed

    def get_min_speed(self):
        """Min speed of machine."""
        print("Min speed:", self.min_speed)
        return self.min_speed

    def get_max_direction(self):
        """Max direction of machine."""
        print("Max direction:", self.max_direction)
        return self.max_direction


if __name__ == "__main__":
    file_path = "test.log"
    file_path = "2020-12-03T22_30_35.121930_nav900.log"
    test = FindSpeedDirInLog(file_path)

    if DEBUG:
        test.extract_log()
        test.get_total_found()
        test.get_max_speed()
        test.get_min_speed()
        test.get_max_direction()
        
    """ Displays the found Speed and Direction logs JSON format"""
    # test.store_log_spdDir()
    # print(json.dumps(test.logs, indent=4))