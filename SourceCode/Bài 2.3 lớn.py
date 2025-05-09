import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 1. ĐỌC DỮ LIỆU
try:
    df = pd.read_csv('result.csv', index_col=0)
    print("✅ Đã đọc file dữ liệu thành công")
except Exception as e:
    print(f"❌ Lỗi khi đọc file: {e}")
    exit()

# 2. THIẾT LẬP CHỈ SỐ
CHI_SO = {
    'tancong': {
        'Goals': 'Bàn thắng',
        'Assists': 'Kiến tạo',
        'SCA': 'Tạo cơ hội dứt điểm'
    },
    'phongthu': {
        'TklW': 'Tắc bóng thành công', 
        'Block_Sh': 'Chặn cú sút',
        'Int': 'Cướp bóng'
    }
}

# 3. KIỂM TRA CỘT DỮ LIỆU
missing_cols = []
for group in CHI_SO.values():
    for col in group.keys():
        if col not in df.columns:
            missing_cols.append(col)

if missing_cols:
    print(f"❌ Thiếu các cột quan trọng: {missing_cols}")
    exit()

# 4. TẠO THƯ MỤC
output_dir = Path('ketqua_histogram')
(output_dir / 'toan_giai').mkdir(parents=True, exist_ok=True)
(output_dir / 'tung_doi').mkdir(exist_ok=True)

# 5. HÀM VẼ BIỂU ĐỒ
def ve_histogram(data, chi_so, ten_chi_so, loai, doi=None):
    plt.figure(figsize=(10, 6))
    
    # Lọc dữ liệu
    clean_data = data.replace([np.inf, -np.inf], np.nan).dropna()
    
    if len(clean_data) == 0:
        print(f"⚠️ Không có dữ liệu {chi_so} cho {doi if doi else 'toàn giải'}")
        plt.close()
        return
    
    # Thiết lập giao diện
    color = '#FF6B6B' if loai == 'phongthu' else '#4ECDC4'
    edge = '#C70039' if loai == 'phongthu' else '#008080'
    
    # Vẽ histogram
    plt.hist(clean_data, bins=12, color=color, edgecolor=edge, alpha=0.8)
    
    # Tính toán thống kê
    median = np.median(clean_data)
    mean = np.mean(clean_data)
    
    # Thêm đường tham chiếu
    plt.axvline(median, color='red', linestyle='--', label=f'Trung vị: {median:.1f}')
    plt.axvline(mean, color='blue', linestyle='--', label=f'Trung bình: {mean:.1f}')
    
    # Định dạng đẹp
    plt.title(f"{ten_chi_so} ({loai.upper()})\n{doi if doi else 'TOÀN GIẢI'}")
    plt.xlabel('Giá trị')
    plt.ylabel('Số cầu thủ')
    plt.legend()
    plt.grid(axis='y', alpha=0.2)
    
    # Lưu file
    filename = f"{loai}_{chi_so}.png"
    if doi:
        save_path = output_dir / 'tung_doi' / f"{doi.replace(' ', '_')}_{filename}"
    else:
        save_path = output_dir / 'toan_giai' / filename
    
    plt.savefig(save_path, bbox_inches='tight', dpi=120)
    plt.close()

# 6. VẼ BIỂU ĐỒ TOÀN GIẢI
print("\n📊 Đang tạo biểu đồ toàn giải...")
for loai, chi_so_dict in CHI_SO.items():
    for chi_so, ten_chi_so in chi_so_dict.items():
        ve_histogram(df[chi_so], chi_so, ten_chi_so, loai)

# 7. VẼ BIỂU ĐỒ TỪNG ĐỘI
print("\n🏟️ Đang tạo biểu đồ theo đội...")
for doi in df['Team'].unique():
    doi_data = df[df['Team'] == doi]
    
    for loai, chi_so_dict in CHI_SO.items():
        for chi_so, ten_chi_so in chi_so_dict.items():
            ve_histogram(doi_data[chi_so], chi_so, ten_chi_so, loai, doi)

# 8. BÁO CÁO KẾT QUẢ
print(f"""
🎉 HOÀN THÀNH! Đã tạo:
- 6 biểu đồ toàn giải trong: {output_dir / 'toan_giai'}
- {len(df['Team'].unique())} đội × 6 biểu đồ trong: {output_dir / 'tung_doi'}
Tổng cộng: {6 + 6*len(df['Team'].unique())} biểu đồ histogram
""")