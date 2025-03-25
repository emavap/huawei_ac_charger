import socket
import struct

def build_rtu_frame(unit_id, function_code, address, count):
    request = struct.pack(">B B H H", unit_id, function_code, address, count)
    crc = calc_crc(request)
    return request + struct.pack("<H", crc)

def build_write_frame(unit_id, function_code, address, value):
    request = struct.pack(">B B H H", unit_id, function_code, address, value)
    crc = calc_crc(request)
    return request + struct.pack("<H", crc)

def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def send_rtu_tcp(ip, port, frame):
    with socket.create_connection((ip, port), timeout=3) as s:
        s.sendall(frame)
        return s.recv(256)