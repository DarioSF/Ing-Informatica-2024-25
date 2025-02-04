import matplotlib.pyplot as plt
import numpy as np

# Leer el archivo de datos y almacenar la información en listas
nombres = []
valores = []

with open("data1.txt", "r") as file:
    for line in file:
        nombre, valor = line.strip().split()
        nombres.append(nombre)
        valores.append(int(valor))

# Lista de colores para cada barra
colores = plt.cm.viridis(np.linspace(0, 1, len(nombres)))  # Genera colores diferentes de viridis

# Crear la gráfica de barras
plt.figure(figsize=(10, 6))
plt.bar(nombres, valores, color=colores)
plt.xlabel("Heurísticas")
plt.ylabel("Número de nodos explorados")
plt.title("Comparación de Heurísticas por Nodos Explorados")

# Guardar la gráfica como imagen (opcional)
plt.savefig("barras_heuristicas.png")

# Mostrar la gráfica
plt.show()
