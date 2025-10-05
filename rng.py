# rng.py
# Módulo RNG (aleatoriedad) del juego.
# Devuelve "piedra", "papel" o "tijera" al azar con probabilidad similar.

import random

OPCIONES = ["piedra", "papel", "tijera"]

def jugada_maquina():
    """
    Retorna una opción al azar: "piedra", "papel" o "tijera".
    """
    return random.choice(OPCIONES)

# Pequeña prueba manual
if __name__ == "__main__":
    for i in range(5):
        print(jugada_maquina())
