import pandas
import matplotlib
import matplotlib.pyplot as plt
from sklearn.calibration import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# Dựa trên elbow ta chọn K = 4

def kmeans_display(X, label, centers, K):
    colors = ['ro', 'go', 'bo', 'co']
    for k in range(K):
        Xk = X[label == k, :]
        plt.plot(Xk[:, 0], Xk[:, 1], colors[k], markersize=4, alpha=0.8)
    plt.scatter(centers[:, 0], centers[:, 1], s=300, c='black', marker='x')
    plt.axis('equal')
    plt.title('KMeans Clustering')
    plt.show()


def main():
    df = pandas.read_csv('ex1/results.csv', na_values='N/a')
    K = 4
    #Chọn các cột bắt đầu từ 6 ->
    target_cols = df.columns[5:]

    # Chuẩn hóa dữ liệu để tất cả các chỉ số có cùng đơn vị
    X = df[target_cols]
    X.fillna(X.mean(), inplace=True)
    X_scaled = StandardScaler().fit_transform(X)

    # Áp dụng PCA để giảm chiều dữ liệu xuống 2 chiều
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Thực hiện phân cụm KMeans với K = 4 khi đã giảm chiều
    kmeans = KMeans(n_clusters=K, random_state=0)
    kmeans.fit(X_pca)
    pred_label = kmeans.predict(X_pca)
    kmeans_display(X_pca, pred_label, kmeans.cluster_centers_, K)


if __name__ == "__main__":
    main()

    
#với k = 4 tương ứng với 4 vị trí chính trong tập cầu thủ là GK, FW, MF, DF, tập điểm ko phân cụm rõ ràng do
# có nhiều cầu thủ đảm nhiệm 2 vị trí nên phân cụm không rõ ràng
