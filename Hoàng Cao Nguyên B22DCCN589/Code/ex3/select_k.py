import pandas
import matplotlib
import matplotlib.pyplot as plt
from sklearn.calibration import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np


# pip install scikit-learn
def main():
    df = pandas.read_csv('ex1/results.csv', na_values='N/a')
    target_cols = df.columns[5:]


    # Chuẩn hóa dữ liệu để tất cả các chỉ số có cùng đơn vị
    X = df[target_cols]
    X.fillna(X.mean(), inplace=True)
    X_scaled = StandardScaler().fit_transform(X)

    # Danh sách để lưu giá trị SSE =  tổng bình phương khoảng cách giữa các điểm và tâm cụm
    sse = []
    k_values = range(1, 16)
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        # SSE là thuộc tính inertia_ của KMeans trong sklearn
        sse.append(kmeans.inertia_)

    # Vẽ biểu đồ Elbow
    plt.figure(figsize=(12, 8))
    plt.plot(k_values, sse, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('SSE (Sum of Squared Errors)')
    plt.title('Elbow Method for Optimal k')
    plt.show()


if __name__ == "__main__":
    main()

# SSE đo lường khoảng cách giữa các điểm dữ liệu và tâm cụm, và giá trị SSE nhỏ hơn đồng nghĩa với cụm dữ liệu tốt hơn.
# Ban đầu, SSE giảm nhanh: Khi K tăng từ 1 đến 2, SSE giảm rất nhanh vì việc thêm cụm mới giúp chia nhỏ dữ liệu thành các nhóm gần hơn với tâm cụm.
# Tại K = 4, 5, sự giảm SSE chậm lại: Đây là điểm mà tốc độ giảm SSE không còn nhiều như trước. Lúc này, việc thêm cụm mới chỉ giúp giảm SSE rất ít, trong khi chi phí tính toán và độ phức tạp của mô hình tăng lên. Điểm này thường được coi là "điểm gấp" (elbow point), nơi mà ta đạt được sự cân bằng giữa số lượng cụm và sự cải thiện của SSE.
# Do đó, K = 4 hoặc 5 là lựa chọn tối ưu vì tại đó, sự cải thiện SSE không còn rõ rệt khi thêm cụm, và bạn đã đạt được mô hình cân đối giữa độ chính xác và sự đơn giản.
