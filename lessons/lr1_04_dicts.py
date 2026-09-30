"""
ЛР1, типовое задание 4: словари.

Запустите файл: python lessons/lr1_04_dicts.py
"""

print("=== Словарь из строки: символ -> сколько раз встретился ===")
s = "Never look back"
freq = {}
for ch in s:
    freq[ch] = freq.get(ch, 0) + 1
print(freq)

print("\n=== Два списка -> словарь ===")
keys = ["a", "b", "c"]
values = [1, 2, 3]
print(dict(zip(keys, values)))

print("\n=== Сортировка по значению ===")
d = {"a": 50, "b": 5, "c": 56, "d": 4, "e": 58, "f": 20}
asc = dict(sorted(d.items(), key=lambda item: item[1]))
desc = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
print("возрастание:", asc)
print("убывание:", desc)

print("\n=== Три ключа с наибольшими / наименьшими значениями ===")
items = sorted(d.items(), key=lambda item: item[1])
print("три минимальных:", items[:3])
print("три максимальных:", items[-3:])

print("\n=== Слияние словарей ===")
print({**{"x": 1}, **{"y": 2, "x": 9}})

print("\n=== Частоты цифр (ключи int) ===")
seq = "01550329"
digit_map = {}
for ch in seq:
    key = int(ch)
    digit_map[key] = digit_map.get(key, 0) + 1
print(digit_map)

print("\n=== Анаграммы ===")


def is_anagram(a: str, b: str) -> bool:
    return sorted(a.lower()) == sorted(b.lower())


print("live / evil:", is_anagram("live", "evil"))

print("\n=== Scrabble (английские буквы) ===")
SCORES = {}
for letters, score in (
    ("AEIOULNSTR", 1),
    ("DG", 2),
    ("BCMP", 3),
    ("FHVWY", 4),
    ("K", 5),
    ("JX", 8),
    ("QZ", 10),
):
    for letter in letters:
        SCORES[letter] = score

word = "hello"
print(word, "очки =", sum(SCORES.get(ch.upper(), 0) for ch in word))

print("\nКак решать своё задание 4:")
print("1) Словарь: {ключ: значение}. Ключ уникален.")
print("2) d[key] = value записывает, d.get(key, 0) читает с запасным нулём.")
print("3) items(), keys(), values() — обход. zip соединяет два списка.")
