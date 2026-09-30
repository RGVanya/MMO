"""
ЛР2: функции, isinstance, try / except / finally.

Общее требование лабораторной: каждое задание — через функции
и с обработкой исключений. Запустите: python lessons/lr2_functions_exceptions.py
"""


def is_palindrome(text: str) -> bool:
    clean = "".join(ch.lower() for ch in text if ch.isalnum())
    return clean == clean[::-1]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def dispatch(value):
    """Одна функция — разное поведение в зависимости от типа аргумента."""
    if isinstance(value, dict):
        return max(value, key=value.get)
    if isinstance(value, list):
        return sum(x for x in value if isinstance(x, (int, float)))
    if isinstance(value, tuple):
        return len(value)
    if isinstance(value, set):
        return sum(value)
    if isinstance(value, int):
        return is_prime(value)
    if isinstance(value, str):
        return len(value.split())
    return "неизвестный тип"


def demo_try_except_finally() -> None:
    print("\n=== try / except / finally ===")
    print("try     — рискованный код")
    print("except  — что делать, если ошибка")
    print("finally — выполнится и при успехе, и при ошибке")
    try:
        number = int("не число")
        print(number)
    except ValueError as error:
        print("Поймали ValueError:", error)
    finally:
        print("finally: закрыли ресурс / сказали «готово»")

    try:
        print(10 / 0)
    except ZeroDivisionError:
        print("На ноль делить нельзя")
    finally:
        print("finally снова сработал")


if __name__ == "__main__":
    print("палиндром 'А роза упала на лапу Азора':", is_palindrome("А роза упала на лапу Азора"))
    print("простое 17:", is_prime(17))
    print("dict ->", dispatch({"a": 1, "b": 9}))
    print("list ->", dispatch([1, 2, "x", 3]))
    print("tuple ->", dispatch((1, 2, 3)))
    print("int ->", dispatch(15))
    print("str ->", dispatch("два слова"))
    demo_try_except_finally()
    print("\nКак оформлять ЛР2:")
    print("1) Каждую подзадачу положите в def имя(...):")
    print("2) Ввод и деление оборачивайте в try/except.")
    print("3) В finally можно напечатать, что проверка закончена.")
    print("4) Тип аргумента проверяйте через isinstance(x, list) и т.д.")
