# ui.py
# UI de Piedra, Papel o Tijera adaptada a arquitectura modular (Core + RNG + Marcador)
# Requiere: customtkinter, pillow

import os
import customtkinter as ctk
from PIL import Image

# Importar capas
import core
import marcador


class PPTApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        try:
            ctk.set_default_color_theme("recursos/tema.json")
        except Exception:
            ctk.set_default_color_theme("dark-blue")
        super().__init__()
        # Ventana
        self.title("Piedra, Papel o Tijera")
        self.geometry("1150x620")
        self.resizable(False, False)

        # ====== Estado (solo UI) ======
        self.ronda = 0
        marcador.reset()  # el estado de puntos vive en 'marcador'

        # Colores resultado
        self.COLOR_WIN = "#22c55e"   # verde
        self.COLOR_LOSE = "#ef4444"  # rojo
        self.COLOR_DRAW = "#a8c5d6"  # celeste pálido 

        # ====== Grid raíz ======
        self.grid_columnconfigure(0, weight=11, minsize=560)  
        self.grid_columnconfigure(1, weight=14)
        self.grid_rowconfigure(0, weight=1)

        # ====== Panel izquierdo ======
        self.panel_izq = ctk.CTkFrame(self)
        self.panel_izq.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")
        self.panel_izq.grid_rowconfigure(0, minsize=140)  # fila de botones
        self.panel_izq.grid_rowconfigure(1, minsize=120)  # fila de contadores
        self.panel_izq.grid_rowconfigure(2, weight=1)     # espacio de relleno
        self.panel_izq.grid_columnconfigure(0, weight=1)

        # ====== Panel derecho ======
        self.panel_der = ctk.CTkFrame(self)
        self.panel_der.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")
        for i in range(3):
            self.panel_der.grid_rowconfigure(i, weight=0)
        self.panel_der.grid_rowconfigure(3, weight=1)  # relleno
        self.panel_der.grid_columnconfigure(0, weight=1)

        # ====== Cargar iconos ======
        self.icon_piedra = self._cargar_icono("recursos/piedra.png", (40, 40))
        self.icon_papel  = self._cargar_icono("recursos/papel.png",  (40, 40))
        self.icon_tijera = self._cargar_icono("recursos/tijera.png", (40, 40))

        # ====== Fila de botones ======
        self.frame_botones = ctk.CTkFrame(self.panel_izq, height=140)
        self.frame_botones.grid(row=0, column=0, padx=14, pady=(14, 10), sticky="nsew")
        self.frame_botones.grid_propagate(False)
        for i in range(3):
            self.frame_botones.grid_columnconfigure(i, weight=1, uniform="botones")
        self.frame_botones.grid_rowconfigure(0, weight=1)

        btn_opts = {
            "width": 150, "height": 118, "corner_radius": 10,
            "compound": "top", "anchor": "center", "font": ("", 15)
        }

        self.btn_piedra = ctk.CTkButton(
            self.frame_botones, text="Piedra", image=self.icon_piedra,
            command=lambda: self.jugar("piedra"), **btn_opts
        )
        self.btn_papel = ctk.CTkButton(
            self.frame_botones, text="Papel", image=self.icon_papel,
            command=lambda: self.jugar("papel"), **btn_opts
        )
        self.btn_tijera = ctk.CTkButton(
            self.frame_botones, text="Tijera", image=self.icon_tijera,
            command=lambda: self.jugar("tijera"), **btn_opts
        )

        self.btn_piedra.grid(row=0, column=0, padx=8, pady=10, sticky="nsew")
        self.btn_papel.grid(row=0, column=1, padx=8, pady=10, sticky="nsew")
        self.btn_tijera.grid(row=0, column=2, padx=8, pady=10, sticky="nsew")

        # ====== Contadores ======
        self.frame_scores = ctk.CTkFrame(self.panel_izq)
        self.frame_scores.grid(row=1, column=0, padx=14, pady=(6, 14), sticky="nsew")
        for i in range(3):
            self.frame_scores.grid_columnconfigure(i, weight=1, uniform="scores")
        self.frame_scores.grid_rowconfigure(0, weight=1)

        def score_card(parent, titulo):
            card = ctk.CTkFrame(parent, corner_radius=12)
            card.grid_propagate(False)
            card.configure(height=90)
            title = ctk.CTkLabel(card, text=titulo, font=("", 16, "bold"))
            value = ctk.CTkLabel(card, text="0", font=("", 28, "bold"))
            title.pack(pady=(10, 2))
            value.pack(pady=(0, 8))
            return card, value

        self.card_jugador, self.lbl_val_jug = score_card(self.frame_scores, "Jugador")
        self.card_empates, self.lbl_val_emp = score_card(self.frame_scores, "Empates")
        self.card_cpu,     self.lbl_val_cpu = score_card(self.frame_scores, "Máquina")

        self.card_jugador.grid(row=0, column=0, padx=10, pady=8, sticky="nsew")
        self.card_empates.grid(row=0, column=1, padx=10, pady=8, sticky="nsew")
        self.card_cpu.grid(row=0, column=2, padx=10, pady=8, sticky="nsew")

        # Espacio de relleno izq + tips
        self.lbl_tips = ctk.CTkLabel(
            self.panel_izq,
            text="Tip: 1=Piedra · 2=Papel · 3=Tijera · R=Reiniciar · Esc=Salir",
            font=("", 13)
        )
        self.lbl_tips.grid(row=2, column=0, padx=16, pady=(0, 10), sticky="sw")

        # ====== Panel derecho: cabecera ======
        header = ctk.CTkFrame(self.panel_der)
        header.grid(row=0, column=0, padx=14, pady=(14, 10), sticky="nsew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        self.lbl_titulo = ctk.CTkLabel(header, text="Haz tu jugada...", font=("", 24, "bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w", padx=12, pady=10)
        self.lbl_ronda = ctk.CTkLabel(header, text="Ronda 0", font=("", 16, "bold"))
        self.lbl_ronda.grid(row=0, column=1, sticky="e", padx=12, pady=10)

        # ====== VS / elecciones ======
        vs = ctk.CTkFrame(self.panel_der)
        vs.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="nsew")
        for i in (0, 2):
            vs.grid_columnconfigure(i, weight=1, uniform="vs")
        vs.grid_columnconfigure(1, weight=0)
        self.panel_jugador = ctk.CTkFrame(vs, height=70, corner_radius=10)
        self.panel_cpu     = ctk.CTkFrame(vs, height=70, corner_radius=10)
        for p in (self.panel_jugador, self.panel_cpu):
            p.grid_propagate(False)
        self.panel_jugador.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.panel_cpu.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.lbl_jug = ctk.CTkLabel(self.panel_jugador, text="Jugador\n—", justify="center", font=("", 16, "bold"))
        self.lbl_cpu = ctk.CTkLabel(self.panel_cpu, text="Máquina\n—", justify="center", font=("", 16, "bold"))
        self.lbl_jug.pack(expand=True, fill="both", padx=8, pady=8)
        self.lbl_cpu.pack(expand=True, fill="both", padx=8, pady=8)

        self.lbl_vs = ctk.CTkLabel(vs, text="VS", font=("", 22, "bold"))
        self.lbl_vs.grid(row=0, column=1, padx=6, pady=10)

        # ====== Resultado grande ======
        self.lbl_resultado = ctk.CTkLabel(self.panel_der, text="Esperando jugada...", font=("", 28, "bold"))
        self.lbl_resultado.grid(row=2, column=0, padx=22, pady=(6, 10), sticky="w")
        # guardamos el color por defecto para restaurarlo al resetear
        self._resultado_color_default = self.lbl_resultado.cget("text_color")  

        # ====== Botón reset ======
        self.btn_reset = ctk.CTkButton(self.panel_der, text="Reiniciar", command=self.reset)
        self.btn_reset.grid(row=3, column=0, padx=20, pady=16, sticky="se")

        # ====== Atajos (globales) ======
        
        self.bind_all("<KeyPress>", self._on_key)  # un solo manejador para todas las teclas

        # Inicializar contadores visibles según 'marcador'
        self._refrescar_scores()

    # ---------- utilidades ----------
    def _cargar_icono(self, ruta, size):
        try:
            if not os.path.exists(ruta):
                raise FileNotFoundError(ruta)
            img = Image.open(ruta)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception as e:
            print(f"[Aviso] No se pudo cargar '{ruta}': {e}")
            return None

    def _refrescar_scores(self):
        estado = marcador.getMarcador()
        self.lbl_val_jug.configure(text=str(estado["puntosJugador"]))
        self.lbl_val_emp.configure(text=str(estado["empates"]))
        self.lbl_val_cpu.configure(text=str(estado["puntosMaquina"]))

    # ---------- manejador de teclado (case-insensitive para letras) ----------
    def _on_key(self, event):
        k = event.keysym  # '1', 'KP_1', 'r', 'R', 'Escape', etc.
        if k in ("1", "KP_1"):
            self.jugar("piedra")
        elif k in ("2", "KP_2"):
            self.jugar("papel")
        elif k in ("3", "KP_3"):
            self.jugar("tijera")
        elif k.lower() == "r":
            self.reset()
        elif k == "Escape":
            self.destroy()

    # ---------- lógica del juego (delegada al Core) ----------
    def jugar(self, eleccion_jugador: str):
        # El Core orquesta la ronda: RNG elige la máquina, se resuelve y se actualiza el marcador.
        resultado, eleccion_cpu = core.jugar_ronda(eleccion_jugador)
        self.ronda += 1

        # Mostrar elecciones
        self.lbl_jug.configure(text=f"Jugador\n{eleccion_jugador.capitalize()}")
        self.lbl_cpu.configure(text=f"Máquina\n{eleccion_cpu.capitalize()}")
        self.lbl_ronda.configure(text=f"Ronda {self.ronda}")

        # Mostrar resultado + color
        if resultado == "empate":
            self.lbl_resultado.configure(text="¡Empate!", text_color=self.COLOR_DRAW)
        elif resultado == "gana_jugador":
            self.lbl_resultado.configure(text="¡Ganaste! 🎉", text_color=self.COLOR_WIN)
        else:
            self.lbl_resultado.configure(text="Perdiste 😅", text_color=self.COLOR_LOSE)

        # Actualizar contadores desde el módulo 'marcador'
        self._refrescar_scores()

    def reset(self):
        self.ronda = 0
        marcador.reset()
        self.lbl_ronda.configure(text="Ronda 0")
        self._refrescar_scores()
        # restaura texto y color por defecto
        self.lbl_resultado.configure(text="Esperando jugada...", text_color=self._resultado_color_default)
        self.lbl_jug.configure(text="Jugador\n—")
        self.lbl_cpu.configure(text="Máquina\n—")
