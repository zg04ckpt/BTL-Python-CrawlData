from concurrent.futures import ThreadPoolExecutor
import csv
import threading
import time
import requests
from bs4 import BeautifulSoup

player_infos = [
    ['Player Name', 'Transfer price']
]

# khởi tạo danh sách player với các chỉ số cơ bản
def getData():
    print("INFO: Bắt đầu thu thập thông tin...")
    # Tính time chạy
    start_time = time.time()

    # link và dữ liệu paging
    url = 'https://www.footballtransfers.com/en/transfers/actions/confirmed/overview'
    form_data = {
        'orderBy': 'date_transfer',
        'orderByDescending': 1,
        'page': 1,
        'pages': 0,
        'pageItems': 500,
        'countryId': 'all',
        'season': 5847,
        'tournamentId': 31,
        'clubFromId': 'all',
        'clubToId': 'all',
        'transferFeeFrom': None,
        'transferFeeTo': None,
    }
    res = requests.post(url, data=form_data)

    if res.status_code == 200:
        json = res.json()

        for record in json['records']:
            player_info = []

            # Thêm tên, giá chuyển nhượng
            player_info.append(record['player_name'])
            player_info.append(record['price_tag']['price'])

            # Lưu dữ liệu
            player_infos.append(player_info)
            print(f'\r-> Đã khởi tạo {len(player_infos) - 1} cầu thủ!', end='')

        print(f'\nSUCCESS: Thời gian chạy: {time.time() - start_time}s')
    else:
        print(f'ERROR: Lỗi crawl player link ({res.status_code})')

def main():
    getData()

    # Ghi vào file csv
    with open('ex4/transfer_price.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(player_infos)
        print(f"SUCCESS: Dữ liệu đã ghi vào file: {file.name}")

if __name__ == "__main__":
    main()