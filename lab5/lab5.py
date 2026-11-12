# -*- coding: utf-8 -*-
"""
Лабораторная работа 5 — Дерево решений (реализация с нуля).

Реализованы:
  1. gini(labels)               — критерий Джини
  2. gain(left, right, root_g)  — прирост информации
  3. build_tree(data, labels)   — критерии останова: max_depth, min_samples
  4. accuracy_metric(actual, predicted)

Запуск: python lab5/lab5.py
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


# ─────────────────────────────────────────────────────────────────────────────
# Узел и лист дерева (из шаблона задания)
# ─────────────────────────────────────────────────────────────────────────────

class Node:
    """Внутренний узел дерева решений."""
    def __init__(self, index, t, true_branch, false_branch):
        self.index = index          # индекс признака для сравнения
        self.t = t                  # порог
        self.true_branch = true_branch    # поддерево x <= t
        self.false_branch = false_branch  # поддерево x > t


class Leaf:
    """Терминальный узел (лист) дерева решений."""
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        self.prediction = self.predict()

    def predict(self):
        """Возвращает класс с наибольшим числом объектов в листе."""
        classes: dict = {}
        for label in self.labels:
            if label not in classes:
                classes[label] = 0
            classes[label] += 1
        return max(classes, key=classes.get)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Критерий Джини
# ─────────────────────────────────────────────────────────────────────────────

def gini(labels) -> float:
    """
    Вычисляет индекс Джини для набора меток.

    Gini(S) = 1 - Σ p_k²

    где p_k — доля объектов класса k среди всех объектов в S.
    Значение 0 — идеально чистый узел, 0.5 — максимальная примесь (2 класса, 50/50).

    Параметры
    ----------
    labels : array-like, метки классов объектов в узле

    Возвращает
    ----------
    float : индекс Джини ∈ [0, 1)
    """
    labels = np.asarray(labels)
    n = len(labels)
    if n == 0:
        return 0.0

    classes, counts = np.unique(labels, return_counts=True)
    probs = counts / n
    return float(1.0 - np.sum(probs ** 2))


# ─────────────────────────────────────────────────────────────────────────────
# 2. Прирост информации (Information Gain)
# ─────────────────────────────────────────────────────────────────────────────

def gain(left_labels, right_labels, root_gini: float) -> float:
    """
    Вычисляет прирост информации при разбиении узла.

    Gain = Gini(root) - (|left|/(|left|+|right|)) * Gini(left)
                      - (|right|/(|left|+|right|)) * Gini(right)

    Параметры
    ----------
    left_labels  : метки левого потомка (x <= t)
    right_labels : метки правого потомка (x > t)
    root_gini    : индекс Джини родительского узла

    Возвращает
    ----------
    float : прирост информации ≥ 0
    """
    left_labels = np.asarray(left_labels)
    right_labels = np.asarray(right_labels)
    n_left = len(left_labels)
    n_right = len(right_labels)
    n_total = n_left + n_right

    # Если одна из ветвей пустая — разбиение не произошло, прироста нет
    if n_total == 0 or n_left == 0 or n_right == 0:
        return 0.0

    weighted_gini = (
        (n_left / n_total) * gini(left_labels)
        + (n_right / n_total) * gini(right_labels)
    )
    return float(root_gini - weighted_gini)


# ─────────────────────────────────────────────────────────────────────────────
# Разбиение датасета в узле (из шаблона задания)
# ─────────────────────────────────────────────────────────────────────────────

def split(data, labels, column_index, t):
    """Делит данные по признаку column_index и порогу t."""
    left = np.where(data[:, column_index] <= t)
    right = np.where(data[:, column_index] > t)
    true_data = data[left]
    false_data = data[right]
    true_labels = labels[left]
    false_labels = labels[right]
    return true_data, false_data, true_labels, false_labels


# ─────────────────────────────────────────────────────────────────────────────
# Нахождение наилучшего разбиения (из шаблона, дополнено min_samples_leaf)
# ─────────────────────────────────────────────────────────────────────────────

def find_best_split(data, labels, min_samples_leaf: int = 1):
    """
    Перебирает все признаки и пороги, выбирает разбиение с максимальным Gain.

    Параметры
    ----------
    min_samples_leaf : минимальное число объектов в листе (критерий останова 1)
    """
    root_gini_val = gini(labels)
    best_gain = 0.0
    best_t = None
    best_index = None
    n_features = data.shape[1]

    for index in range(n_features):
        t_values = np.unique(data[:, index])
        for t in t_values:
            true_data, false_data, true_labels, false_labels = split(
                data, labels, index, t
            )
            # критерий останова 1: мин. объектов в листе
            if len(true_labels) < min_samples_leaf or len(false_labels) < min_samples_leaf:
                continue
            current_gain = gain(true_labels, false_labels, root_gini_val)
            if current_gain > best_gain:
                best_gain = current_gain
                best_t = t
                best_index = index

    return best_gain, best_t, best_index


# ─────────────────────────────────────────────────────────────────────────────
# Построение дерева с критериями останова
# ─────────────────────────────────────────────────────────────────────────────

def build_tree(
    data,
    labels,
    min_samples: int = 1,
    max_depth: int = None,
    _current_depth: int = 0,
):
    """
    Рекурсивно строит дерево решений.

    Критерии останова:
      1. min_samples — минимальное число объектов в узле (не разбиваем меньше)
      2. max_depth   — максимальная глубина дерева
      3. gain == 0   — разбиение не улучшает качество (базовый случай шаблона)

    Параметры
    ----------
    data         : матрица признаков
    labels       : метки классов
    min_samples  : мин. объектов для разбиения (критерий останова 1)
    max_depth    : макс. глубина (None = без ограничения) (критерий останова 2)
    _current_depth : служебный параметр рекурсии
    """
    # Критерий останова 2: достигнута максимальная глубина
    if max_depth is not None and _current_depth >= max_depth:
        return Leaf(data, labels)

    # Критерий останова 1: слишком мало объектов для разбиения
    if len(labels) < max(2, min_samples):
        return Leaf(data, labels)

    # Базовый случай из шаблона: ищем лучшее разбиение
    best_gain, t, index = find_best_split(data, labels, min_samples_leaf=1)

    # Критерий останова 3 (из шаблона): нет прироста качества
    if best_gain == 0:
        return Leaf(data, labels)

    true_data, false_data, true_labels, false_labels = split(data, labels, index, t)

    # Рекурсивно строим два поддерева
    true_branch = build_tree(
        true_data, true_labels,
        min_samples=min_samples, max_depth=max_depth,
        _current_depth=_current_depth + 1,
    )
    false_branch = build_tree(
        false_data, false_labels,
        min_samples=min_samples, max_depth=max_depth,
        _current_depth=_current_depth + 1,
    )

    return Node(index, t, true_branch, false_branch)


# ─────────────────────────────────────────────────────────────────────────────
# Классификация и предсказание (из шаблона)
# ─────────────────────────────────────────────────────────────────────────────

def classify_object(obj, node):
    """Рекурсивно классифицирует один объект, проходя по дереву."""
    if isinstance(node, Leaf):
        return node.prediction
    if obj[node.index] <= node.t:
        return classify_object(obj, node.true_branch)
    else:
        return classify_object(obj, node.false_branch)


def predict(data, tree):
    """Предсказывает классы для массива объектов."""
    return [classify_object(obj, tree) for obj in data]


# ─────────────────────────────────────────────────────────────────────────────
# Вывод структуры дерева (из шаблона)
# ─────────────────────────────────────────────────────────────────────────────

def print_tree(node, spacing=""):
    """Рекурсивно печатает структуру дерева."""
    if isinstance(node, Leaf):
        print(spacing + "Прогноз:", node.prediction)
        return
    print(spacing + "Индекс", str(node.index), "<=", str(node.t))
    print(spacing + "--> True:")
    print_tree(node.true_branch, spacing + "  ")
    print(spacing + "--> False:")
    print_tree(node.false_branch, spacing + "  ")


def tree_depth(node) -> int:
    """Возвращает глубину дерева."""
    if isinstance(node, Leaf):
        return 0
    return 1 + max(tree_depth(node.true_branch), tree_depth(node.false_branch))


# ─────────────────────────────────────────────────────────────────────────────
# 4. Метрика точности
# ─────────────────────────────────────────────────────────────────────────────

def accuracy_metric(actual, predicted) -> float:
    """
    Вычисляет точность как долю правильно классифицированных объектов.

    Accuracy = (число правильных предсказаний) / (общее число объектов)

    Параметры
    ----------
    actual    : истинные метки классов
    predicted : предсказанные метки классов

    Возвращает
    ----------
    float : точность ∈ [0, 1]
    """
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)
    if len(actual) == 0:
        return 0.0
    return float(np.sum(actual == predicted) / len(actual))


# ─────────────────────────────────────────────────────────────────────────────
# Основной эксперимент
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Лабораторная работа 5 — Дерево решений")
    print("=" * 60)

    # ── Датасет ──────────────────────────────────────────────────────────────
    print("\n1. Генерация датасета")
    X, y = make_classification(
        n_samples=500,
        n_features=4,
        n_informative=3,
        n_redundant=1,
        random_state=RANDOM_STATE,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"Классы: {np.unique(y)}, баланс: {y.mean():.2f}")

    # ── Наше дерево ──────────────────────────────────────────────────────────
    print("\n2. Обучение самописного дерева решений")
    my_tree = build_tree(X_train, y_train, min_samples=3, max_depth=None)
    my_predictions = predict(X_test, my_tree)
    my_acc = accuracy_metric(y_test, my_predictions)
    depth = tree_depth(my_tree)
    print(f"Глубина дерева: {depth}")
    print(f"Accuracy (наше дерево): {my_acc:.4f}")

    # ── Структура дерева (первые уровни) ─────────────────────────────────────
    print("\n3. Структура дерева (первые 2 уровня):")
    # Печатаем только верхние уровни, чтобы не переполнять вывод
    def print_tree_limited(node, spacing="", max_levels=2, level=0):
        if level > max_levels:
            print(spacing + "... (обрезано)")
            return
        if isinstance(node, Leaf):
            print(spacing + "Прогноз:", node.prediction)
            return
        print(spacing + "Индекс", str(node.index), "<=", str(round(node.t, 4)))
        print(spacing + "--> True:")
        print_tree_limited(node.true_branch, spacing + "  ", max_levels, level + 1)
        print(spacing + "--> False:")
        print_tree_limited(node.false_branch, spacing + "  ", max_levels, level + 1)

    print_tree_limited(my_tree, max_levels=2)

    # ── sklearn дерево ───────────────────────────────────────────────────────
    print("\n4. Дерево из sklearn (criterion='gini')")
    sk_tree = DecisionTreeClassifier(criterion="gini", random_state=RANDOM_STATE)
    sk_tree.fit(X_train, y_train)
    sk_predictions = sk_tree.predict(X_test)
    sk_acc = accuracy_metric(y_test, sk_predictions)
    print(f"Accuracy (sklearn): {sk_acc:.4f}")
    print(f"Глубина (sklearn): {sk_tree.get_depth()}")

    # ── Сравнение ────────────────────────────────────────────────────────────
    print("\n5. Сравнение результатов")
    print(f"  Наше дерево: {my_acc:.4f}")
    print(f"  sklearn    : {sk_acc:.4f}")
    diff = abs(my_acc - sk_acc)
    print(f"  Разница    : {diff:.4f}  ({'OK — результаты близки' if diff < 0.05 else 'ВНИМАНИЕ — большое расхождение'})")

    # ── Эксперименты с max_depth ─────────────────────────────────────────────
    print("\n6. Эксперименты с max_depth")
    print(f"{'max_depth':>10} | {'Наше':>8} | {'sklearn':>8} | {'Глубина':>8}")
    print("-" * 42)
    for md in [1, 2, 3, 5, None]:
        t_custom = build_tree(X_train, y_train, min_samples=1, max_depth=md)
        t_sk = DecisionTreeClassifier(
            criterion="gini",
            max_depth=md,
            random_state=RANDOM_STATE,
        )
        t_sk.fit(X_train, y_train)
        acc_c = accuracy_metric(y_test, predict(X_test, t_custom))
        acc_s = accuracy_metric(y_test, t_sk.predict(X_test))
        depth_c = tree_depth(t_custom)
        label = str(md) if md else "None"
        print(f"{label:>10} | {acc_c:>8.4f} | {acc_s:>8.4f} | {depth_c:>8}")

    # ── Эксперименты с min_samples ───────────────────────────────────────────
    print("\n7. Эксперименты с min_samples (критерий останова)")
    print(f"{'min_samples':>12} | {'Accuracy':>8} | {'Глубина':>8}")
    print("-" * 38)
    for ms in [1, 3, 5, 10, 20]:
        t_ms = build_tree(X_train, y_train, min_samples=ms, max_depth=None)
        acc_ms = accuracy_metric(y_test, predict(X_test, t_ms))
        depth_ms = tree_depth(t_ms)
        print(f"{ms:>12} | {acc_ms:>8.4f} | {depth_ms:>8}")

    # ── Проверка unit-значений ────────────────────────────────────────────────
    print("\n8. Проверка корректности функций")
    g = gini([0, 0, 1, 1])
    print(f"  gini([0,0,1,1]) = {g:.4f}  (ожидается 0.5000)")
    assert abs(g - 0.5) < 1e-9, "gini ОШИБКА!"

    g_pure = gini([1, 1, 1, 1])
    print(f"  gini([1,1,1,1]) = {g_pure:.4f}  (ожидается 0.0000)")
    assert g_pure == 0.0, "gini чистого узла ОШИБКА!"

    acc_test = accuracy_metric([0, 1, 0, 1], [0, 1, 0, 0])
    print(f"  accuracy([0,1,0,1],[0,1,0,0]) = {acc_test:.4f}  (ожидается 0.7500)")
    assert abs(acc_test - 0.75) < 1e-9, "accuracy_metric ОШИБКА!"

    print("\nВсе проверки пройдены!")

    print("\n" + "=" * 60)
    print("Итог")
    print("=" * 60)
    print(f"  Accuracy нашего дерева : {my_acc:.4f}")
    print(f"  Accuracy sklearn       : {sk_acc:.4f}")
    print(f"  Разница                : {diff:.4f}")
    if diff < 0.02:
        print("  → Результаты практически совпадают ✓")
    else:
        print("  → Результаты близки, небольшое расхождение из-за порядка обхода")
