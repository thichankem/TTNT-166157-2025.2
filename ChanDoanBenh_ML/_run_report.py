# -*- coding: utf-8 -*-
"""Chay toan bo pipeline ChanDoanBenh_ML va sinh anh ket qua cho bao cao."""
import os, re, json, pickle, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "_report_assets")
os.makedirs(OUT, exist_ok=True)

# ============ 1. TIEN XU LY ============
benh = pd.read_csv(os.path.join(BASE, "01_data/benh_trieuchung.csv"))
trongso = pd.read_csv(os.path.join(BASE, "01_data/trongso_mucdo_nghiemtrong.csv"))
trong_so = dict(zip(trongso["TrieuChung"], trongso["TrongSo"]))
ds_trieuchung = list(trongso["TrieuChung"])

cot_trieuchung = [c for c in benh.columns if c.startswith("TrieuChung")]
X = pd.DataFrame(0, index=benh.index, columns=ds_trieuchung)
for i in range(len(benh)):
    for cot in cot_trieuchung:
        tc = benh.loc[i, cot]
        if isinstance(tc, str) and tc.strip() in trong_so:
            X.loc[i, tc.strip()] = trong_so[tc.strip()]
X["Benh"] = benh["Benh"]
os.makedirs(os.path.join(BASE, "01_data/processed"), exist_ok=True)
X.to_csv(os.path.join(BASE, "01_data/processed/features.csv"), index=False, encoding="utf-8-sig")

print("So ca benh:", len(benh))
print("So benh khac nhau:", benh["Benh"].nunique())
print("So trieu chung (cot):", len(ds_trieuchung))
print("Bang dac trung (features):", X.shape)
print("Trong so min/max:", trongso["TrongSo"].min(), trongso["TrongSo"].max())

# ============ 2. NLP INPUT ============
inp = pd.read_csv(os.path.join(BASE, "01_data/input_mota_benhnhan.csv"))
def chuan_hoa(t):
    t = str(t).lower(); t = re.sub(r"[.,;!?()]"," ",t); return re.sub(r"\s+"," ",t).strip()
dong_nghia = {"tức ngực":"đau ngực","đau tức ngực":"đau ngực","sợ ánh sáng":"nhạy cảm ánh sáng","đau mỏi cơ":"đau nhức cơ"}
def tim(text):
    norm = chuan_hoa(text); found=[]
    for cum in sorted(list(ds_trieuchung)+list(dong_nghia.keys()), key=len, reverse=True):
        if cum in norm:
            ch = dong_nghia.get(cum,cum)
            if ch not in found: found.append(ch)
            norm = norm.replace(cum," ")
    return found
inp["trieu_chung"] = inp["mo_ta"].apply(tim)
print("\n=== NLP nhan dien trieu chung tu cau mo ta ===")
for _,r in inp.iterrows():
    print(f"  Input {r['id']}: {r['trieu_chung']}")

# ============ 3. HUAN LUYEN 3 MO HINH ============
from sklearn.model_selection import train_test_split, validation_curve, learning_curve
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv(os.path.join(BASE, "01_data/processed/features.csv"))
Xd = data.drop(columns=["Benh"]); y = data["Benh"]
le = LabelEncoder(); y_num = le.fit_transform(y)
Xtr,Xte,ytr,yte = train_test_split(Xd,y_num,test_size=0.2,random_state=42,stratify=y_num)
print("\nTrain:",Xtr.shape,"Test:",Xte.shape,"So benh:",len(le.classes_))

models = {
    "Random Forest": RandomForestClassifier(n_estimators=100,random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
}
results = {}
for name,m in models.items():
    m.fit(Xtr,ytr); yp = m.predict(Xte)
    acc = accuracy_score(yte,yp)
    prec = precision_score(yte,yp,average="macro",zero_division=0)
    rec = recall_score(yte,yp,average="macro",zero_division=0)
    results[name] = (acc,prec,rec)
    print(f"{name}: acc={acc:.3f} precision={prec:.3f} recall={rec:.3f}")

# --- Bieu do so sanh accuracy ---
fig,ax = plt.subplots(figsize=(6,3.6))
names = list(results.keys()); accs=[results[n][0] for n in names]
bars = ax.bar(names, accs, color=["#2E75B6","#70AD47","#ED7D31"])
for b,a in zip(bars,accs): ax.text(b.get_x()+b.get_width()/2, a+0.01, f"{a:.3f}", ha="center", fontweight="bold")
ax.set_ylim(0,1.05); ax.set_ylabel("Accuracy (tap test)"); ax.set_title("So sanh do chinh xac 3 mo hinh")
ax.grid(axis="y",alpha=0.3); plt.tight_layout(); plt.savefig(os.path.join(OUT,"accuracy_compare.png"),dpi=130); plt.close()

# --- Validation curve Random Forest (n_estimators) ---
gt = [10,25,50,100,150,200]
tr_sc,va_sc = validation_curve(RandomForestClassifier(random_state=42),Xtr,ytr,
    param_name="n_estimators",param_range=gt,cv=3,scoring="accuracy")
fig,ax=plt.subplots(figsize=(6,3.6))
ax.plot(gt,tr_sc.mean(1),"o-",label="Train")
ax.plot(gt,va_sc.mean(1),"o-",label="Kiem tra (CV)")
ax.set_xlabel("So cay (n_estimators)"); ax.set_ylabel("Accuracy"); ax.set_title("Validation curve - Random Forest")
ax.legend(); ax.grid(alpha=0.3); plt.tight_layout(); plt.savefig(os.path.join(OUT,"vc_rf.png"),dpi=130); plt.close()
print("RF n_estimators tot nhat:", gt[int(np.argmax(va_sc.mean(1)))])

# --- Validation curve KNN (k) ---
gk=[1,3,5,7,9,11,15,21]
tr_k,va_k = validation_curve(KNeighborsClassifier(),Xtr,ytr,param_name="n_neighbors",param_range=gk,cv=3,scoring="accuracy")
fig,ax=plt.subplots(figsize=(6,3.6))
ax.plot(gk,tr_k.mean(1),"o-",label="Train"); ax.plot(gk,va_k.mean(1),"o-",label="Kiem tra (CV)")
ax.set_xlabel("So lang gieng (k)"); ax.set_ylabel("Accuracy"); ax.set_title("Validation curve - KNN")
ax.legend(); ax.grid(alpha=0.3); plt.tight_layout(); plt.savefig(os.path.join(OUT,"vc_knn.png"),dpi=130); plt.close()
print("KNN k tot nhat:", gk[int(np.argmax(va_k.mean(1)))])

# --- Learning curve Random Forest ---
sizes,tr2,va2 = learning_curve(RandomForestClassifier(n_estimators=100,random_state=42),Xd,y_num,cv=3,
    scoring="accuracy",train_sizes=np.linspace(0.1,1.0,6))
fig,ax=plt.subplots(figsize=(6,3.6))
ax.plot(sizes,tr2.mean(1),"o-",label="Train"); ax.plot(sizes,va2.mean(1),"o-",label="Kiem tra (CV)")
ax.set_xlabel("So mau huan luyen"); ax.set_ylabel("Accuracy"); ax.set_title("Learning curve - Random Forest")
ax.legend(); ax.grid(alpha=0.3); plt.tight_layout(); plt.savefig(os.path.join(OUT,"lc_rf.png"),dpi=130); plt.close()

# --- Dump ket qua ra json ---
summary = {
    "n_ca": int(len(benh)), "n_benh": int(benh["Benh"].nunique()), "n_trieuchung": len(ds_trieuchung),
    "features_shape": list(X.shape), "train_shape": list(Xtr.shape), "test_shape": list(Xte.shape),
    "results": {k:[round(v[0],3),round(v[1],3),round(v[2],3)] for k,v in results.items()},
    "rf_best_n": gt[int(np.argmax(va_sc.mean(1)))], "knn_best_k": gk[int(np.argmax(va_k.mean(1)))],
}
with open(os.path.join(OUT,"summary.json"),"w",encoding="utf-8") as f: json.dump(summary,f,ensure_ascii=False,indent=2)
print("\n=== SUMMARY ===")
print(json.dumps(summary,ensure_ascii=False,indent=2))
print("\nXONG - anh luu tai", OUT)
