import threading
import time
import random

# version secuencial
# Creacion de la matriz
matriz = []
# Hace una lista de mil listas cada una con 1000 elementos enteros del 1 al 100 (matriz)
for i in range(1000):
    matriz.append([random.randint(1, 1000) for i in range(1000)])
# suma secuencial
suma = 0
inicio = time.time()
for i in range(len(matriz)):
    suma += sum(matriz[i])
fin = time.time()


# version paralela


# Suma la el torozo correspondiente a la posicion
def suma_parcial(trozo, resultados, posicion):
    suma = 0

    for fila in trozo:
        suma += sum(fila)

    resultados[posicion] = suma


if __name__ == "__main__":
    print(f"resultado: {suma}, calculado secuencialmete en {fin - inicio}")
    matriz = []
    # Hace una lista de mil listas cada una con 1000 elementos aleatorios enteros entre 1 y 1000 (matriz)
    for i in range(0, 1000):
        matriz.append([random.randint(1, 1000) for i in range(1000)])

    inicio = time.time()
    hilos = []
    # Aqui se almacenaran los resultados de las sumas
    resultados = [0] * 100
    posicion = 0
    # Recorrer las filas de 100 en 100

    for i in range(0, 1000, 100):
        # Recorrer las columnas de 100 en 100
        for j in range(0, 1000, 100):
            trozo = [fila[j : j + 100] for fila in matriz[i : i + 100]]
            hilo = threading.Thread(
                target=suma_parcial, args=(trozo, resultados, posicion)
            )
            hilos.append(hilo)
            posicion += 1

    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    fin = time.time()
    final = fin - inicio
    # se suman todos los resultados posibles
    suma_total = sum(resultados)
    print(f"la suma total es de {suma_total}. Calculando paralelamente en {final}")
