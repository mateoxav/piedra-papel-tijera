# core.py
# Módulo Core (motor de reglas).
# Compara las jugadas y dice quién gana.

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

# Pruebas rápidas si se ejecuta el archivo solo:
if __name__ == "__main__":
    print(resolver_resultado("piedra", "tijera"))  # gana_jugador
    print(resolver_resultado("papel", "tijera"))   # gana_maquina
    print(resolver_resultado("papel", "papel"))    # empate

