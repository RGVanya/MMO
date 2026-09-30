"""
ЛР2, типовое задание 3: матрица — список списков.

Запустите: python lessons/lr2_matrices.py
"""


def print_matrix(matrix) -> None:
    for row in matrix:
        print(*row)


def identity_pattern(n: int) -> list[list[int]]:
    """1 на диагонали, 0 выше, 2 ниже."""
    return [[1 if i == j else 0 if i < j else 2 for j in range(n)] for i in range(n)]


def chess(n: int, m: int) -> list[list[str]]:
    """Шахматы из . и *, слева сверху точка."""
    board = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append("." if (i + j) % 2 == 0 else "*")
        board.append(row)
    return board


def max_index(matrix) -> tuple[int, int]:
    best_i = best_j = 0
    best = matrix[0][0]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value > best:
                best, best_i, best_j = value, i, j
    return best_i, best_j


def row_sums(matrix) -> list[int]:
    return [sum(row) for row in matrix]


def col_sums(matrix) -> list[int]:
    cols = len(matrix[0])
    return [sum(matrix[i][j] for i in range(len(matrix))) for j in range(cols)]


def swap_columns(matrix, i: int, j: int) -> None:
    for row in matrix:
        row[i], row[j] = row[j], row[i]


def is_symmetric(matrix) -> bool:
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


if __name__ == "__main__":
    print("Диагональный шаблон n=4:")
    print_matrix(identity_pattern(4))
    print("\nШахматы 3x4:")
    print_matrix(chess(3, 4))

    m = [
        [1, 9, 3],
        [4, 0, 6],
        [7, 2, 8],
    ]
    print("\nИндекс максимума:", max_index(m))
    print("Суммы строк:", row_sums(m))
    print("Суммы столбцов:", col_sums(m))
    print("Симметрична?", is_symmetric(m))

    copy_m = [row[:] for row in m]
    swap_columns(copy_m, 0, 2)
    print("Столбцы 0 и 2 поменяли:")
    print_matrix(copy_m)

    print("\nКак читать матрицу с клавиатуры:")
    print("n, m = map(int, input().split())")
    print("matrix = [list(map(int, input().split())) for _ in range(n)]")
