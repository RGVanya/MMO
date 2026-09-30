"""
ЛР1, типовое задание 2: строки, буквы, слова, регистр.

Запустите файл: python lessons/lr1_02_strings.py
"""

text = "Hello World 123"
print("Строка:", text)

print("\n=== Регистр и проверки символа ===")
ch = "A"
print(ch, "isalpha", ch.isalpha(), "isdigit", ch.isdigit())
print(ch, "islower", ch.islower(), "isupper", ch.isupper())
print("swapcase:", text.swapcase())
print("код Unicode 'A':", ord("A"), "обратно:", chr(65))

print("\n=== Гласные и согласные ===")
VOWELS = set("аеёиоуыэюяaeiouy")


def count_letters(s: str) -> tuple[int, int]:
    vowels = consonants = 0
    for ch in s.lower():
        if not ch.isalpha():
            continue
        if ch in VOWELS:
            vowels += 1
        else:
            consonants += 1
    return vowels, consonants


v, c = count_letters("Привет Python")
print("гласных =", v, "согласных =", c)

print("\n=== Слова ===")
# split() режет строку по пробелам
words = "Never look back".split()
print("слова:", words, "количество:", len(words))
print("чётной длины:", [w for w in words if len(w) % 2 == 0])
print("самое длинное:", max(words, key=len))

print("\n=== Палиндром ===")
# Слово читается одинаково слева направо и справа налево


def is_palindrome(word: str) -> bool:
    clean = "".join(ch.lower() for ch in word if ch.isalnum())
    return clean == clean[::-1]


print("шалаш:", is_palindrome("шалаш"))
print("python:", is_palindrome("python"))

print("\n=== Пары регистра рядом (пример HjkLM) ===")
word = "HjkLM"
lower_pairs = upper_pairs = 0
for a, b in zip(word, word[1:]):
    if a.islower() and b.islower():
        lower_pairs += 1
    if a.isupper() and b.isupper():
        upper_pairs += 1
print("нижний:", lower_pairs, "верхний:", upper_pairs)

print("\n=== Числа внутри строки ===")
import re

raw = "Цена 12 и ещё 300 рублей"
print(re.findall(r"\d+", raw))

print("\n=== Частота символов ===")
from collections import Counter

s = "hello"
print(dict(Counter(s)))
print("самый частый:", Counter(s).most_common(1))

print("\nКак решать своё задание 2:")
print("1) Считать строку: text = input()")
print("2) Пройти for ch in text или for word in text.split()")
print("3) Копить счётчики. Срезы: s[::-1] разворачивает строку.")
