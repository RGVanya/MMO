# -*- coding: utf-8 -*-
"""Лабораторная 2: подготовка данных. Запуск: python lab2.py"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


def save(name):
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=120, bbox_inches="tight")
    plt.close()


df = pd.read_csv(ROOT / "data" / "train.csv")
print("1. Загружен датасет:", df.shape)
print(df.head())
print()
df.info()
print()
print(df.describe().T)

missing = pd.DataFrame(
    {"пропусков": df.isna().sum(), "доля, %": (df.isna().mean() * 100).round(2)}
)
print("\n2. Пропуски:")
print(missing[missing["пропусков"] > 0])

plt.figure(figsize=(12, 5))
sns.heatmap(df.isna(), cbar=False, yticklabels=False)
plt.title("Тепловая карта пропусков (до обработки)")
save("01_missing_before.png")

suspect = [
    "Rooms",
    "Square",
    "LifeSquare",
    "KitchenSquare",
    "Floor",
    "HouseFloor",
    "HouseYear",
    "Price",
]
print("\nСтатистики подозрительных столбцов:")
print(df[suspect].describe().T)

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, col in zip(axes.ravel(), suspect):
    ax.hist(df[col].dropna(), bins=40, color="steelblue", edgecolor="white")
    ax.set_title(col)
plt.suptitle("Распределения числовых признаков (до обработки)")
save("02_hist_before.png")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, col in zip(axes.ravel(), suspect):
    ax.boxplot(df[col].dropna(), orientation="vertical")
    ax.set_title(col)
plt.suptitle("BoxPlot числовых признаков (до обработки)")
save("03_box_before.png")


def iqr_bounds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


print("\nЧисло точек за границами IQR:")
for col in suspect:
    low, high = iqr_bounds(df[col].dropna())
    n = ((df[col] < low) | (df[col] > high)).sum()
    print(f"  {col:15s}: {n:5d}   границы [{low:.2f}; {high:.2f}]")

df_clean = df.copy()
df_clean.loc[df_clean["HouseYear"] == 20052011, "HouseYear"] = 2005
df_clean.loc[df_clean["HouseYear"] == 4968, "HouseYear"] = 1968
df_clean["HouseYear"] = df_clean["HouseYear"].clip(1910, 2020)

rooms_median = df_clean["Rooms"].median()
df_clean.loc[df_clean["Rooms"] < 1, "Rooms"] = 1
df_clean.loc[df_clean["Rooms"] > 6, "Rooms"] = rooms_median

df_clean.loc[df_clean["HouseFloor"] <= 0, "HouseFloor"] = df_clean["Floor"]
too_high = df_clean["Floor"] > df_clean["HouseFloor"]
df_clean.loc[too_high, "HouseFloor"] = df_clean.loc[too_high, "Floor"]

df_clean.loc[df_clean["KitchenSquare"] > df_clean["Square"], "KitchenSquare"] = np.nan
df_clean.loc[df_clean["LifeSquare"] > df_clean["Square"], "LifeSquare"] = np.nan

for col in ["Square", "LifeSquare", "KitchenSquare", "HouseFloor", "Price"]:
    low, high = iqr_bounds(df_clean[col].dropna())
    df_clean[col] = df_clean[col].clip(lower=max(low, 0), upper=high)

df_clean["Healthcare_1"] = df_clean["Healthcare_1"].fillna(df_clean["Healthcare_1"].median())
ratio = (df_clean["LifeSquare"] / df_clean["Square"]).median()
df_clean["LifeSquare"] = df_clean["LifeSquare"].fillna(df_clean["Square"] * ratio)
df_clean["LifeSquare"] = df_clean["LifeSquare"].fillna(df_clean["LifeSquare"].median())
df_clean["KitchenSquare"] = df_clean["KitchenSquare"].fillna(df_clean["KitchenSquare"].median())

print("\nПропусков после обработки:", int(df_clean.isna().sum().sum()))
print(df_clean[suspect].describe().T)

plt.figure(figsize=(12, 5))
sns.heatmap(df_clean.isna(), cbar=False, yticklabels=False)
plt.title("Тепловая карта пропусков (после обработки)")
save("04_missing_after.png")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, col in zip(axes.ravel(), suspect):
    ax.boxplot(df_clean[col].dropna(), orientation="vertical")
    ax.set_title(col)
plt.suptitle("BoxPlot после устранения выбросов")
save("05_box_after.png")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, col in zip(axes.ravel(), suspect):
    ax.hist(df_clean[col].dropna(), bins=40, color="seagreen", edgecolor="white")
    ax.set_title(col)
plt.suptitle("Распределения после обработки")
save("06_hist_after.png")

df_clean["LifeSquare_was_missing"] = df["LifeSquare"].isna().astype(int)
df_clean["HouseAge"] = 2020 - df_clean["HouseYear"]
df_clean["PricePerSqM"] = df_clean["Price"] / df_clean["Square"]
df_clean["KitchenShare"] = df_clean["KitchenSquare"] / df_clean["Square"]
df_clean["LifeSquareShare"] = df_clean["LifeSquare"] / df_clean["Square"]
print("\n3. Новые признаки:")
print(df_clean[["HouseAge", "PricePerSqM", "KitchenShare", "LifeSquareShare", "LifeSquare_was_missing"]].head())

df_clean["Shops_2"] = df_clean["Shops_2"].map({"A": 0, "B": 1})
df_clean = pd.get_dummies(df_clean, columns=["Ecology_2", "Ecology_3"], drop_first=True)
df_clean = df_clean.drop(columns=["Id"])
print("Столбцы после кодирования:", df_clean.columns.tolist())

binary_cols = ["Shops_2", "Ecology_2_B", "Ecology_3_B", "LifeSquare_was_missing"]
num_cols = [c for c in df_clean.columns if c not in binary_cols]

df_std = df_clean.copy()
df_mm = df_clean.copy()
df_std[num_cols] = StandardScaler().fit_transform(df_clean[num_cols])
df_mm[num_cols] = MinMaxScaler().fit_transform(df_clean[num_cols])

print("\n4. После стандартизации (mean ~ 0, std ~ 1):")
print(df_std[num_cols].describe().T[["mean", "std", "min", "max"]].round(3))
print("\nПосле нормализации (min = 0, max = 1):")
print(df_mm[num_cols].describe().T[["mean", "std", "min", "max"]].round(3))

compare_cols = ["Square", "Price", "HouseAge", "PricePerSqM"]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, col in zip(axes.ravel(), compare_cols):
    ax.hist(df_std[col], bins=30, alpha=0.7, label="стандартизация")
    ax.hist(df_mm[col], bins=30, alpha=0.7, label="нормализация")
    ax.set_title(col)
    ax.legend()
plt.suptitle("Сравнение масштабов после StandardScaler и MinMaxScaler")
save("07_scaling.png")

print("\nГотово. Графики в папке figures")
print("Итоговая таблица:", df_clean.shape)
