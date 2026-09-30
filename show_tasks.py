"""Печатает формулировки заданий вашего варианта из выгрузок PDF."""

import re
from pathlib import Path

from config import VARIANT

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "ЛР1": ROOT / "ЛР01_1.txt",
    "ЛР2": ROOT / "ЛР01_2.txt",
    "ЛР3": ROOT / "ЛР01_3.txt",
}


def split_variants(text: str) -> dict[int, str]:
    pattern = re.compile(r"Вариант\s+(\d+)\s*[.:]?", re.IGNORECASE)
    matches = list(pattern.finditer(text))
    result = {}
    for i, match in enumerate(matches):
        number = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        result[number] = body
    return result


def main() -> None:
    if VARIANT < 1 or VARIANT > 31:
        print("Сначала откройте config.py и поставьте VARIANT = число от 1 до 31.")
        return

    print(f"Вариант {VARIANT}\n")
    for title, path in SOURCES.items():
        variants = split_variants(path.read_text(encoding="utf-8"))
        text = variants.get(VARIANT)
        print("=" * 72)
        print(title)
        print("=" * 72)
        print(text if text else "Текст варианта не найден.")
        print()


if __name__ == "__main__":
    main()
