from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Cm

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "ЛР01_вариант27.docx"


def set_run_font(run, name="Times New Roman", size=14, bold=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold


def add_center(doc, text, size=14, bold=False, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p


def add_body(doc, text, first_line=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25) if first_line else Cm(0)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run)
    return p


def add_heading_ru(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_run_font(run, size=16, bold=True)


def add_code(doc, text):
    for line in text.splitlines() or [""]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(line if line else " ")
        set_run_font(run, name="Consolas", size=10)


def main():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(1.5)

    add_center(doc, "МИНИСТЕРСТВО ОБРАЗОВАНИЯ РЕСПУБЛИКИ БЕЛАРУСЬ", bold=True, size=12)
    add_center(doc, "УЧРЕЖДЕНИЕ ОБРАЗОВАНИЯ", bold=True, size=12)
    add_center(
        doc,
        "«БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ",
        bold=True,
        size=12,
    )
    add_center(doc, "ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ»", bold=True, size=12)
    add_center(doc, "")
    add_center(doc, "Факультет ______________________________")
    add_center(doc, "Кафедра ______________________________")
    add_center(doc, "")
    add_center(doc, "")
    add_center(doc, "ОТЧЁТ", bold=True, size=18)
    add_center(doc, "по лабораторной работе", bold=True, size=16)
    add_center(doc, "«Основы языка программирования Python»", bold=True, size=16)
    add_center(doc, "Вариант 27", bold=True, size=16)
    add_center(doc, "")
    add_center(doc, "")
    add_center(doc, "Выполнил: студент группы __________")
    add_center(doc, "________________________________")
    add_center(doc, "Проверил: _______________________")
    add_center(doc, "")
    add_center(doc, "")
    add_center(doc, "Минск 2026")
    doc.add_page_break()

    add_heading_ru(doc, "1. Цель работы")
    add_body(
        doc,
        "Изучить базовые конструкции языка Python (числа, строки, списки, словари, "
        "кортежи), оформить решение в виде функций с обработкой исключений "
        "try/except/finally, освоить работу с матрицами и основы объектно-ориентированного "
        "программирования: классы, наследование, переопределение методов, методы "
        "экземпляра, класса и статические методы.",
    )

    add_heading_ru(doc, "2. Теория")
    add_body(
        doc,
        "В Python тип принадлежит значению, а не имени переменной. Основные типы данной "
        "работы: int, float, str, bool, list, tuple, dict. Функция input() читает строку, "
        "int() преобразует её в целое число, print() выводит результат. Ветвление задаётся "
        "if/elif/else, циклы — for и while.",
    )
    add_body(
        doc,
        "Цифры числа получают остатком от деления: n % 10 даёт последнюю цифру, n // 10 "
        "отбрасывает её. Чётность проверяют как n % 2 == 0. Простое число больше 1 и не "
        "делится ни на одно целое от 2 до квадратного корня из числа.",
    )
    add_body(
        doc,
        "Строка неизменяема. Методы isupper/islower определяют регистр, split() делит текст "
        "на слова, срез s[::-1] разворачивает строку. Список изменяем: min, max, sum, remove, "
        "срезы и генераторы. Словарь хранит пары ключ–значение; sorted(d.items()) сортирует "
        "по ключу. Кортеж похож на список, но его нельзя менять на месте.",
    )
    add_body(
        doc,
        "Функция объявляется как def имя(аргументы): и может вернуть значение через return. "
        "isinstance(x, list) проверяет тип аргумента, поэтому одна функция обрабатывает "
        "список, словарь, число и строку по-разному. Исключения перехватывают блоком "
        "try/except/finally: try содержит рискованный код, except обрабатывает ошибку "
        "(ValueError, ZeroDivisionError), finally выполняется всегда.",
    )
    add_body(
        doc,
        "Матрица — список списков. Элемент a[i][j], i — строка, j — столбец. Столбец "
        "собирают как [a[i][j] for i in range(n)]. Среднее — сумма элементов, делённая на "
        "их количество.",
    )
    add_body(
        doc,
        "Класс — описание объекта. Конструктор __init__ задаёт поля через self. Наследование "
        "class Child(Parent) перенимает методы родителя; super().__init__() вызывает "
        "родительский конструктор. Переопределение метода в потомке заменяет поведение "
        "(например, show_speed у TownCar проверяет лимит 60). Метод экземпляра работает с "
        "конкретным объектом, @staticmethod не использует self, @classmethod получает cls "
        "и работает с данными всего класса. Защищённые поля помечают одним подчёркиванием "
        "(_price), приватные — двумя (__make_deal).",
    )

    add_heading_ru(doc, "3. Формулировка индивидуального задания")
    add_body(doc, "Вариант 27. Задания из трёх частей методички.", first_line=True)
    add_body(
        doc,
        "Часть 1. 1) Определить, сколько в числе чётных и нечётных цифр. "
        "2) Посчитать пары соседних букв верхнего и нижнего регистра и число букв в слове. "
        "3) Произведение элементов списка с нечётными номерами; удалить наибольший элемент. "
        "4) Отсортировать словарь по ключу по возрастанию и вывести первые три элемента. "
        "5) Программа «Магазин игрушек» с шестью пунктами меню и покупкой. "
        "6) Сумма элементов кортежа после первого положительного.",
    )
    add_body(
        doc,
        "Часть 2 (через функции и try/except/finally). 1) Вывести все простые числа в диапазоне. "
        "2) Одна функция: список — произведение нечётных номеров и удаление максимума; "
        "словарь — три наибольших значения; число — сумма цифр; строка — гласные, согласные, слова. "
        "3) Первый столбец матрицы, все элементы которого отрицательны, и их среднее. "
        "4) Демонстрация try/except/finally.",
    )
    add_body(
        doc,
        "Часть 3. 1) Класс Triangle: существование, площадь, периметр. "
        "2) House, SmallHouse, Human: скидка и покупка дома. "
        "3) Car и наследники TownCar, SportCar, WorkCar, PoliceCar; контроль скорости. "
        "4) Собственный класс с методом экземпляра, статическим методом и методом класса.",
    )

    add_heading_ru(doc, "4. Код решения")
    add_body(
        doc,
        "Решение оформлено тремя файлами: lab1/lab1_1.py, lab1/lab1_2.py, lab1/lab1_3.py. "
        "Каждое задание — отдельная функция, запуск из main.",
        first_line=True,
    )
    for title, path in (
        ("Файл lab1_1.py", ROOT / "lab1" / "lab1_1.py"),
        ("Файл lab1_2.py", ROOT / "lab1" / "lab1_2.py"),
        ("Файл lab1_3.py", ROOT / "lab1" / "lab1_3.py"),
    ):
        add_heading_ru(doc, title)
        add_code(doc, path.read_text(encoding="utf-8"))

    add_heading_ru(doc, "5. Результаты выполнения")
    add_body(
        doc,
        "Ниже приведены протоколы работы программ. Интерактивные задания "
        "(ввод числа, слово, магазин, деление) запускаются из меню соответствующего файла. "
        "Для сдачи сделайте скриншоты консоли и вставьте их вместо или дополнительно к этому разделу.",
    )
    add_code(doc, (Path(__file__).resolve().parent / "результаты_выполнения.txt").read_text(encoding="utf-8"))
    add_body(
        doc,
        "Дополнительно проверено: число 2547 — 2 чётные и 2 нечётные цифры; слово HjkLM — "
        "1 пара нижнего и 1 пара верхнего регистра, 5 букв; покупка 2 кукол и 3 мячей даёт сумму 80 "
        "и остатки 10 / 17 / 8; деление 10/0 ловится ZeroDivisionError, блок finally выполняется всегда.",
    )

    add_heading_ru(doc, "6. Выводы")
    add_body(
        doc,
        "В ходе работы освоены базовые типы и циклы Python, разбор числа на цифры, обработка строк "
        "и коллекций, диалоговое меню на словаре. Решение второй части оформлено функциями: "
        "проверка типа через isinstance, поиск простых чисел, обход столбцов матрицы, обработка "
        "ошибок блоком try/except/finally. В третьей части реализованы классы с наследованием "
        "и переопределением методов, а также три вида методов на примере LibraryBook. "
        "Программы запускаются по отдельности из папки lab1 и позволяют выбрать номер задания.",
    )

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
