import fpdf
from prettytable import PrettyTable
import csv


def main():
    #Phần 1:
    with open('ex1/results.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = [row for row in csv_reader]
        header = data[0]
        body = data[1:]

    # tạo table
    table = PrettyTable()
    table.field_names = ['Attribute', 'Top 3 max', 'Top 3 min']
    cols = len(header)
    for j in range(5, cols):
        valid = [row for row in body if row[j] != 'N/a']
        valid = sorted(valid, key=lambda x: float(x[j]))
        if len(valid) < 3:
            continue
        row = [
            header[j],
            f'{valid[-1][0]}({valid[-1][2]}),\n{valid[-2][0]}({valid[-2][2]}),\n{valid[-3][0]}({valid[-3][2]})',
            f'{valid[0][0]}({valid[0][2]}),\n{valid[1][0]}({valid[1][2]}),\n{valid[2][0]}({valid[2][2]})',
        ]
        table.add_row(row, divider=True)

    #print to PDF
    pdf = fpdf.FPDF(format='A4')
    pdf.add_page()

    pdf.add_font("Courier", "", "fonts/CourierPrime-Regular.ttf", uni=True)
    pdf.set_font("Courier", size=10)

    table.align = 'l'
    table.align['Attribute'] = 'c'
    table.max_width['Attribute'] = 10
    table.max_width['Top 3 max'] = 35
    table.max_width['Top 3 min'] = 35

    pdf.multi_cell(200, 6, txt="Top 3 max and top 3 min for each attribute:", align='c')
    pdf.multi_cell(200, 3, txt=table.get_string())
    pdf.output("ex2/top3.pdf")
    print("SUCCESS: Kết quả top 3 đã được lưu vào file ex2/top3.pdf")


if __name__ == "__main__":
    main()