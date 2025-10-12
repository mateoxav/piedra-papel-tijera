# core.py
# Módulo Core (motor de reglas + orquestación de una ronda).

from rng import jugada_maquina
import marcador

def resolver_resultado(jugador, maquina):
    """
    Parámetros:
        jugador: "piedra" | "papel" | "tijera"
        maquina: "piedra" | "papel" | "tijera"
    Retorna:
        "gana_jugador" | "gana_maquina" | "empate"
    """
    if jugador == maquina:
        return "empate"

    # Casos en los que el jugador gana
    if (jugador == "piedra" and maquina == "tijera") \
       or (jugador == "tijera" and maquina == "papel") \
       or (jugador == "papel"  and maquina == "piedra"):
        return "gana_jugador"
    else:
        return "gana_maquina"

def jugar_ronda(jugada_jugador):
    """
    Orquesta una ronda completa:
      1) La máquina elige con RNG.
      2) Se resuelve el resultado (Core).
      3) Se actualiza el marcador (Estado).
      4) Se devuelve (resultado, jugada_maquina).

    Retorna:
        (resultado, jugada_maquina)
    """
    jugada_m = jugada_maquina()
    resultado = resolver_resultado(jugada_jugador, jugada_m)

    if resultado == "gana_jugador":
        marcador.sumarJugador()
    elif resultado == "gana_maquina":
        marcador.sumarMaquina()
    else:
        marcador.sumarEmpate()

    return resultado, jugada_m

# Pruebas rápida si se ejecuta el archivo solo:
if __name__ == "__main__":
    marcador.reset()
    r, m = jugar_ronda("piedra")
    print("Máquina:", m, "| Resultado:", r, "| Marcador:", marcador.getMarcador())
