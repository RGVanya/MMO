"""
ЛР1, типовое задание 6: кортежи и множества.

Запустите файл: python lessons/lr1_06_tuples_sets.py
"""

print("=== Кортеж нельзя менять на месте ===")
# tuple — как список, но неизменяемый. Чтобы «отсортировать», делают новый.
t = (35, 78, 21, 37, 2)
print("min", min(t), "max", max(t), "индекс min", t.index(min(t)))

sorted_desc = tuple(sorted(t, reverse=True))
print("по убыванию:", sorted_desc, "первый", sorted_desc[0], "последний", sorted_desc[-1])

print("\n=== Два кортежа: сумма и склейка ===")
c1 = (35, 78, 21)
c2 = (45, 21, 124)
print("сумма c1", sum(c1), "сумма c2", sum(c2))
print("склейка:", c1 + c2)

print("\n=== Из текста в кортеж слов без знаков ===")
import string

text = "Hello, world! Python."
clean = text.translate(str.maketrans("", "", string.punctuation))
print(tuple(clean.split()))

print("\n=== Случайный кортеж ===")
import random

rnd = tuple(random.randint(1, 20) for _ in range(10))
print(rnd, "max", max(rnd), "min", min(rnd))

print("\n=== Множества ===")
a = {1, 2, 3, 4}
b = {3, 4, 5}
print("пересечение (есть и там, и там):", a & b)
print("только в первом:", a - b)
print("уникальные из списка наоборот:", tuple(list(dict.fromkeys([3, 1, 3, 2]))[::-1]))

print("\nКак решать своё задание 6:")
print("1) Кортеж создают скобками: (1, 2, 3).")
print("2) Нужен новый порядок — tuple(sorted(...)).")
print("3) Множества: &, |, -.")
