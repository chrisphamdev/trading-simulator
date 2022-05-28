import random

def generate_matrix(n):
    matrix = []
    for i in range(2*n):
        row = []
        for j in range(2*n):
            row.append(random.randrange(1,500))
        matrix.append(row)
    return matrix

def display_matrix(matrix):
    for row in matrix:
        print()
        for elm in row:
            print(elm, end=' '*(5-len(str(elm))))
        

matrix = generate_matrix(2)
display_matrix(matrix)
