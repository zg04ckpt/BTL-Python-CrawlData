from math import pi
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import matplotlib
import argparse
import numpy as np
import pandas
import sys



def draw_radar_chart(p1_name, p2_name, attributes, df):
    labels = attributes
    num_variables = len(attributes)
    player1 = df.loc[df['Player'] == p1_name, attributes].astype(float).values.flatten()
    player2 = df.loc[df['Player'] == p2_name, attributes].astype(float).values.flatten()

    player1 = np.append(player1, player1[0])
    player2 = np.append(player2, player2[0])

    # Tính toán góc
    angles = [n / float(num_variables) * 2 * pi for n in range(num_variables)]
    angles = np.append(angles, angles[0])

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

    # Vẽ cho cầu thủ 1
    ax.plot(angles, player1, linewidth=1, linestyle='solid', label=p1_name)
    ax.fill(angles, player1, 'b', alpha=0.1)

    # Vẽ cho cầu thủ 2
    ax.plot(angles, player2, linewidth=1, linestyle='solid', label=p2_name)
    ax.fill(angles, player2, 'r', alpha=0.1)

    # Thêm nhãn cho các trục
    plt.xticks(angles[:-1], labels)

    # Đặt tiêu đề và chú thích
    plt.title(f'So sánh giữa {p1_name} và {p2_name}')
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.show()


def main():
    # Đọc dữ liệu nguồn 
    df = pandas.read_csv('ex1/results.csv')
    df.replace('N/a', 0, inplace=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', required=True)
    parser.add_argument('--p2', required=True)
    parser.add_argument('--Attribute', required=True)
    args = parser.parse_args()
    attributes = args.Attribute.split(',')
    validAttrs = df.columns[5:]

    # Check exist
    if args.p1 not in df['Player'].values:
        print("ERROR: Tên cầu thủ p1 không có trong danh sách")
        sys.exit(-1)
    
    if args.p2 not in df['Player'].values:
        print("ERROR: Tên cầu thủ p2 không có trong danh sách")
        sys.exit(-1)
    
    if not set(attributes).issubset(set(validAttrs)):
        print("ERROR: Tên thuộc tính hợp lệ bao gồm: " + ','.join(validAttrs))
        sys.exit(-1)
    
    draw_radar_chart(p1_name=args.p1, p2_name=args.p2, attributes=attributes, df=df)


if __name__ == '__main__':
    main()

# python radarChartPlot.py --p1 'Max Aarons' --p2 'Tosin Adarabioyo' --Attribute 'Mn/Sub,unSub,PPM,onG,onGA,onxG,onxGA,G-PK'