"""Заполняет lr1/lr2/lr3 формулировками заданий из PDF для VARIANT."""

import re
from pathlib import Path

from config import VARIANT
from show_tasks import split_variants

ROOT = Path(__file__).resolve().parent
LABS = [
    ("ЛР1", ROOT / "ЛР01_1.txt", ROOT / "lr1", 6),
    ("ЛР2", ROOT / "ЛР01_2.txt", ROOT / "lr2", 4),
    ("ЛР3", ROOT / "ЛР01_3.txt", ROOT / "lr3", 4),
]

HEADER = '''"""
{lab}, вариант {variant}, задание {num}.

Формулировка из методички:
{task}

Напишите решение ниже. Учебные примеры: папка lessons/
"""


def main() -> None:
    pass


if __name__ == "__main__":
    main()
'''


def split_tasks(body: str, expected: int) -> list[str]:
    parts = re.split(r"\n(?=\s*(?:\d+|Задание|Задача)\s*[.:])", body)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= expected:
        return parts[:expected]
    return parts + [""] * (expected - len(parts))


def main() -> None:
    if VARIANT < 1 or VARIANT > 31:
        print("Сначала поставьте VARIANT в config.py")
        return

    for lab, src, folder, count in LABS:
        folder.mkdir(exist_ok=True)
        variants = split_variants(src.read_text(encoding="utf-8"))
        body = variants.get(VARIANT, "")
        tasks = split_tasks(body, count)
        for i, task in enumerate(tasks, start=1):
            path = folder / f"task{i}.py"
            path.write_text(
                HEADER.format(lab=lab, variant=VARIANT, num=i, task=task),
                encoding="utf-8",
            )
        print(f"{lab}: записано {count} файлов в {folder}")


if __name__ == "__main__":
    main()
