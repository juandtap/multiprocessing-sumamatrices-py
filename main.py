import multiprocessing
import numpy as np
import time

# proceso en background (demonio) para escribir el resultado en un archivo
def write_to_file(sumaMatrix, size, tiempo , num_procesos,filename="resultado_suma_multiprocessing.txt"):
    with open(filename, "w") as file:
        file.write("Suma con Multiprocessing: \n")
        file.write(f"tiempo tomado al sumar las {size} filas con {num_procesos} procesos: {tiempo:.2f} segundos") 
    print(f"Resultados escritos en {filename}")

# matriz con datos aleatorios
def generar_matriz(size):
    return np.random.randint(0, 100, size=(size, size))

# suma las filas 
def sumar_parcial(matrixA, matrixB, sumaMatrix, filaInicio, filaFin):
    
    for i in range(filaInicio, filaFin):
        for j in range(matrixA.shape[1]):
            sumaMatrix[i][j] = matrixA[i][j] + matrixB[i][j]


if __name__ == "__main__":
    
    size = 5000
    num_procesos = 20

    # Generar matrices
    matrixA = generar_matriz(size)
    matrixB = generar_matriz(size)


    # Sumar matrices en paralelo
    inicio_tiempo = time.time()

    sumaMatrix = multiprocessing.Array('i', size * size)  # Array compartido para almacenar el resultado
    sumaMatrix_np = np.frombuffer(sumaMatrix.get_obj(), dtype='i').reshape(size, size)

   
    filas_por_proceso = size // num_procesos
    procesos = []

    for i in range(num_procesos):
        filaInicio = i * filas_por_proceso
        filaFin = size if i == num_procesos - 1 else (i + 1) * filas_por_proceso
        proceso = multiprocessing.Process(target=sumar_parcial, 
                                          args=(matrixA, matrixB, sumaMatrix_np, filaInicio, filaFin))
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()


    fin_tiempo = time.time()

    tiempo_total = fin_tiempo - inicio_tiempo

    print(f"Suma terminada en: {tiempo_total:.2f} segundos")

    proceso_demoniaco = multiprocessing.Process(
        target=write_to_file, args=(sumaMatrix_np, size, tiempo_total,num_procesos),daemon=True)

    proceso_demoniaco.start()
     
    proceso_demoniaco.join()