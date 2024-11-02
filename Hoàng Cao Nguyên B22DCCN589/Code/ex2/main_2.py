import csv
import numpy
from prettytable import PrettyTable

#hàm tính median, mean và std từ danh sách cầu thủ
def calc(data):
    result = []
    for j in range(5, len(data[0])):
        row = []
        for i in range(len(data)):
            if data[i][j] != 'N/a': 
                row.append(float(data[i][j]))
        result.append(str(round(numpy.median(row), 4)))
        result.append(str(round(numpy.mean(row), 4)))
        result.append(str(round(numpy.std(row), 4)))
    return result


def main():
    #lấy dữ liệu
    with open('ex1/results.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        players = [row for row in csv_reader]
    data = players[1:]

    # Chỉ tính các chỉ số từ cột MP trở đi
    attributes = players[0][5:]
    table = []
    table_row = []

    #tạo headers
    table_row = ["", ""]
    for attr in attributes:
        table_row.append('Median of ' + attr)
        table_row.append('Mean of ' + attr)
        table_row.append('Std of ' + attr)
    table.append(table_row)
    

    #tính toàn giải
    table_row = [0, 'all']
    table_row.extend(calc(data=data))
    table.append(table_row)

    #tính cho từng đội
    squads = {} #chia các cầu thủ theo đội
    for row in data:
        squad_name = row[2] #lấy tên cầu thủ
        if squad_name not in squads:
            squads[squad_name] = [row]
        else:
            squads[squad_name].append(row)
        
    order = 1
    for key, value in squads.items():
        table_row = [order, key]
        table_row.extend(calc(data=value))
        table.append(table_row)
        order += 1

    #ghi kết quả ra file
    with open('ex2/results2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(table)
        print('SUCCESS: Tính toán thành công, kết quả lưu vào ' + file.name)


if __name__ == "__main__":
    main()





