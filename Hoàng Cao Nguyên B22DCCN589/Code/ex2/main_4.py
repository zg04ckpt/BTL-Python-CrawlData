
import fpdf
import pandas
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from prettytable import PrettyTable


def main():
    df = pandas.read_csv('ex1/results.csv', na_values='N/a')

    target_cols = df.columns[5:]
    squads = df.groupby('Squad')[target_cols].mean()

    # Dữ liệu để vẽ biểu đồ phân bố với những chỉ số tốt
    positive_attrs_max_squads = [] 

    #chuẩn bị ghi kết quả ra pdf
    table = PrettyTable()
    table.field_names = ['Attribute', 'Top squad']
    table.align = 'l'
    pdf = fpdf.FPDF(format='A4')
    pdf.add_page()
    pdf.add_font("Courier", "", "fonts/CourierPrime-Regular.ttf", uni=True)
    pdf.set_font("Courier", size=13)

    # Những chỉ số xấu
    negative_attrs = ['CrdY', 'CrdR', 'GA', 'GA90', 'Lost', 'Off', 'Mis', 'Err', 'Tkld%'] 

    for col in target_cols:
        # Tìm đội có chỉ số cao nhất trong cột chỉ số
        squad = squads[col].idxmax() 
        # Lưu những chỉ số tích cực
        if col not in negative_attrs:
            positive_attrs_max_squads.append(squad)
        # Cập nhật bảng kết quả
        table.add_row([col, squad])

    # ghi ra pdf bảng kết quả
    pdf.multi_cell(200, 6, txt="Top squads for each attribute:")
    pdf.multi_cell(200, 4, txt=table.get_string())
    pdf.output("ex2/top_squads.pdf")
    print("SUCCESS: Đã ghi kết quả ra ex2/top_squads.pdf")

    #Phân tích số lần đạt top -> đội phong độ tốt nhất
    plt.figure(figsize=(12, 6))
    plt.hist(positive_attrs_max_squads, bins=50, edgecolor='black', alpha=0.7)
    plt.title("Distribution of the number of times each team reaches the top positive attribute")
    plt.xlabel(f'Squad name')
    plt.ylabel('Number of times reaching the top')
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.grid(True)
    plt.show()

    #kết luận
    analyzed_result = pandas.Series(positive_attrs_max_squads).value_counts()
    print(f'-> Đội phong độ tốt nhất: {analyzed_result.idxmax()} ({analyzed_result.max()} lần đạt top)')


if __name__ == "__main__":
    main()
