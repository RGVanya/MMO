import math


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


def task1():
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


def task2():
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


def task3():
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


def task4():
    book = LibraryBook.from_string("Питон;200")
    print("Метод экземпляра:", book.describe())
    print("Статический метод:", LibraryBook.minutes_to_read(book.pages), "мин")
    print("Метод класса, создано книг:", LibraryBook.created_count())


def main():
    tasks = {
        "1": task1,
        "2": task2,
        "3": task3,
        "4": task4,
    }

    while True:
        print("\nВариант 27, файл 3")
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
