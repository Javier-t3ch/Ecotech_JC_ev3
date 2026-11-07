import os
import sys


def limpiar_pantalla():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pausar_y_limpiar():
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()
