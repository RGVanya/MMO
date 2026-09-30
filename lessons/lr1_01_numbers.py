"""
ЛР1, типовое задание 1: числа, цифры, простые числа, циклы.

Запустите файл: python lessons/lr1_01_numbers.py
Это учебные примеры, не готовый ответ вашего варианта.
"""

print("=== 1. Ввод числа ===")
# input() всегда возвращает строку. int() превращает её в целое число.
# Пример: text = input("Число: "); n = int(text)

n = 2547
print("Пример числа:", n)

print("\n=== 2. Разбор числа на цифры ===")
# n % 10  — последняя цифра
# n // 10 — число без последней цифры
digits = []
temp = n
while temp > 0:
    digits.append(temp % 10)
    temp //= 10
digits.reverse()
print("Цифры:", digits)

print("\n=== 3. Чётные и нечётные цифры ===")
# Чётная цифра: d % 2 == 0
even = [d for d in digits if d % 2 == 0]
odd = [d for d in digits if d % 2 == 1]
print("Чётные:", even, "сумма =", sum(even))
print("Нечётные:", odd, "сумма =", sum(odd))

print("\n=== 4. Простое число ===")
# Простое: делится только на 1 и на себя. 0 и 1 не простые.


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True


print("17 простое?", is_prime(17))
print("15 простое?", is_prime(15))

print("\n=== 5. Простые числа в диапазоне и n-е простое ===")
primes = [x for x in range(10, 30) if is_prime(x)]
print("Простые от 10 до 29:", primes)

found = []
x = 2
while len(found) < 10:
    if is_prime(x):
        found.append(x)
    x += 1
print("Первые 10 простых:", found)

print("\n=== 6. Делители числа ===")
number = 36
divisors = [d for d in range(1, number + 1) if number % d == 0]
print("Делители 36:", divisors)

print("\n=== 7. Секунды -> дни:часы:минуты:секунды ===")
total = 100000
days = total // 86400
hours = (total % 86400) // 3600
minutes = (total % 3600) // 60
seconds = total % 60
print(f"{days}:{hours:02d}:{minutes:02d}:{seconds:02d}")

print("\nКак решать своё задание 1:")
print("1) Понять, что дают на вход: одно число, диапазон, секунды...")
print("2) Выбрать цикл: while для разбора цифр, for для диапазона.")
print("3) Собрать нужную величину: сумму, количество, список простых.")
print("4) Вывести результат через print.")
