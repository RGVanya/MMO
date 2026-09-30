# Задание 1
def task1():
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
def task2():
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
def task3():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    product = 1
    for i in range(0, len(nums), 2):
        product *= nums[i]
    print("Произведение элементов с нечётными номерами:", product)

    max_element = max(nums)
    nums.remove(max_element)
    print("Список без наибольшего элемента:", nums)


# Задание 4
def task4():
    my_dict = {" a": 50, " c": 5, "d": 56, " e": 4, "f": 58, "z": 20}
    sorted_dict = sorted(my_dict.items())
    print(sorted_dict[:3])


# Задание 5
def task5():
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
def task6():
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


def main():
    tasks = {
        "1": task1,
        "2": task2,
        "3": task3,
        "4": task4,
        "5": task5,
        "6": task6,
    }

    while True:
        print("\nВариант 27")
        print("1-6 — запустить задание")
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
