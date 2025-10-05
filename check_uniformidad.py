
# check_uniformidad.py
# Experimento simple para ver que las tres opciones salen parecido.

from rng import jugada_maquina

def contar(n):
    conteo = {"piedra": 0, "papel": 0, "tijera": 0}
    for i in range(n): # Primer bucle: repite n veces (en este caso, 6000)
        opcion = jugada_maquina()
        conteo[opcion] += 1

    print("Total intentos:", n)
    print(conteo)
    print("Frecuencias aproximadas:")
    for k in conteo: # Segundo bucle: recorre cada clave del diccionario (piedra, papel, tijera)
        # Calcula la frecuencia relativa dividiendo el conteo entre el total de intentos
        print(k, "->", round(conteo[k] / n, 3)) # Muestra la frecuencia con 3 decimales

if __name__ == "__main__":
    contar(6000)
