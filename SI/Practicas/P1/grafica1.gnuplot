set terminal pngcairo size 800,600
set output 'grafica1.png'

# Configurar el estilo de la gráfica para barras
set style data histograms
set style fill solid border -1

# Etiquetas y configuración de los ejes
set xlabel "Heurísticas" 
set ylabel "Número de nodos explorados" 
set title "Comparación de Heurísticas por Nodos Explorados"

# Ajustar el estilo de las barras
set boxwidth 0.5 relative

# Dibujar la gráfica usando el archivo de datos
plot 'data1.txt' using 2:xtic(1) title "Nodos Explorados"
