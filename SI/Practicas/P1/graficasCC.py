import matplotlib.pyplot as plt
import numpy as np

# Leer el archivo de datos y almacenar la información en listas
nombres = []
costes = []
calorias = []

with open("data.txt", "r") as file:
    for line in file:
        nombre, coste, caloria = line.strip().split()
        nombres.append(nombre)
        costes.append(float(coste))
        calorias.append(float(caloria))

# Configurar el ancho de las barras y sus posiciones
x = np.arange(len(nombres))  # Posiciones para cada grupo de barras
ancho = 0.35  # Ancho de cada barra

# Crear la gráfica de barras
plt.figure(figsize=(10, 6))
plt.bar(x - ancho/2, costes, width=ancho, label="Coste", color="skyblue")
plt.bar(x + ancho/2, calorias, width=ancho, label="Calorías", color="salmon")

# Añadir etiquetas y título
plt.xlabel("Heurísticas")
plt.ylabel("Valores")
plt.title("Comparación de Coste y Calorías por Heurística")
plt.xticks(x, nombres)  # Configurar nombres en el eje x
plt.legend()  # Mostrar leyenda

# Guardar la gráfica como imagen (opcional)
plt.savefig("barras_coste_calorias.png")

# Mostrar la gráfica
plt.show()
