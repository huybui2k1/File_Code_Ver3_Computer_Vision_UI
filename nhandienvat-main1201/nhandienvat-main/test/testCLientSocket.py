import socket
import struct
# Khởi tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server
host = '192.168.100.60'
port = 48951

client_socket.connect((host, port))
print(f"Đã kết nối tới {host}:{port}")

# Gửi dữ liệu 1 byte đến server
# data = 1
number_to_send = 1
data = number_to_send.to_bytes(1, byteorder='big')
# client_socket.send(data)
client_socket.send(data)
print(f"Đã gửi dữ liệu: {number_to_send}, kich thuoc: {len(data)} byte")
received_array = []
while True:
    # Nhận dữ liệu từ server
    data = client_socket.recv(1024)
    if data is not None:
     data_receive = b''
     data_receive = data_receive + data
    #  received_number = int.from_bytes(data, byteorder='big')
    #  print('Dữ liệu nhận được từ server:', data_receive.decode('utf-8'))
     print('Dữ liệu nhận được từ server:', data)

     break

# print(f"Mảng nhận được từ server: {received_array}")
# Đóng kết nối
client_socket.close()
