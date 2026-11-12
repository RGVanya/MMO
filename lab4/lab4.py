# -*- coding: utf-8 -*-
"""
Лабораторная работа 4 — Бинарная классификация.
Датасет: Heart Disease and Hospitals (heart_disease_dataset.zip)
Таргет: heart_disease (0 / 1)

Запуск: python lab4/lab4.py
Графики сохраняются в lab4/figures/
"""

from pathlib import Path
import io
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
    f1_score,
    roc_auc_score,
    roc_curve,
    accuracy_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Загрузка датасета
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("1. Загрузка датасета")
print("=" * 60)

zip_path = ROOT / "heart_disease_dataset.zip"
with zipfile.ZipFile(zip_path) as zf:
    csv_name = next(n for n in zf.namelist() if n.endswith(".csv"))
    with zf.open(csv_name) as f:
        df = pd.read_csv(f)

print(f"Размер: {df.shape}")
print(df.head(3).to_string())
print("\nТипы столбцов:")
print(df.dtypes)
print("\nЦелевая переменная — распределение классов:")
print(df["heart_disease"].value_counts())


# ─────────────────────────────────────────────────────────────────────────────
# 2. Очистка и предобработка
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. Очистка и предобработка")
print("=" * 60)

# 2.1 Пропуски
missing = df.isna().sum()
print("Пропуски по столбцам:")
print(missing[missing > 0] if missing.any() else "  пропусков нет")

# 2.2 Удаляем нерелевантные столбцы (ФИО, больница, дата и пр.)
drop_cols = ["full_name", "first_name", "last_name", "hospital", "treatment", "treatment_date"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])
print(f"\nУдалены столбцы: {drop_cols}")

# 2.3 Целевая переменная
y = df["heart_disease"].values
X_df = df.drop(columns=["heart_disease"])
print(f"Признаков: {X_df.shape[1]}, объектов: {len(y)}")

# 2.4 Кодирование категориальных признаков
cat_cols = X_df.select_dtypes(include=["object", "str"]).columns.tolist()
print(f"Категориальные признаки: {cat_cols}")

le = LabelEncoder()
for col in cat_cols:
    X_df[col] = le.fit_transform(X_df[col].astype(str))

print("После кодирования:")
print(X_df.dtypes)

# 2.5 Анализ выбросов по числовым признакам (IQR)
num_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()

def iqr_bounds(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

print("\nВыбросы (IQR):")
for col in num_cols:
    lo, hi = iqr_bounds(X_df[col])
    n_out = ((X_df[col] < lo) | (X_df[col] > hi)).sum()
    print(f"  {col:20s}: {n_out:5d}  [{lo:.2f}; {hi:.2f}]")

# Клиппинг выбросов (мягкий)
for col in num_cols:
    lo, hi = iqr_bounds(X_df[col])
    X_df[col] = X_df[col].clip(lower=lo, upper=hi)

X = X_df.values
print(f"\nИтоговый датасет: X={X.shape}, y={y.shape}")
print(f"Баланс классов: 0={np.sum(y==0)}, 1={np.sum(y==1)}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Разбивка на обучение/тест и масштабирование
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. Train/Test split + StandardScaler")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print(f"Train pos: {y_train.mean():.3f}, Test pos: {y_test.mean():.3f}")

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Обучение моделей
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. Обучение моделей")
print("=" * 60)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "SVM (linear)":        SVC(kernel="linear", probability=True, random_state=42),  # noqa: FutureWarning
    "Decision Tree (CART)": DecisionTreeClassifier(max_depth=5, random_state=42),
}

results: dict[str, dict] = {}

for name, model in models.items():
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)
    auc  = roc_auc_score(y_test, y_prob)

    results[name] = {
        "model": model,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "accuracy":  acc,
        "precision": prec,
        "recall":    rec,
        "f1":        f1,
        "roc_auc":   auc,
    }

    print(f"\n{'─'*40}")
    print(f"Модель: {name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall   : {rec:.4f}")
    print(f"  F1       : {f1:.4f}")
    print(f"  ROC-AUC  : {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Нет болезни", "Есть болезнь"]))


# ─────────────────────────────────────────────────────────────────────────────
# 5. Графики — матрицы ошибок
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. Матрицы ошибок")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, res) in zip(axes, results.items()):
    ConfusionMatrixDisplay.from_predictions(
        y_test, res["y_pred"],
        display_labels=["Нет болезни", "Есть болезнь"],
        ax=ax,
        colorbar=False,
    )
    ax.set_title(f"{name}\nF1={res['f1']:.3f}, AUC={res['roc_auc']:.3f}")
plt.suptitle("Матрицы ошибок — бинарная классификация", fontsize=13)
plt.tight_layout()
plt.savefig(FIG / "01_confusion_matrices.png", dpi=120, bbox_inches="tight")
plt.close()
print("Матрицы ошибок сохранены.")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Графики — ROC-кривые
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. ROC-кривые")
print("=" * 60)

colors = ["steelblue", "tomato", "seagreen"]
plt.figure(figsize=(7, 6))
for (name, res), color in zip(results.items(), colors):
    fpr, tpr, _ = roc_curve(y_test, res["y_prob"])
    plt.plot(fpr, tpr, lw=2, color=color,
             label=f"{name} (AUC={res['roc_auc']:.3f})")
plt.plot([0, 1], [0, 1], "k--", lw=1, label="Случайная (AUC=0.5)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC-кривые — сравнение моделей")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(FIG / "02_roc_curves.png", dpi=120, bbox_inches="tight")
plt.close()
print("ROC-кривые сохранены.")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Сводная таблица метрик
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. Сводная таблица метрик")
print("=" * 60)

summary = pd.DataFrame(
    {name: {k: v for k, v in res.items() if k not in ("model", "y_pred", "y_prob")}
     for name, res in results.items()}
).T
summary = summary.astype(float).round(4)
print(summary.to_string())


# ─────────────────────────────────────────────────────────────────────────────
# 8. Гистограмма F1-score
# ─────────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 4))
names = list(results.keys())
metrics_to_plot = ["accuracy", "precision", "recall", "f1", "roc_auc"]
x = np.arange(len(names))
width = 0.15
colors_m = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

for i, metric in enumerate(metrics_to_plot):
    vals = [results[n][metric] for n in names]
    ax.bar(x + i * width, vals, width, label=metric.upper(), color=colors_m[i], alpha=0.85)

ax.set_xticks(x + width * 2)
ax.set_xticklabels(names, rotation=10, ha="right")
ax.set_ylim(0, 1.15)
ax.set_ylabel("Значение метрики")
ax.set_title("Сравнение метрик классификации")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(FIG / "03_metrics_comparison.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nГистограмма метрик сохранена.")

print(f"\nВсе графики в: {FIG}")
