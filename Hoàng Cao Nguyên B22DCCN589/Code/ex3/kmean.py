import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np


def kmeans_display(X, label, centers, K):
    colors = ['ro', 'go', 'bo', 'co']
    
    for k in range(K):
        Xk = X[label == k, :]
        plt.plot(Xk[:, 0], Xk[:, 1], colors[k], markersize=4, alpha=0.8)
    
    plt.scatter(centers[:, 0], centers[:, 1], s=300, c='black', marker='x')
    plt.axis('equal')
    plt.title('KMeans Clustering')


def main():
    df = pandas.read_csv('ex1/results.csv', na_values='N/a')
    # Dựa trên elbow ta chọn K = 4
    K = 4
    #Chọn các cột bắt đầu từ 6 ->
    target_cols = df.columns[5:]

    # Chuẩn hóa dữ liệu để tất cả các chỉ số có cùng đơn vị
    X = df[target_cols]
    X.fillna(X.mean(), inplace=True)
    X_scaled = StandardScaler().fit_transform(X)

    # Hiển thị kết quả phân cụm khi chưa giảm chiều
    kmeans_1 = KMeans(n_clusters=K, random_state=0)
    kmeans_1.fit(X_scaled)
    label = kmeans_1.predict(X_scaled)
    kmeans_display(X_scaled, label, kmeans_1.cluster_centers_, K)
    plt.show()


if __name__ == "__main__":
    main()

#với k = 4 tương ứng với 4 vị trí chính trong tập cầu thủ là GK, FW, MF, DF, tập điểm ko phân cụm rõ ràng do
# có nhiều cầu thủ đảm nhiệm 2 vị trí
