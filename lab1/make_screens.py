# -*- coding: utf-8 -*-
"""Снимает протоколы запуска lab1.py в PNG для отчёта."""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import lab1  # noqa: E402

OUT = ROOT / "screens"
OUT.mkdir(exist_ok=True)


def render(name: str, text: str, title: str) -> None:
    lines = text.replace("\t", "    ").splitlines() or [""]
    fig_h = max(3.2, 0.28 * (len(lines) + 3))
    fig, ax = plt.subplots(figsize=(11.2, fig_h))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title, loc="left", fontsize=11, pad=8)
    ax.text(
        0.01,
        0.97,
        "\n".join(lines),
        va="top",
        ha="left",
        family="Consolas",
        fontsize=8.5,
        wrap=False,
        transform=ax.transAxes,
    )
    fig.patch.set_facecolor("white")
    fig.savefig(OUT / name, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def capture(func, answers: list[str] | None = None) -> str:
    buf = io.StringIO()
    answers = list(answers or [])
    iterator = iter(answers)

    def fake_input(prompt=""):
        try:
            value = next(iterator)
        except StopIteration as exc:
            raise EOFError("закончился ввод") from exc
        print(f"{prompt}{value}")
        return value

    with redirect_stdout(buf), patch("builtins.input", fake_input):
        func()
    return buf.getvalue()


def main() -> None:
    p1 = []
    p1.append("=== 1.1 Чётные и нечётные цифры ===")
    p1.append(capture(lab1.p1_task1, ["2547"]))
    p1.append("=== 1.2 Пары регистра ===")
    p1.append(capture(lab1.p1_task2, ["HjkLM"]))
    p1.append("=== 1.3 Список ===")
    p1.append(capture(lab1.p1_task3))
    p1.append("=== 1.4 Словарь ===")
    p1.append(capture(lab1.p1_task4))
    p1.append("=== 1.6 Кортеж ===")
    p1.append(capture(lab1.p1_task6))
    render("run_part1.png", "\n".join(p1), "lab1.py — часть 1, задания 1.1–1.4 и 1.6")

    shop_answers = [
        "4",
        "5",
        "кукла",
        "2",
        "мяч",
        "3",
        "n",
        "3",
        "6",
    ]
    shop = "=== 1.5 Магазин игрушек ===\n" + capture(lab1.p1_task5, shop_answers)
    render("run_shop.png", shop, "lab1.py — часть 1, задание 1.5 (магазин)")

    p2 = []
    p2.append("=== 2.1 Простые числа ===")
    p2.append(capture(lab1.p2_task1, ["10", "30"]))
    p2.append("=== 2.2 isinstance ===")
    p2.append(capture(lab1.p2_task2))
    p2.append("=== 2.3 Матрица ===")
    p2.append(capture(lab1.p2_task3))
    p2.append("=== 2.4 Деление (10 / 2) ===")
    p2.append(capture(lab1.p2_task4, ["10", "2"]))
    p2.append("=== 2.4 Деление на ноль ===")
    p2.append(capture(lab1.p2_task4, ["10", "0"]))
    render("run_part2.png", "\n".join(p2), "lab1.py — часть 2")

    p3 = []
    p3.append("=== 3.1 Треугольник ===")
    p3.append(capture(lab1.p3_task1))
    p3.append("=== 3.2 Дом и человек ===")
    p3.append(capture(lab1.p3_task2))
    p3.append("=== 3.3 Автомобили ===")
    p3.append(capture(lab1.p3_task3))
    p3.append("=== 3.4 Виды методов ===")
    p3.append(capture(lab1.p3_task4))
    render("run_part3.png", "\n".join(p3), "lab1.py — часть 3")
    print("Скриншоты:", OUT)


if __name__ == "__main__":
    main()
