import multiprocessing
import numpy as np
import time

# proceso en background (demonio) para escribir el resultado en un archivo
def write_to_file(sumaMatrix, size, tiempo ,filename="resultado_suma_normal.txt"):
    with open(filename, "w") as file:
        file.write("Suma normal: \n")
        file.write(f"tiempo tomado al sumar las {size} filas : {tiempo:.2f} segundos") 
    print(f"Resultados escritos en {filename}")

# matriz con datos aleatorios
def generar_matriz(size):
    return np.random.randint(0, 100, size=(size, size))

# suma las filas 
def sumar_matrices(matrixA, matrixB):
    
    sumaMatrix = np.zeros_like(matrixA)

    for i in range(matrixA.shape[1]):
        for j in range(matrixA.shape[1]):
            sumaMatrix[i][j] = matrixA[i][j] + matrixB[i][j]

    return sumaMatrix

if __name__ == "__main__":
    
    size = 5000
   

    # Generar matrices
    matrixA = generar_matriz(size)
    matrixB = generar_matriz(size)

    

    # Sumar matrices en paralelo
    inicio_tiempo = time.time()

   
    sumaMatrix = sumar_matrices(matrixA, matrixB)

    fin_tiempo = time.time()

    tiempo_total = fin_tiempo - inicio_tiempo

    print(f"Suma terminada en: {tiempo_total:.2f} segundos")

    write_to_file(sumaMatrix, size, tiempo_total)