# Задание 1
def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def primes_in_range(start, end):
    if start > end:
        start, end = end, start
    return [x for x in range(start, end + 1) if is_prime(x)]


def task1():
    try:
        start = int(input("Начало диапазона: "))
        end = int(input("Конец диапазона: "))
        print("Простые числа:", primes_in_range(start, end))
    except ValueError:
        print("Нужно ввести целые числа")
    finally:
        print("Задание 1 завершено")


# Задание 2
def handle_value(value):
    if isinstance(value, dict):
        values = sorted(value.values(), reverse=True)[:3]
        print("Три наибольших значения:", values)
        return values
    if isinstance(value, list):
        data = value.copy()
        product = 1
        for i in range(0, len(data), 2):
            product *= data[i]
        print("Произведение элементов с нечётными номерами:", product)
        if data:
            data.remove(max(data))
        print("Список без наибольшего элемента:", data)
        return product, data
    if isinstance(value, int):
        n = abs(value)
        total = 0
        if n == 0:
            total = 0
        while n > 0:
            total += n % 10
            n //= 10
        print("Сумма цифр:", total)
        return total
    if isinstance(value, str):
        vowels_set = set("аеёиоуыэюяaeiouy")
        vowels = consonants = 0
        for ch in value.lower():
            if not ch.isalpha():
                continue
            if ch in vowels_set:
                vowels += 1
            else:
                consonants += 1
        words = len(value.split())
        print(f"Гласных: {vowels}, согласных: {consonants}, слов: {words}")
        return vowels, consonants, words
    print("Неизвестный тип")
    return None


def task2():
    try:
        print("Проверка списка:")
        handle_value([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print("\nПроверка словаря:")
        handle_value({"a": 50, "b": 5, "c": 56, "d": 4, "e": 58, "f": 20})
        print("\nПроверка числа:")
        handle_value(2547)
        print("\nПроверка строки:")
        handle_value("Hello World")
    except TypeError as error:
        print("Ошибка типа:", error)
    finally:
        print("Задание 2 завершено")


# Задание 3
def first_negative_column(matrix):
    if not matrix:
        return None, None
    rows = len(matrix)
    cols = len(matrix[0])
    for j in range(cols):
        column = [matrix[i][j] for i in range(rows)]
        if all(x < 0 for x in column):
            mean = sum(column) / len(column)
            return j, mean
    return None, None


def task3():
    matrix = [
        [1, -2, -5],
        [3, -3, -1],
        [4, -4, -7],
    ]
    try:
        print("Матрица:")
        for row in matrix:
            print(*row)
        index, mean = first_negative_column(matrix)
        if index is None:
            print("Нет столбца, где все элементы отрицательные")
        else:
            print("Первый отрицательный столбец (номер с нуля):", index)
            print("Среднее арифметическое:", mean)
    except ZeroDivisionError:
        print("Нельзя посчитать среднее")
    finally:
        print("Задание 3 завершено")


# Задание 4
def task4():
    try:
        a = int(input("Первое число: "))
        b = int(input("Второе число: "))
        print("Частное:", a / b)
    except ValueError:
        print("Ошибка: нужно ввести числа")
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
    finally:
        print("Блок finally выполнился в любом случае")


def main():
    tasks = {
        "1": task1,
        "2": task2,
        "3": task3,
        "4": task4,
    }

    while True:
        print("\nВариант 27, файл 2")
        print("1-4 — запустить задание")
        print("0 — выход")
        choice = input("Номер задания: ").strip()
        if choice == "0":
            break
        task = tasks.get(choice)
        if task is None:
            print("Нет такого задания")
            continue
        print()
        task()


if __name__ == "__main__":
    main()
