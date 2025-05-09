import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import re

# Đọc dữ liệu
stats_df = pd.read_csv('result.csv')
transfer_df = pd.read_csv('transfer_value.csv')

# Chuyển giá trị 'Price' sang số (triệu € → số thực)
def extract_price(val):
    if isinstance(val, str):
        val = val.lower().replace(',', '').strip()
        match = re.search(r'([\d.]+)', val)
        if match:
            price = float(match.group(1))
            if 'm' in val:
                return price * 1_000_000
            elif 'k' in val:
                return price * 1_000
            else:
                return price
    return None

transfer_df['Price'] = transfer_df['Price'].apply(extract_price)

# Gộp dữ liệu theo tên cầu thủ
merged_df = pd.merge(stats_df, transfer_df, how='inner', left_on='Name', right_on='Player')

# Chọn các đặc trưng đầu vào
features = [
    'Age', 'Minutes', 'Goals', 'Assists', 'xG', 'xAG',
    'PrgC', 'PrgP', 'PrgR', 'Touches', 'Tkl', 'Int', 'SCA90', 'GCA90'
]
features = [f for f in features if f in merged_df.columns]

# Xử lý số có dấu phẩy thành float
for col in features:
    merged_df[col] = merged_df[col].astype(str).str.replace(',', '')
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

# Tạo X và y
X = merged_df[features].fillna(0)
y = merged_df['Price']

# Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Huấn luyện mô hình
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Dự đoán
y_pred = model.predict(X_test)

# Đánh giá
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:,.0f} €")
print(f"R² Score: {r2:.2f}")

# Hiển thị độ quan trọng của các đặc trưng
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop đặc trưng ảnh hưởng đến giá trị cầu thủ:")
print(importance_df.to_string(index=False))
