import csv
import numpy as np
def extractCSV(csv_file_path,result,score):
    # result_csv = result + score
    # print("treasdfd: ",result)
    with open(csv_file_path, mode='w', newline='') as file:
        # Sử dụng DictWriter để ghi dữ liệu theo dạng từ điển
        csv_writer = csv.DictWriter(file, fieldnames=[ 'X', 'Y', 'Angle', 'Possible' ])
        
        # Viết tiêu đề cho các cột
        csv_writer.writeheader()
        writer = csv.writer(file)  
        # Ghi dữ liệu từ list dictionaries vào tệp CSV
        writer.writerows(result)
