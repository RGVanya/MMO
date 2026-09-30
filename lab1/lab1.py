"""Лабораторная работа 1. Вариант 27.

Часть 1 — базовые конструкции Python, часть 2 — функции и исключения,
часть 3 — классы и наследование. Запуск: python lab1.py
"""
import math


# --- Часть 1 ---


# Задание 1
def p1_task1():
    number = abs(int(input("Введите число: ")))
    even_count = 0
    odd_count = 0

    if number == 0:
        even_count = 1
    else:
        while number > 0:
            digit = number % 10
            if digit % 2 == 0:
                even_count += 1
            else:
                odd_count += 1
            number //= 10

    print(f"Четных цифр: {even_count}, нечетных: {odd_count}")


# Задание 2
def p1_task2():
    word = input("Введите слово: ")
    upper_count = 0
    lower_count = 0

    for i in range(len(word) - 1):
        if word[i].isupper() and word[i + 1].isupper():
            upper_count += 1
        elif word[i].islower() and word[i + 1].islower():
            lower_count += 1

    print(f"Пар верхнего регистра: {upper_count}, пар нижнего регистра: {lower_count}")
    print(f"Всего букв: {len(word)}")


# Задание 3
def p1_task3():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    product = 1
    for i in range(0, len(nums), 2):
        product *= nums[i]
    print("Произведение элементов с нечётными номерами:", product)

    max_element = max(nums)
    nums.remove(max_element)
    print("Список без наибольшего элемента:", nums)


# Задание 4
def p1_task4():
    my_dict = {" a": 50, " c": 5, "d": 56, " e": 4, "f": 58, "z": 20}
    sorted_dict = sorted(my_dict.items())
    print(sorted_dict[:3])


# Задание 5
def p1_task5():
    shop = {
        "кукла": ["пластик, ткань", 25, 12],
        "мяч": ["резина", 10, 20],
        "конструктор": ["пластик", 40, 8],
    }
    total = 0

    while True:
        print("\nМагазин игрушек")
        print("1. Просмотр описания")
        print("2. Просмотр цены")
        print("3. Просмотр количества")
        print("4. Всю информацию")
        print("5. Покупка")
        print("6. До свидания")
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            for name, data in shop.items():
                print(f"{name} — {data[0]}")
        elif choice == "2":
            for name, data in shop.items():
                print(f"{name} — {data[1]}")
        elif choice == "3":
            for name, data in shop.items():
                print(f"{name} — {data[2]}")
        elif choice == "4":
            for name, data in shop.items():
                print(f"{name}: состав — {data[0]}, цена — {data[1]}, остаток — {data[2]}")
        elif choice == "5":
            print("Покупка. Чтобы выйти, введите n")
            while True:
                name = input("Название игрушки: ").strip()
                if name.lower() == "n":
                    break
                if name not in shop:
                    print("Такой игрушки нет")
                    continue
                amount = int(input("Количество: "))
                if amount <= 0:
                    print("Количество должно быть больше 0")
                    continue
                if amount > shop[name][2]:
                    print("Не хватает на складе. Есть:", shop[name][2])
                    continue
                shop[name][2] -= amount
                cost = shop[name][1] * amount
                total += cost
                print("Сумма этой покупки:", cost, "Общая сумма:", total)
            print("Текущая сумма покупок:", total)
            print("Остатки:")
            for name, data in shop.items():
                print(f"{name} — {data[2]}")
        elif choice == "6":
            print("До свидания")
            print("Итог покупок:", total)
            print("Осталось в магазине:")
            for name, data in shop.items():
                print(f"{name} — {data[2]}")
            break
        else:
            print("Нет такого пункта")


# Задание 6
def p1_task6():
    numbers = (-2, -1, 4, 5, 6, -3, 8)
    print("Кортеж:", numbers)

    index = None
    for i, value in enumerate(numbers):
        if value > 0:
            index = i
            break

    if index is None or index == len(numbers) - 1:
        result = 0
    else:
        result = sum(numbers[index + 1 :])

    print("Сумма после первого положительного:", result)


# --- Часть 2 ---


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


# Задание 1
def p2_task1():
    try:
        start = int(input("Начало диапазона: "))
        end = int(input("Конец диапазона: "))
        print("Простые числа:", primes_in_range(start, end))
    except ValueError:
        print("Нужно ввести целые числа")
    finally:
        print("Задание 1 завершено")


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


# Задание 2
def p2_task2():
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


# Задание 3
def p2_task3():
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
def p2_task4():
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


# --- Часть 3 ---


# Задание 1
class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def exists(self):
        return self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a

    def area(self):
        if not self.exists():
            return 0
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


def p3_task1():
    ok = Triangle(3, 4, 5)
    bad = Triangle(1, 2, 10)
    print("3, 4, 5 существует:", ok.exists(), "периметр:", ok.perimeter(), "площадь:", ok.area())
    print("1, 2, 10 существует:", bad.exists(), "периметр:", bad.perimeter(), "площадь:", bad.area())


# Задание 2
class House:
    def __init__(self, area, price):
        self._area = area
        self._price = price

    def final_price(self, discount):
        return self._price * (1 - discount / 100)


class SmallHouse(House):
    def __init__(self, price):
        super().__init__(40, price)


class Human:
    def __init__(self, name, money):
        self.name = name
        self._money = money
        self._house = None

    def __make_deal(self, house, price):
        self._money -= price
        self._house = house

    def buy_house(self, house, discount):
        price = house.final_price(discount)
        if self._money >= price:
            self.__make_deal(house, price)
            print(f"{self.name} купил дом за {price}, осталось денег {self._money}")
        else:
            print(f"{self.name}: недостаточно денег (нужно {price}, есть {self._money})")


def p3_task2():
    house = House(80, 100000)
    small = SmallHouse(40000)
    person = Human("Анна", 50000)
    print("Цена большого дома со скидкой 10%:", house.final_price(10))
    person.buy_house(house, 10)
    person.buy_house(small, 20)


# Задание 3
class Car:
    def __init__(self, speed, color, name, is_police=False):
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        print(self.name, "поехала")

    def stop(self):
        print(self.name, "остановилась")

    def turn(self, direction):
        print(self.name, "повернула", direction)

    def show_speed(self):
        print(self.name, "скорость", self.speed)


class TownCar(Car):
    def show_speed(self):
        super().show_speed()
        if self.speed > 60:
            print("Превышение скорости (город)")


class SportCar(Car):
    pass


class WorkCar(Car):
    def show_speed(self):
        super().show_speed()
        if self.speed > 40:
            print("Превышение скорости (работа)")


class PoliceCar(Car):
    def __init__(self, speed, color, name):
        super().__init__(speed, color, name, is_police=True)


def p3_task3():
    cars = [
        TownCar(72, "белый", "Solaris"),
        SportCar(120, "красный", "Ferrari"),
        WorkCar(35, "жёлтый", "Газель"),
        WorkCar(50, "синий", "Камаз"),
        PoliceCar(90, "синий", "ДПС"),
    ]
    for car in cars:
        car.go()
        car.show_speed()
        car.turn("направо")
        car.stop()
        print("Полиция:", car.is_police)
        print()


# Задание 4
class LibraryBook:
    library_name = "Городская библиотека"
    _created = 0

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        LibraryBook._created += 1

    def describe(self):
        return f"{self.title}, {self.pages} стр., {LibraryBook.library_name}"

    @staticmethod
    def minutes_to_read(pages, speed=2):
        return pages * speed

    @classmethod
    def created_count(cls):
        return cls._created

    @classmethod
    def from_string(cls, raw):
        title, pages = raw.split(";")
        return cls(title, int(pages))


def p3_task4():
    book = LibraryBook.from_string("Питон;200")
    print("Метод экземпляра:", book.describe())
    print("Статический метод:", LibraryBook.minutes_to_read(book.pages), "мин")
    print("Метод класса, создано книг:", LibraryBook.created_count())


TASKS = {
    "1.1": p1_task1,
    "1.2": p1_task2,
    "1.3": p1_task3,
    "1.4": p1_task4,
    "1.5": p1_task5,
    "1.6": p1_task6,
    "2.1": p2_task1,
    "2.2": p2_task2,
    "2.3": p2_task3,
    "2.4": p2_task4,
    "3.1": p3_task1,
    "3.2": p3_task2,
    "3.3": p3_task3,
    "3.4": p3_task4,
}


def main():
    print("Лабораторная работа 1, вариант 27")
    print("Номера: 1.1–1.6, 2.1–2.4, 3.1–3.4")
    while True:
        key = input("\nЗадание (0 — выход): ").strip()
        if key == "0":
            break
        func = TASKS.get(key)
        if func is None:
            print("Нет такого номера")
            continue
        print()
        func()


if __name__ == "__main__":
    main()
