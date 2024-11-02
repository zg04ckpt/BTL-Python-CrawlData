import csv
import sys
import requests
from bs4 import BeautifulSoup

# mảng 2 chiều lưu các dòng dữ liệu để in vào result.csv
# hàng 1 là tên cột
result = []

# Hàm kiểm tra null
def check(v):
    if v is None or str(v).strip() == '':
        return 'N/a'
    return v


#lấy các cầu thủ thi đấu hơn 90p
def get_data_playing_time():
    url = 'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_playing_time'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {header.get_text(): index for index, header in enumerate(rows[1].findAll('th'))}
        #khởi tạo cột cho mảng kết quả
        result.append(['Player', 'Nation', 'Squad', 'Pos', 'Age', 'MP', 'Starts', 'Min', 'Mn/Start', 
        'Compl', 'Subs', 'Mn/Sub', 'unSub', 'PPM', 'onG', 'onGA', 'onxG', 'onxGA'])

        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            # kiểm tra phút thi đấu:
            min = str(row_data[column_names['Min']]).replace(',', '')
            if min.strip() == '' or int(min) <= 90:
                continue

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []
            row_result.append(check(row_data[column_names['Player']]))
            row_result.append(check(row_data[column_names['Nation']]))
            row_result.append(check(row_data[column_names['Squad']]))
            row_result.append(check(row_data[column_names['Pos']]))
            row_result.append(check(row_data[column_names['Age']]))
            row_result.append(check(row_data[column_names['MP']]))
            row_result.append(check(row_data[column_names['Starts']]))
            row_result.append(check(min))
            row_result.append(check(row_data[column_names['Mn/Start']]))
            row_result.append(check(row_data[column_names['Compl']]))
            row_result.append(check(row_data[column_names['Subs']]))
            row_result.append(check(row_data[column_names['Mn/Sub']]))
            row_result.append(check(row_data[column_names['unSub']]))
            row_result.append(check(row_data[column_names['PPM']]))
            row_result.append(check(row_data[column_names['onG']]))
            row_result.append(check(row_data[column_names['onGA']]))
            row_result.append(check(row_data[column_names['onxG']]))
            row_result.append(check(row_data[column_names['onxGA']]))

            #thêm dòng kết quả
            result.append(row_result)

        print(f'SUCCESS: Đã khởi tạo {len(result) - 1} cầu thủ thỏa mãn (>90p) từ bảng Playing Time')
    else:
        print("ERROR:", "Lỗi request (playing time): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng tiêu chuẩn
def get_data_standard():
    url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_standard'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['G-PK', 'PK', 'Ast', 'CrdY', 'CrdR', 'xG', 'npxG', 'xAG', 'PrgC', 
        'PrgP', 'PrgR', 'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'])
        new_col_count = 21

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thừ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[column_names['G-PK']]))
            row_result.append(check(row_data[column_names['PK']]))
            row_result.append(check(row_data[column_names['Ast']]))
            row_result.append(check(row_data[column_names['CrdY']]))
            row_result.append(check(row_data[column_names['CrdR']]))
            row_result.append(check(row_data[column_names['xG']]))
            row_result.append(check(row_data[column_names['npxG']]))
            row_result.append(check(row_data[column_names['xAG']]))
            row_result.append(check(row_data[column_names['PrgC']]))
            row_result.append(check(row_data[column_names['PrgP']]))
            row_result.append(check(row_data[column_names['PrgR']]))

            #bị trùng tên cột nên dùng chỉ số
            row_result.append(check(row_data[26]))
            row_result.append(check(row_data[27]))
            row_result.append(check(row_data[28]))
            row_result.append(check(row_data[29]))
            row_result.append(check(row_data[30]))
            row_result.append(check(row_data[31]))
            row_result.append(check(row_data[32]))
            row_result.append(check(row_data[33]))
            row_result.append(check(row_data[34]))
            row_result.append(check(row_data[35]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (standard)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Standard')
    else:
        print("ERROR:", "Lỗi request (standard): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng thủ môn
def get_data_goalkeeping():
    url = 'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_keeper'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv', 'PKm', 'Save%'])
        new_col_count = 15

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[column_names['GA']]))
            row_result.append(check(row_data[column_names['GA90']]))
            row_result.append(check(row_data[column_names['SoTA']]))
            row_result.append(check(row_data[column_names['Saves']]))
            row_result.append(check(row_data[column_names['Save%']]))
            row_result.append(check(row_data[column_names['W']]))
            row_result.append(check(row_data[column_names['D']]))
            row_result.append(check(row_data[column_names['L']]))
            row_result.append(check(row_data[column_names['CS']]))
            row_result.append(check(row_data[column_names['CS%']]))
            row_result.append(check(row_data[column_names['PKatt']]))
            row_result.append(check(row_data[column_names['PKA']]))
            row_result.append(check(row_data[column_names['PKsv']]))
            row_result.append(check(row_data[column_names['PKm']]))

            #bị trùng tên cột nên dùng chỉ số
            row_result.append(check(row_data[25]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (goalkeeping)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} thủ môn từ bảng Goalkeeping')
    else:
        print("ERROR:", "Lỗi request (goalkeeping): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Shooting
def get_data_shooting():
    url = 'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_shooting'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Gls', 'Sh', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'Dist', 'FK', 'PK', 'PKatt', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG'])
        new_col_count = 17

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[column_names['Gls']]))
            row_result.append(check(row_data[column_names['Sh']]))
            row_result.append(check(row_data[column_names['SoT']]))
            row_result.append(check(row_data[column_names['SoT%']]))
            row_result.append(check(row_data[column_names['Sh/90']]))
            row_result.append(check(row_data[column_names['SoT/90']]))
            row_result.append(check(row_data[column_names['G/Sh']]))
            row_result.append(check(row_data[column_names['G/SoT']]))
            row_result.append(check(row_data[column_names['Dist']]))
            row_result.append(check(row_data[column_names['FK']]))
            row_result.append(check(row_data[column_names['PK']]))
            row_result.append(check(row_data[column_names['PKatt']]))
            row_result.append(check(row_data[column_names['xG']]))
            row_result.append(check(row_data[column_names['npxG']]))
            row_result.append(check(row_data[column_names['npxG/Sh']]))
            row_result.append(check(row_data[column_names['G-xG']]))
            row_result.append(check(row_data[column_names['np:G-xG']]))


            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team}, (Shooting)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Shooting')
    else:
        print("ERROR:", "Lỗi request (Shooting): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Passing
def get_data_passing():
    url = 'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_passing'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist', 'Cmp', 'Att', 'Cmp%', 'Cmp', 'Att', 'Cmp%', 'Cmp', 'Att', 'Cmp%', 'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP'])
        new_col_count = 23

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[8]))
            row_result.append(check(row_data[9]))
            row_result.append(check(row_data[10]))
            row_result.append(check(row_data[11]))
            row_result.append(check(row_data[12]))
            row_result.append(check(row_data[13]))
            row_result.append(check(row_data[14]))
            row_result.append(check(row_data[15]))
            row_result.append(check(row_data[16]))
            row_result.append(check(row_data[17]))
            row_result.append(check(row_data[18]))
            row_result.append(check(row_data[19]))
            row_result.append(check(row_data[20]))
            row_result.append(check(row_data[21]))
            row_result.append(check(row_data[22]))
            row_result.append(check(row_data[23]))
            row_result.append(check(row_data[24]))
            row_result.append(check(row_data[25]))
            row_result.append(check(row_data[26]))
            row_result.append(check(row_data[27]))
            row_result.append(check(row_data[28]))
            row_result.append(check(row_data[29]))
            row_result.append(check(row_data[30]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Passing)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Passing')
    else:
        print("ERROR:", "Lỗi request (Passing): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Pass Types
def get_data_pass_types():
    url = 'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_passing_types'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Live', 'Dead', 'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 'In', 'Out', 'Str', 'Cmp', 'Off', 'Blocks'])
        new_col_count = 14

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[9]))
            row_result.append(check(row_data[10]))
            row_result.append(check(row_data[11]))
            row_result.append(check(row_data[12]))
            row_result.append(check(row_data[13]))
            row_result.append(check(row_data[14]))
            row_result.append(check(row_data[15]))
            row_result.append(check(row_data[16]))
            row_result.append(check(row_data[17]))
            row_result.append(check(row_data[18]))
            row_result.append(check(row_data[19]))
            row_result.append(check(row_data[20]))
            row_result.append(check(row_data[21]))
            row_result.append(check(row_data[22]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Pass Types)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Pass Types')
    else:
        print("ERROR:", "Lỗi request (Pass Types): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Goal and Shot Creation
def get_data_goal_and_shot_creation():
    url = 'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_gca'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['SCA', 'SCA90', 'PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def', 'GCA', 'GCA90', 'PassLive', 'PassDead', 'TO', 'Sh', 'Fld', 'Def'])
        new_col_count = 16

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[8]))
            row_result.append(check(row_data[9]))
            row_result.append(check(row_data[10]))
            row_result.append(check(row_data[11]))
            row_result.append(check(row_data[12]))
            row_result.append(check(row_data[13]))
            row_result.append(check(row_data[14]))
            row_result.append(check(row_data[15]))
            row_result.append(check(row_data[16]))
            row_result.append(check(row_data[17]))
            row_result.append(check(row_data[18]))
            row_result.append(check(row_data[19]))
            row_result.append(check(row_data[20]))
            row_result.append(check(row_data[21]))
            row_result.append(check(row_data[22]))
            row_result.append(check(row_data[23]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Goal and Shot Creation)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Goal and Shot Creation')
    else:
        print("ERROR:", "Lỗi request (Goal and Shot Creation): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Defensive Actions
def get_data_defensive_actions():
    url = 'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_defense'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Tkl', 'TklW', 'TklW', 'Mid 3rd', 'Att 3rd', 'Tkl', 'Att', 'Tkl%', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int', 'Tkl + Int', 'Clr', 'Err'])
        new_col_count = 16

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[8]))
            row_result.append(check(row_data[9]))
            row_result.append(check(row_data[10]))
            row_result.append(check(row_data[11]))
            row_result.append(check(row_data[12]))
            row_result.append(check(row_data[13]))
            row_result.append(check(row_data[14]))
            row_result.append(check(row_data[15]))
            row_result.append(check(row_data[16]))
            row_result.append(check(row_data[17]))
            row_result.append(check(row_data[18]))
            row_result.append(check(row_data[19]))
            row_result.append(check(row_data[20]))
            row_result.append(check(row_data[21]))
            row_result.append(check(row_data[22]))
            row_result.append(check(row_data[23]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Defensive Actions)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Defensive Actions')
    else:
        print("ERROR:", "Lỗi request (Defensive Actions): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng Possession
def get_data_possession():
    url = 'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_possession'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Live', 'Att', 'Succ', 'Succ%', 'Tkld', 'Tkld%', 'Carries', 'TotDist', 'ProDist', 'ProgC', '1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'PrgR'])
        new_col_count = 22

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[8]))
            row_result.append(check(row_data[9]))
            row_result.append(check(row_data[10]))
            row_result.append(check(row_data[11]))
            row_result.append(check(row_data[12]))
            row_result.append(check(row_data[13]))
            row_result.append(check(row_data[14]))
            row_result.append(check(row_data[15]))
            row_result.append(check(row_data[16]))
            row_result.append(check(row_data[17]))
            row_result.append(check(row_data[18]))
            row_result.append(check(row_data[19]))
            row_result.append(check(row_data[20]))
            row_result.append(check(row_data[21]))
            row_result.append(check(row_data[22]))
            row_result.append(check(row_data[23]))
            row_result.append(check(row_data[24]))
            row_result.append(check(row_data[25]))
            row_result.append(check(row_data[26]))
            row_result.append(check(row_data[27]))
            row_result.append(check(row_data[28]))
            row_result.append(check(row_data[29]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Possession)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Possession')
    else:
        print("ERROR:", "Lỗi request (Possession): " + str(response.status_code))
        sys.exit(1)


#lấy dữ liệu từ bảng  Miscellaneous Stats
def get_data_miscellaneous_stats():
    url = 'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table_container = soup.find('div', attrs={'id': 'all_stats_misc'})
        #xử lý dữ liệu trong comment
        s = str(table_container).find('<table')
        e = str(table_container).find('</table>')
        table_str = str(table_container)[s:e] + '</table>'
        table = BeautifulSoup(table_str, 'html.parser')


        #lấy tất cả các dòng
        rows = table.findAll('tr')
        #map tên các cột để lấy vị trí (trong dòng thứ 2)
        column_names = {}
        for index, header in enumerate(rows[1].findAll('th')):
            name = header.get_text()
            if name not in column_names:
                column_names[name] = index

        #Thêm cột cho mảng kết quả
        result[0].extend(['Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov', 'Won', 'Lost', 'Won%'])
        new_col_count = 9

        #map lưu các dòng dữ liệu lấy được
        row_results = {}

        #lấy dữ liệu
        for i in range(2, len(rows)):
            #lấy cột đầu tiên trong th
            row_data = [rows[i].find('th').get_text()]
            #từ cột thứ 2 lấy trong td
            row_data += [col.get_text() for col in rows[i].findAll('td')]

            #bỏ qua hàng tiêu đề
            if len(row_data) == 1:
                continue

            #xác định dữ liệu thuộc về cầu thủ nào (bằng tên và tên đội)
            name = row_data[column_names['Player']]
            team = row_data[column_names['Squad']]
            key = f'{name}_{team}'

            #dòng kết quả phân tích 1 cầu thủ
            row_result = []

            row_result.append(check(row_data[column_names['Fls']]))
            row_result.append(check(row_data[column_names['Fld']]))
            row_result.append(check(row_data[column_names['Off']]))
            row_result.append(check(row_data[column_names['Crs']]))
            row_result.append(check(row_data[column_names['OG']]))
            row_result.append(check(row_data[column_names['Recov']]))
            row_result.append(check(row_data[column_names['Won']]))
            row_result.append(check(row_data[column_names['Lost']]))
            row_result.append(check(row_data[column_names['Won%']]))

            #thêm dòng kết quả vào map
            if key not in row_results:
                row_results[key] = row_result
            else:
                print(f"ERROR: Trùng dòng {i}, name={name}, team={team} (Miscellaneous Stats)")

        #thêm dữ liệu vào result
        count = 0
        for i in range(1, len(result)):
            row = result[i]
            key = f'{row[0]}_{row[2]}'
            if key in row_results:
                count += 1
                row.extend(row_results[key])
            else:
                row.extend(['N/a'] * new_col_count)

        #log
        print(f'SUCCESS: Thành công cập nhật {count} cầu thủ từ bảng Miscellaneous Stats')
    else:
        print("ERROR:", "Lỗi request (Miscellaneous Stats): " + str(response.status_code))
        sys.exit(1)


# Main
def main():
    global result
    get_data_playing_time()
    get_data_standard()
    get_data_goalkeeping()
    get_data_shooting()
    get_data_passing()
    get_data_pass_types()
    get_data_goal_and_shot_creation()
    get_data_defensive_actions()
    get_data_possession()
    get_data_miscellaneous_stats()

    # Sắp xếp
    header = result[:1]
    body = result[1:]
    body = sorted(body, key=lambda x: (str(x[0]).split()[-1], x[4]))
    print(f"SUCCESS: Đã sắp xếp")
    result = header + body


    # Mở file csv để ghi
    with open('ex1/results.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(result)
        print(f"SUCCESS: Dữ liệu đã ghi vào file: {file.name}")


if __name__ == "__main__":
    main()