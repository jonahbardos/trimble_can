PGN_OFFSET = 2
PGN_OFFSET_END = 6
SENT_BY_OFFSET = 6
DATA_LENGTH_OFFSET = 1
TRANS_OFFSET = 0
CAN_MSG = 0
DATABYTE_OFFSET = 1

PGN_SPEED_DIR       = "18FEE8AA"
PGN_SPEED_OFFSET    = 4
PGN_DIR_OFFSET      = 4
PGN_DIR_OFFSET_END  = 8

# RESOLUTIONS
VEHICLE_DIRECTION_RES = 1 / 128
VEHICLE_SPEED_RES     = 1 / 256

class FindSpeedDirInLog:
    def __init__(self, log) -> None:
        self.log = log
        self.total_found = 0
    
    def extract_log(self) -> None:
        file = open(self.log, "r+")
        
        for line in file:
            data = (line.strip().split())
            time_ = data[0]
            data2 = data[1]
            data_packet = data[2]
            self.find_speed_dir_data(data_packet)
        file.close()
    
    def find_speed_dir_data(self, data: str) -> str:
        data = data.replace("0x", "").split("#")
        
        if data[CAN_MSG] == PGN_SPEED_DIR:
            trans_rate = data[CAN_MSG][TRANS_OFFSET]
            data_length = data[CAN_MSG][DATA_LENGTH_OFFSET]
            pgn = data[CAN_MSG][PGN_OFFSET:PGN_OFFSET_END]
            data_bytes = data[DATABYTE_OFFSET]
            sender = data[CAN_MSG][SENT_BY_OFFSET:]
            self.total_found += 1
            print("Packet:",(trans_rate, data_length, pgn, sender, data_bytes))
            self.get_machine_direction(data_bytes)
            self.get_speed_direction(data_bytes)
            return data_bytes
    
    def get_machine_direction(self, data_bytes: str) -> float:
        dir_hex = data_bytes[PGN_DIR_OFFSET:PGN_DIR_OFFSET_END]
        val = self.convert_to_lil_endian(dir_hex)
        scale = VEHICLE_DIRECTION_RES
        offset = 0
        output = scale * val + offset
        print("Machine Direction in degrees", output)
        return output
    
    def get_speed_direction(self, data_bytes: str) -> float:
        speed_hex = data_bytes[:PGN_SPEED_OFFSET]
        val = self.convert_to_lil_endian(speed_hex)
        scale = VEHICLE_SPEED_RES
        offset = 0
        output = scale * val + offset
        print("Machine speed in km/h", output)
        return output
    
    def convert_to_lil_endian(self, val: str) -> int:
        little_hex = bytearray.fromhex(val)
        little_hex.reverse()
        str_little = ''.join(format(x, '02x') for x in little_hex)
        return int(str_little, 16)

    def get_total_found(self):
        return self.total_found
    

if __name__ == "__main__":
    # file_path = "test.log"
    file_path = "2020-12-03T22_30_35.121930_nav900.log"
    test = FindSpeedDirInLog(file_path)
    test.extract_log()
    print("Total logs found for Speed and Direction", test.total_found)