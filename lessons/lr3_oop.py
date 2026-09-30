"""
ЛР3: классы, наследование, три вида методов.

Запустите: python lessons/lr3_oop.py
"""


class Figure:
    """Родитель: общее имя и общая площадь-заглушка."""

    def __init__(self, name: str) -> None:
        self.name = name

    def area(self) -> float:
        return 0.0

    def info(self) -> str:
        return f"{self.name}: площадь {self.area()}"


class Square(Figure):
    def __init__(self, side: float) -> None:
        super().__init__("квадрат")
        self.side = side

    def area(self) -> float:
        return self.side ** 2


class Rectangle(Figure):
    def __init__(self, width: float, height: float) -> None:
        super().__init__("прямоугольник")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class LibraryBook:
    """Пример своего класса со всеми тремя видами методов (задание 4 ЛР3)."""

    library_name = "Городская библиотека"
    _created = 0

    def __init__(self, title: str, pages: int) -> None:
        self.title = title
        self.pages = pages
        LibraryBook._created += 1

    def describe(self) -> str:
        """Метод экземпляра: видит конкретную книгу (self)."""
        return f"{self.title}, {self.pages} стр."

    @staticmethod
    def minutes_to_read(pages: int, speed: int = 2) -> int:
        """Статический метод: не нужен ни объект, ни класс."""
        return pages * speed

    @classmethod
    def created_count(cls) -> int:
        """Метод класса: работает с данными всего класса."""
        return cls._created

    @classmethod
    def from_string(cls, raw: str) -> "LibraryBook":
        title, pages = raw.split(";")
        return cls(title, int(pages))


class Car:
    def __init__(self, speed: int, color: str, name: str, is_police: bool = False) -> None:
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self) -> None:
        print(self.name, "поехала")

    def stop(self) -> None:
        print(self.name, "остановилась")

    def turn(self, direction: str) -> None:
        print(self.name, "повернула", direction)

    def show_speed(self) -> None:
        print(self.name, "скорость", self.speed)


class TownCar(Car):
    def show_speed(self) -> None:
        super().show_speed()
        if self.speed > 60:
            print("Превышение скорости (город)")


class WorkCar(Car):
    def show_speed(self) -> None:
        super().show_speed()
        if self.speed > 40:
            print("Превышение скорости (работа)")


if __name__ == "__main__":
    print(Square(4).info())
    print(Rectangle(3, 5).info())

    book = LibraryBook.from_string("Питон;200")
    print(book.describe())
    print("минут на чтение:", LibraryBook.minutes_to_read(book.pages))
    print("создано книг:", LibraryBook.created_count())
    print("библиотека:", LibraryBook.library_name)

    town = TownCar(72, "белый", "Solaris")
    town.go()
    town.show_speed()
    town.turn("налево")
    town.stop()

    print("\nКак решать ЛР3:")
    print("1) class Имя:  затем def __init__(self, ...): self.поле = ...")
    print("2) Наследование: class Child(Parent): и super().__init__(...)")
    print("3) Переопределение: в потомке тот же метод с другим телом.")
    print("4) Задание 4: один свой класс + describe + @staticmethod + @classmethod.")
