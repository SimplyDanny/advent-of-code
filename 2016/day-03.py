from common import print_results, read


def is_triangle(possible_triangle):
    a, b, c = sorted(possible_triangle)
    return a + b > c

#### Main part.

sides = list(map(int, read(__file__).split()))

row_triangles = [
    sides[i:i + 3]
    for i in range(0, len(sides), 3)
]

column_triangles = [
    sides[i + j:i + j + 7:3]
    for i in range(0, len(sides), 9)
    for j in range(3)
]

print_results(
    sum(is_triangle(triangle) for triangle in row_triangles),
    sum(is_triangle(triangle) for triangle in column_triangles)
)
