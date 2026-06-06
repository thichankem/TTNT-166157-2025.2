# -*- coding: utf-8 -*-
"""Sinh bo du lieu tieng Viet LON: ~400 benh, ~120 trieu chung, ~5000 dong.

Cach lam: moi benh = (loai benh ly) + (co quan). Trieu chung suy ra tu nhom co quan
cong them dac trung cua loai benh ly. Co bien thien & nhieu de tranh qua khop.
"""
import csv, os, random

random.seed(42)
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "01_data")
os.makedirs(DATA, exist_ok=True)

# ───────────────────────────────────────────────────────────────────────────
# 1) Trieu chung dac trung theo NHOM CO QUAN
# ───────────────────────────────────────────────────────────────────────────
CAT_SYMS = {
    "ho_hap":      ["ho", "khó thở", "đau ngực", "ho có đờm", "thở khò khè"],
    "tieu_hoa_tren":["đau thượng vị", "ợ chua", "buồn nôn", "đầy hơi", "chán ăn"],
    "tieu_hoa_duoi":["đau bụng", "tiêu chảy", "táo bón", "đầy hơi", "đi ngoài ra máu"],
    "gan_mat":     ["vàng da", "đau hạ sườn phải", "buồn nôn", "chán ăn", "mệt mỏi"],
    "tiet_nieu":   ["tiểu buốt", "tiểu rắt", "đau lưng", "tiểu ra máu", "tiểu nhiều lần"],
    "sinh_duc":    ["đau bụng dưới", "ra khí hư", "rối loạn kinh nguyệt", "đau khi quan hệ"],
    "tim_mach":    ["đau ngực", "khó thở", "hồi hộp", "phù chân", "mệt mỏi"],
    "co_xuong_khop":["đau khớp", "sưng khớp", "cứng khớp", "hạn chế vận động", "đau xương"],
    "da":          ["ngứa", "phát ban", "da đỏ", "mụn nước", "bong tróc da"],
    "tai_mui_hong":["đau họng", "nghẹt mũi", "ho", "đau tai", "khàn tiếng"],
    "mat":         ["mắt đỏ", "mờ mắt", "chảy nước mắt", "cộm mắt", "đau mắt"],
    "than_kinh":   ["đau đầu", "chóng mặt", "tê tay chân", "co giật", "yếu liệt tay chân"],
    "noi_tiet":    ["mệt mỏi", "sụt cân", "hồi hộp", "run tay", "sạm da"],
    "mau_hach":    ["mệt mỏi", "da xanh xao", "sưng hạch", "bầm tím", "chảy máu cam"],
    "rang_ham_mat":["đau răng", "sưng lợi", "chảy máu chân răng", "hôi miệng"],
}

# Co quan: (ten dung trong ten benh, nhom)
ORGANS = [
    # ho hap
    ("phổi","ho_hap"),("phế quản","ho_hap"),("tiểu phế quản","ho_hap"),("màng phổi","ho_hap"),
    ("khí quản","ho_hap"),("thanh quản","ho_hap"),("trung thất","ho_hap"),
    # tieu hoa tren
    ("dạ dày","tieu_hoa_tren"),("thực quản","tieu_hoa_tren"),("tá tràng","tieu_hoa_tren"),("tâm vị","tieu_hoa_tren"),
    # tieu hoa duoi
    ("đại tràng","tieu_hoa_duoi"),("ruột non","tieu_hoa_duoi"),("ruột thừa","tieu_hoa_duoi"),
    ("trực tràng","tieu_hoa_duoi"),("manh tràng","tieu_hoa_duoi"),("hồi tràng","tieu_hoa_duoi"),("hậu môn","tieu_hoa_duoi"),
    # gan mat tuy
    ("gan","gan_mat"),("túi mật","gan_mat"),("đường mật","gan_mat"),("tụy","gan_mat"),("lách","gan_mat"),
    # tiet nieu
    ("thận","tiet_nieu"),("bàng quang","tiet_nieu"),("niệu quản","tiet_nieu"),("niệu đạo","tiet_nieu"),("bể thận","tiet_nieu"),
    # sinh duc
    ("tử cung","sinh_duc"),("buồng trứng","sinh_duc"),("vòi trứng","sinh_duc"),("cổ tử cung","sinh_duc"),
    ("âm đạo","sinh_duc"),("tuyến tiền liệt","sinh_duc"),("tinh hoàn","sinh_duc"),("mào tinh hoàn","sinh_duc"),
    # tim mach
    ("cơ tim","tim_mach"),("màng ngoài tim","tim_mach"),("nội tâm mạc","tim_mach"),("van tim","tim_mach"),("động mạch chủ","tim_mach"),
    # co xuong khop
    ("khớp gối","co_xuong_khop"),("khớp háng","co_xuong_khop"),("khớp vai","co_xuong_khop"),
    ("cột sống","co_xuong_khop"),("cột sống cổ","co_xuong_khop"),("gân gót","co_xuong_khop"),
    ("bao hoạt dịch","co_xuong_khop"),("sụn khớp","co_xuong_khop"),
    # da
    ("da","da"),("nang lông","da"),("tuyến bã","da"),("móng","da"),
    # tai mui hong
    ("họng","tai_mui_hong"),("amidan","tai_mui_hong"),("xoang","tai_mui_hong"),("tai giữa","tai_mui_hong"),
    ("tai ngoài","tai_mui_hong"),("vòm họng","tai_mui_hong"),("dây thanh","tai_mui_hong"),
    # mat
    ("kết mạc","mat"),("giác mạc","mat"),("mống mắt","mat"),("võng mạc","mat"),("tuyến lệ","mat"),("bờ mi","mat"),
    # than kinh
    ("màng não","than_kinh"),("dây thần kinh","than_kinh"),("tủy sống","than_kinh"),("não","than_kinh"),
    # noi tiet
    ("tuyến giáp","noi_tiet"),("tuyến thượng thận","noi_tiet"),("tuyến yên","noi_tiet"),("tuyến cận giáp","noi_tiet"),
    # mau hach
    ("hạch","mau_hach"),("tủy xương","mau_hach"),
    # rang ham mat
    ("lợi","rang_ham_mat"),("tủy răng","rang_ham_mat"),("tuyến nước bọt","rang_ham_mat"),
]

# Loai benh ly ap dung cho tung nhom (de ten benh hop ly)
CAT_PREFIXES = {
    "ho_hap":      ["Viêm", "Ung thư", "Áp xe"],
    "tieu_hoa_tren":["Viêm", "Ung thư", "Loét", "Polyp"],
    "tieu_hoa_duoi":["Viêm", "Ung thư", "Polyp", "Nhiễm trùng"],
    "gan_mat":     ["Viêm", "Ung thư", "Áp xe", "U lành tính"],
    "tiet_nieu":   ["Viêm", "Ung thư", "Sỏi", "Nhiễm trùng"],
    "sinh_duc":    ["Viêm", "Ung thư", "U lành tính", "Nhiễm trùng"],
    "tim_mach":    ["Viêm", "Hẹp", "Phình"],
    "co_xuong_khop":["Viêm", "Thoái hóa", "Lao"],
    "da":          ["Viêm", "Ung thư", "Nhiễm trùng", "U lành tính"],
    "tai_mui_hong":["Viêm", "Ung thư", "U lành tính"],
    "mat":         ["Viêm", "U lành tính"],
    "than_kinh":   ["Viêm", "Ung thư", "U lành tính"],
    "noi_tiet":    ["Viêm", "Ung thư", "Suy", "Cường"],
    "mau_hach":    ["Viêm", "Ung thư", "Lao"],
    "rang_ham_mat":["Viêm", "Áp xe", "U lành tính"],
}

# Trieu chung them theo loai benh ly: (them vao core, them vao optional)
# Cac dac trung nay giup PHAN BIET cac benh cung co quan.
PREFIX_RULES = {
    "Viêm":         (["sốt"],                       ["đau"]),
    "Ung thư":      (["sụt cân", "mệt mỏi"],        ["chán ăn", "đau"]),
    "Áp xe":        (["sốt cao", "sưng"],           ["đau", "ớn lạnh"]),
    "U lành tính":  ([],                            ["đau"]),
    "Nhiễm trùng":  (["sốt", "ớn lạnh"],            ["mệt mỏi"]),
    "Loét":         (["nôn ra máu"],                ["đau"]),
    "Polyp":        (["đi ngoài ra máu"],           []),
    "Sỏi":          (["đau quặn thận"],             ["tiểu ra máu"]),
    "Thoái hóa":    (["hạn chế vận động"],          ["cứng khớp"]),
    "Lao":          (["sụt cân", "đổ mồ hôi đêm"],  ["sốt nhẹ"]),
    "Suy":          (["mệt mỏi", "phù chân"],       []),
    "Cường":        (["hồi hộp", "run tay"],        ["sụt cân"]),
    "Hẹp":          (["khó thở"],                   ["mệt mỏi"]),
    "Phình":        (["đau ngực"],                  ["khó thở"]),
}

# Cac nhom dung them bien the cap / man de tang so luong benh (du de cat con 400)
CAP_MAN_CATS = set(CAT_SYMS.keys())


def derive(name, base_syms, prefix, suffix=""):
    """Tao (core, optional) cho mot benh tu trieu chung nhom + loai benh ly."""
    rnd = random.Random(abs(hash(name)) % (2**32))
    base = list(dict.fromkeys(base_syms))
    rnd.shuffle(base)
    k = min(len(base), 3)
    n_core = max(2, k - 1)
    core = base[:n_core]
    optional = base[n_core:]
    ec, eo = PREFIX_RULES.get(prefix, ([], []))
    for s in ec:
        if s not in core:
            core.append(s)
    for s in eo:
        if s not in core and s not in optional:
            optional.append(s)
    if suffix == "cấp":
        for s in ["sốt", "đau dữ dội"]:
            if s not in core and s not in optional:
                optional.append(s)
    elif suffix == "mạn":
        for s in ["mệt mỏi", "kéo dài"]:
            if s not in core and s not in optional:
                optional.append(s)
    return core, optional


# ───────────────────────────────────────────────────────────────────────────
# 2) Mot so benh THUONG GAP co thuc (uu tien giu, dat truoc)
# ───────────────────────────────────────────────────────────────────────────
SPECIFIC = {
    "Cảm cúm":          (["sốt cao","đau nhức cơ","mệt mỏi"], ["đau đầu","ho","đau họng","ớn lạnh"]),
    "Cảm lạnh":         (["hắt hơi","sổ mũi","nghẹt mũi"], ["đau họng","ho","mệt mỏi"]),
    "Sốt xuất huyết":   (["sốt cao","đau sau hốc mắt","phát ban"], ["đau đầu","đau khớp","buồn nôn","chảy máu cam"]),
    "Sốt rét":          (["sốt cao","ớn lạnh","đổ mồ hôi"], ["đau đầu","buồn nôn","mệt mỏi"]),
    "Sởi":              (["sốt cao","phát ban","ho"], ["chảy nước mắt","sổ mũi","mắt đỏ"]),
    "Thủy đậu":         (["phát ban","ngứa","mụn nước"], ["sốt","mệt mỏi","chán ăn"]),
    "Quai bị":          (["sưng tuyến mang tai","sốt"], ["đau khi nhai","đau đầu","mệt mỏi"]),
    "Tay chân miệng":   (["phát ban","loét miệng","sốt"], ["chán ăn","mệt mỏi"]),
    "Zona thần kinh":   (["phát ban","đau rát da","mụn nước"], ["ngứa","sốt nhẹ"]),
    "Mề đay":           (["nổi mẩn","ngứa"], ["phát ban","sưng môi"]),
    "Dị ứng":           (["hắt hơi","ngứa"], ["phát ban","chảy nước mắt","nghẹt mũi"]),
    "Hen suyễn":        (["khó thở","thở khò khè"], ["ho","đau ngực"]),
    "Lao phổi":         (["ho kéo dài","ho ra máu","sụt cân"], ["sốt nhẹ","đổ mồ hôi đêm","mệt mỏi"]),
    "COVID-19":         (["sốt","ho khan","mệt mỏi"], ["mất khứu giác","khó thở","đau họng","đau nhức cơ"]),
    "Đau nửa đầu":      (["đau đầu","nhạy cảm ánh sáng"], ["buồn nôn","chóng mặt","nôn"]),
    "Tăng huyết áp":    (["đau đầu","chóng mặt"], ["hồi hộp","mờ mắt","ù tai"]),
    "Tiểu đường":       (["khát nước nhiều","tiểu nhiều"], ["sụt cân","mệt mỏi","mờ mắt","đói nhiều"]),
    "Thiếu máu":        (["mệt mỏi","da xanh xao","chóng mặt"], ["khó thở","hồi hộp","đau đầu"]),
    "Cường giáp":       (["hồi hộp","sụt cân","run tay"], ["đổ mồ hôi","mất ngủ","lồi mắt"]),
    "Suy giáp":         (["mệt mỏi","tăng cân","sợ lạnh"], ["táo bón","da khô","rụng tóc"]),
    "Gout":             (["đau khớp","sưng khớp","đỏ khớp"], ["đau dữ dội về đêm","nóng khớp"]),
    "Viêm khớp dạng thấp":(["đau khớp","sưng khớp","cứng khớp"], ["mệt mỏi","sốt nhẹ"]),
    "Sỏi thận":         (["đau lưng","đau quặn thận"], ["tiểu ra máu","buồn nôn","tiểu buốt"]),
    "Sỏi mật":          (["đau hạ sườn phải","buồn nôn"], ["sốt","vàng da"]),
    "Trào ngược dạ dày":(["ợ chua","ợ nóng"], ["đau ngực","ho khan","khó nuốt"]),
    "Trĩ":              (["đi ngoài ra máu","đau hậu môn"], ["ngứa hậu môn","sa búi trĩ"]),
    "Táo bón":          (["đi ngoài khó","phân cứng"], ["đau bụng","đầy hơi","chán ăn"]),
    "Ngộ độc thực phẩm":(["buồn nôn","nôn","tiêu chảy"], ["đau bụng","sốt","mất nước"]),
    "Đột quỵ":          (["méo miệng","yếu liệt tay chân","nói khó"], ["đau đầu dữ dội","chóng mặt","mờ mắt"]),
    "Nhồi máu cơ tim":  (["đau ngực","khó thở","đổ mồ hôi lạnh"], ["buồn nôn","đau lan cánh tay","hồi hộp"]),
    "Viêm màng não":    (["sốt cao","đau đầu dữ dội","cứng cổ"], ["buồn nôn","nhạy cảm ánh sáng","lơ mơ"]),
    "Xơ gan":           (["vàng da","phù chân","mệt mỏi"], ["chán ăn","bầm tím","đau hạ sườn phải"]),
    "Suy thận":         (["phù chân","tiểu ít","mệt mỏi"], ["buồn nôn","khó thở","da xanh xao"]),
    "Suy tim":          (["khó thở","phù chân","mệt mỏi"], ["ho","hồi hộp","đau ngực"]),
    "Parkinson":        (["run tay","cứng đờ","đi lại khó"], ["chậm chạp","mất thăng bằng"]),
    "Động kinh":        (["co giật","mất ý thức"], ["lơ mơ","đau đầu"]),
    "Viêm phổi":        (["sốt cao","ho có đờm","khó thở"], ["đau ngực","mệt mỏi","ớn lạnh"]),
    "Viêm phế quản":    (["ho có đờm","khó thở"], ["đau ngực","mệt mỏi","sốt nhẹ"]),
    "Viêm xoang":       (["nghẹt mũi","đau mặt"], ["đau đầu","sổ mũi","giảm khứu giác"]),
    "Viêm họng":        (["đau họng","khó nuốt"], ["sốt","sưng hạch","ho"]),
    "Viêm amidan":      (["đau họng","sưng amidan","khó nuốt"], ["sốt","sưng hạch","hôi miệng"]),
    "Viêm dạ dày":      (["đau thượng vị","ợ chua"], ["buồn nôn","đầy hơi","chán ăn"]),
    "Viêm gan":         (["vàng da","mệt mỏi","chán ăn"], ["buồn nôn","đau hạ sườn phải","nước tiểu sẫm màu"]),
    "Viêm ruột thừa":   (["đau bụng","đau hố chậu phải"], ["buồn nôn","sốt","chán ăn"]),
    "Viêm kết mạc":     (["mắt đỏ","ngứa mắt"], ["chảy nước mắt","ghèn mắt","cộm mắt"]),
    "Viêm tai giữa":    (["đau tai","sốt"], ["giảm thính lực","chảy mủ tai","ù tai"]),
    "Viêm bàng quang":  (["tiểu buốt","tiểu rắt","tiểu nhiều lần"], ["đau bụng dưới","nước tiểu đục"]),
    "Trầm cảm":         (["buồn bã kéo dài","mất ngủ","chán ăn"], ["mệt mỏi","mất hứng thú","khó tập trung"]),
    "Rối loạn lo âu":   (["lo lắng quá mức","hồi hộp"], ["mất ngủ","khó thở","chóng mặt"]),
}

# ───────────────────────────────────────────────────────────────────────────
# 3) Sinh danh sach benh: SPECIFIC truoc, roi to hop co quan x loai benh ly
# ───────────────────────────────────────────────────────────────────────────
diseases = {}                          # ten -> (core, optional)
for name, (c, o) in SPECIFIC.items():
    diseases[name] = (c, o)

for noun, cat in ORGANS:
    base = CAT_SYMS[cat]
    for prefix in CAT_PREFIXES[cat]:
        name = f"{prefix} {noun}"
        if name not in diseases:
            diseases[name] = derive(name, base, prefix)
    # them bien the cap / man cho nhom phu hop (chi voi "Viêm")
    if cat in CAP_MAN_CATS:
        for suffix in ("cấp", "mạn"):
            name = f"Viêm {noun} {suffix}"
            if name not in diseases:
                diseases[name] = derive(name, base, "Viêm", suffix)

# Cat dung ~400 benh
TARGET_DISEASES = 400
names = list(diseases.keys())
if len(names) > TARGET_DISEASES:
    names = names[:TARGET_DISEASES]
diseases = {n: diseases[n] for n in names}

# ───────────────────────────────────────────────────────────────────────────
# 4) Bang trong so muc do nghiem trong
# ───────────────────────────────────────────────────────────────────────────
WEIGHTS = {
    "sốt cao":6,"sốt":4,"sốt nhẹ":3,"đau đầu":4,"đau đầu dữ dội":6,"đau nhức cơ":3,"mệt mỏi":3,
    "ho":3,"ho khan":3,"ho có đờm":4,"ho kéo dài":4,"ho ra máu":7,"đau họng":4,"ớn lạnh":4,
    "hắt hơi":2,"sổ mũi":2,"nghẹt mũi":2,"khó nuốt":3,"sưng hạch":4,"sưng amidan":4,"hôi miệng":1,
    "khó thở":6,"thở khò khè":5,"đau ngực":6,"đau sau hốc mắt":5,"đau khớp":4,"sưng khớp":4,
    "cứng khớp":4,"đỏ khớp":4,"nóng khớp":3,"đau dữ dội về đêm":4,"hạn chế vận động":3,"đau xương":4,
    "phát ban":4,"mụn nước":3,"buồn nôn":3,"nôn":4,"nôn ra máu":6,"chảy máu cam":5,"tiêu chảy":4,
    "đau bụng":4,"đau bụng dưới":4,"đau bụng trên dữ dội":6,"đau thượng vị":4,"đau hố chậu phải":5,
    "đau lan ra lưng":4,"mất nước":5,"ợ chua":2,"ợ nóng":2,"đầy hơi":2,"chán ăn":3,"đi ngoài khó":3,
    "phân cứng":2,"đi ngoài ra máu":5,"đau hậu môn":3,"ngứa hậu môn":2,"sa búi trĩ":3,"vàng da":5,
    "nước tiểu sẫm màu":4,"nước tiểu đục":3,"đổ mồ hôi":3,"đổ mồ hôi đêm":3,"đổ mồ hôi lạnh":6,
    "sụt cân":5,"chảy nước mắt":2,"ngứa":2,"ngứa mắt":2,"mắt đỏ":3,"ghèn mắt":1,"cộm mắt":2,
    "nhạy cảm ánh sáng":3,"chóng mặt":4,"đau mặt":3,"giảm khứu giác":3,"mất khứu giác":4,"đau tai":4,
    "giảm thính lực":4,"chảy mủ tai":4,"ù tai":3,"sưng tuyến mang tai":4,"đau khi nhai":3,"loét miệng":3,
    "đau rát da":4,"nổi mẩn":2,"da khô":1,"da đỏ":2,"bong tróc da":2,"sưng môi":4,"hồi hộp":4,"mờ mắt":4,
    "da xanh xao":3,"khát nước nhiều":4,"tiểu nhiều":3,"tiểu nhiều lần":3,"đói nhiều":2,"run tay":3,
    "mất ngủ":3,"lồi mắt":4,"tăng cân":2,"sợ lạnh":2,"táo bón":3,"rụng tóc":1,"đau lưng":4,
    "đau quặn thận":6,"tiểu ra máu":5,"tiểu buốt":4,"tiểu rắt":3,"tiểu ít":4,"buồn bã kéo dài":4,
    "mất hứng thú":3,"khó tập trung":3,"lo lắng quá mức":4,"cứng cổ":6,"lơ mơ":6,"méo miệng":7,
    "yếu liệt tay chân":7,"nói khó":6,"đau lan cánh tay":6,"khàn tiếng":3,"phù chân":4,"bầm tím":3,
    "ra khí hư":2,"rối loạn kinh nguyệt":3,"đau khi quan hệ":3,"tê tay chân":3,"co giật":7,
    "sạm da":2,"đau răng":4,"sưng lợi":3,"chảy máu chân răng":3,"sưng":3,"đau":3,"đau dữ dội":5,
    "kéo dài":2,"mất ý thức":7,"cứng đờ":4,"đi lại khó":4,"chậm chạp":2,"mất thăng bằng":4,"phù":4,
}

# Gom trieu chung thuc su xuat hien
ALL_SYMPTOMS = []
for c, o in diseases.values():
    for s in c + o:
        if s not in ALL_SYMPTOMS:
            ALL_SYMPTOMS.append(s)
ALL_SYMPTOMS.sort()
TRONGSO = {s: WEIGHTS.get(s, 3) for s in ALL_SYMPTOMS}

# ───────────────────────────────────────────────────────────────────────────
# 5) Sinh ~5000 dong (chia deu cac benh)
# ───────────────────────────────────────────────────────────────────────────
TARGET_ROWS = 5000
MAX_COLS = 8
disease_items = list(diseases.items())
rows = []
i = 0
while len(rows) < TARGET_ROWS:
    name, (core, optional) = disease_items[i % len(disease_items)]
    i += 1
    syms = list(core)
    if len(syms) > 1 and random.random() < 0.15:
        syms.remove(random.choice(syms))
    for s in optional:
        if random.random() < 0.5:
            syms.append(s)
    if random.random() < 0.10:
        pool = [x for x in ALL_SYMPTOMS if x not in core and x not in optional]
        if pool:
            syms.append(random.choice(pool))
    if not syms:
        syms = [random.choice(core)]
    syms = list(dict.fromkeys(syms))
    random.shuffle(syms)
    syms = syms[:MAX_COLS]
    rows.append((name, syms))
random.shuffle(rows)

# ───────────────────────────────────────────────────────────────────────────
# 6) Ghi file
# ───────────────────────────────────────────────────────────────────────────
with open(os.path.join(DATA, "benh_trieuchung.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Benh"] + [f"TrieuChung_{i+1}" for i in range(MAX_COLS)])
    for name, syms in rows:
        w.writerow([name] + syms + [""] * (MAX_COLS - len(syms)))

with open(os.path.join(DATA, "trongso_mucdo_nghiemtrong.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["TrieuChung", "TrongSo"])
    for s in ALL_SYMPTOMS:
        w.writerow([s, TRONGSO[s]])

inputs = [
    "Mấy hôm nay tôi sốt cao, đau nhức cơ và mệt mỏi, kèm theo ho và ớn lạnh",
    "Tôi bị hắt hơi liên tục, sổ mũi và nghẹt mũi, hơi đau họng",
    "Bệnh nhân sốt cao, nổi phát ban, đau sau hốc mắt và đau khớp",
    "Tôi ho có đờm nhiều, khó thở và đau tức ngực",
    "Đau bụng quặn từng cơn, tiêu chảy nhiều lần kèm buồn nôn",
    "Đau đầu dữ dội một bên, sợ ánh sáng, buồn nôn và chóng mặt",
]
with open(os.path.join(DATA, "input_mota_benhnhan.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id", "mo_ta"])
    for i, t in enumerate(inputs, 1):
        w.writerow([i, t])

print(f"Da sinh {len(rows)} dong | {len(ALL_SYMPTOMS)} trieu chung | {len(diseases)} benh")
