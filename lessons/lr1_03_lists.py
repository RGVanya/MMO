"""
ЛР1, типовое задание 3: списки.

Запустите файл: python lessons/lr1_03_lists.py
"""

nums = [3, 0, -2, 5, 0, 8, -1, 5, 4]
print("Список:", nums)

print("\n=== Индексы: чётные / нечётные номера ===")
# В заданиях «нечётные номера» часто имеют в виду 1, 3, 5... как у людей,
# то есть индексы 0, 2, 4 в Python. Уточняйте по формулировке.
print("элементы с нечётным индексом Python:", nums[1::2])

print("\n=== Суммы и произведения ===")
positive = [x for x in nums if x > 0]
negative = [x for x in nums if x < 0]
print("сумма положительных:", sum(positive))
print("сумма отрицательных:", sum(negative))

print("\n=== Между двумя нулями ===")
if nums.count(0) >= 2:
    a = nums.index(0)
    b = nums.index(0, a + 1)
    print("между первыми нулями:", nums[a + 1 : b], "сумма =", sum(nums[a + 1 : b]))
else:
    print("двух нулей нет")

print("\n=== После первого нуля ===")
if 0 in nums:
    print(sum(nums[nums.index(0) + 1 :]))

print("\n=== Чётный минимум / максимум ===")
evens = [x for x in nums if x % 2 == 0]
print("мин. чётный:", min(evens) if evens else nums[0])

print("\n=== Нули вперёд, остальные как есть ===")
zeros = [x for x in nums if x == 0]
rest = [x for x in nums if x != 0]
print(zeros + rest)

print("\n=== Уникальные и повторы ===")
print("только один раз:", [x for x in nums if nums.count(x) == 1])
# пары равных: для каждого значения k штук даёт k*(k-1)//2 пар
from collections import Counter

pairs = sum(c * (c - 1) // 2 for c in Counter(nums).values())
print("число пар равных элементов:", pairs)

print("\n=== Смешанный список: числа и слова ===")
mixed = [13, 56, "Python", 34, 19, "love"]
for item in mixed:
    if isinstance(item, int):
        if item % 2 == 0:
            s = 0
            t = item
            while t:
                s += t % 10
                t //= 10
            print(item, "чётное, сумма цифр =", s)
        else:
            print(item, "нечётное")
    else:
        print(item, "слово, длина =", len(item))

print("\n=== Кубы n чисел и разворот ===")
source = [1, 2, 3, 4]
cubes = [x ** 3 for x in source]
print(cubes, "сумма", sum(cubes), "наоборот", cubes[::-1])

print("\nКак решать своё задание 3:")
print("1) Создать список: вручную или циклом input.")
print("2) Не меняйте исходный список вслепую: сначала посчитайте, потом преобразуйте.")
print("3) Полезное: min, max, sum, count, index, срезы, list comprehension.")
