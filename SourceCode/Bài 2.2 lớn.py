import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv', index_col=0)

# Chọn các cột số để tính toán (loại bỏ cột phân loại như tên, vị trí, đội bóng)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Tạo DataFrame mới để lưu kết quả
results = pd.DataFrame()

# Tính toán cho tất cả cầu thủ
all_players_stats = {
    'Group': 'all',
    **{f'Median_{col}': df[col].median() for col in numeric_cols},
    **{f'Mean_{col}': df[col].mean() for col in numeric_cols},
    **{f'Std_{col}': df[col].std() for col in numeric_cols}
}
results = pd.DataFrame([all_players_stats])

# Tính toán cho từng đội bóng
teams = df['Team'].unique()
for team in teams:
    team_df = df[df['Team'] == team]
    team_stats = {
        'Group': team,
        **{f'Median_{col}': team_df[col].median() for col in numeric_cols},
        **{f'Mean_{col}': team_df[col].mean() for col in numeric_cols},
        **{f'Std_{col}': team_df[col].std() for col in numeric_cols}
    }
    results = pd.concat([results, pd.DataFrame([team_stats])], ignore_index=True)

# Sắp xếp lại cột để có định dạng: Median | Mean | Std cho từng thuộc tính
sorted_columns = []
for col in numeric_cols:
    sorted_columns.extend([f'Median_{col}', f'Mean_{col}', f'Std_{col}'])
    
results = results[['Group'] + sorted_columns]

# Lưu kết quả vào file CSV
results.to_csv('results2.csv', index_label='Index')

print("Đã tính toán và lưu kết quả vào file 'results2.csv'")
print(f"Các thuộc tính được tính toán: {numeric_cols}")