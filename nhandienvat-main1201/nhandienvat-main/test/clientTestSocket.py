import socket
import numpy as np
import struct

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
host = '172.25.144.1'
port = 48951

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



server_address = (host, port)
c.connect(server_address)
data_to_send = b'8'
c.sendall(data_to_send)

    # Nhận dữ liệu từ server
# data_received = int.from_bytes(c.recv(24), byteorder='big')
# data_received = c.recv(1)

 # Nhận dữ liệu từ server
# data = c.recv(1)


received_array = []

while True:
        # Nhận dữ liệu từ server
        data = c.recv(4)

        if not data:
            break  # Kết thúc khi không còn dữ liệu

        # Chuyển đổi từ byte sang giá trị float
        received_element = struct.unpack('!f', data)[0]
        received_array.append(received_element)
        print(f"Phần tử nhận được từ server: {received_element}")

print(f"Mảng nhận được từ server: {received_array}")

c.close()