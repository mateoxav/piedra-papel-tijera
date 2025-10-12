# marcador.py
# Estado del marcador en memoria.

puntosJugador = 0
puntosMaquina = 0
empates = 0

def reset():
    global puntosJugador, puntosMaquina, empates
    puntosJugador = 0
    puntosMaquina = 0
    empates = 0

def sumarJugador():
    global puntosJugador
    puntosJugador += 1

def sumarMaquina():
    global puntosMaquina
    puntosMaquina += 1

def sumarEmpate():
    global empates
    empates += 1

def getMarcador():
    return {
        "puntosJugador": puntosJugador,
        "puntosMaquina": puntosMaquina,
        "empates": empates
    }
