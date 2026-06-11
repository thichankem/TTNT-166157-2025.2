# -*- coding: utf-8 -*-
"""Sinh anh bang du lieu (style anh chup) cho bao cao."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_report_assets")
os.makedirs(OUT, exist_ok=True)

def table_img(df, fname, fontsize=8, col_w=None, title=None):
    n_rows, n_cols = df.shape
    fig_w = min(12, max(6, n_cols*1.4))
    fig_h = 0.45*(n_rows+1) + (0.4 if title else 0)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    if title: ax.set_title(title, fontsize=fontsize+2, fontweight="bold", pad=8)
    tbl = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="left", loc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(fontsize); tbl.scale(1, 1.4)
    for (r,c),cell in tbl.get_celld().items():
        cell.set_edgecolor("#BFBFBF")
        if r==0:
            cell.set_facecolor("#2E75B6"); cell.set_text_props(color="white", fontweight="bold")
        elif r%2==0:
            cell.set_facecolor("#EAF1FB")
    plt.tight_layout(); plt.savefig(os.path.join(OUT,fname), dpi=130, bbox_inches="tight"); plt.close()
    print("wrote", fname)

# 1. benh_trieuchung head
benh = pd.read_csv(os.path.join(BASE,"01_data/benh_trieuchung.csv")).fillna("")
table_img(benh[["Benh","TrieuChung_1","TrieuChung_2","TrieuChung_3","TrieuChung_4"]].head(6),
          "tbl_benh.png", title="benh_trieuchung.csv (trich)")

# 2. trongso head
ts = pd.read_csv(os.path.join(BASE,"01_data/trongso_mucdo_nghiemtrong.csv"))
ts2 = ts.head(10).reset_index(drop=True)
table_img(ts2, "tbl_trongso.png", title="trongso_mucdo_nghiemtrong.csv (trich)")

# 3. features head (vai cot)
ft = pd.read_csv(os.path.join(BASE,"01_data/processed/features.csv"))
cols = list(ft.columns[:6]) + ["Benh"]
table_img(ft[cols].head(6), "tbl_features.png", title="features.csv - one-hot co trong so (trich)")

# 4. NLP ket qua
import re
trongso = ts; ds = list(trongso["TrieuChung"])
dong_nghia = {"tức ngực":"đau ngực","đau tức ngực":"đau ngực","sợ ánh sáng":"nhạy cảm ánh sáng","đau mỏi cơ":"đau nhức cơ"}
def chuan_hoa(t): return re.sub(r"\s+"," ",re.sub(r"[.,;!?()]"," ",str(t).lower())).strip()
def tim(text):
    norm=chuan_hoa(text); found=[]
    for cum in sorted(list(ds)+list(dong_nghia.keys()),key=len,reverse=True):
        if cum in norm:
            ch=dong_nghia.get(cum,cum)
            if ch not in found: found.append(ch)
            norm=norm.replace(cum," ")
    return found
inp = pd.read_csv(os.path.join(BASE,"01_data/input_mota_benhnhan.csv"))
inp["Trieu chung nhan dien"] = inp["mo_ta"].apply(lambda x: ", ".join(tim(x)))
nlp = inp[["mo_ta","Trieu chung nhan dien"]].copy()
nlp.columns = ["Cau mo ta cua benh nhan","Trieu chung nhan dien"]
# rut gon mo ta
nlp["Cau mo ta cua benh nhan"] = nlp["Cau mo ta cua benh nhan"].str.slice(0,55)
table_img(nlp, "tbl_nlp.png", fontsize=8, title="Ket qua NLP: cau mo ta -> trieu chung")
print("DONE")
