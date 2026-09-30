"""
ЛР1, типовое задание 5: меню магазина на словаре.

Структура у всех вариантов одна и та же, меняются только товары.
Это учебный каркас. Подставьте свои ключи и значения из варианта.

Запустите: python lessons/lr1_05_shop.py
"""

# ключ — название
# значение — [описание/состав, цена, количество]
shop = {
    "торт": ["мука, сахар, крем", 15.0, 800],
    "маффин": ["мука, шоколад", 8.0, 400],
    "пирожное": ["безе, крем", 6.5, 250],
}

cart_sum = 0.0


def show_descriptions() -> None:
    for name, data in shop.items():
        print(f"{name} — {data[0]}")


def show_prices() -> None:
    for name, data in shop.items():
        print(f"{name} — {data[1]}")


def show_amounts() -> None:
    for name, data in shop.items():
        print(f"{name} — {data[2]}")


def show_all() -> None:
    for name, data in shop.items():
        print(f"{name}: состав={data[0]}, цена={data[1]}, остаток={data[2]}")


def buy() -> None:
    global cart_sum
    print("Покупка. Чтобы выйти из покупки, введите n")
    while True:
        name = input("Название: ").strip()
        if name.lower() == "n":
            break
        if name not in shop:
            print("Такого товара нет")
            continue
        try:
            amount = float(input("Количество: "))
        except ValueError:
            print("Нужно число")
            continue
        if amount <= 0:
            print("Количество должно быть больше 0")
            continue
        if amount > shop[name][2]:
            print("Не хватает на складе. Есть:", shop[name][2])
            continue
        shop[name][2] -= amount
        # если цена за 100 г — стоимость = цена * (граммы / 100)
        cost = shop[name][1] * amount
        cart_sum += cost
        print("Добавлено на сумму", cost)


def main() -> None:
    menu = {
        "1": ("Просмотр описания", show_descriptions),
        "2": ("Просмотр цены", show_prices),
        "3": ("Просмотр количества", show_amounts),
        "4": ("Вся информация", show_all),
        "5": ("Покупка", buy),
        "6": ("До свидания", None),
    }
    while True:
        print("\n--- Меню ---")
        for key, (title, _) in menu.items():
            print(f"{key}. {title}")
        choice = input("Пункт: ").strip()
        if choice == "6":
            print("До свидания")
            print("Итог покупок:", cart_sum)
            print("Остатки:")
            show_amounts()
            break
        action = menu.get(choice)
        if action is None:
            print("Нет такого пункта")
            continue
        action[1]()


if __name__ == "__main__":
    print("Это демонстрация. Для своего варианта замените словарь shop.")
    print("Если цена за 100 г, в buy посчитайте: цена * (граммы / 100).")
    main()
