# demo_cli.py
# Demo por consola para mostrar el avance (RNG + Core).
# Usa un bucle while para jugar varias rondas.

from rng import jugada_maquina
from core import resolver_resultado

def normaliza(texto):
    t = texto.strip().lower()
    if t == "piedra":
        return "piedra"
    if t == "papel":
        return "papel"
    if t == "tijera":
        return "tijera"
    return None

def main():
    print("=== Piedra, Papel, Tijera (avance AA2) ===")
    print("Escribe piedra / papel / tijera. Escribe 'salir' para terminar.")
    rondas = 0

    while True:
        entrada = input("> Tu jugada: ")
        if entrada.strip().lower() == "salir":
            break

        jugador = normaliza(entrada)
        if jugador is None:
            print("Entrada no válida. Intenta con piedra, papel o tijera.")
            continue  # vuelve al inicio del bucle

        maquina = jugada_maquina()
        resultado = resolver_resultado(jugador, maquina)

        print("Tú:", jugador, "| Máquina:", maquina)
        if resultado == "gana_jugador":
            print("Resultado: ¡Ganas!")
        elif resultado == "gana_maquina":
            print("Resultado: Gana la máquina.")
        else:
            print("Resultado: Empate.")

        rondas += 1

    print("Gracias por jugar. Rondas jugadas:", rondas)

if __name__ == "__main__":
    main()
