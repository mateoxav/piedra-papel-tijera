# demo_cli_marcador.py
# UI de consola: llama a core.jugar_ronda y solo lee el marcador.

import marcador
from core import jugar_ronda

def normaliza(texto):
    t = texto.strip().lower()
    if t == "piedra": return "piedra"
    if t == "papel":  return "papel"
    if t == "tijera": return "tijera"
    return None

def mostrar_marcador():
    m = marcador.getMarcador()
    print(f"Marcador -> Tú: {m['puntosJugador']} | Máquina: {m['puntosMaquina']} | Empates: {m['empates']}")

def main():
    print("=== Piedra, Papel, Tijera (demo con marcador) ===")
    print("Escribe piedra / papel / tijera. 'reset' para reiniciar. 'salir' para terminar.")
    marcador.reset()

    while True:
        entrada = input("> Tu jugada: ")
        t = entrada.strip().lower()

        if t == "salir":
            break
        if t == "reset":
            marcador.reset()
            mostrar_marcador()
            continue

        jugada = normaliza(entrada)
        if jugada is None:
            print("Entrada no válida. Intenta con piedra, papel o tijera.")
            continue

        resultado, jugada_m = jugar_ronda(jugada)

        print("Tú:", jugada, "| Máquina:", jugada_m)
        if resultado == "gana_jugador":
            print("Resultado: ¡Ganas!")
        elif resultado == "gana_maquina":
            print("Resultado: Gana la máquina.")
        else:
            print("Resultado: Empate.")

        mostrar_marcador()

    print("Fin del juego.")
    mostrar_marcador()

if __name__ == "__main__":
    main()
