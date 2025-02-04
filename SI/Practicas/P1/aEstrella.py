import math
from casilla import Casilla
from mapa import *
import heapq

class Nodo:
    def __init__(self, casilla, padre=None, g=0, h=0):
        self.casilla = casilla  # Casilla actual (posición)
        self.padre = padre  # Nodo padre (de dónde venimos)
        self.g = g  # Costo desde el inicio hasta esta casilla
        self.h = h  # Heurística (estimación del costo desde esta casilla hasta la meta)
        self.f = g + h  # Costo total (g + h)

    def __lt__(self, other):
        return self.f < other.f  # Comparar nodos por f para obtener el mejor nodo

def reconstruir_camino(nodo_final):
    camino = []
    nodo_actual = nodo_final
    while nodo_actual is not None:
        camino.append((nodo_actual.casilla.getFila(), nodo_actual.casilla.getCol()))
        nodo_actual = nodo_actual.padre
    return camino[::-1]  # Invertir el camino para que vaya desde el origen hasta el destino

def a_estrella(mapi, origen, destino, calcular_heuristica, calcular_costo, camino, parametro_heuristica, verbose):
    # Crear las listas de frontera (nodos a explorar) y lista interior (nodos ya explorados)
    lista_frontera = []
    lista_interior = set()
    # Calculo las calorías de la casilla inicial para restarlas antes de devolver las calorías totales
    calorias_iniciales = get_calorias(mapi.getCelda(origen.getFila(), origen.getCol()))
    # Nodo de inicio
    nodo_inicio = Nodo(origen, None, 0, calcular_heuristica(origen, destino, parametro_heuristica))
    lista_frontera.append(nodo_inicio)

    while lista_frontera:
        # Obtener el nodo de la lista frontera con el menor valor de f
        lista_frontera.sort(key=lambda x: x.f)  # Ordenar por f
        nodo_actual = lista_frontera.pop(0)  # Nodo con menor f
        lista_interior.add((nodo_actual.casilla.getFila(), nodo_actual.casilla.getCol()))  # Añadir a explorados

        # Verificar si llegamos a la meta
        if nodo_actual.casilla.getFila() == destino.getFila() and nodo_actual.casilla.getCol() == destino.getCol():
            # Guardamos el coste antes de empezar a recorrer los padres
            coste_total = nodo_actual.g
            calorias_total = 0  # Inicializar las calorías totales

            # Reconstruir el camino desde la meta al origen
            while nodo_actual is not None:
                fila_actual = nodo_actual.casilla.getFila()
                col_actual = nodo_actual.casilla.getCol()
                camino[fila_actual][col_actual] = 'x'  # Marcar solo el camino óptimo
                
                # Sumar las calorías de la casilla actual
                calorias_total += get_calorias(mapi.getCelda(fila_actual, col_actual))
                
                nodo_actual = nodo_actual.padre

            return coste_total, calorias_total - calorias_iniciales  # Devolver el coste total y las calorías

        # Explorar los vecinos
        vecinos = obtener_vecinos(nodo_actual.casilla, mapi)
        if verbose:
            print(f"\nNodo actual: ({nodo_actual.casilla.getFila()}, {nodo_actual.casilla.getCol()})")
            print(f"Vecinos del nodo actual: {[(vec.getFila(), vec.getCol()) for vec in vecinos]}")
        for vecino in vecinos:
            # Ignorar el vecino si ya está explorado
            if (vecino.getFila(), vecino.getCol()) in lista_interior:
                if verbose:
                    print(f"Vecino ({vecino.getFila()}, {vecino.getCol()}) ya explorado, se omite.")
                continue

            # Calcular los costes g, h y f para el vecino
            g_nuevo = nodo_actual.g + calcular_costo(nodo_actual.casilla, vecino)
            h_nuevo = calcular_heuristica(vecino, destino)
            f_nuevo = g_nuevo + h_nuevo
            if verbose:
                print(f"Evaluando vecino ({vecino.getFila()}, {vecino.getCol()}): g={g_nuevo}, h={h_nuevo}, f={f_nuevo}")
            # Comprobar si el vecino ya está en la lista frontera con un menor costo
            nodo_vecino = next((nodo for nodo in lista_frontera if nodo.casilla.getFila() == vecino.getFila() and nodo.casilla.getCol() == vecino.getCol()), None)
            if nodo_vecino is None:
                # Añadir el nuevo vecino a la lista frontera
                nuevo_nodo = Nodo(vecino, nodo_actual, g_nuevo, h_nuevo)
                lista_frontera.append(nuevo_nodo)
                if verbose:
                    print(f"Añadiendo nuevo vecino ({vecino.getFila()}, {vecino.getCol()}) a la frontera.")
            elif g_nuevo < nodo_vecino.g:
                # Actualizar el nodo vecino con un nuevo mejor camino
                nodo_vecino.g = g_nuevo
                nodo_vecino.f = f_nuevo
                nodo_vecino.padre = nodo_actual
                if verbose:
                    print(f"ACTUALIZANDO vecino ({vecino.getFila()}, {vecino.getCol()}) en la frontera con mejor g={g_nuevo} y f={f_nuevo}.")
            elif verbose:
                print(f"No se añade/actualiza vecino ({vecino.getFila()}, {vecino.getCol()}) ya tiene un mejor camino.")
        if verbose:
            nodos_explorados = len(lista_interior)
            print(f"Número de nodos explorados: {nodos_explorados}")
            
    return -1, 0  # No se encontró un camino, devolver 0 calorías

def a_estrella_sub_epsilon(mapi, origen, destino, calcular_heuristica, calcular_costo, camino, parametro_heuristica, epsilon, verbose):
    # Crear las listas de frontera (nodos a explorar) y lista interior (nodos ya explorados)
    lista_frontera = []
    lista_interior = set()
    
    # Calculo las calorías de la casilla inicial para restarlas antes de devolver las calorías totales
    calorias_iniciales = get_calorias(mapi.getCelda(origen.getFila(), origen.getCol()))
    
    # Nodo de inicio
    nodo_inicio = Nodo(origen, None, 0, calcular_heuristica(origen, destino, parametro_heuristica))
    # Insertar el nodo inicial en lista_frontera usando heapq
    heapq.heappush(lista_frontera, (nodo_inicio.f, nodo_inicio))

    while lista_frontera:
        # Obtener el nodo con menor f(n) en la lista frontera
        mejor_f = lista_frontera[0][0]

        # Construir la lista focal con nodos que cumplen la condición f(n) <= (1 + ε) * mejor_f
        lista_focal = [nodo for f_val, nodo in lista_frontera if f_val <= (1 + epsilon) * mejor_f]
        if verbose:
            print("\nLista focal:", [(nodo.casilla.getFila(), nodo.casilla.getCol(), nodo.f) for nodo in lista_focal])
        
        # Seleccionar el nodo con el menor valor de calorías en la lista focal
        nodo_actual = min(lista_focal, key=lambda x: get_calorias(mapi.getCelda(x.casilla.getFila(), x.casilla.getCol())))
        if verbose:
            print(f"\nNodo actual seleccionado: ({nodo_actual.casilla.getFila()}, {nodo_actual.casilla.getCol()}) con f={nodo_actual.f}")

        # Eliminar el nodo seleccionado de la lista frontera y añadirlo a la lista interior
        lista_frontera = [(f_val, nodo) for f_val, nodo in lista_frontera if nodo != nodo_actual]
        heapq.heapify(lista_frontera)  # Reajustar el heap tras eliminar el nodo
        lista_interior.add((nodo_actual.casilla.getFila(), nodo_actual.casilla.getCol()))
        if verbose:
            print("Lista frontera después de extracción:", [(f_val, nodo.casilla.getFila(), nodo.casilla.getCol()) for f_val, nodo in lista_frontera])
            print("Lista interior actual:", list(lista_interior))

        # Verificar si llegamos a la meta
        if nodo_actual.casilla.getFila() == destino.getFila() and nodo_actual.casilla.getCol() == destino.getCol():
            # Guardamos el coste antes de empezar a recorrer los padres
            coste_total = nodo_actual.g
            calorias_total = 0
            
            # Reconstruir el camino desde la meta al origen
            while nodo_actual is not None:
                fila_actual = nodo_actual.casilla.getFila()
                col_actual = nodo_actual.casilla.getCol()
                camino[fila_actual][col_actual] = 'x'  # Marcar solo el camino óptimo
                
                # Sumar las calorías de la casilla actual
                calorias_total += get_calorias(mapi.getCelda(fila_actual, col_actual))
                
                nodo_actual = nodo_actual.padre

            return coste_total, calorias_total - calorias_iniciales  # Devolver el coste total y las calorías

        # Explorar los vecinos
        vecinos = obtener_vecinos(nodo_actual.casilla, mapi)
        if verbose:
            print(f"Vecinos del nodo actual ({nodo_actual.casilla.getFila()}, {nodo_actual.casilla.getCol()}):", 
              [(vec.getFila(), vec.getCol()) for vec in vecinos])

        for vecino in vecinos:
            # Ignorar el vecino si ya está explorado
            if (vecino.getFila(), vecino.getCol()) in lista_interior:
                if verbose:
                    print(f"Vecino ({vecino.getFila()}, {vecino.getCol()}) ya explorado, se omite.")
                continue

            # Calcular los costes g, h y f para el vecino
            g_nuevo = nodo_actual.g + calcular_costo(nodo_actual.casilla, vecino)
            h_nuevo = calcular_heuristica(vecino, destino, parametro_heuristica)
            f_nuevo = g_nuevo + h_nuevo
            if verbose:
                print(f"Evaluando vecino ({vecino.getFila()}, {vecino.getCol()}): g={g_nuevo}, h={h_nuevo}, f={f_nuevo}")

            # Comprobar si el vecino ya está en la lista frontera con un menor costo
            nodo_vecino = next((nodo for f_val, nodo in lista_frontera if nodo.casilla.getFila() == vecino.getFila() and nodo.casilla.getCol() == vecino.getCol()), None)
            if nodo_vecino is None:
                # Añadir el nuevo vecino a la lista frontera
                nuevo_nodo = Nodo(vecino, nodo_actual, g_nuevo, h_nuevo)
                heapq.heappush(lista_frontera, (nuevo_nodo.f, nuevo_nodo))
                if verbose:
                    print(f"Añadiendo nuevo vecino ({vecino.getFila()}, {vecino.getCol()}) a la frontera.")
            elif g_nuevo < nodo_vecino.g:
                # Actualizar el nodo vecino con un nuevo mejor camino
                nodo_vecino.g = g_nuevo
                nodo_vecino.f = f_nuevo
                nodo_vecino.padre = nodo_actual
                heapq.heapify(lista_frontera)  # Reajustar el heap tras la actualización
                if verbose:
                    print(f"ACTUALIZANDO vecino ({vecino.getFila()}, {vecino.getCol()}) en la frontera con mejor g={g_nuevo} y f={f_nuevo}.")
            else:
                if verbose:
                    print(f"No se añade/actualiza vecino ({vecino.getFila()}, {vecino.getCol()}), ya tiene un mejor camino.")
        if verbose:
            nodos_explorados = len(lista_interior)
            print(f"Número de nodos explorados: {nodos_explorados}")
    
    
    return -1, 0  # No se encontró un camino, devolver 0 calorías



def obtener_vecinos(casilla, mapi):
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Ortogonales y diagonales
    for dx, dy in movimientos:
        nueva_fila = casilla.getFila() + dx
        nueva_col = casilla.getCol() + dy

        # Verificar que el vecino esté dentro del mapa y no sea una casilla bloqueada
        if 0 <= nueva_fila < mapi.getAlto() and 0 <= nueva_col < mapi.getAncho():
            if mapi.getCelda(nueva_fila, nueva_col) != 1:  # Suponiendo que 1 es una celda bloqueada
                vecinos.append(Casilla(nueva_fila, nueva_col))
    return vecinos

def calcular_costo(casilla_actual, vecino):
    # Si el movimiento es diagonal, el costo es 1.5, de lo contrario, 1
    dx = abs(casilla_actual.getFila() - vecino.getFila())
    dy = abs(casilla_actual.getCol() - vecino.getCol())
    if dx == 1 and dy == 1:
        return 1.5  # Movimiento diagonal
    return 1  # Movimiento ortogonal

def calcular_heuristica(casilla, destino, tipo="nada"):
    dx = abs(casilla.getFila() - destino.getFila())
    dy = abs(casilla.getCol() - destino.getCol())
    
    if tipo == "nada":
        return 0
    elif tipo == "manhattan":
        # Distancia de Manhattan
        return dx + dy
    elif tipo == "euclidea":
        # Distancia Euclidiana
        return math.sqrt(dx ** 2 + dy ** 2)
    elif tipo == "chebyshev":
        # Distancia de Chebyshev
        return max(dx, dy)
    elif tipo == "octile":
        # Distancia Octile
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy) 
    elif tipo == "octileV2":
        # Distancia Octile ajustada (sqrt(2) - 1 --> 1.5 - 1)
        return max(dx, dy) + 0.5 * min(dx, dy)

def get_calorias(celda):
    if celda == 0: # Hierba
        return 2
    elif celda == 4: # Agua
        return 4
    elif celda == 5: # Roca
        return 6
