import matplotlib
import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    matplotlib.use('Agg')
    df = pandas.read_csv('ex1/results.csv', na_values='N/a')
    
    # tính cho toàn giải
    with PdfPages("ex2/histograms/all.pdf") as pdf:
        
        for j in range(5, len(df.columns)):
            plt.figure(figsize=(8, 6))
            plt.hist(df.iloc[:, j].dropna(), bins=20, edgecolor='black', alpha=0.7)
            plt.title(df.columns[j])
            plt.xlabel(f'Giá trị')
            plt.ylabel('Tần xuất')
            plt.grid(True)
            pdf.savefig() 
            plt.close()
    print("SUCCESS: Đã vẽ xong cho toàn giải")

    # tính cho mỗi đội
    squads = df.groupby('Squad')
    for squad_name, squad_data in squads:
        with PdfPages(f'ex2/histograms/{squad_name}.pdf') as pdf:
            for j in range(5, len(squad_data.columns)):
                plt.figure(figsize=(8, 6))
                plt.hist(squad_data.iloc[:, j].dropna(), bins=20, edgecolor='black', alpha=0.7)
                plt.title(squad_data.columns[j])
                plt.xlabel(f'Giá trị')
                plt.ylabel('Tần xuất')
                plt.grid(True)
                pdf.savefig() 
                plt.close()
        print(f'SUCCESS: Đã vẽ xong cho đội {squad_name}');


if __name__ == "__main__":
    main()
    print("SUCCESS: Hoàn thành! Các biểu đồ lưu tại ex2/histograms")
