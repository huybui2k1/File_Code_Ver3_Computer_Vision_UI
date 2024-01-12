# server.py
import socket
import numpy as np
import struct
import requests
import time
const_img = r"C:\Users\TKD01A-1\Desktop\Projects\final_img\XLA_IMAGE_01\XLA_IMAGE_01\31201927_12_25_16_46_57_498.jpg"
# 4
# "C:\Users\TKD01A-1\Desktop\Projects\final_img\XLA_IMAGE_01\XLA_IMAGE_01\31201927_12_25_16_46_57_498.jpg"
# 3
# "C:\Users\TKD01A-1\Desktop\Projects\final_img\XLA_IMAGE_01\XLA_IMAGE_01\31201927_12_25_16_48_14_626.jpg"
# 4
# "C:\Users\TKD01A-1\Desktop\Projects\final_img\XLA_IMAGE_01\XLA_IMAGE_01\31201927_12_25_16_46_57_498.jpg"
# 3
# "C:\Users\TKD01A-1\Desktop\Projects\final_img\XLA_IMAGE_01\XLA_IMAGE_01\31201927_12_25_16_48_14_626.jpg"
def init_socket():
    # Định nghĩa host và port mà server sẽ chạy và lắng nghe
    host = '172.27.32.1'
    # host = '172.24.160.1'
    port = 48951

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)  # Chỉ chấp nhận 1 kết nối đồng thời
    print("Server listening on port", port)
    return s



# def send_data_to_robot(data_arr):
#     # byte_value_length = struct.pack('!i', len(data_arr))
#     # print("value length: ",byte_value_length)
#     # conn.sendall(byte_value_length)
#     # print(f"Dữ liệu gui từ server: {byte_value_length}")
#     for object in data_arr:
#         for element in object:
#             print("data item: ",element)
#             byte_value = struct.pack('!f', element)
#             # conn.sendall(byte_value)
#             print(f"Dữ liệu gui từ server: {byte_value}")
#     print("done!!")

def send_data_to_robot(data_arr,conn):
    # byte_value_length = struct.pack('!i', len(data_arr))
    # print("value length: ",byte_value_length)
    # conn.sendall(byte_value_length)
    # print(f"Dữ liệu gui từ server: {byte_value_length}")
   
    byte_string=b""
    for object in data_arr:
        for element in object:
            if isinstance(element,int):
                print("data item: ",element)
                byte_item = struct.pack('!i', element)
                byte_string = byte_string + byte_item
                print(f"Dữ liệu : {byte_item}")
            if isinstance(element,float):
                print("data item: ",element)
                byte_item = struct.pack('!f', element)
                byte_string = byte_string + byte_item
                print(f"Dữ liệu : {byte_item}")
    print(f"Dữ liệu gui từ server: {byte_string}")
    
    conn.sendall(byte_string)
    print("done!!")
    

def send_simple_data_robot(conn):
    a=1
    byte_item = struct.pack("!i",a)
    print("byte_item",byte_item)
    conn.sendall(byte_item)
    print("send to serve: ",byte_item)

def send_four_data_robot(conn):
    t=2
    a=1.3
    b=2.1
    c=3.3
    d=4.4
    e=5.5
    f=6.6
    g=7.7
    h=8.8
    i=419.9
    # data = b""
    byte_item_T = struct.pack("!i",t)
    byte_item = struct.pack("!f",a)
    byte_item2 = struct.pack("!f",b)
    byte_item3 = struct.pack("!f",c)
    byte_item4 = struct.pack("!f",d)
    byte_item5 = struct.pack("!f",e)
    byte_item6 = struct.pack("!f",f)
    byte_item7 = struct.pack("!f",g)
    byte_item8 = struct.pack("!f",h)
    byte_item9 = struct.pack("!f",i)
    # data = byte_item_T + byte_item + byte_item2 + byte_item3 + byte_item4 + byte_item5 + byte_item6 + byte_item7 + byte_item8 + byte_item9
    data =  b'\x00\x00\x00\x03\x00\x00\x00\x08C\xe5:\x06B\xd3/l\xc2\xf2\x98\x8cC\xb5\xb54\xc2\t\xb8\xe7\xc2\xfd$\xd9C\xd1\xd2>A\xf9\xc1\xf3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    print("byte_item",byte_item_T)
    conn.sendall(data)
    print("send to serve: ",data)


def process_request(conn):
    print("process_request")
    api_url = "http://127.0.0.1:5000/cvu_process"
    form_data={
                    "imgLink" : const_img,
                    "templateLink" : r"C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\template.jpg",
                    "modelLink" : r"C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\runs_final\segment\train\weights\last.pt",
                    "pathSaveOutputImg" : "",
                    "csvLink" : "",
                    "outputImgLink" : "",
                    "min_modify" : "-10",
                    "max_modify" : "10",
                    "configScore" : "0.8",
                    "img_size" : "640",
                    "method" : "cv2.TM_CCORR_NORMED",
                    "server_ip" : ""
                }
    response = requests.post(api_url, data=form_data)
    if response.status_code == 200:
        print("respons and type: ", response.json(), type(response))
        data_arr = response.json()
        print("data: ",data_arr)
        send_data_to_robot(data_arr,conn)

# init_socket()




# try:
#     while True:
#         c, addr = s.accept()
#         print("Connected from", str(addr))

#         # # Server sử dụng kết nối để gửi dữ liệu tới client dưới dạng binary
#         # c.send(b"Hello, how are you")
#         while True:
#             # Nhận 1 byte dữ liệu từ client
#             data = c.recv(1)
#             # decode_data = struct.unpack('!f', data)[0]
#             decode_data = int.from_bytes(data, byteorder='little')
#             print(f"Received data: {decode_data}")
#             if decode_data == 1:
#                 # for i in range(len(data_arr)):
#                 #     data_arr[i] = data_arr[i] + 10
#                 # for element in data_arr:
                    
#                 #     print("hjkhjk: ",element)
#                 #     byte_value = struct.pack('!1f', element)
#                 #     c.sendall(byte_value)
#                 #     print(f"Dữ liệu gui từ server: {byte_value}")
#                 #     # ////////////////////////////////
#                 process_request()

try:
    
        s = init_socket()
        conn, addr = s.accept()
        print("Connected from", str(addr))
        print("loop")
        while True:
            data_receive = conn.recv(1)
            decode_data = int.from_bytes(data_receive, byteorder='little')
            if decode_data == 1:
                print(decode_data)
                # send_simple_data_robot(conn)
                send_four_data_robot(conn)
                # process_request(conn)
                decode_data = 0
                break
                
                
                

        # process_request()   
    
except Exception as e:
    print("Error:", str(e))

finally:
    print("")
    # s.close()
