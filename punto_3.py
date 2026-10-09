import threading
import time
import numpy as np

# ==============================================================================
# TALLER 4 - EJERCICIO INTEGRADOR: SIMULACIÓN DE UN SISTEMA HÍBRIDO SMP-SIMD
# ==============================================================================


TAMANO_MATRIZ = 10000
TAMANO_BLOQUE = 1000


def suma_parcial_simd(bloque, resultados, posicion):
    """
    Función ejecutada por cada hilo (Componente SMP):
    Aplica operaciones vectorizadas SIMD a través de NumPy dentro del bloque asignado.
    """
    # Operación SIMD: Suma a lo largo del eje 1 (filas) usando vectorización SIMD
    suma_filas = np.sum(bloque, axis=1, dtype=np.int64)
    # Reducción final del vector a un valor escalar
    resultados[posicion] = int(np.sum(suma_filas, dtype=np.int64))


def version_secuencial_bloques(matriz, tam_matriz, tam_bloque):
    """
    Versión secuencial que procesa la matriz bloque por bloque (1000x1000)
    en un único hilo (sin paralelismo SMP).
    """
    suma_total = 0
    for i in range(0, tam_matriz, tam_bloque):
        for j in range(0, tam_matriz, tam_bloque):
            bloque = matriz[i : i + tam_bloque, j : j + tam_bloque]
            suma_filas = np.sum(bloque, axis=1, dtype=np.int64)
            suma_total += int(np.sum(suma_filas, dtype=np.int64))
    return suma_total


def version_hibrida_smp_simd(matriz, tam_matriz, tam_bloque):
    """
    Versión híbrida SMP-SIMD:
    - SMP: Se dividen los bloques y se asigna cada bloque (1000x1000) a un hilo de ejecución.
    - SIMD: Cada hilo delega el cálculo matemático intensivo a instrucciones vectoriales de NumPy.
    """
    num_bloques_eje = tam_matriz // tam_bloque
    total_bloques = num_bloques_eje * num_bloques_eje
    resultados = [0] * total_bloques
    hilos = []
    posicion = 0

    # 1. División de la matriz en bloques de 1000x1000 y asignación a hilos (SMP)
    for i in range(0, tam_matriz, tam_bloque):
        for j in range(0, tam_matriz, tam_bloque):
            # Vista del bloque en NumPy (sin duplicar memoria)
            bloque = matriz[i : i + tam_bloque, j : j + tam_bloque]
            hilo = threading.Thread(
                target=suma_parcial_simd,
                args=(bloque, resultados, posicion)
            )
            hilos.append(hilo)
            posicion += 1

    # Iniciar todos los hilos
    for hilo in hilos:
        hilo.start()

    # Esperar a que todos los hilos finalicen
    for hilo in hilos:
        hilo.join()

    # Combinación de los resultados de todos los hilos
    suma_total = sum(resultados)
    return suma_total


if __name__ == "__main__":
    print("Ejecutando simulación con matriz de 10,000 x 10,000...")
    matriz = np.random.randint(1, 1000, size=(TAMANO_MATRIZ, TAMANO_MATRIZ), dtype=np.int64)

    # 1. Versión Secuencial
    inicio_sec = time.time()
    suma_sec = version_secuencial_bloques(matriz, TAMANO_MATRIZ, TAMANO_BLOQUE)
    t_sec = time.time() - inicio_sec

    # 2. Versión Híbrida SMP-SIMD
    inicio_hib = time.time()
    suma_hib = version_hibrida_smp_simd(matriz, TAMANO_MATRIZ, TAMANO_BLOQUE)
    t_hib = time.time() - inicio_hib

    # Cálculos comparativos
    speedup = t_sec / t_hib if t_hib > 0 else 0
    coinciden = "SÍ (Correcto)" if suma_sec == suma_hib else "NO (Error)"

    # Tabla
    sep = "+" + "-" * 22 + "+" + "-" * 17 + "+" + "-" * 12 + "+"
    print("\n" + sep)
    print(f"| {'Versión':<20} | {'Suma Total':<15} | {'Tiempo':<10} |")
    print(sep)
    print(f"| {'Secuencial':<20} | {suma_sec:<15} | {f'{t_sec:.4f} s':<10} |")
    print(f"| {'Híbrido (SMP+SIMD)':<20} | {suma_hib:<15} | {f'{t_hib:.4f} s':<10} |")
    print(sep)
    print(f"Speedup: {speedup:.2f}x | Consistencia: {coinciden}\n")
