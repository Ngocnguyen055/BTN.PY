import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from sklearn.impute import SimpleImputer

# Đọc file
df = pd.read_csv("result.csv")

# Danh sách đầy đủ các chỉ số cần thiết
selected_columns = [
    'Name', 'Nation', 'Team', 'Position', 'Age',
    'MP', 'Starts', 'Minutes',
    'Goals', 'Assists', 'CrdY', 'CrdR',
    'xG', 'xAG',
    'PrgC', 'PrgP', 'PrgR',
    'Gls_per90', 'Ast_per90', 'xG_per90', 'xGA_per90',
    'GA90', 'Save%', 'CS%', 'PK_Save%',
    'SoT%', 'SoT/90', 'G/sh', 'Dist',
    'Cmp', 'Cmp%', 'TotDist', 'Cmp%_S', 'Cmp%_M', 'Cmp%_L', 'KP', 'Pass_1/3', 'PPA', 'CrsPA', 'Pass_PrgP',
    'SCA', 'SCA90', 'GCA', 'GCA90',
    'Tkl', 'TklW', 'Chal_Att', 'Chal_Lost', 'Blocks', 'Block_Sh', 'Block_Pass', 'Int',
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen', 'TO_Att', 'Succ%', 'Tkld%', 'Carries', 
    'Carry_ProDist', 'Carry_ProgC', 'Carry_1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'Rec_PrgR',
    'Fls', 'Fld', 'Off', 'Crs', 'Recov', 'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

# Chọn các cột số (loại bỏ các cột phân loại)
numeric_columns = [col for col in selected_columns if col not in ['Name', 'Nation', 'Team', 'Position']]
df_selected = df[numeric_columns].copy()

# Hàm xử lý các chuỗi dạng 'x-y' -> (x + y)/2 và chuyển đổi sang số
def parse_value(val):
    if pd.isna(val) or val == "N/a":
        return np.nan
    if isinstance(val, str):
        if "-" in val:
            parts = val.split("-")
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return np.nan
        try:
            return float(val)
        except:
            return np.nan
    return val

# Áp dụng xử lý từng giá trị
for col in numeric_columns:
    df_selected[col] = df_selected[col].apply(parse_value)

# Xử lý missing data: thay thế bằng giá trị trung bình của cột
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(df_selected)
df_imputed = pd.DataFrame(data_imputed, columns=numeric_columns)

# Chuẩn hóa dữ liệu
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df_imputed)

# Phân tích Elbow để tìm số cụm tối ưu
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(data_scaled)
    sse.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Sum of Squared Errors')
plt.grid(True)
plt.savefig("elbow_plot_full.png")
plt.show()

# Chọn k=5 dựa trên biểu đồ Elbow (có thể điều chỉnh)
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(data_scaled)

# PCA giảm chiều
pca = PCA(n_components=2)
components = pca.fit_transform(data_scaled)

# Tạo DataFrame kết quả
result_df = df[['Name', 'Position', 'Team']].copy()
result_df['Cluster'] = clusters
result_df['PCA1'] = components[:, 0]
result_df['PCA2'] = components[:, 1]

# Vẽ biểu đồ 2D với màu theo cụm và chú thích vị trí
plt.figure(figsize=(12, 8))
scatter = plt.scatter(result_df['PCA1'], result_df['PCA2'], c=result_df['Cluster'], cmap='viridis', alpha=0.6)

# Thêm chú thích cho một số cầu thủ tiêu biểu
for i, row in result_df.sample(20).iterrows():
    plt.annotate(row['Name'], (row['PCA1'], row['PCA2']), fontsize=8)

plt.colorbar(scatter, label='Cluster')
plt.title(f"K-Means Clustering of Players (k={optimal_k}) with PCA Reduction")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.grid(True)
plt.savefig("kmeans_clusters_full.png")
plt.show()

# Phân tích các cụm
cluster_stats = df_imputed.copy()
cluster_stats['Cluster'] = clusters

# Tính trung bình các chỉ số theo cụm
cluster_means = cluster_stats.groupby('Cluster').mean()
print("\nThống kê trung bình theo cụm:")
print(cluster_means)

# Lưu kết quả phân cụm
result_df.to_csv("player_clusters.csv", index=False)