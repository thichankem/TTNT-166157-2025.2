import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# ==========================================
# 1. Load dữ liệu
# ==========================================
df = pd.read_csv('data/transformed_dataset.xls')
df.columns = [c.strip() for c in df.columns]

symptom_cols = [col for col in df.columns if col not in ['Unnamed: 0', 'Disease', 'Disease_code']]
X = df[symptom_cols]
y = df['Disease']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Dataset: {df.shape[0]} mẫu, {len(symptom_cols)} features, {y.nunique()} classes")
print(f"Train: {X_train.shape[0]} mẫu | Test: {X_test.shape[0]} mẫu")

# ==========================================
# 2. So sánh Train Accuracy vs Test Accuracy theo K
# ==========================================
print("\n" + "="*70)
print("KIỂM TRA 1: So sánh Train Accuracy vs Test Accuracy")
print("="*70)
print(f"{'K':>3} | {'Train Acc':>10} | {'Test Acc':>10} | {'Gap':>8} | {'Đánh giá'}")
print("-"*70)

k_range = range(1, 26)
train_accs = []
test_accs = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    
    train_acc = accuracy_score(y_train, knn.predict(X_train))
    test_acc = accuracy_score(y_test, knn.predict(X_test))
    
    train_accs.append(train_acc)
    test_accs.append(test_acc)
    
    gap = train_acc - test_acc
    
    if gap > 0.10:
        status = "⚠️ QUÁ KHỚP NẶNG"
    elif gap > 0.05:
        status = "⚠️ Có dấu hiệu quá khớp"
    elif gap > 0.02:
        status = "🔶 Quá khớp nhẹ"
    else:
        status = "✅ Ổn"
    
    print(f"  {k:2d} | {train_acc*100:9.2f}% | {test_acc*100:9.2f}% | {gap*100:6.2f}% | {status}")

# ==========================================
# 3. Cross-Validation (5-fold)
# ==========================================
print("\n" + "="*70)
print("KIỂM TRA 2: Cross-Validation 5-Fold")
print("="*70)

best_k_idx = np.argmax(test_accs)
best_k = list(k_range)[best_k_idx]

print(f"\nK tối ưu (theo Test Accuracy): K={best_k}")
print(f"\nThử Cross-Validation với một số giá trị K:")
print(f"{'K':>3} | {'CV Mean':>10} | {'CV Std':>8} | {'Test Acc':>10} | {'Gap (CV-Test)':>13}")
print("-"*60)

for k in [1, 3, 5, 7, best_k, 11, 15, 21, 25]:
    k = min(k, 25)
    knn = KNeighborsClassifier(n_neighbors=k)
    cv_scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
    
    test_knn = KNeighborsClassifier(n_neighbors=k)
    test_knn.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, test_knn.predict(X_test))
    
    gap = cv_scores.mean() - test_acc
    print(f"  {k:2d} | {cv_scores.mean()*100:9.2f}% | {cv_scores.std()*100:6.2f}% | {test_acc*100:9.2f}% | {gap*100:11.2f}%")

# ==========================================
# 4. Learning Curve (với K tối ưu)
# ==========================================
print("\n" + "="*70)
print(f"KIỂM TRA 3: Learning Curve (K={best_k})")
print("="*70)

knn_best = KNeighborsClassifier(n_neighbors=best_k)
train_sizes, train_scores, val_scores = learning_curve(
    knn_best, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

print(f"\n{'Train Size':>12} | {'Train Acc':>10} | {'Val Acc':>10} | {'Gap':>8}")
print("-"*50)
for i in range(len(train_sizes)):
    gap = train_mean[i] - val_mean[i]
    print(f"  {train_sizes[i]:10d} | {train_mean[i]*100:9.2f}% | {val_mean[i]*100:9.2f}% | {gap*100:6.2f}%")

# ==========================================
# 5. Vẽ đồ thị tổng hợp
# ==========================================
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# --- Chart 1: Train vs Test Accuracy theo K ---
ax1 = axes[0]
ax1.plot(list(k_range), [a*100 for a in train_accs], 'o-', label='Train Accuracy', 
         color='#E53935', linewidth=2, markersize=5)
ax1.plot(list(k_range), [a*100 for a in test_accs], 's-', label='Test Accuracy', 
         color='#1E88E5', linewidth=2, markersize=5)
ax1.fill_between(list(k_range), 
                 [t*100 for t in test_accs], 
                 [t*100 for t in train_accs], 
                 alpha=0.15, color='red', label='Overfitting Gap')
ax1.axvline(x=best_k, color='green', linestyle='--', alpha=0.7, label=f'Best K={best_k}')
ax1.set_xlabel('Giá trị K', fontsize=11)
ax1.set_ylabel('Accuracy (%)', fontsize=11)
ax1.set_title('Train vs Test Accuracy theo K\n(Khoảng cách = mức độ quá khớp)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9)
ax1.set_xticks(list(k_range))
ax1.grid(True, alpha=0.3)

# --- Chart 2: Overfitting Gap theo K ---
ax2 = axes[1]
gaps = [(train_accs[i] - test_accs[i])*100 for i in range(len(k_range))]
colors = ['#E53935' if g > 10 else '#FF9800' if g > 5 else '#FFC107' if g > 2 else '#4CAF50' for g in gaps]
ax2.bar(list(k_range), gaps, color=colors, alpha=0.8, edgecolor='white')
ax2.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='Ngưỡng quá khớp (5%)')
ax2.axhline(y=2, color='orange', linestyle='--', alpha=0.5, label='Ngưỡng cảnh báo (2%)')
ax2.set_xlabel('Giá trị K', fontsize=11)
ax2.set_ylabel('Gap: Train - Test (%)', fontsize=11)
ax2.set_title('Mức độ Quá khớp (Overfitting Gap) theo K', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9)
ax2.set_xticks(list(k_range))
ax2.grid(True, alpha=0.3, axis='y')

# --- Chart 3: Learning Curve ---
ax3 = axes[2]
ax3.plot(train_sizes, train_mean*100, 'o-', label='Training Score', color='#E53935', linewidth=2)
ax3.fill_between(train_sizes, (train_mean - train_std)*100, (train_mean + train_std)*100, alpha=0.1, color='#E53935')
ax3.plot(train_sizes, val_mean*100, 's-', label='Validation Score', color='#1E88E5', linewidth=2)
ax3.fill_between(train_sizes, (val_mean - val_std)*100, (val_mean + val_std)*100, alpha=0.1, color='#1E88E5')
ax3.set_xlabel('Số lượng mẫu huấn luyện', fontsize=11)
ax3.set_ylabel('Accuracy (%)', fontsize=11)
ax3.set_title(f'Learning Curve (K={best_k})\n(2 đường hội tụ = không quá khớp)', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model/overfitting_analysis.png', dpi=150, bbox_inches='tight')
print(f"\nĐồ thị đã lưu: model/overfitting_analysis.png")

# ==========================================
# 6. Tổng kết đánh giá
# ==========================================
print("\n" + "="*70)
print("TỔNG KẾT ĐÁNH GIÁ QUÁ KHỚP (OVERFITTING)")
print("="*70)

best_train_acc = train_accs[best_k_idx]
best_test_acc = test_accs[best_k_idx]
best_gap = best_train_acc - best_test_acc

print(f"\n  K tối ưu         : {best_k}")
print(f"  Train Accuracy   : {best_train_acc*100:.2f}%")
print(f"  Test Accuracy    : {best_test_acc*100:.2f}%")
print(f"  Gap (Train-Test) : {best_gap*100:.2f}%")

# Learning curve convergence
final_gap = train_mean[-1] - val_mean[-1]
print(f"  Learning Curve Gap (cuối): {final_gap*100:.2f}%")

print(f"\n  📊 ĐÁNH GIÁ:")
if best_gap > 0.10:
    print(f"  ❌ Model ĐANG BỊ QUÁ KHỚP NẶNG (gap = {best_gap*100:.2f}% > 10%)")
    print(f"     → Khuyến nghị: Tăng K, thu thập thêm dữ liệu, hoặc giảm features")
elif best_gap > 0.05:
    print(f"  ⚠️ Model CÓ DẤU HIỆU quá khớp (gap = {best_gap*100:.2f}% > 5%)")
    print(f"     → Khuyến nghị: Cân nhắc tăng K hoặc sử dụng feature selection")
elif best_gap > 0.02:
    print(f"  🔶 Model có quá khớp NHẸ (gap = {best_gap*100:.2f}%), chấp nhận được")
    print(f"     → Model hoạt động tốt, có thể cải thiện thêm nếu cần")
else:
    print(f"  ✅ Model KHÔNG bị quá khớp (gap = {best_gap*100:.2f}% ≤ 2%)")
    print(f"     → Model tổng quát hóa tốt trên dữ liệu mới")

if best_train_acc > 0.99 and best_test_acc > 0.95:
    print(f"\n  ℹ️ Lưu ý: Cả Train ({best_train_acc*100:.1f}%) và Test ({best_test_acc*100:.1f}%) accuracy đều rất cao.")
    print(f"     Có thể dataset quá đơn giản hoặc có data leakage. Cần kiểm tra thêm.")

print("\n" + "="*70)
