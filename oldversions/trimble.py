PGN_OFFSET = 2
PGN_OFFSET_END = 6
SENT_BY_OFFSET = 6
DATA_LENGTH_OFFSET = 1
TRANS_OFFSET = 0
CAN_MSG = 0
DATABYTE_OFFSET = 1

PGN_SPEED_DIR = "18FEE8AA"
PGN_SPEED_OFFSET = 4
PGN_DIR_OFFSET = 4
PGN_DIR_OFFSET_END = 8

def convert_to_dec(data: tuple):
    strng = ""
    for item in data:
        item = "0x" + item
        strng += f'HEX {item} DEC:{int(item,16)}\n'
    print(strng)


def convert_to_lil_endian(val):
    little_hex = bytearray.fromhex(val)
    little_hex.reverse()
    # print("Byte array format:", little_hex)

    str_little = ''.join(format(x, '02x') for x in little_hex)
    print(str_little, int(str_little, 16))
    return int(str_little,16)


def get_machine_direction(val):
    scale = 1 / 128
    offset = 0
    output = scale * val + offset
    print("Machine Direction in degrees ", output)
    return output


def get_speed_direction(val):
    scale = 1 / 256
    offset = 0
    output = scale * val + offset
    print("Machine speed in km/h", output)
    return output


def grab_spd_dir(data_bytes):
    print(data_bytes)
    speed_hex = data_bytes[:PGN_SPEED_OFFSET]
    dir_hex = data_bytes[PGN_DIR_OFFSET:PGN_DIR_OFFSET_END]
    print(speed_hex, dir_hex)
    spd = convert_to_lil_endian(speed_hex)
    direction = convert_to_lil_endian(dir_hex)
    get_machine_direction(direction)
    get_speed_direction(spd)


def decode_can_message(can_msg: str):
    can_msg = can_msg.replace("0x", "").split("#")

    if can_msg[CAN_MSG] == PGN_SPEED_DIR:
        pgn = can_msg[CAN_MSG][PGN_OFFSET:PGN_OFFSET_END]
        data_bytes = can_msg[DATABYTE_OFFSET]
        trans_rate = can_msg[CAN_MSG][TRANS_OFFSET]
        data_length = can_msg[CAN_MSG][DATA_LENGTH_OFFSET]
        sender = can_msg[CAN_MSG][SENT_BY_OFFSET:]

        can_packet = (pgn, trans_rate, data_length, sender) 
        grab_spd_dir(data_bytes)

        return can_packet


def grab_data_log(file_path):
    file = open(file_path, "r+")
    for line in file:
        data = (line.strip().split())
        data1, data2, data3 = data[0], data[1], data[2]
        decode_can_message(data3)
    file.close()

if __name__ == "__main__":
    # file_path = input("Input filepath")
    file_path = "test.log"
    grab_data_log(file_path)