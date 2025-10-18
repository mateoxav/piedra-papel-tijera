# main.py
# Punto de entrada de la app.

import os
import sys

# 1) Fijar el directorio de trabajo a main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# 2) Asegurar que este directorio está en sys.path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 3) Importar y lanzar la UI
from ui import PPTApp

def main():
    app = PPTApp()
    app.mainloop()  

if __name__ == "__main__":  
    main()
