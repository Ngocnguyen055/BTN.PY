import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv', index_col=0)

# Chọn các cột số để phân tích (loại bỏ cột phân loại)
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

# Mở file để ghi kết quả
with open('top_3.txt', 'w', encoding='utf-8') as f:
    for col in numeric_cols:
        # Kiểm tra nếu cột có dữ liệu hợp lệ
        if df[col].notna().sum() < 3:
            continue
            
        # Ghi tiêu đề chỉ số
        f.write(f"\n=== Chỉ số: {col} ===\n")
        
        # 3 cầu thủ có điểm cao nhất
        top3 = df.nlargest(3, col)[['Name', 'Team', 'Position', col]]
        f.write("\nTop 3 cầu thủ cao nhất:\n")
        f.write(top3.to_string(index=False))
        
        # 3 cầu thủ có điểm thấp nhất
        bottom3 = df.nsmallest(3, col)[['Name', 'Team', 'Position', col]]
        f.write("\n\nTop 3 cầu thủ thấp nhất:\n")
        f.write(bottom3.to_string(index=False))
        
        f.write("\n" + "="*50 + "\n")

print("Đã lưu kết quả vào file 'top_3.txt'")