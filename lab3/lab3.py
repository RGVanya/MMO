# -*- coding: utf-8 -*-
"""
Лабораторная работа 3 — Градиентный спуск.
Вариант 27 (нечётный) → L2 регуляризация.

Запуск: python lab3/lab3.py
Графики сохраняются в lab3/figures/
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


# ─────────────────────────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────────────────────────

def add_bias(X: np.ndarray) -> np.ndarray:
    """Добавляет столбец единиц (свободный член) к матрице признаков."""
    return np.hstack([np.ones((X.shape[0], 1)), X])


def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Среднеквадратичная ошибка (MSE)."""
    return float(np.mean((y_true - y_pred) ** 2))


# ─────────────────────────────────────────────────────────────────────────────
# 1. Пакетный градиентный спуск (Batch GD)
# ─────────────────────────────────────────────────────────────────────────────

def gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    lr: float = 0.01,
    n_iter: int = 1000,
    eps: float = 1e-6,
) -> tuple[np.ndarray, list[float]]:
    """
    Пакетный градиентный спуск для линейной регрессии.

    Алгоритм:
        w_new = w - lr * (2/n) * X^T (X w - y)
    Останов: ||w_new - w|| < eps  ИЛИ  достигнуто n_iter итераций.

    Параметры
    ----------
    X : матрица признаков БЕЗ столбца единиц, (n, p)
    y : вектор целевой переменной, (n,)
    lr : шаг обучения (learning rate)
    n_iter : максимальное количество итераций
    eps : порог останова по изменению весов

    Возвращает
    ----------
    weights : финальные веса [w0, w1, ..., wp], форма (p+1,)
    history : список MSE на каждой итерации
    """
    Xb = add_bias(X)
    n, p = Xb.shape
    w = np.zeros(p)
    history: list[float] = []

    for _ in range(n_iter):
        y_pred = Xb @ w
        history.append(mse(y, y_pred))
        grad = (2 / n) * Xb.T @ (y_pred - y)
        w_new = w - lr * grad
        if np.linalg.norm(w_new - w) < eps:
            w = w_new
            break
        w = w_new

    return w, history


# ─────────────────────────────────────────────────────────────────────────────
# 2. Стохастический градиентный спуск (SGD)
# ─────────────────────────────────────────────────────────────────────────────

def stochastic_gd(
    X: np.ndarray,
    y: np.ndarray,
    lr: float = 0.01,
    n_iter: int = 1000,
    eps: float = 1e-6,
) -> tuple[np.ndarray, list[float]]:
    """
    Стохастический градиентный спуск для линейной регрессии.

    На каждой итерации выбирается ОДИН случайный объект.
    Останов: ||w_new - w|| < eps  ИЛИ  достигнуто n_iter итераций.

    Возвращает
    ----------
    weights : финальные веса [w0, w1, ..., wp], форма (p+1,)
    history : список MSE по ВСЕЙ выборке на каждой итерации
    """
    Xb = add_bias(X)
    n, p = Xb.shape
    w = np.zeros(p)
    history: list[float] = []

    rng = np.random.default_rng(RANDOM_STATE)

    for _ in range(n_iter):
        history.append(mse(y, Xb @ w))
        i = rng.integers(0, n)
        xi = Xb[i]
        yi = y[i]
        grad = 2 * xi * (xi @ w - yi)
        w_new = w - lr * grad
        if np.linalg.norm(w_new - w) < eps:
            w = w_new
            break
        w = w_new

    return w, history


# ─────────────────────────────────────────────────────────────────────────────
# 3. Градиентный спуск с L2-регуляризацией (Ridge)
#    Вариант 27 — нечётный → L2
# ─────────────────────────────────────────────────────────────────────────────

def gradient_descent_l2(
    X: np.ndarray,
    y: np.ndarray,
    lr: float = 0.01,
    n_iter: int = 1000,
    eps: float = 1e-6,
    lam: float = 1.0,
) -> tuple[np.ndarray, list[float]]:
    """
    Пакетный GD с L2-регуляризацией (Ridge / Тихонов).

    Целевая функция:  L = MSE + λ * ||w||²  (свободный член НЕ регуляризируется)
    Градиент:         ∂L/∂w = (2/n) X^T(Xw - y) + 2λ w
                      ∂L/∂w0 = (2/n) * sum(Xw - y)  (без λ для w0)

    Параметры
    ----------
    lam : коэффициент регуляризации λ

    Возвращает
    ----------
    weights : финальные веса [w0, w1, ..., wp], форма (p+1,)
    history : список MSE (без штрафа) на каждой итерации
    """
    Xb = add_bias(X)
    n, p = Xb.shape
    w = np.zeros(p)
    history: list[float] = []

    # маска: не регуляризируем свободный член w[0]
    reg_mask = np.ones(p)
    reg_mask[0] = 0.0

    # При большом λ нужен меньший шаг, чтобы гарантировать сходимость.
    # Условие устойчивости: lr_eff * 2 * lam < 1  ⟹  lr_eff < 1/(2λ).
    lr_eff = lr / max(1.0, 2.0 * lam * lr)

    for _ in range(n_iter):
        y_pred = Xb @ w
        history.append(mse(y, y_pred))
        grad = (2 / n) * Xb.T @ (y_pred - y) + 2 * lam * reg_mask * w
        w_new = w - lr_eff * grad
        if np.linalg.norm(w_new - w) < eps:
            w = w_new
            break
        w = w_new

    return w, history


# ─────────────────────────────────────────────────────────────────────────────
# Подготовка данных
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("1. Генерация и подготовка датасета")
print("=" * 60)

X_raw, y_raw = make_regression(
    n_samples=300, n_features=3, noise=15, random_state=RANDOM_STATE
)
print(f"Датасет: {X_raw.shape[0]} объектов, {X_raw.shape[1]} признака")

X_train_r, X_test_r, y_train, y_test = train_test_split(
    X_raw, y_raw, test_size=0.2, random_state=RANDOM_STATE
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_r)
X_test = scaler.transform(X_test_r)

print(f"Обучающая выборка: {X_train.shape}, тестовая: {X_test.shape}")


# ─────────────────────────────────────────────────────────────────────────────
# Эксперимент 1: разные learning rate для пакетного GD
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. Эксперимент: влияние скорости обучения (lr) — пакетный GD")
print("=" * 60)

lr_values = [0.001, 0.01, 0.1]
N_ITER = 500

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)
results_lr: dict[float, tuple[np.ndarray, list[float]]] = {}

for ax, lr in zip(axes, lr_values):
    w, hist = gradient_descent(X_train, y_train, lr=lr, n_iter=N_ITER, eps=1e-8)
    results_lr[lr] = (w, hist)
    y_pred_test = add_bias(X_test) @ w
    test_mse = mse(y_test, y_pred_test)
    ax.plot(hist, color="steelblue")
    ax.set_title(f"lr = {lr}\nTest MSE = {test_mse:.1f}")
    ax.set_xlabel("Итерация")
    ax.set_ylabel("MSE (обучение)")
    ax.set_yscale("log")
    print(f"  lr={lr:5.3f}: итераций={len(hist):4d}, train MSE={hist[-1]:.2f}, test MSE={test_mse:.2f}")

plt.suptitle("Пакетный GD — влияние скорости обучения", fontsize=13)
plt.tight_layout()
plt.savefig(FIG / "01_gd_learning_rate.png", dpi=120, bbox_inches="tight")
plt.close()
print("Вывод: при lr=0.001 сходимость медленная; lr=0.1 — быстрая, но может расходиться при плохой инициализации.")


# ─────────────────────────────────────────────────────────────────────────────
# Эксперимент 2: GD vs SGD на одном графике
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. GD vs SGD — сравнение сходимости")
print("=" * 60)

LR_BEST = 0.01
N_COMPARE = 300

w_gd, hist_gd = gradient_descent(X_train, y_train, lr=LR_BEST, n_iter=N_COMPARE, eps=1e-10)
w_sgd, hist_sgd = stochastic_gd(X_train, y_train, lr=LR_BEST, n_iter=N_COMPARE, eps=1e-10)

mse_gd_test = mse(y_test, add_bias(X_test) @ w_gd)
mse_sgd_test = mse(y_test, add_bias(X_test) @ w_sgd)

print(f"GD  → train MSE={hist_gd[-1]:.2f}, test MSE={mse_gd_test:.2f}, весов: {w_gd}")
print(f"SGD → train MSE={hist_sgd[-1]:.2f}, test MSE={mse_sgd_test:.2f}, весов: {w_sgd}")

plt.figure(figsize=(9, 4))
plt.plot(hist_gd, label=f"Batch GD (lr={LR_BEST})", color="steelblue", lw=2)
plt.plot(hist_sgd, label=f"SGD (lr={LR_BEST})", color="tomato", lw=1.5, alpha=0.85)
plt.xlabel("Итерация")
plt.ylabel("MSE")
plt.title("Batch GD vs Стохастический GD — кривые MSE")
plt.legend()
plt.yscale("log")
plt.tight_layout()
plt.savefig(FIG / "02_gd_vs_sgd.png", dpi=120, bbox_inches="tight")
plt.close()
print("Вывод: GD сходится плавно; SGD осциллирует, но достигает сопоставимого MSE.")


# ─────────────────────────────────────────────────────────────────────────────
# Сравнение с sklearn LinearRegression
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. Сравнение с sklearn LinearRegression")
print("=" * 60)

sk_model = LinearRegression()
sk_model.fit(X_train, y_train)
mse_sklearn = mse(y_test, sk_model.predict(X_test))

print(f"sklearn MSE (test): {mse_sklearn:.2f}")
print(f"GD      MSE (test): {mse_gd_test:.2f}")
print(f"SGD     MSE (test): {mse_sgd_test:.2f}")
ratio_gd = mse_gd_test / mse_sklearn
ratio_sgd = mse_sgd_test / mse_sklearn
print(f"GD/sklearn: {ratio_gd:.3f}  (должно быть ≈ 1.0 ± 0.05)")
print(f"SGD/sklearn: {ratio_sgd:.3f}")


# ─────────────────────────────────────────────────────────────────────────────
# Эксперимент 3: L2-регуляризация — как веса меняются от λ
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. L2-регуляризация (Ridge) — зависимость весов от λ")
print("=" * 60)

lambdas = np.logspace(-3, 3, 20)
all_weights: list[np.ndarray] = []
mse_train_l2: list[float] = []
mse_test_l2: list[float] = []

for lam in lambdas:
    w_l2, hist_l2 = gradient_descent_l2(
        X_train, y_train, lr=0.01, n_iter=2000, eps=1e-8, lam=lam
    )
    all_weights.append(w_l2)
    mse_train_l2.append(mse(y_train, add_bias(X_train) @ w_l2))
    mse_test_l2.append(mse(y_test, add_bias(X_test) @ w_l2))

weights_arr = np.array(all_weights)  # (20, p+1)

# График весов от λ (пропускаем w0 — свободный член)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors = ["steelblue", "tomato", "seagreen"]
for i in range(1, weights_arr.shape[1]):
    ax1.plot(lambdas, weights_arr[:, i], marker="o", ms=4,
             label=f"w{i}", color=colors[i - 1])
ax1.set_xscale("log")
ax1.set_xlabel("λ (коэффициент L2)")
ax1.set_ylabel("Значение веса")
ax1.set_title("Веса модели vs λ (L2-регуляризация)")
ax1.legend()
ax1.axhline(0, color="black", lw=0.8, ls="--")

ax2.plot(lambdas, mse_train_l2, marker="s", ms=4, label="Train MSE", color="steelblue")
ax2.plot(lambdas, mse_test_l2, marker="^", ms=4, label="Test MSE", color="tomato")
ax2.set_xscale("log")
ax2.set_xlabel("λ (коэффициент L2)")
ax2.set_ylabel("MSE")
ax2.set_title("MSE vs λ (L2-регуляризация)")
ax2.legend()

plt.tight_layout()
plt.savefig(FIG / "03_l2_regularization.png", dpi=120, bbox_inches="tight")
plt.close()

idx_lambda1 = int(np.argmin(np.abs(lambdas - 1.0)))
print(f"λ={lambdas[0]:.4f}: веса = {weights_arr[0, 1:]}")
print(f"λ={lambdas[-1]:.1f}: веса = {weights_arr[-1, 1:]}  (должны → 0)")
print("Вывод: с ростом λ веса стягиваются к 0; при очень большом λ модель недообучена.")


# ─────────────────────────────────────────────────────────────────────────────
# Итоговый отчёт
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("Итог")
print("=" * 60)
print(f"sklearn  test MSE : {mse_sklearn:.2f}")
print(f"GD       test MSE : {mse_gd_test:.2f}  (lr={LR_BEST}, {len(hist_gd)} ит.)")
print(f"SGD      test MSE : {mse_sgd_test:.2f}  (lr={LR_BEST}, {len(hist_sgd)} ит.)")
print(f"L2 (λ≈1) test MSE : {mse_test_l2[idx_lambda1]:.2f}  (λ={lambdas[idx_lambda1]:.3f})")
print(f"\nГрафики сохранены в {FIG}")
