# server.py
import socket
import numpy as np
import struct
import requests
import time
import random

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
# host = '172.22.144.1'
host = '192.168.0.222'
port = 48951

headers = {"Content-Type": "application/json", "Authorization": "Bearer your_token"}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)  # Chỉ chấp nhận 1 kết nối đồng thời
print("Server listening on port", port)
# data_arr=[]




try:
    while True:
        c, addr = s.accept()
        print("Connected from", str(addr))

        # # Server sử dụng kết nối để gửi dữ liệu tới client dưới dạng binary
        # c.send(b"Hello, how are you")
        while True:
            # Nhận 1 byte dữ liệu từ client
            data = c.recv(1)
            # decode_data = struct.unpack('!f', data)[0]
            decode_data = int.from_bytes(data, byteorder='little')
            print(f"Received data: {decode_data}")
            if decode_data == 1:
                # a = random.randrange(1,5)
                a=3
                print("type: ",a)
                byte_value = struct.pack('!i', a)
                c.sendall(byte_value)
                print("send: ",byte_value)
                print("LENGTH: ",len(byte_value))
                break
                
except Exception as e:
    print("Error:", str(e))

finally:
    print("loi")
    s.close()
