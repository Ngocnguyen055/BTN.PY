import pandas as pd
from collections import defaultdict

# Đọc dữ liệu từ file result.csv
try:
    df = pd.read_csv('result.csv')
    print("Đọc file thành công. Số lượng cầu thủ:", len(df))
except Exception as e:
    print(f"Lỗi khi đọc file: {e}")
    exit()

# Danh sách đầy đủ 75 chỉ số (ban đầu), bao gồm cả Age và Position
all_stats_raw = [
    'MP', 'Starts', 'Minutes', 'Age', 'Position',  # Thông tin cơ bản (5)
    'Goals', 'Assists', 'CrdY', 'CrdR',            # Hiệu suất (4)
    'xG', 'xAG',                                    # Dữ liệu kỳ vọng (2)
    'PrgC', 'PrgP', 'PrgR',                         # Chuyền phát triển (3)
    'Gls_per90', 'Ast_per90', 'xG_per90', 'xGA_per90', # Trung bình/90 (4)
    'GA90', 'Save%', 'CS%', 'PK_Save%',            # Thủ môn (4)
    'SoT%', 'SoT/90', 'G/sh', 'Dist',              # Sút bóng (4)
    'Cmp', 'Cmp%', 'TotDist',                      # Chuyền tổng thể (3)
    'Cmp%_S', 'Cmp%_M', 'Cmp%_L',                   # Chuyền theo khoảng cách (3)
    'KP', 'Pass_1/3', 'PPA', 'CrsPA', 'Pass_PrgP',  # Chuyền tấn công (5)
    'SCA', 'SCA90', 'GCA', 'GCA90',                 # Cơ hội tạo ra (4)
    'Tkl', 'TklW', 'Chal_Att', 'Chal_Lost',         # Phòng ngự cá nhân (4)
    'Blocks', 'Block_Sh', 'Block_Pass', 'Int',      # Phòng ngự tập thể (4)
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen',  # Kiểm soát vị trí (6)
    'TO_Att', 'Succ%', 'Tkld%',                     # Tranh chấp (3)
    'Carries', 'Carry_ProDist', 'Carry_ProgC', 'Carry_1/3', 'CPA',  # Dẫn bóng (5)
    'Mis', 'Dis',                                   # Mất bóng (2)
    'Rec', 'Rec_PrgR',                              # Nhận bóng (2)
    'Fls', 'Fld', 'Off', 'Crs', 'Recov',            # Chỉ số khác (5)
    'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'      # Không chiến (3)
]

# ❗ Lọc bỏ Age và Position để còn đúng 73 chỉ số thống kê chuyên môn
all_stats = [s for s in all_stats_raw if s not in ['Age', 'Position']]

# Phân nhóm chi tiết cho 73 chỉ số (giữ nguyên như bạn đã viết)
stat_groups = {
    'THỜI LƯỢNG THI ĐẤU': ['MP', 'Starts', 'Minutes'],
    'HIỆU SUẤT CƠ BẢN': ['Goals', 'Assists', 'CrdY', 'CrdR'],
    'CHỈ SỐ KỲ VỌNG': ['xG', 'xAG'],
    'PHÁT TRIỂN TẤN CÔNG': ['PrgC', 'PrgP', 'PrgR'],
    'CHỈ SỐ TRUNG BÌNH/90': ['Gls_per90', 'Ast_per90', 'xG_per90', 'xGA_per90'],
    'THỦ MÔN': ['GA90', 'Save%', 'CS%', 'PK_Save%'],
    'SÚT BÓNG': ['SoT%', 'SoT/90', 'G/sh', 'Dist'],
    'CHUYỀN BÓNG - TỔNG THỂ': ['Cmp', 'Cmp%', 'TotDist'],
    'CHUYỀN BÓNG - THEO KHOẢNG CÁCH': ['Cmp%_S', 'Cmp%_M', 'Cmp%_L'],
    'CHUYỀN BÓNG - TẤN CÔNG': ['KP', 'Pass_1/3', 'PPA', 'CrsPA', 'Pass_PrgP'],
    'TẠO CƠ HỘI': ['SCA', 'SCA90', 'GCA', 'GCA90'],
    'PHÒNG NGỰ - CÁ NHÂN': ['Tkl', 'TklW', 'Chal_Att', 'Chal_Lost'],
    'PHÒNG NGỰ - TẬP THỂ': ['Blocks', 'Block_Sh', 'Block_Pass', 'Int'],
    'KIỂM SOÁT BÓNG - VỊ TRÍ': ['Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen'],
    'KIỂM SOÁT BÓNG - DẪN BÓNG': ['Carries', 'Carry_ProDist', 'Carry_ProgC', 'Carry_1/3', 'CPA'],
    'KIỂM SOÁT BÓNG - TRANH CHẤP': ['TO_Att', 'Succ%', 'Tkld%'],
    'KIỂM SOÁT BÓNG - MẤT BÓNG': ['Mis', 'Dis'],
    'KIỂM SOÁT BÓNG - NHẬN BÓNG': ['Rec', 'Rec_PrgR'],
    'CHỈ SỐ KHÁC': ['Fls', 'Fld', 'Off', 'Crs', 'Recov'],
    'KHÔNG CHIẾN': ['Aerial_Won', 'Aerial_Lost', 'Aerial_Won%']
}

# Kiểm tra và lọc các chỉ số có trong dữ liệu
available_stats = []
stats_not_found = []

for stat in all_stats:
    if stat in df.columns:
        available_stats.append(stat)
    else:
        stats_not_found.append(stat)

print(f"\nTìm thấy {len(available_stats)}/{len(all_stats)} chỉ số trong dữ liệu")
if stats_not_found:
    print("\nCác chỉ số không có trong dữ liệu:")
    print(stats_not_found)

# Chuyển đổi dữ liệu sang số
for col in available_stats:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Hàm phân tích và xếp hạng
def analyze_stats(data, stats_list):
    results = {}
    for stat in stats_list:
        if stat in data.columns:
            try:
                if data[stat].notna().any():
                    max_val = data[stat].max()
                    top_team = data[data[stat] == max_val].iloc[0]['Team']
                    results[stat] = {'Team': top_team, 'Value': round(max_val, 2)}
            except Exception as e:
                print(f"Lỗi khi xử lý {stat}: {e}")
    return results

# Tính toán thống kê theo đội
team_stats = df.groupby('Team')[available_stats].mean().reset_index()

print("\nKẾT QUẢ PHÂN TÍCH THEO NHÓM:")
overall_ranking = defaultdict(int)

for group_name, stats in stat_groups.items():
    group_stats = [s for s in stats if s in available_stats]
    if not group_stats:
        continue
    
    group_results = analyze_stats(team_stats, group_stats)
    
    if group_results:
        print(f"\n{group_name}:")
        for stat, data in group_results.items():
            print(f"{stat:<15}: {data['Team']} ({data['Value']})")
            overall_ranking[data['Team']] += 1

# Phân tích tổng thể
if overall_ranking:
    sorted_teams = sorted(overall_ranking.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTỔNG HỢP SỐ LẦN ĐỨNG ĐẦU:")
    for rank, (team, count) in enumerate(sorted_teams, 1):
        print(f"{rank}. {team}: {count} chỉ số")
    
    best_team = sorted_teams[0][0]
    print(f"\nĐỘI XUẤT SẮC NHẤT: {best_team} (đứng đầu {sorted_teams[0][1]} chỉ số)")
else:
    print("\nKhông đủ dữ liệu để đánh giá tổng thể")

# Xuất kết quả ra file CSV
team_stats.to_csv('team_analysis_results.csv', index=False)
print("\nĐã lưu kết quả phân tích vào file 'team_analysis_results.csv'")
