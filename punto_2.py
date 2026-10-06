import numpy
import time
import random

# Hace una lista de mil listas cada una con 1000 elementos aleatorios enteros entre 1 y 1000 (matriz)
m1 = [[random.randint(1, 1000) for _ in range(1000)] for _ in range(1000)]
# Hace una lista de mil listas cada una con 1000 elementos aleatorios enteros entre 1 y 1000 (matriz)

m2 = [[random.randint(1, 1000) for _ in range(1000)] for _ in range(1000)]

resultado = [[0 for _ in range(1000)] for _ in range(1000)]


def mutliplicar_matrices_tradicional(m1, m2):

    for i in range(1000):
        for j in range(1000):
            for k in range(1000):
                resultado[i][j] += m1[i][k] * m2[k][j]


# Multiplica las 2 matrices de numpy
def mutiplicar_matrices_numpy(NPm1, NPm2):
    NPm3 = NPm1 @ NPm2


if __name__ == "__main__":
    # creacion de 2 matrices cada una de 1000x1000 con los mismos numeros de m1 y m2
    NPm1 = numpy.array(m1)
    NPm2 = numpy.array(m2)
    # se guarda la multiplicacion
    inicionp = time.time()
    NPm3 = mutiplicar_matrices_numpy(NPm1, NPm2)
    finalnp = time.time()
    tiemponp = finalnp - inicionp
    print(f"multiplicacion calculada con numpy en {tiemponp }")
    inicio = time.time()
    mutliplicar_matrices_tradicional(m1, m2)
    final = time.time()
    tiempo_for_tradicional = final - inicio
    print(f"La multiplicacion sin numpy se realizó en {tiempo_for_tradicional}")
